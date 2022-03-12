import json
import glob

import pandas as pd

from typing import List

def get_spells_df(
    path_prefix: str = '../',
    sort_by: List[str]  = None
):
    """This function returns the spells DataFrame from the .json files.

    You might specify the path to the json files, the default is '../'.
    """
    files = glob.glob(f'{path_prefix}*.json')
    files = list(map(lambda x: x[len(path_prefix):], files))
    files.remove('_Template.json')

    result = list()
    for file_name in files:
        with open(f'{path_prefix}{file_name}', 'r') as file:
            result.append(json.load(file))

    if sort_by is None:
        sort_by = ['name', 'nivel']

    result = pd.DataFrame(result).sort_values(by=sort_by).reset_index(drop=True)
    return result
