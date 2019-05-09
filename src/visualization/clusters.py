"""A script for making UMAP plots and tSNE plots

UMAP is an alternative to tSNE that has some benefits such as speed and retaining local structure

This would probably be better structured in some kind of visualising class with methods
but am currently too short on time
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import umap
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from yellowbrick.text import TSNEVisualizer

import src.data.CleanFrame as cf

# Read in the data
frontal = pd.read_pickle("data/interim/frontal_full.pkl")
cingulate = pd.read_pickle("data/interim/cingulate_full.pkl")

# Prep for umap plot - frontal
frontal_umap = (
    cf.CleanFrame(frontal)
    .T.reset_index()
    .rename_axis(columns=None)
    .drop(columns=["level_0"])
    .rename(columns={"level_1": "label"})
    .filter_by_val(col="label", vals=["q_score", "pep_score"], keep=False)
    .sort_values(by=["label"])
    .reset_index()
    .drop(columns=["index"])
)
frontal_umap["label"] = frontal_umap["label"].str[:-1]
frontal_umap["label"] = frontal_umap["label"].astype("category")
pd.to_pickle(frontal_umap, "data/interim/frontal_umap.pkl")

# Reducer for umap, reccomended to reduce to 50 with PCA, then UMAP
X_frontal = frontal_umap.drop(columns=["label"])
y_frontal = frontal_umap["label"]
pipe_frontal = Pipeline(
    [("PCA", PCA(n_components=40, random_state=1)), ("UMAP", umap.UMAP(random_state=1))]
)
embedding_frontal = pipe_frontal.fit_transform(X_frontal)

# Reducer for tSNE
tsne_frontal = TSNEVisualizer(decompose='pca', decompose_by=40, random_state=1)
tsne_frontal.fit(X_frontal, y_frontal)

# Prep for umap plot - cingulate
cingulate_umap = (
    cf.CleanFrame(cingulate)
    .T.reset_index()
    .rename_axis(columns=None)
    .drop(columns=["level_0"])
    .rename(columns={"level_1": "label"})
    .filter_by_val(col="label", vals=["q_score", "pep_score"], keep=False)
    .sort_values(by=["label"])
    .reset_index()
    .drop(columns=["index"])
)
cingulate_umap["label"] = cingulate_umap["label"].str[:-1]
cingulate_umap["label"] = cingulate_umap["label"].astype("category")
pd.to_pickle(cingulate_umap, "data/interim/cingulate_umap.pkl")

# Reducer for umap
X_cingulate = cingulate_umap.drop(columns=["label"])
y_cingulate = cingulate_umap["label"]
reducer_cingulate = umap.UMAP(random_state=1)
embedding_cingulate = reducer_cingulate.fit_transform(X_cingulate)

# Reducer for tSNE
tsne_cingulate = TSNEVisualizer(decompose='pca', decompose_by=40, random_state=1)
tsne_cingulate.fit(X_cingulate, y_cingulate)

# Create conditions/choices for colors
choices = [1, 2, 3]
cond_frontal = [y_frontal == 'ad', y_frontal == 'pd', y_frontal == 'adpd']
cond_cingulate = [y_cingulate == 'ad', y_cingulate == 'pd', y_cingulate == 'adpd']

# Plot UMAP
for data in zip((embedding_frontal, embedding_cingulate), (cond_frontal, cond_cingulate), ('Frontal', 'Cingulate')):
    plt.scatter(data[0][:, 0], data[0][:, 1], s=5, c=np.select(data[1], choices, 0), cmap='Spectral')
    plt.gca().set_aspect('equal', 'datalim')
    cbar = plt.colorbar(boundaries=np.arange(5)-0.5, ticks=np.arange(4))
    cbar.ax.set_yticklabels(['Control', 'AD', 'PD', 'ADPD'])
    plt.title(f'UMAP Plot - {data[2]}')
    plt.savefig(f'reports/figures/UMAP{data[2]}.png', dpi=600)
    plt.close()

for df in (frontal_volc, cingulate_volc):
    fig, ax = plt.subplots(nrows=1, ncols=3, sharex=True, sharey=True)
    fig.suptitle(df.name)
    fig.text(0.5, 0.05, "log2(fold change)", ha="center", va="center", fontsize=8)
    fig.text(
        0.05,
        0.5,
        "-log10(q-score)",
        ha="center",
        va="center",
        rotation="vertical",
        fontsize=8,
    )
    for items in zip(cols_data, cols_color, ax):
        # Creates color column
        conditions = [
            (df["-log10_q"] >= 1.30103) & (df[items[0]] >= 0.5),
            (df["-log10_q"] >= 1.30103) & (df[items[0]] <= -0.5),
        ]
        df[items[1]] = np.select(conditions, choices, default=1)
        # Creates volcano plots
        items[2].scatter(df[items[0]], df["-log10_q"], c=df[items[1]], cmap=cmap, s=1)
        items[2].set_title(items[0].split("_")[1].upper(), fontsize=8)
        items[2].set_xbound(lower=-2.1, upper=5.1)
        items[2].set_xticks(np.arange(-2, 5.1, 1), minor=False)
        items[2].set_xticks(np.arange(-2, 5.1, 0.25), minor=True)
        items[2].set_xticklabels([-2, -1, 0, 1, 2, 3, 4, 5], fontsize=4)
        items[2].set_ybound(lower=0, upper=6.1)
        items[2].set_yticks(np.arange(0, 6.1, 1), minor=False)
        items[2].set_yticks(np.arange(0, 6.1, 0.25), minor=True)
        items[2].set_yticklabels([0, 1, 2, 3, 4, 5, 6], fontsize=4)
    plt.savefig(f"reports/figures/{df.name}.png", dpi=600)
    plt.close()
print("Volcano Plots Made!")
