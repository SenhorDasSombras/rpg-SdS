import pandas as pd
import json
import glob

def get_spells_df():
    path_prefix = '../'
    files = glob.glob(f'{path_prefix}*.json')
    files = list(map(lambda x: x[len(path_prefix):], files))
    files.remove('_Template.json')

    result = list()
    for file_name in files:
        with open(f'{path_prefix}{file_name}', 'r') as file:
            result.append(json.load(file))

    return pd.DataFrame(result).sort_values(by=['name', 'nivel']).reset_index(drop=True)
