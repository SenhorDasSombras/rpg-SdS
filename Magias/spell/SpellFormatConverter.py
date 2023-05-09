"""This module converts the spell Markdown format into LaTeX format."""

import re
from functools import reduce

from pandas import DataFrame, Series

import spell.SpellPrinter as spell_printer


def _sub_all(pattern: str, repl: str, string: str) -> str:
    for _ in range(10):
        string = re.sub(pattern, repl, string, 1)
    return string


def _replace_italics(markdown_text: str) -> str:
    string = markdown_text
    for _ in range(10):
        string = re.sub(r"(?P<tmp>_)", r"\\textit{", string, 1)
        string = re.sub(r"_", r"}", string, 1)
    return string


def _replace_bold(markdown_text: str) -> str:
    string = markdown_text
    for _ in range(10):
        string = re.sub(r"(?P<tmp>\*\*)", r"\\textbf{", string, 1)
        string = re.sub(r"\*\*", r"}", string, 1)
    return string


def _replace_newlines(markdown_text: str) -> str:
    latex_text = _sub_all(r"<br>", r"\\\\", markdown_text)
    return latex_text


def _replace_tabs(markdown_text: str) -> str:
    latex_text = _sub_all(r"&emsp;", r"\\t ", markdown_text)
    return latex_text


def _replace_size(string: str, font_size: str) -> str:
    if font_size == "10px":
        font_size = "\\tiny"
    elif font_size == "11px":
        font_size = "\\scriptsize"
    elif font_size == "13px":
        font_size = "\\small"
    else:
        font_size = "\\normalsize"

    sized_string = "{%s %s}" % (font_size, string)
    return sized_string


def _replace_span(markdown_text: str) -> str:
    pattern = r"<span style='color:(?P<color>.*);font-size:(?P<fontsize>.*)'>(?P<str>.*)<\/span>"

    match_obj = re.match(pattern, markdown_text)

    if match_obj is None:
        raise ValueError("No string matched the pattern.")

    string = match_obj.group("str")
    color = match_obj.group("color")
    font_size = match_obj.group("fontsize")

    if color != "None":
        colored_string = "\\textcolor{%s}{%s}" % (color, string)
    else:
        colored_string = string
    latex_text = _replace_size(colored_string, font_size)
    return latex_text


def _replace_all(markdown_text: str) -> str:
    latex_text = markdown_text
    replacements = [
        _replace_italics,
        _replace_bold,
        _replace_newlines,
        _replace_tabs,
        _replace_span,
    ]

    for func in replacements:
        latex_text = func(latex_text)
    return latex_text


def get_latex_str_for_parts(parts_str: list) -> str:
    latex_parts = list()
    for markdown_part in parts_str:
        latex_part = _replace_all(markdown_part)
        latex_parts.append(latex_part)

    latex_text = reduce(lambda x, y: f"{x}\n{y}", latex_parts)
    return latex_text


def get_latex_spell_description(spell_series: Series) -> str:
    parts_str = spell_printer.get_spell_parts_str(spell_series)
    latex_text = get_latex_str_for_parts(parts_str)
    latex_text = r"\noindent" + latex_text
    return latex_text


def get_latex_spell_resume(spell_series: Series) -> str:
    rare_str = spell_printer._get_rare_str(spell_series)
    part_str = f"{spell_series['nome']} _({spell_series['name']})_{rare_str}\n "
    part_str = spell_printer.get_styled_str(part_str)

    latex_text = get_latex_str_for_parts([part_str])
    return latex_text


def get_latex_spells_resume(spells_df: DataFrame) -> str:
    latex_text = r"\chapter{Sumário}\n\n"
    for level, group_df in spells_df.groupby("nivel"):
        level = "Truques" if level == 0 else f"Ciclo {level}"
        header = r"\noindent\textbf{%s}\jump" % level
        latex_text += header
        for _, spell_series in group_df.iterrows():
            latex_spell = get_latex_spell_resume(spell_series)
            latex_text += f"{latex_spell}\n"
        latex_text += r"\jump"
    return latex_text


def get_latex_spells_description(spells_df: DataFrame) -> str:
    latex_text = r"\chapter{Magias}\n\n"
    for _, spell_series in spells_df.iterrows():
        latex_spell = get_latex_spell_description(spell_series)
        latex_text += f"{latex_spell}\jump"
    return latex_text


def get_latex_spells(spells_df: DataFrame) -> str:
    latex_text = ""

    latex_text += get_latex_spells_resume(spells_df)
    latex_text += get_latex_spells_description(spells_df)

    return latex_text
