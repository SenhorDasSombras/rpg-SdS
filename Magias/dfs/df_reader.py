"""Read the .json files and return a DataFrame with the spells.

Read the spells from the .json files inside a particular folder
and returns a DataFrame with the spells.

It has two main functions, one to return the raw DataFrame and another to
return the DataFrame with the schema asserted.
"""

# Python Standard Libraries
import glob
import json
from pathlib import Path
from typing import Any

# Third Party Libraries
import pandas as pd
from pandera.errors import SchemaError
from tqdm import tqdm

# Local Folder Libraries
from .spells_schema import spells_schema


def get_spells_df(
    path_prefix: str = "./data/",
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


def get_asserted_spells_df(
    *args,
    config_path: Path = Path("./dfs/schema_config.json"),
    verbose: bool = False,
    **kwargs,
) -> pd.DataFrame:
    """Return the spells DataFrame from the .json files with the schema
    asserted.
    """
    configs = json.load(open(config_path, "r"))

    spells_df = get_spells_df(*args, **kwargs)
    spells_df = _fill_columns_with_default_values(spells_df, configs)
    spells_df = _convert_column_to_list(spells_df, "escola")

    try:
        if verbose:
            print("Validating schema...")
        spells_schema.validate(spells_df)
        if verbose:
            print("Schema validated.")
    except SchemaError as err:
        _print_schema_error_message(err, spells_df)

    return spells_df


def _print_schema_error_message(
    err: SchemaError, spells_df: pd.DataFrame
) -> None:
    assert err.failure_cases is not None  # This is to make mypy happy.

    print("Schema errors.")
    failure_index = list(err.failure_cases["index"])
    if failure_index[0] is None:
        print("No failure cases. This library sucks.")
        return

    failure_spell_names = list(spells_df.iloc[failure_index].nome)
    failure_cases = list(err.failure_cases["failure_case"])

    failure_report = pd.DataFrame(
        {
            "index": failure_index,
            "spell_name": failure_spell_names,
            "failure_case": failure_cases,
        }
    )
    print(failure_report)


def _fill_columns_with_default_values(
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
        if isinstance(default_value, list):
            # replace non-list values by the default list value
            df[column_name] = df[column_name].apply(
                lambda x: x if isinstance(x, list) else default_value
            )
            continue

        df[column_name] = df[column_name].fillna(default_value)

    return df


def _convert_column_to_list(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Make sure all column values are lists.

    If value is scalar, it convert it to a list with that value.
    """
    df = df.copy()
    convert_scalars_to_list = lambda x: [x] if type(x) != list else x  # noqa
    df[column] = df[column].apply(convert_scalars_to_list)
    return df
