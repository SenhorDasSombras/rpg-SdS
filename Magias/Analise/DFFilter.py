def filter_value_column(df, column, filter_value):
    """Receives a DataFrame, a column to filter and a filter value to filter by
    and return a view of the DataFrame filtered by that value.
    """
    return df[df[column] == filter]


def filter_list_column(df, column, filter_value):
    """Receives a DataFrame, a column which type is a list and a filter value to
    filter by. Then, returns all the rows where filter_value is contained in the
    list column.
    """
    return df[df[column].apply(lambda x: filter_value in x)]


def filter_df(df, filter_dict):
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
        type_is_list = type(df[column].iloc[0]) == list
        df: pandas.DataFrame
        if type_is_list:
            df = filter_list_column(df, column, filter_value)
        else:
            df = filter_value_column(df, column, filter_value)

    return df
