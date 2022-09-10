"""This module reads the spells from the .json files inside a particular folder
and returns a DataFrame with the spells.

It has two main functions, one to return the raw DataFrame and another to
return the DataFrame with the schema asserted."""

import glob
import json
from typing import List, Union

import pandas as pd
from tqdm import tqdm

from .DFFormatAsserter import (
    assert_columns_not_null,
    assert_df_schema,
    convert_and_assert_column_to_list,
    fill_na_by_column,
)


def get_spells_df(
    path_prefix: str = "../",
    sort_by: Union[List[str], None] = None,
    verbose: bool = False,
):
    """This function returns the spells DataFrame from the .json files.

    You might specify the path to the json files, the default is '../'.
    """
    files = glob.glob(f"{path_prefix}*.json")
    files = list(map(lambda x: x[len(path_prefix) :], files))
    files.remove("_Template.json")

    if verbose:
        files = tqdm(files, desc="Spells")

    result = list()
    for file_name in files:
        with open(f"{path_prefix}{file_name}", "r") as file:
            try:
                result.append(json.load(file))
            except json.JSONDecodeError as e:
                print(f"{file_name} is not a valid json file.")
                print(e)

    if sort_by is None:
        sort_by = ["nivel", "nome"]

    result = pd.DataFrame(result).sort_values(by=sort_by).reset_index(drop=True)
    return result


def get_asserted_spells_df(*args, **kwargs):
    """Returns a DataFrame containing the spells from the .json files.

    It does the following steps:
        - Gets the DataFrame using the keyword arguments (see get_spells_df for the list of possible parameters);
        - Fills the NaN values by the column;
        - Asserts the DataFrame don't still have any null values;
        - Convert the "escola" column to a list column;
        - Asserts the DataFRame has the expected schema;
        - Returns the DataFrame;
    """
    spells_df = get_spells_df(*args, **kwargs)
    spells_df = fill_na_by_column(spells_df)
    assert_columns_not_null(spells_df)
    spells_df = convert_and_assert_column_to_list(spells_df, "escola")

    try:
        assert_df_schema(spells_df)
    except ValueError as e:
        print("Wrong values.")
        print(e)
    except TypeError as e:
        print("Wrong types.")
        print(e)

    return spells_df
