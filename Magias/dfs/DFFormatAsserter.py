"""This module asserts the schema of the spell dataframe. Making sure it has
the right columns and right values inside each of the columns.

    Note: right now there are many things hardcoded that could and should be
    put into a config file.
"""

# Python Standard Libraries
from functools import reduce
import re

# Third Party Libraries
from utils.utils import get_global_vars_from_json

GLOBAL_VARS_PATH = "./dfs/global_vars.json"
GLOBAL_VARS = get_global_vars_from_json(GLOBAL_VARS_PATH)


def fill_na_by_column(df):
    """Receives a spell df and fill its NA values using the default for each
    column."""
    df = df.copy()
    df.elementos = df.elementos.apply(
        lambda x: x if isinstance(x, list) else []
    )
    df.attack_save.fillna("N/A", inplace=True)
    df.dmg_effect.fillna("N/A", inplace=True)
    df.dmg.fillna("N/A", inplace=True)
    df.ritual.fillna(False, inplace=True)
    df.mana_adicional.fillna("N/A", inplace=True)
    df.magia_rara.fillna(False, inplace=True)
    return df


def assert_column_not_null(df, column):
    """Receive a DataFrame and a column and return a ValueError if that column
    has null values."""
    if any(df[column].isna()):
        raise ValueError(f"Column '{column}' shouldn't have null values!")


def assert_columns_not_null(df, not_null_columns=None):
    """Receives a DataFrame and a set of columns and returns a ValueError if any
    of them have null values. The set of columns has a default value."""

    if not_null_columns is None:
        not_null_columns = {
            "nome",
            "name",
            "nivel",
            "escola",
            "tempo_conjuracao",
            "alcance_area",
            "componentes",
            "mana",
            "duracao",
            "classes",
            "tags",
            "descricao",
            "source",
            "mana_adicional",
        }

    for column in not_null_columns:
        assert_column_not_null(df, column)


def convert_and_assert_column_to_list(df, column):
    """Make sure all column values are lists. If value is scalar, it convert it to
    a list with that value."""
    df = df.copy()
    convert_scalars_to_list = lambda x: [x] if type(x) != list else x
    df[column] = df[column].apply(convert_scalars_to_list)
    return df


def _get_non_null_rows_of_columns(df, columns):
    """Private function that returns the index for all non null columns.

    The rows will appear the number of times a column from the set is non null.
    """
    rows = [df[column].dropna().index for column in columns]
    if len(rows) >= 2:
        rows = reduce(lambda x, y: x.append(y), rows)
    elif len(rows) == 1:
        rows = rows[0]

    return rows


def assert_no_extra_columns(df):
    """
    Assert a spell df has no extra column beyond the columns we expect.

    It returns a possibly empty list with the names of all the extra columns and
    """
    extra_columns = list()
    for column in df.columns:
        if column not in GLOBAL_VARS["G_COLUMNS"]:
            extra_columns.append(column)

    return extra_columns, _get_non_null_rows_of_columns(df, extra_columns)


def assert_no_missing_columns(df):
    missing_columns = list()
    for column in GLOBAL_VARS["G_COLUMNS"]:
        if column not in df.columns:
            missing_columns.append(column)

    return missing_columns, _get_non_null_rows_of_columns(df, missing_columns)


def assert_df_columns(df):
    extra_columns, extra_col_rows = assert_no_extra_columns(df)
    missing_columns, missing_col_rows = assert_no_missing_columns(df)

    error_str = ""
    if len(extra_columns) > 0:
        error_str += f"Extra columns: {extra_columns}\n"
        error_str += (
            f'{df.iloc[extra_col_rows][["nome", "name"] + extra_columns]}'
        )
    if len(missing_columns) > 0:
        error_str += f"Missing columns: {missing_columns}\n"
        error_str += (
            f'{df.iloc[missing_col_rows][["nome", "name"] + missing_columns]}'
        )
    if len(error_str) > 0:
        raise TypeError(error_str)


def return_columns_not_matching_mask(df, column, mask):
    return df[["nome", "name", column]][~mask]


def get_mask_from_list(df, column, list_of_possible_values):
    unique_values = set(df[column].sum())

    get_values_out_of_list = lambda x: x not in list_of_possible_values
    wrong_values = list(filter(get_values_out_of_list, unique_values))

    true_if_any_element_is_wrong = lambda a_list: any(
        [True if element in wrong_values else False for element in a_list]
    )
    mask = df[column].apply(true_if_any_element_is_wrong)
    mask = ~mask

    return mask


def assert_column_using_mask(df, column, mask):
    if not mask.all():
        error_str = (
            f"Column '{column}' have wrong"
            f" values:\n{return_columns_not_matching_mask(df, column, mask)}"
        )
        raise ValueError(error_str)


def assert_df_column_types(df):
    mask = get_mask_from_list(df, "escola", GLOBAL_VARS["G_ESCOLAS"])
    assert_column_using_mask(df, "escola", mask)

    mask = get_mask_from_list(df, "elementos", GLOBAL_VARS["G_ELEMENTOS"])
    assert_column_using_mask(df, "elementos", mask)

    tempo_conjuracao_regex = re.compile(
        r"\d+\ (ação|ações|ação bônus|ações"
        r" bônus|reação|reações|minuto|minutos|hora|horas)"
    )
    mask = df.tempo_conjuracao.str.fullmatch(tempo_conjuracao_regex)
    assert_column_using_mask(df, "tempo_conjuracao", mask)

    alcance_regex = re.compile(
        r"(pessoal(\ \(cone\ de\ \d+(,\d+)\ metros?\))?|toque|\d+(,\d+)?\ metros?)"
    )
    mask = df.alcance_area.str.fullmatch(alcance_regex)
    assert_column_using_mask(df, "alcance_area", mask)

    componentes_regex = re.compile(r"V?S?M?(\ \(.+\))?")
    mask = df.componentes.str.fullmatch(componentes_regex)
    assert_column_using_mask(df, "componentes", mask)

    mask = df.duracao.str.islower()
    assert_column_using_mask(df, "duracao", mask)

    attack_save_regex = re.compile(
        r"(N/A|corpo-a-corpo|distância|(STR|DEX|CON|INT|WIS|CHA)\ (Test|Save))"
    )
    mask = df.attack_save.str.fullmatch(attack_save_regex)
    assert_column_using_mask(df, "attack_save", mask)

    mask = get_mask_from_list(df, "tags", GLOBAL_VARS["G_TAGS"])
    assert_column_using_mask(df, "tags", mask)

    mask = get_mask_from_list(df, "classes", GLOBAL_VARS["G_CLASSES"])
    assert_column_using_mask(df, "classes", mask)

    # TODO: pass possible names to global variables
    source_regex = re.compile(r"(LDJ|Xanathar|Tasha|Etc.|Custom)")
    mask = df.source.str.fullmatch(source_regex)
    assert_column_using_mask(df, "source", mask)


def assert_df_schema(df):
    assert_df_columns(df)
    assert_df_column_types(df)
