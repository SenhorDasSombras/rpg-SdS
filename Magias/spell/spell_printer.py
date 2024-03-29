"""This module converts a spell series into a markdown string that can be
printed also using this module."""

# Python Standard Libraries
import re

# Third Party Libraries
from IPython.display import Markdown, display


# === GENERAL FUNCTIONS ===
def get_styled_str(string, color=None, size=None):
    """Receives a string and return a CSS Styled string."""
    string = string.replace("\n", "<br>").replace("\t", "&emsp;")
    string = f"<span style='color:{color};font-size:{size}'>{string}</span>"
    return string


# === ATTRIBUTE STRINGS ===
def _get_lvl_str(spell_series):
    lvl_str = (
        f" lvl {spell_series.nivel}" if spell_series.nivel > 0 else " - truque"
    )
    return lvl_str


def _get_ritual_str(spell_series):
    ritual_str = " - ritual" if spell_series.ritual else ""
    return ritual_str


def _get_rare_str(spell_series):
    rare_str = r" (Rara)" if spell_series.magia_rara else ""
    return rare_str


def _get_escola_str(spell_series):
    escola_str = ""
    for escola in spell_series.escola[:-1]:
        escola_str += f"{escola}, "
    escola_str += f"{spell_series.escola[-1]}"

    if "elemental" not in spell_series.escola:
        return f"{escola_str}"

    elemental_str = ""
    for element in spell_series.elementos[:-1]:
        elemental_str += f"{element}, "
    elemental_str += f"{spell_series.elementos[-1]}"
    elemental_str = f"(_{elemental_str}_)"

    escola_str = f"{escola_str} {elemental_str}"
    return escola_str


def _get_componentes_str(spell_series):
    componentes_str: str
    regex_match = re.search(r"\(.+\)", spell_series.componentes)
    if regex_match is None:
        componentes_str = f"{spell_series.componentes}"
    else:
        componentes_str = (
            f"{spell_series.componentes.split(' ')[0]} _{regex_match.group(0)}_"
        )
    return componentes_str


def _get_mana_str(spell_series):
    mana_str: str
    if spell_series["mana_adicional"] == "N/A":
        mana_str = f"{spell_series.mana}"
    else:
        mana_str = f"{spell_series.mana} (_+ {spell_series.mana_adicional}_)"
    return mana_str


def _get_tags_str(spell_series):
    tags_str = ""
    tags = sorted(spell_series.tags)
    for tag in tags[:-1]:
        tags_str += f"{tag}, "
    tags_str += tags[-1]
    tags_str = f"[{tags_str}]\n"
    return tags_str


def _get_classes_str(spell_series):
    classes_str = ""
    classes = sorted(spell_series.classes)
    for _class in classes[:-1]:
        classes_str += f"{_class}, "
    classes_str += classes[-1]
    classes_str = f"[{classes_str}]\n"
    return classes_str


# === SPELL PARTS STRINGS FUNCTIONS ===
def _get_name_part_str(spell_series, styled=True):
    lvl_str = _get_lvl_str(spell_series)
    ritual_str = _get_ritual_str(spell_series)
    rare_str = _get_rare_str(spell_series)

    name_str = (
        f"**{spell_series['nome']} _({spell_series['name']})_**{lvl_str}{ritual_str}{rare_str}\n"
    )
    if styled:
        name_str = get_styled_str(name_str)
    return name_str


