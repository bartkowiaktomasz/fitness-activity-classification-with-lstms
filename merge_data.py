import pandas as pd
import glob

from config import * # Global variables

if __name__ == '__main__':

    dfs = []
    for file in glob.glob(DATA_DIR + '*.pckl'):
        data = pd.read_pickle(file)
        dfs.append(data)

    df = pd.concat(dfs, ignore_index=True)
    print("Final data shape: ", df.shape)
    df.to_pickle(DATA_DIR + 'data.pckl')
