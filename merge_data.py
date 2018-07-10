import pandas as pd
import glob

from config import * # Global variables

def merge_pckls():
    dfs = []
    for file in glob.glob(DATA_TEMP_DIR + '*.pckl'):
        data = pd.read_pickle(file)
        dfs.append(data)

    df = pd.concat(dfs, ignore_index=True)
    df.to_pickle(DATA_TEMP_DIR + 'data_merged.pckl')
    return df

if __name__ == '__main__':
    df = merge_pckls()
    print("Final data shape: ", df.shape)
