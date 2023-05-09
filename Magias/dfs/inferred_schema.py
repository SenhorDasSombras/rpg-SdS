"""Inferred schema for the spells dataset.

This file was generated automatically using the pandera library and modified
to fine tune the schema.
"""

# Python Standard Libraries
import re
from re import Pattern
from typing import Any

# Third Party Libraries
from pandera import Check, Column, DataFrameSchema, Index, MultiIndex

escola_possible_values = [
    "elemental",
    "necromancia",
    "psíquica",
    "ilusionista",
    "invocação",
    "espiritual",
    "atrativa",
    "musical",
    "pura",
    "receita",
]
elementos_possible_values = [
    "ar",
    "fogo",
    "luz",
    "metal",
    "relâmpago",
    "sombras",
    "terra",
    "veneno",
    "água",
]
tags_possible_values = [
    "area",
    "buff",
    "debuff",
    "controle",
    "utilidade",
    "dano",
    "defesa",
    "cura",
    "distância",
    "corpo-a-corpo",
    "toque",
    "arma",
    "comunicação",
    "social",
    "detecção",
    "exploração",
]
classes_possible_values = [
    "arqueiro",
    "bardo",
    "monge",
    "ladino",
    "guerreiro",
    "mago",
    "xamã",
]
dmg_effect_possible_values = [
    "N/A",
    # elements and schools
    "ar",
    "fogo",
    "luz",
    "metal",
    "relâmpago",
    "sombras",
    "terra",
    "veneno",
    "água",
    "elemental",
    "psíquico",
    "necrótico",
    "energia",
    # weapon damages
    "concussão",
    "perfurante",
    "cortante",
    # conditions
    "cego",
    "enfeitiçado",
    "surdo",
    "amedrontado",
    "agarrado",
    "incapacitado",
    "invisível",
    "paralisado",
    "petrificado",
    "envenenado",
    "caído",
    "contido",
    "estunado",
    "inconsciente",
    "exausto",
]
source_possible_values = [
    "LDJ",
    "Tasha",
    "Xanathar",
    "Etc.",
    "Homebrew",
]


def check_list_values_are_valid(
    list_values: list[Any], possible_values: list[Any]
) -> bool:
    """Check if all values in a list are valid.

    A value inside a list is valid if it is present in the possible_values list.

    Parameters
    ----------
    list_values : list[Any]
        List of values to be checked.
    possible_values : list[Any]
        List of possible values.
    """
    for value in list_values:
        if value not in possible_values:
            return False
    return True


def CheckValidList(  # pylint: disable=invalid-name
    possible_values: list[Any],
) -> Check:
    """Check if all values in a list are valid.

    A value inside a list is valid if it is present in the possible_values list.

    Parameters
    ----------
    possible_values : list[Any]
        List of possible values.
    """
    return Check(
        lambda x: check_list_values_are_valid(x, possible_values),
        name="valid_list",
        error="Invalid list values.",
        element_wise=True,
        title="Valid List",
        description="Check if all values in a list are valid.",
    )


def check_function(regex, x: Any) -> bool:
    match = re.fullmatch(duracao_regex, x)
    if not match:
        print(f"Failed to match '{x}'")
    return bool(match)


def CheckRegex(regex: str | Pattern) -> Check:  # pylint: disable=invalid-name
    """Check if a string matches a regex."""
    return Check(
        # lambda x: check_function(regex, x),
        lambda x: bool(re.fullmatch(regex, x)),
        name="regex",
        error="Regex failed.",
        element_wise=True,
        title="Regex",
        description="Check if a string matches a regex.",
    )


tempo_conjuracao_regex = re.compile(
    r"\d+\ (ação|ações|ação bônus|ações"
    r" bônus|reação|reações|minuto|minutos|hora|horas)"
)

alcance_regex = re.compile(
    r"(pessoal(\ \(cone\ de\ \d+(,\d+)\ metros?\))?|toque|\d+(,\d+)?\ metros?)"
)

componentes_regex = re.compile(r"V?S?M?(\ \(.+\))?")

duracao_regex = re.compile(
    r"^"
    r"(concentração,\s)?"
    r"(até\s)?"
    r"(\d+\s)?"
    r"(minuto(s)?|hora(s)?|dia(s)?|rodada(s)?|turno(s)?|instantâne[oa]|"
    r"dissipada)"
    r"$"
)

attack_save_regex = re.compile(
    r"^"
    r"((N/A)|"
    r"((DEX|STR|INT|CON|WIS|CHA)\sSave)|"
    r"((DEX|STR|INT|CON|WIS|CHA)\sTest)|"
    r"(distância)|"
    r"(corpo-a-corpo))"
    r"$"
)


spells_schema = DataFrameSchema(
    columns={
        "nome": Column(
            dtype="str",
            checks=None,
            nullable=False,
            unique=True,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "name": Column(
            dtype="str",
            checks=None,
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "nivel": Column(
            dtype="int64",
            checks=[
                Check.greater_than_or_equal_to(min_value=0.0),
                Check.less_than_or_equal_to(max_value=9.0),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "escola": Column(
            dtype="object",
            checks=[
                CheckValidList(escola_possible_values),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "ritual": Column(
            dtype="bool",
            checks=None,
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "elementos": Column(
            dtype="object",
            checks=[
                CheckValidList(elementos_possible_values),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "tempo_conjuracao": Column(
            dtype="object",
            checks=[
                CheckRegex(tempo_conjuracao_regex),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "alcance_area": Column(
            dtype="object",
            checks=[
                CheckRegex(alcance_regex),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "componentes": Column(
            dtype="object",
            checks=[
                CheckRegex(componentes_regex),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "mana": Column(
            dtype="int64",
            checks=[
                Check.greater_than_or_equal_to(min_value=0.0),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "duracao": Column(
            dtype="object",
            checks=[
                CheckRegex(duracao_regex),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "attack_save": Column(
            dtype="object",
            checks=[
                CheckRegex(attack_save_regex),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "dmg_effect": Column(
            dtype="object",
            checks=[
                Check.isin(dmg_effect_possible_values),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "dmg": Column(
            dtype="object",
            checks=None,
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "classes": Column(
            dtype="object",
            checks=[
                CheckValidList(classes_possible_values),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "tags": Column(
            dtype="object",
            checks=[
                # Check(
                #     lambda x: check_list_values_are_valid(
                #         x, tags_possible_values
                #     )
                # )
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "descricao": Column(
            dtype="object",
            checks=None,
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "source": Column(
            dtype="object",
            checks=[
                # Check(
                #     lambda x: check_list_values_are_valid(
                #         x, source_possible_values
                #     )
                # )
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "mana_adicional": Column(
            dtype="object",
            checks=None,
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "magia_rara": Column(
            dtype="bool",
            checks=None,
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
    },
    checks=None,
    index=Index(
        dtype="int64",
        checks=[],
        nullable=False,
        coerce=False,
        name=None,
        description=None,
        title=None,
    ),
    dtype=None,
    coerce=True,
    strict=False,
    name=None,
    ordered=False,
    unique=None,
    report_duplicates="all",
    unique_column_names=False,
    title=None,
    description=None,
)
