"""This module exports a spell dataframe into a LaTeX format (not an entire document, just using LaTeX markup language)."""

import os

from IPython.display import clear_output
from pandas import DataFrame

from SpellFormatConverter import get_latex_spells


def export_tex_file(spells_df: DataFrame, filename: str, verbose: bool = False):
    """Creates a LaTeX file with the spells contained in the dataframe.

    Parameters
    ----------
    spells_df : DataFrame
        A dataframe containing the spells.
    filename : str
        The file name without the .tex extension.
    verbose : bool, default=False
        If True, prints the commands used.
    """

    latex_tamplate = r"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\documentclass{RPG_Adventure}[2021/10/20]

\input{/home/giatro/.config/user/giatro_packages.tex}

\input{/home/giatro/.config/user/giatro_macros.tex}

\title{Magias de\\ \Huge{O Senhor das Sombras}}
\date{\today}
\author{Lucas Paiolla Forastiere}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\begin{document}

\maketitle

%s

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\end{document}
    """
    if verbose:
        print(f"Exporting {filename}.tex")

    with open(f"{filename}.tex", "w") as f:
        latex_text = get_latex_spells(spells_df)
        latex_text = latex_tamplate % latex_text
        f.write(latex_text)


def compile_tex_file(filename: str, verbose: bool = False):
    """Compiles a LaTeX file into a PDF file.

    It's important to have the RPG_Adventure.cls file in the same folder as the LaTeX file.

    Parameters
    ----------
    filename : str
        The file name without the .tex extension.
    verbose : bool, default=False
        If True, prints the commands used.
    """
    base_filename = os.path.basename(filename)
    dir = os.path.dirname(filename)
    cwd = os.getcwd()

    try:
        os.chdir(dir)

        compile_cmd = f"pdflatex -no-file-line-error -interaction nonstopmode {base_filename}.tex > /dev/null 2>&1"
        rm_cmd = f"rm *.out *.log *.aux"

        if verbose:
            print(compile_cmd)
        os.system(compile_cmd)

        if verbose:
            print(rm_cmd)
        os.system(rm_cmd)
    finally:
        os.chdir(cwd)


def open_pdf(filename: str, verbose: bool = False):
    """Opens a PDF file.

    Parameters
    ----------
    filename : str
        The file name without the .pdf extension.
    verbose : bool, default=False
        If True, prints the commands used. The default is False.
    """
    if verbose:
        print(f"Opening {filename}.pdf")
    os.system(f"zathura {filename}.pdf")


def delete_tex_file(filename: str, verbose: bool = False):
    """Deletes a LaTeX file.

    Parameters
    ----------
    filename : str
        The file name.
    verbose : bool, default=False
        If True, prints the commands used. The default is False.
    """
    if verbose:
        print(f"Deleting {filename}.tex")
    os.system(f"rm {filename}.tex")


def export_spells(
    spells_df: DataFrame,
    filename: str,
    verbose: bool = False,
    open_file: bool = False,
    delete_tex: bool = False,
):
    """The main function of the module.

    It exports the spells contained in the dataframe into a LaTeX file and compiles it into a PDF file.

    Also, it has options to open the PDF file and delete the LaTeX file.

    Parameters
    ----------
    spells_df : DataFrame
        The dataframe containing the spells.
    filename : str
        The filename without any extension.
    verbose : bool, default=False
        If True, prints the commands used. The default is False.
    open_file : bool, default=False
        If True, opens the PDF file. The default is False.
    delete_tex : bool, default=False
        If True, deletes the LaTeX file. The default is False.
    """
    basename = os.path.basename(filename)
    file_folder = os.path.dirname(filename)
    filename = f"latex_compilation/{basename}"

    export_tex_file(spells_df, filename, verbose)
    compile_tex_file(filename, verbose)

    if open_file:
        open_pdf(filename, verbose)

    if delete_tex:
        delete_tex_file(filename, verbose)
    else:
        os.system(f"mv latex_compilation/{basename}.tex {file_folder}")

    os.system(f"mv latex_compilation/{basename}.pdf {file_folder}")

    if not verbose:
        clear_output()
