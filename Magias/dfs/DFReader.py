"""Read the .json files and return a DataFrame with the spells.

Read the spells from the .json files inside a particular folder
and returns a DataFrame with the spells.

It has two main functions, one to return the raw DataFrame and another to
return the DataFrame with the schema asserted.
"""

# Python Standard Libraries
import glob
import json

# Third Party Libraries
import pandas as pd
from tqdm import tqdm

# Local Folder Libraries
from .DFFormatAsserter import (
    assert_columns_not_null,
    assert_df_schema,
    convert_and_assert_column_to_list,
    fill_na_by_column,
)


def get_spells_df(
    path_prefix: str = "../",
    sort_by: list[str] | None = None,
    verbose: bool = False,
) -> pd.DataFrame:
    """Return the spells DataFrame from the .json files.

    You might specify the path to the json files, the default is '../'.
    """
    files = glob.glob(f"{path_prefix}*.json")
    path_prefix_len = len(path_prefix)
    files = list(map(lambda x: x[path_prefix_len:], files))
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

    result_df = (
        pd.DataFrame(result).sort_values(by=sort_by).reset_index(drop=True)
    )
    return result_df


def get_asserted_spells_df(*args, **kwargs) -> pd.DataFrame:
    """Return a DataFrame containing the spells from the .json files.

    It does the following steps:
        - Gets the DataFrame using the keyword arguments (see get_spells_df for
          the list of possible parameters);
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
