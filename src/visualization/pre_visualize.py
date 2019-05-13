"""A script for visualising data before feature engineering and training

Three plots are used here - volcano and UMAP and tSNE

The volcano plot allows for a visualisation of those genes that are differentially expressed
and the significance of those changes.

UMAP is an alternative to tSNE plotting and is a dimensionality reduction technique 
for visualising clusters

This would probably be better structured in some kind of visualising class with methods
but am currently too short on time
"""

# import src.visualization.clusters

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
import src.data.CleanFrame as cf


def prep_volcano(df):
    """Prep data for volcano plots

    Cleans off unnecessary columns information then aggregates by means
    """
    df.columns = df.columns.droplevel(0)
    df.columns = df.columns.str.rstrip("12")
    columns = df.columns.unique()
    for col in columns:
        df[f"mean_{col}"] = df[col].mean(axis=1)
    df = df.drop(columns=columns)
    df["mean_q_score"] = df["mean_q_score"].replace(0, 0.000001)
    return df


if __name__ == "__main__":

    # Read in the data
    frontal = cf.CleanFrame(pd.read_pickle("data/interim/frontal_full.pkl"))
    cingulate = cf.CleanFrame(pd.read_pickle("data/interim/cingulate_full.pkl"))

    # Prep data
    frontal_volc = prep_volcano(frontal)
    cingulate_volc = prep_volcano(cingulate)

    # Save data
    pd.to_pickle(frontal_volc, "data/interim/frontal_volc.pkl")
    pd.to_pickle(cingulate_volc, "data/interim/cingulate_volc.pkl")

    # Plot data
    data = ["mean_ad", "mean_pd", "mean_adpd"]
    for data in zip((frontal_volc, cingulate_volc), ("Frontal", "Cingulate")):
        for col in ("mean_ad", "mean_pd", "mean_adpd"):
            data[0].volcano(
                col,
                "mean_q_score",
                is_log=False,
                title=f"{data[1]} {col}",
                show=False,
                save=True,
                path=f"reports/figures/{data[1]}_{col}.png",
            )
            plt.close()
