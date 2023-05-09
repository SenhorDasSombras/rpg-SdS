"""Validate the schema and values of a particular data frame according to
configuration file.
"""

# Python Standard Libraries
from typing import Any

# Third Party Libraries
import pandas as pd
from utils.utils import get_global_vars_from_json

GLOBAL_VARS_PATH = "./dfs/global_vars.json"
GLOBAL_VARS = get_global_vars_from_json(GLOBAL_VARS_PATH)


def validate_column_names(df: pd.DataFrame, config: dict[str, Any]) -> bool:
    """Validate the column names of a data frame.

    Parameters
    ----------
    df : pd.DataFrame
        The data frame to validate.
    config : dict[str, str]
        A configuration dictionary. This must contain a key `column_names`
        which is a list of column names.

    Returns
    -------
    valid : bool
        True if the data frame's column names match the expected column names,
        False otherwise.
    """
    expected_column_names = config["df_columns"]
    return set(df.columns) == set(expected_column_names)


def validate_column_dtypes(df: pd.DataFrame, config: dict[str, Any]) -> bool:
    """Validate the data types of each column in a data frame.

    Parameters
    ----------
    df : pd.DataFrame
        The data frame to validate.
    config : dict[str, str]
        A configuration dictionary. This must contain a key `column_dtypes`
        which is a dictionary of column names and their expected data types as
        strings.

    Returns
    -------
    valid : bool
        True if the data frame's column data types match the expected data
        types, False otherwise.
    """
    column_dtypes = config["column_dtypes"]

    for column_name, expected_dtype in column_dtypes.items():
        if df[column_name].dtype != expected_dtype:
            return False

    return True


def fill_columns_with_default_values(
    df: pd.DataFrame, config: dict[str, Any]
) -> pd.DataFrame:
    """Fill columns with default values if they are missing.

    Parameters
    ---------
    df : pd.DataFrame
        The data frame to validate.
    config : dict[str, str]
        A configuration dictionary. This must contain a key
        `columns_default_values` which is a dictionary of column names and
        their expected default values.

    Returns
    -------
    df : pd.DataFrame
        The data frame with missing values filled with default values.
    """
    df = df.copy()
    default_value_per_column = config["columns_default_values"]

    for column_name, default_value in default_value_per_column.items():
        df[column_name] = df[column_name].fillna(default_value)

    return df


def validate_there_arent_null_values(df: pd.DataFrame) -> bool:
    """Validate that there are no null values in the data frame.

    Parameters
    ----------
    df : pd.DataFrame
        The data frame to validate.

    Returns
    -------
    valid : bool
        True if there are no null values in the data frame, False otherwise.
    """
    return df.isnull().sum().sum() == 0
