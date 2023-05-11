"""Export filtered spells to latex file.

This module reads the spells from the .json files contained in a folder,
filters it using a json file, and exports it to a .tex file. Also, it can
automaticaly generate the .pdf file from the .tex file and open the .pdf.

Right now, it uses zathura as the pdf reader, but in the future it might be
changed to use the default pdf reader.

This script receives the following parameters:
- path_prefix: The path to the .json files. The default is '../'.
- sort_by: The list of columns to sort the DataFrame by. The default is
['nivel', 'name'].
- verbose: If True, the progress bar will be shown. The default is False.
- filter_json_path: The path to the .json file containing the filters. The
default is None (i.e. no filter is performed).
- output_tex_path: The path to the .tex file to export the spells. The default
is 'latex_compilation/spells'. If the file already exists, it will be
overwritten. The pdf file will be generated in the same folder with the same
name.
"""

# Python Standard Libraries
import argparse

# Third Party Libraries
import dfs.df_filter as filter
import dfs.df_reader as reader
import pandas as pd
import spell.spell_exporter as exporter


def parse_input_args():
    """Parse the input arguments.

    Returns
    -------
        The parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description=(
            "This module reads the spells from the .json files contained in a "
            "folder, filters it using a json file, and exports it to a .tex "
            "file. Also, it can automaticaly generate the .pdf file from the "
            ".tex file and open the .pdf."
        )
    )
    parser.add_argument(
        "--input_folder",
        "-i",
        type=str,
        default="./data/",
        help="The path to the .json files. The default is './data/'.",
    )
    parser.add_argument(
        "--sort_by",
        type=str,
        default="nivel,nome",
        help=(
            "The list of columns to sort the DataFrame by. The default is "
            "['nivel', 'nome']."
        ),
    )
    parser.add_argument(
        "--verbose",
        "-V",
        "-v",
        action="store_true",
        default=False,
        help="If True, the progress bar will be shown. The default is False.",
    )
    parser.add_argument(
        "--filter_path",
        "-F",
        "-f",
        type=str,
        default=None,
        help=(
            "The path to the .json file containing the filters. The default "
            "is None (i.e. no filter is performed)."
        ),
    )
    parser.add_argument(
        "--output_path",
        "-o",
        type=str,
        default="latex_compilation/spells",
        help=(
            "The path to the .tex file to export the spells. The default is "
            "'latex_compilation/spells'. If the file already exists, it will "
            "be overwritten. The pdf file will be generated in the same "
            "folder with the same name."
        ),
    )
    parser.add_argument(
        "--open_pdf",
        "-O",
        action="store_true",
        default=False,
        help="If True, opens the PDF file. The default is False.",
    )
    parser.add_argument(
        "--delete_tex",
        action="store_true",
        default=False,
        help="If True, deletes the .tex file. The default is False.",
    )
    args = parser.parse_args()
    return args


def main() -> None:
    """Execute main program."""
    args = parse_input_args()
    kwargs = {
        "path_prefix": args.input_folder,
        "sort_by": args.sort_by.split(","),
        "verbose": args.verbose,
    }

    spells_df: pd.DataFrame
    if args.filter_path is not None:
        spells_df = filter.filter_spells_df_using_json(
            args.filter_path, **kwargs
        )
    else:
        spells_df = reader.get_asserted_spells_df(**kwargs)

    kwargs = {
        "filename": args.output_path,
        "verbose": args.verbose,
        "open_file": args.open_pdf,
        "delete_tex": args.delete_tex,
    }
    exporter.export_spells(spells_df, **kwargs)


if __name__ == "__main__":
    main()
