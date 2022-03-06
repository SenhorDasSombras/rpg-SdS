def filter_list_column(df, column, filter_value):
    return df[df[column].apply(lambda x: filter_value in x)]

def filter_df(df, filter_dict):
    for column, filter in filter_dict.items():
        if type(df[column].iloc[0]) == list:
            df = filter_list_column(df, column, filter)
        else:
            df = df[df[column] == filter]

    return df