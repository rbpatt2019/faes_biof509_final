import glob

import pandas as pd

import src.data.CleanFrame as cf


def make_data(
    files, usecols=None, names=None, index_col=None, axis=0, join="outer", keys=None
):
    # Type check files
    if not isinstance(files, str):
        raise ValueError(f"files must be a str, not {type(files)}")
    # Find files
    paths = glob.iglob(files)
    # Read in files, sep=None with engine='python' will auto determine delim
    reads = (
        pd.read_csv(
            file,
            usecols=usecols,
            header=0,
            names=names,
            index_col=index_col,
            sep=None,
            engine="python",
        )
        for file in paths
    )
    # Convert to CleanFrame
    cfs = (cf.CleanFrame(i) for i in reads)
    # Clean data
    clean = (i.prep_data() for i in cfs)
    # Create final CleanFrame
    data = cf.CleanFrame(
        pd.concat(clean, axis=axis, join=join, keys=keys, sort=False, copy=False)
    )
    return data
