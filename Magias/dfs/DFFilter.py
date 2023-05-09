"""Filter any DataFrame using different filters."""

# Python Standard Libraries
import json
from typing import Any

# Third Party Libraries
import dfs.DFReader as reader
import pandas as pd


def filter_value_column(
    df: pd.DataFrame, column: str, filter_values: list[Any]
) -> pd.DataFrame:
    """Filter a column with a list of values.

    Receives a DataFrame, a column to filter and a list of filter values to
    filter by and returns a copy of the DataFrame filtered by that value.
    """
    if not isinstance(filter_values, list):
        filter_values = [filter_values]

    filter_query = " | ".join(
        [f"{column} == {value}" for value in filter_values]
    )
    return df.query(filter_query).copy()


def filter_list_column(
    df: pd.DataFrame, column: str, filter_values: list[Any]
) -> pd.DataFrame:
    """Filter a list column with a list of values.

    Receives a DataFrame, a column which type is a list and a list of filter
    values to filter by. Then, returns all the rows where list of that column
    contains the filter_value.
    """
    if not isinstance(filter_values, list):
        filter_values = [filter_values]

    def query_function(column_values: list) -> bool:
        for value in filter_values:
            if value in column_values:
                return True
        return False

    return df[df[column].apply(query_function)].copy()


def filter_df(df: pd.DataFrame, filter_dict: dict[str, Any]) -> pd.DataFrame:
    """Filter a DataFrame using a dictionary of filters.

    Receive a DataFrame and a filter dictionary, then filter the
    DataFrame using all filter mutually.

    The filter_dict must have the following format:
        {
            "column_name1": "filter_value1",
            ...
            "column_nameN": "filter_valueN",
        }
    """
    for column, filter_value in filter_dict.items():
        is_list_column = isinstance(df[column].iloc[0], list)
        if is_list_column:
            df = filter_list_column(df, column, filter_value)
        else:
            df = filter_value_column(df, column, filter_value)

    return df


def filter_df_using_json(df: pd.DataFrame, json_path: str) -> pd.DataFrame:
    """Filter a DataFrame using a json file.

    Receives a DataFrame and a json file path, then filter the
    DataFrame using all filter mutually.

    The json file must have the following format:
        {
            "column_name1": "filter_value1",
            ...
            "column_nameN": "filter_valueN",
        }
    """
    with open(json_path, "r", encoding="utf8") as file:
        filter_dict = json.load(file)

    return filter_df(df, filter_dict)


def filter_spells_df(
    filter_dict: dict[str, Any], *args, **kwargs
) -> pd.DataFrame:
    """Filter the spells DataFrame using a dictionary of filters.

    Receives a filter dictionary and the parameters to get the spells
    DataFrame, then filter the DataFrame using all filter mutually.

    The filter_dict must have the following format:
        {
            "column_name1": "filter_value1",
            ...
            "column_nameN": "filter_valueN",
        }
    """
    spells_df = reader.get_asserted_spells_df(*args, **kwargs)
    return filter_df(spells_df, filter_dict)


def filter_spells_df_using_json(
    json_path: str, *args, **kwargs
) -> pd.DataFrame:
    """Filter the spells DataFrame using a json file.

    Receives a json file path and the parameters to get the spells
    DataFrame, then filter the DataFrame using all filter mutually.

    The json file must have the following format:
        {
            "column_name1": "filter_value1",
            ...
            "column_nameN": "filter_valueN",
        }
    """
    spells_df = reader.get_asserted_spells_df(*args, **kwargs)
    return filter_df_using_json(spells_df, json_path)
