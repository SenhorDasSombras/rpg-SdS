"""This module exports a spell dataframe into a LaTeX format (not an entire document, just using LaTeX markup language)."""

import re
from functools import reduce

from pandas import DataFrame, Series

import SpellPrinter as spell_printer


def sub_all(pattern: str, repl: str, string: str) -> str:
    for _ in range(10):
        string = re.sub(pattern, repl, string, 1)
    return string


def replace_italics(markdown_text: str) -> str:
    string = markdown_text
    for _ in range(10):
        string = re.sub(r"(?P<tmp>_)", r"\\textit{", string, 1)
        string = re.sub(r"_", r"}", string, 1)
    return string


def replace_bold(markdown_text: str) -> str:
    string = markdown_text
    for _ in range(10):
        string = re.sub(r"(?P<tmp>\*\*)", r"\\textbf{", string, 1)
        string = re.sub(r"\*\*", r"}", string, 1)
    return string


def replace_newlines(markdown_text: str) -> str:
    latex_text = sub_all(r"<br>", r"\\\\", markdown_text)
    return latex_text


def replace_tabs(markdown_text: str) -> str:
    latex_text = sub_all(r"&emsp;", r"\\t ", markdown_text)
    return latex_text


def replace_size(string: str, font_size: str) -> str:
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


def replace_span(markdown_text: str) -> str:
    pattern = r"<span style='color:(?P<color>.*);font-size:(?P<fontsize>.*)'>(?P<str>.*)<\/span>"

    match_obj = re.match(pattern, markdown_text)

    string = match_obj.group("str")
    color = match_obj.group("color")
    font_size = match_obj.group("fontsize")

    if color != "None":
        colored_string = "\\textcolor{%s}{%s}" % (color, string)
    else:
        colored_string = string
    latex_text = replace_size(colored_string, font_size)
    return latex_text


def replace_all(markdown_text: str) -> str:
    latex_text = markdown_text
    replacements = [
        replace_italics,
        replace_bold,
        replace_newlines,
        replace_tabs,
        replace_span,
    ]

    for func in replacements:
        latex_text = func(latex_text)
    return latex_text


def get_latex_str_for_parts(parts_str: list) -> str:
    latex_parts = list()
    for markdown_part in parts_str:
        latex_part = replace_all(markdown_part)
        latex_parts.append(latex_part)

    latex_text = reduce(lambda x, y: f"{x}\n{y}", latex_parts)
    return latex_text


def get_latex_spell(spell_series: Series) -> str:
    parts_str = spell_printer.get_spell_parts_str(spell_series)
    latex_text = get_latex_str_for_parts(parts_str)
    return latex_text


def get_latex_spells(spells_df: DataFrame) -> str:
    latex_text = ""
    for _, spell_series in spells_df.iterrows():
        latex_spell = get_latex_spell(spell_series)
        latex_text += f"{latex_spell}\jump"
    return latex_text


def export_spells(spells_df: DataFrame, filename: str, verbose: bool = False):
    latex_tamplate = r"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\documentclass[12pt, a4paper, oneside]{book}

\input{/home/giatro/.config/user/giatro_packages.tex}

\input{/home/giatro/.config/user/giatro_macros.tex}

\title{Spells}
\date{\today}
\author{Lucas Paiolla Forastiere}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\begin{document}

\maketitle
\tableofcontents
\newpage

%s

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\end{document}
    """

    with open(filename, "w") as f:
        latex_text = get_latex_spells(spells_df)
        if verbose:
            print(latex_text)
        latex_text = latex_tamplate % latex_text
        f.write(latex_text)
