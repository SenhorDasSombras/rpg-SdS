"""Filter any DataFrame using different filters."""

# Python Standard Libraries
import json
from typing import Any

# Third Party Libraries
import dfs.df_reader as reader
import pandas as pd


class DFFilter:
    """Filter any DataFrame using different filters.

    Filtering a DataFrame means that you will reduce the amount of lines in that
    DataFrame using a filter. If many filters are applied, the DataFrame will
    be reduced to the rows that match all the filters (i.e. its intersection).
    """

    @staticmethod
    def filter_df(
        df: pd.DataFrame, filter_dict: dict[str, Any]
    ) -> pd.DataFrame:
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
                df = DFFilter._filter_list_column(df, column, filter_value)
            else:
                df = DFFilter._filter_value_column(df, column, filter_value)

        return df

    @staticmethod
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

        return DFFilter.filter_df(df, filter_dict)

    @staticmethod
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
        return DFFilter.filter_df(spells_df, filter_dict)

    @staticmethod
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
        return DFFilter.filter_df_using_json(spells_df, json_path)

    @staticmethod
    def _filter_value_column(
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

    @staticmethod
    def _filter_list_column(
        df: pd.DataFrame, column: str, filter_values: list[Any]
    ) -> pd.DataFrame:
        """Filter a list column with a list of values.

        Receives a DataFrame, a column which type is a list and a list of filter
        values to filter by. Then, returns all the rows where list of that
        column contains the filter_value.
        """
        if not isinstance(filter_values, list):
            filter_values = [filter_values]

        def query_function(column_values: list) -> bool:
            for value in filter_values:
                if value in column_values:
                    return True
            return False

        return df[df[column].apply(query_function)].copy()


class DFQuerrier:
    """Query any DataFrame using different queries.

    Querying a DataFrame means you can pass any query string to the Pandas query
    function. This query can be as complex as you want. Thus, this is more
    flexible than filtering, but can be more complex to use.
    """

    @staticmethod
    def query_df(df: pd.DataFrame, query: str) -> pd.DataFrame:
        """Query a DataFrame using a query string.

        Receives a DataFrame and a query string, then query the DataFrame using
        the query string.
        """
        return df.query(query).copy()

    @staticmethod
    def query_df_from_file(df: pd.DataFrame, file_path: str) -> pd.DataFrame:
        """Query a DataFrame using a query file.

        Receives a DataFrame and a query file path, then query the DataFrame
        using the query file.
        """
        query = DFQuerrier._read_query_file(file_path)
        return DFQuerrier.query_df(df, query)

    @staticmethod
    def query_spells_df(query: str, *args, **kwargs) -> pd.DataFrame:
        """Query the spells DataFrame using a query string.

        Receives a query string and the parameters to get the spells DataFrame,
        then query the DataFrame using the query string.
        """
        spells_df = reader.get_asserted_spells_df(*args, **kwargs)
        spells_df = DFQuerrier._preprocess_spells_df(spells_df)
        spells_df = DFQuerrier.query_df(spells_df, query)
        spells_df = DFQuerrier._postprocess_spells_df(spells_df)
        return spells_df

    @staticmethod
    def query_spells_df_from_file(
        file_path: str, *args, **kwargs
    ) -> pd.DataFrame:
        """Query the spells DataFrame using a query file.

        Receives a query file path and the parameters to get the spells
        DataFrame, then query the DataFrame using the query file.
        """
        spells_df = reader.get_asserted_spells_df(*args, **kwargs)
        spells_df = DFQuerrier._preprocess_spells_df(spells_df)
        spells_df = DFQuerrier.query_df_from_file(spells_df, file_path)
        spells_df = DFQuerrier._postprocess_spells_df(spells_df)
        return spells_df

    @staticmethod
    def _read_query_file(file_path: str) -> str:
        """Read a query file and return its content."""
        with open(file_path, "r", encoding="utf8") as file:
            multiline_query = file.readlines()
        multiline_query = list(map(lambda line: line.strip(), multiline_query))
        query = " ".join(multiline_query)
        return query

    @staticmethod
    def _preprocess_spells_df(spells_df: pd.DataFrame) -> pd.DataFrame:
        """Preprocess the spells DataFrame to be queried.

        Receives the spells DataFrame and preprocess it to be queried.
        """
        spells_df = spells_df.copy()

        list_columns = ["escola", "elementos", "classes", "tags"]
        for list_column in list_columns:
            spells_df[list_column] = spells_df[list_column].str.join(", ")

        return spells_df

    @staticmethod
    def _postprocess_spells_df(spells_df: pd.DataFrame) -> pd.DataFrame:
        """Postprocess the spells DataFrame after being queried.

        Receives the spells DataFrame and postprocess it after being queried.
        """
        spells_df = spells_df.copy()

        list_columns = ["escola", "elementos", "classes", "tags"]
        for list_column in list_columns:
            spells_df[list_column] = spells_df[list_column].str.split(", ")

        return spells_df
