import abc
from typing import Optional

import pandas as pd

from pyrasgo.utils import dataframe
from pyrasgo.session import Session


class DataWarehouse(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def user_connection(self):
        pass

    @property
    @abc.abstractmethod
    def user_credentials(self):
        pass

    @abc.abstractmethod
    def get_source_table(self, table_name: str,
                         record_limit: Optional[int] = None) -> pd.DataFrame:
        # TODO: This likely should not be "table" for s3 storage
        pass

    @abc.abstractmethod
    def get_source_tables(self) -> pd.DataFrame:
        # TODO: This likely should not be "tables" for s3 storage
        pass

    @abc.abstractmethod
    def get_source_columns(self) -> pd.DataFrame:
        pass

    @abc.abstractmethod
    def get_source(self, source_name: str,
                   record_limit: Optional[int] = None) -> pd.DataFrame:
        # TODO: This likely should not be "table" for s3 storage
        pass

    @abc.abstractmethod
    def get_sources(self) -> pd.DataFrame:
        # TODO: This likely should not be "tables" for s3 storage
        pass

    @abc.abstractmethod
    def _write_dataframe_to_table(self, df: pd.DataFrame, *,
                                  table_name: str):
        pass

    @classmethod
    def connect(cls):
        """
        Returns an instance of the account's Data Warehouse connection
        :param session: Session object describing the current user's session
        :return:
        """
        # TODO: Provide the setup for other warehouses here:
        from pyrasgo.storage.snowflake import SnowflakeDataWarehouse

        return SnowflakeDataWarehouse()

    def write_dataframe_to_table(self, df: pd.DataFrame, *,
                                 table_name: str):
        with self.user_connection.cursor() as cursor:
            cursor.execute(dataframe.generate_ddl(df, table_name=table_name))
        self._write_dataframe_to_table(df, table_name)


class DataWarehouseSession(type(DataWarehouse), type(Session)):
    pass
