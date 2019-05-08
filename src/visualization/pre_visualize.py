"""A script for visualising data before feature engineering and training

Two plots are used here - volcano and UMAP

The volcano plot allows for a visualisation of those genes that are differentially expressed
and the significance of those changes.

UMAP is an alternative to tSNE plotting and is a dimensionality reduction technique 
for visualising clusters

This would probably be better structured in some kind of visualising class with methods
but am currently too short on time
"""

import umap
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
    
if __name__ == "__main__":

    # Read in the data
    frontal = pd.read_pickle("data/interim/frontal_full.pkl")
    cingulate = pd.read_pickle("data/interim/cingulate_full.pkl")

    # Prep for volcano plot - frontal
    frontal_volc = pd.DataFrame()
    frontal_volc.name = 'Frontal Cortex Volcano Plots'
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
    pd.to_pickle(frontal_volc, 'data/interim/frontal_volcano.pkl')

    #Prep for volcano plot - cingulate
    cingulate_volc = pd.DataFrame()
    cingulate_volc.name = 'Anterior Cingulate Gyrus Volcano Plots'
    cingulate_volc["-log10_q"] = -np.log10(
        cingulate.xs("q_score", level=1, axis=1).mean(axis=1).replace(0, 0.000001)
    )
    cingulate_volc["log2_ad"] = np.log2(
        pd.concat(
            (
                cingulate.xs("ad1", level=1, axis=1).mean(axis=1),
                cingulate.xs("ad2", level=1, axis=1).mean(axis=1),
            ),
            axis=1,
        ).mean(axis=1)
    )
    cingulate_volc["log2_pd"] = np.log2(
        pd.concat(
            (
                cingulate.xs("pd1", level=1, axis=1).mean(axis=1),
                cingulate.xs("pd2", level=1, axis=1).mean(axis=1),
            ),
            axis=1,
        ).mean(axis=1)
    )
    cingulate_volc["log2_adpd"] = np.log2(
        pd.concat(
            (
                cingulate.xs("adpd1", level=1, axis=1).mean(axis=1),
                cingulate.xs("adpd2", level=1, axis=1).mean(axis=1),
            ),
            axis=1,
        ).mean(axis=1)
    )
    pd.to_pickle(cingulate_volc, 'data/interim/cingulate_volcano.pkl')

    # Create red, black green custom color map
    cmap = LinearSegmentedColormap.from_list('Volcano', [(1, 0, 0), (0, 0, 0), (0, 1, 0)], N=3)

    # Set color column and plot
    cols_data = ('log2_ad', 'log2_pd', 'log2_adpd')
    cols_color = ('ad_color', 'pd_color', 'adpd_color')
    choices = [2, 0]
    for df in (frontal_volc, cingulate_volc):
        fig, ax = plt.subplots(nrows=1, ncols=3, sharex=True, sharey=True)
        fig.suptitle(df.name)
        fig.text(0.5, 0.05, 'log2(fold change)', ha='center', va='center', fontsize=8)
        fig.text(0.05, 0.5, '-log10(q-score)', ha='center', va='center', rotation='vertical', fontsize=8)
        for items in zip(cols_data, cols_color, ax):
            # Creates color column
            conditions = [(df['-log10_q'] >= 1.30103) & (df[items[0]] >= 0.5), (df['-log10_q'] >= 1.30103) & (df[items[0]] <= -0.5)]
            df[items[1]] = np.select(conditions, choices, default=1)
            # Creates volcano plots
            items[2].scatter(df[items[0]], df['-log10_q'], c=df[items[1]], cmap=cmap, s=1)
            items[2].set_title(items[0].split('_')[1].upper(), fontsize=8)
            items[2].set_xbound(lower=-2.1, upper=5.1)
            items[2].set_xticks(np.arange(-2, 5.1, 1), minor=False)
            items[2].set_xticks(np.arange(-2, 5.1, 0.25), minor=True)
            items[2].set_xticklabels([-2, -1, 0, 1, 2, 3, 4, 5], fontsize=4)
            items[2].set_ybound(lower=0, upper=6.1)
            items[2].set_yticks(np.arange(0, 6.1, 1), minor=False)
            items[2].set_yticks(np.arange(0, 6.1, 0.25), minor=True)
            items[2].set_yticklabels([0, 1, 2, 3, 4, 5, 6], fontsize=4)
        plt.savefig(f'reports/figures/{df.name}.png', dpi=600)
        plt.close()
