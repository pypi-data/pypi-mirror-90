import logging
import os
from typing import Optional

import pandas as pd
from snowflake import connector as snowflake
from snowflake.connector import SnowflakeConnection

from pyrasgo.monitoring import track_usage
from pyrasgo.storage.base import DataWarehouse, DataWarehouseSession
from pyrasgo.session import Session
from pyrasgo.utils import dataframe


class SnowflakeDataWarehouse(DataWarehouse, Session, metaclass=DataWarehouseSession):
    def __init__(self):
        username = os.environ.get('SNOWFLAKE_USERNAME', self.profile.get("snowUsername", None))
        if username is None:
            raise EnvironmentError("Your user is missing credentials, please contact Rasgo support.")
        self.username = username

        organization = self.profile.get("organization")
        self.organization_code = organization.get("code", None)
        if self.organization_code is None:
            raise EnvironmentError("Your organization is missing credentials, please contact Rasgo support.")

        self.password = os.environ.get("SNOWFLAKE_PASSWORD", self.profile.get("snowPassword"))
        self.account = os.environ.get("SNOWFLAKE_ACCOUNT", organization.get("account"))
        self.database = os.environ.get("SNOWFLAKE_DATABASE", organization.get("database"))
        self.schema = os.environ.get("SNOWFLAKE_SCHEMA", organization.get("schema"))
        self.warehouse = os.environ.get("SNOWFLAKE_WAREHOUSE", organization.get("warehouse"))
        self.user_role = os.environ.get("SNOWFLAKE_ROLE",
                                        self.profile.get("role", f"{self.organization_code}_{self.username}"))

    @property
    def publisher_role(self):
        return f"{self.organization_code}PUBLISHER"

    @property
    def reader_role(self):
        return f"{self.organization_code}READER"

    @property
    def public_role(self):
        return "PUBLIC"

    @property
    @track_usage
    def user_connection(self) -> SnowflakeConnection:
        return snowflake.connect(**self.user_credentials)

    @property
    @track_usage
    def user_credentials(self) -> dict:
        return {
            "user": self.username,
            "password": self.password,
            "account": self.account,
            "database": self.database,
            "schema": self.schema,
            "warehouse": self.warehouse,
            "role": self.user_role
        }

    @property
    @track_usage
    def publisher_connection(self) -> SnowflakeConnection:
        return snowflake.connect(**self.publisher_credentials)

    @property
    @track_usage
    def publisher_credentials(self) -> dict:
        return {
            "user": self.username,
            "password": self.password,
            "account": self.account,
            "database": self.database,
            "schema": self.schema,
            "warehouse": self.warehouse,
            "role": self.user_role
        }

    @track_usage
    def execute_query(self, query: str, params: Optional[dict] = None, as_publisher: bool = False):
        """
        Execute a query on the [cloud] data platform.

        :param query: String to be executed on the data platform
        :param params: Optional parameters
        :param as_publisher: Flag on whether to run the query as the publisher role.
        :return:
        """
        if as_publisher:
            return self.publisher_connection.cursor().execute(query, params)
        return self.user_connection.cursor().execute(query, params)

    @track_usage
    def get_source_table(self, table_name: str,
                         record_limit: Optional[int] = None) -> pd.DataFrame:
        if record_limit is None:
            logging.info(f"Loading all rows from {table_name}...")
        result_set = self.execute_query(f"SELECT * FROM {table_name} {f'LIMIT {record_limit}' if record_limit else ''}")
        return pd.DataFrame.from_records(iter(result_set), columns=[x[0] for x in result_set.description])

    @track_usage
    def get_source_tables(self):
        result_set = self.execute_query('SELECT * FROM RASGO_DATA_SOURCE_TABLES')
        return pd.DataFrame.from_records(iter(result_set), columns=[x[0] for x in result_set.description])

    @track_usage
    def get_source_columns(self):
        result_set = self.execute_query('SELECT * FROM RASGO_DATA_SOURCE_COLUMNS')
        return pd.DataFrame.from_records(iter(result_set), columns=[x[0] for x in result_set.description])

    @track_usage
    def get_source(self, source_name: str,
                   record_limit: Optional[int] = None) -> pd.DataFrame:
        return self.get_source_table(table_name=source_name, record_limit=record_limit)

    @track_usage
    def get_sources(self) -> pd.DataFrame:
        return self.get_source_tables()

    def _write_dataframe_to_table(self, df: pd.DataFrame, table_name: str):
        # Convert all strings to work with Snowflake
        from snowflake.connector.pandas_tools import write_pandas

        self._snowflakify_dataframe(df)
        write_pandas(self.user_connection, df=df, table_name=self._snowflakify_name(table_name))

    @classmethod
    def _snowflakify_dataframe(cls, df: pd.DataFrame):
        """
        Renames all columns in a pandas dataframe to Snowflake compliant names in place
        """
        df.rename(columns={r: cls._snowflakify_name(r) for r in dataframe.build_schema(df)},
                  inplace=True)

    @classmethod
    def _snowflakify_list(cls, list_in):
        """
        param list_in: list
        return list_out: list
        Changes a list of columns to Snowflake compliant names
        """
        return [cls._snowflakify_name(n) for n in list_in]

    @staticmethod
    def _snowflakify_name(name):
        """
        param name: string
        return: string
        Converts a string to a snowflake compliant value
        Removes double quotes, replaces dashes with underscores, casts to upper case
        """
        return name.replace("-", "_").replace('"', '').upper()
