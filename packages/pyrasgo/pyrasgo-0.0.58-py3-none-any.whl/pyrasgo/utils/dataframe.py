from typing import List

import pandas as pd


def build_schema(dataframe: pd.DataFrame, include_index=False) -> dict:
    from pandas.io.json import build_table_schema
    schema_list = build_table_schema(dataframe)
    if not include_index:
        return {column['name']: column
                for column in schema_list['fields'] if column['name'] != 'index'}
    return {column['name']: column
            for column in schema_list['fields']}


def generate_ddl(dataframe: pd.DataFrame,
                 table_name: str):
    return pd.io.sql.get_schema(dataframe.reset_index(), table_name) \
        .replace('CREATE TABLE', 'CREATE OR REPLACE TABLE') \
        .replace('"', '')
