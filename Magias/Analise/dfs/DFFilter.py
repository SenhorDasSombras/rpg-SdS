"""Module to filter any DataFrame using different filters."""

import json
from typing import Any, Dict

from pandas import DataFrame

from .DFReader import get_asserted_spells_df


def filter_value_column(
    df: DataFrame, column: str, filter_value: Any
) -> DataFrame:
    """Receives a DataFrame, a column to filter and a filter value to filter by
    and return a view of the DataFrame filtered by that value.
    """
    return df[df[column] == filter_value]


def filter_list_column(
    df: DataFrame, column: str, filter_value: Any
) -> DataFrame:
    """Receives a DataFrame, a column which type is a list and a filter value to
    filter by. Then, returns all the rows where list of that column contains the filter_value.
    """
    return df[df[column].apply(lambda x: filter_value in x)]


def filter_df(df: DataFrame, filter_dict: Dict[str, Any]) -> DataFrame:
    """Receives a DataFrame and a filter dictionary, then filter the
    DataFrame using all filter mutually.

    The filter_dict must have the following format:
        {
            "column_name1": "filter_value1",
            ...
            "column_nameN": "filter_valueN",
        }
    """
    for column, filter_value in filter_dict.items():
        is_list_column = type(df[column].iloc[0]) == list
        if is_list_column:
            df = filter_list_column(df, column, filter_value)
        else:
            df = filter_value_column(df, column, filter_value)

    return df


def filter_df_using_json(df: DataFrame, json_path: str) -> DataFrame:
    """Receives a DataFrame and a json file path, then filter the
    DataFrame using all filter mutually.

    The json file must have the following format:
        {
            "column_name1": "filter_value1",
            ...
            "column_nameN": "filter_valueN",
        }
    """
    with open(json_path, "r") as f:
        filter_dict = json.load(f)

    return filter_df(df, filter_dict)


def filter_spells_df(filter_dict: Dict[str, Any], *args, **kwargs) -> DataFrame:
    """Receives a filter dictionary and the parameters to get the spells
    DataFrame, then filter the DataFrame using all filter mutually.

    The filter_dict must have the following format:
        {
            "column_name1": "filter_value1",
            ...
            "column_nameN": "filter_valueN",
        }
    """
    spells_df = get_asserted_spells_df(*args, **kwargs)
    return filter_df(spells_df, filter_dict)


def filter_spells_df_using_json(json_path: str, *args, **kwargs) -> DataFrame:
    """Receives a json file path and the parameters to get the spells
    DataFrame, then filter the DataFrame using all filter mutually.

    The json file must have the following format:
        {
            "column_name1": "filter_value1",
            ...
            "column_nameN": "filter_valueN",
        }
    """
    spells_df = get_asserted_spells_df(*args, **kwargs)
    return filter_df_using_json(spells_df, json_path)
