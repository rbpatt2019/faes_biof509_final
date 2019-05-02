"""A script for generating dataframes from the raw data

Unfortunately, due to the terms on the host website, an account must be created and registered before the data can be obtained.
Thus, this script operates on the assumption that you have already downloaded the data to the project/data/raw folder.

The data is located at: https://www.synapse.org/#!Synapse:syn10239444

The necessary files are:
    'Anterior Cingulate Gyrus/cingulate_batch 1__Proteins.txt'
    'Anterior Cingulate Gyrus/cingulate_batch 2__Proteins.txt'
    'Anterior Cingulate Gyrus/cingulate_batch 3__Proteins.txt'
    'Anterior Cingulate Gyrus/cingulate_batch 4__Proteins.txt'
    'Anterior Cingulate Gyrus/cingulate_batch 5__Proteins.txt'
    'Fronatl Cortex/frontal_batch 1__Proteins.txt'
    'Fronatl Cortex/frontal_batch 2__Proteins.txt'
    'Fronatl Cortex/frontal_batch 3__Proteins.txt'
    'Fronatl Cortex/frontal_batch 4__Proteins.txt'
    'Fronatl Cortex/frontal_batch 5__Proteins.txt'
"""

import glob

import pandas as pd

import src.data.CleanFrame as cf


def make_data(files, usecols=None, axis=0, join="outer", keys=None):
    """Make a full CleanFrame from multiple files

    Uses glob to find all files matching files
    Reads them into a CleanFrame, with the option to use only a subset of columns
    Then calls pd.concat, allowing the user to specify the axis, join, and keys

    By containing all data in generators, the computational load is reduced.

    Inputs
    ------
    files: str
        A regex strig that matches the file names to be used
        See https://docs.python.org/3.7/library/glob.html for more info on supported regexes
    usecols: list-like or callable, optional
        Return a subset of columns
        See https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
    aixs: {0/'index', 1/'columns'}, default 0
        for pd.concat
        The axis to concatenate along
    join: {'inner', 'outer'}, default 'outer'
        for pd.concat
        How to handle indexes on other axis(es)
    keys: sequence, optional
        for pd.concat
        Construct hierarchal index using the passed keys as the outermost level

    Returns
    -------
    data: src.data.CleanFrame.CleanFrame
        The full CleanFrame
    """
    # Type check files
    if not isinstance(files, str):
        raise ValueError(f"files must be a str, not {type(files)}")
    # Find files
    paths = glob.iglob(files)
    # Read in files, sep=None with engine='python' will auto determine delim
    reads = (
        pd.read_csv(file, usecols=usecols, sep=None, engine="python") for file in paths
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


if __name__ == "__main__":
    # Frontal cortex data
    frontal = make_data(
        "data/raw/f*",
        usecols=[
            "Master",
            "Accession",
            "Exp. q-value",
            "Sum PEP Score",
            "Abundance Ratio: (F1, 127N) / (F1, 126)",
            "Abundance Ratio: (F1, 127C) / (F1, 126)",
            "Abundance Ratio: (F1, 128N) / (F1, 126)",
            "Abundance Ratio: (F1, 128C) / (F1, 126)",
            "Abundance Ratio: (F1, 129N) / (F1, 126)",
            "Abundance Ratio: (F1, 129C) / (F1, 126)",
            "Abundance Ratio: (F1, 130N) / (F1, 126)",
            "Abundance Ratio: (F1, 130C) / (F1, 126)",
        ],
        axis=1,
        join="inner",
        keys=[1, 2, 3, 4, 5],
    )
    pd.to_pickle(frontal, "data/interim/frontal_full.pkl")

    # Anterior cingulate cortex data
    cingulate = make_data(
        "data/raw/c*",
        usecols=[
            "Master",
            "Accession",
            "Exp. q-value",
            "Sum PEP Score",
            "Abundance Ratio: (F1, 127N) / (F1, 126)",
            "Abundance Ratio: (F1, 127C) / (F1, 126)",
            "Abundance Ratio: (F1, 128N) / (F1, 126)",
            "Abundance Ratio: (F1, 128C) / (F1, 126)",
            "Abundance Ratio: (F1, 129N) / (F1, 126)",
            "Abundance Ratio: (F1, 129C) / (F1, 126)",
            "Abundance Ratio: (F1, 130N) / (F1, 126)",
            "Abundance Ratio: (F1, 130C) / (F1, 126)",
        ],
        axis=1,
        join="inner",
        keys=[1, 2, 3, 4, 5],
    )
    pd.to_pickle(frontal, "data/interim/cingulate_full.pkl")