def _get_header_part_str(spell_series, styled=True):
    escola_str = _get_escola_str(spell_series)
    componentes_str = _get_componentes_str(spell_series)
    mana_str = _get_mana_str(spell_series)

    header_str = f"\t**Escola(s):** {escola_str}\n"
    header_str += f"\t**Tempo conjuração:** {spell_series.tempo_conjuracao}\n"
    header_str += f"\t**Alcance:** {spell_series.alcance_area}\n"
    header_str += f"\t**Componentes:** {componentes_str}\n"
    header_str += f"\t**Mana:** {mana_str}\n"
    header_str += f"\t**Duração:** {spell_series.duracao}\n"
    if spell_series.dmg != "N/A":
        header_str += f"\t**Dano**: {spell_series.dmg}\n"
    if spell_series.attack_save != "N/A":
        header_str += f"\t**Attack/Save:** {spell_series.attack_save}\n"
    if spell_series.dmg_effect != "N/A":
        header_str += f"\t**Dmg/effect:** {spell_series.dmg_effect}\n"

    if styled:
        header_str = get_styled_str(header_str, size="13px")

    return header_str


def _get_desc_part_str(spell_series, styled=True):
    desc_str = f"{spell_series.descricao}\n"
    if styled:
        desc_str = get_styled_str(desc_str)
    return desc_str


def _get_tags_part_str(spell_series, styled=True):
    tags_str = _get_tags_str(spell_series)
    if styled:
        tags_str = get_styled_str(tags_str, color="gray", size="11px")
    return tags_str


def _get_classes_part_str(spell_series, styled=True):
    classes_str = _get_classes_str(spell_series)
    if styled:
        classes_str = get_styled_str(classes_str, color="gray", size="11px")
    return classes_str


def _get_source_part_str(spell_series, styled=True):
    source_str = f"_{spell_series.source}_"

    if styled:
        source_str = get_styled_str(source_str, color="gray", size="10px")
    return source_str


# === PUBLIC PRINT FUNCTIONS ===
def print_markdown(string):
    """Receives a string and print it using IPython Markdown style."""
    display(Markdown(string))


def print_markdown_list(strings):
    """Receives a list of strings and print them using IPython Markdown style."""
    string = ""
    for s in strings:
        string += s
    print_markdown(string)


def get_spell_parts_str(
    spell_series,
    name=True,
    header=True,
    desc=True,
    tags=True,
    classes=True,
    source=True,
):
    """Receives a spell row and returns the string of it.
    This function is modularized so that we can choose which parts will be
    returned.
    By default, all parts are returned.
    """
    str_list = list()
    if name:
        name_str = _get_name_part_str(spell_series)
        str_list.append(name_str)
    if header:
        header_str = _get_header_part_str(spell_series)
        str_list.append(header_str)
    if desc:
        desc_str = _get_desc_part_str(spell_series)
        str_list.append(desc_str)
    if tags:
        tags_str = _get_tags_part_str(spell_series)
        str_list.append(tags_str)
    if classes:
        classes_str = _get_classes_part_str(spell_series)
        str_list.append(classes_str)
    if source:
        source_str = _get_source_part_str(spell_series)
        str_list.append(source_str)

    return str_list


def print_spell_parts(
    spell_series,
    name=True,
    header=True,
    desc=True,
    tags=True,
    classes=True,
    source=True,
):
    """Receives a spell row and prints its parts.
    This function is modularized so that we can choose which parts will be
    printed.
    By default, all parts are printed.
    """
    str_list = get_spell_parts_str(
        spell_series, name, header, desc, tags, classes, source
    )
    print_markdown_list(str_list)


def print_spell(spell_series, **kwargs):
    """Receives a Pandas Series of spell and prints it in a nice style."""
    print_spell_parts(spell_series, **kwargs)


def print_spells_for_df(spells_df, **kwargs):
    """Receives a Pandas DataFrame of spells and prints all of them using a nice style."""
    for _, row in spells_df.iterrows():
        print_spell(row, **kwargs)


def print_spells_by_name(spells_df, name, **kwargs):
    """Receives a Pandas DataFrame of spells and a name and prints the spell
    with that name.
    """
    spells_df = spells_df[
        (spells_df["nome"].str.contains(name, case=False))
        | (spells_df["name"].str.contains(name, case=False))
    ]
    print_spells_for_df(spells_df, **kwargs)
