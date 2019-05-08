"""A script for visualising data before feature engineering and training

Two plots are used here - volcano and UMAP

The volcano plot allows for a visualisation of those genes that are differentially expressed
and the significance of those changes.

UMAP is an alternative to tSNE plotting and is a dimensionality reduction technique 
for visualising clusters
"""

import umap
import pandas as pd
import numpy as np

if __name__ == "__main__":

    # Read in the data
    frontal = pd.read_pickle("data/interim/frontal_full.pkl")
    cingulate = pd.read_pickle("data/interim/cingulate_full.pkl")

    # Prep for volcano plot
    frontal_volc = pd.DataFrame()
    frontal_volc["-log10_q"] = -np.log10(
        frontal.xs("q_score", level=1, axis=1).mean(axis=1).replace(0, 0.000001)
    )
    frontal_volc["log2_ad"] = np.log2(
        pd.concat(
            (
                frontal.xs("ad1", level=1, axis=1).mean(axis=1),
                frontal.xs("ad2", level=1, axis=1).mean(axis=1),
            ),
            axis=1,
        ).mean(axis=1)
    )
    frontal_volc["log2_pd"] = np.log2(
        pd.concat(
            (
                frontal.xs("pd1", level=1, axis=1).mean(axis=1),
                frontal.xs("pd2", level=1, axis=1).mean(axis=1),
            ),
            axis=1,
        ).mean(axis=1)
    )
    frontal_volc["log2_adpd"] = np.log2(
        pd.concat(
            (
                frontal.xs("adpd1", level=1, axis=1).mean(axis=1),
                frontal.xs("adpd2", level=1, axis=1).mean(axis=1),
            ),
            axis=1,
        ).mean(axis=1)
    )
    # Set Colors
    conditions = [(frontal_volc['log10_q'] >= 1.30103) & (frontal_volc['log2_ad'] >= 0.5), (frontal_volc['log10_q'] >= 1.30103) & (frontal_volc['log2_ad'] <= -0.5)]
    choices = [2, 0]
    frontal_volc['ad_color'] = np.select(conditions, choices, default=1)
    cmap = LinearSegmentedColormap.fron_list('Volcano', [(1, 0, 0), (0, 0, 0), (0, 1, 0), N=3])
    plt.scatter(frontal_volc['log2_ad'], frontal_volc['log10_q'], c=frontal_volc['ad_color'], cmap=cmap)
