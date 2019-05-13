"""A script for making UMAP plots and tSNE plots

UMAP is an alternative to tSNE that has some benefits such as speed and retaining local structure

This would probably be better structured in some kind of visualising class with methods
but am currently too short on time
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import umap
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
reducer_frontal = umap.UMAP(random_state=1)
embedding_frontal = reducer_frontal.fit_transform(X_frontal)

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

# Create conditions/choices for colors
choices = [1, 2, 3]
cond_frontal = [y_frontal == "ad", y_frontal == "pd", y_frontal == "adpd"]
cond_cingulate = [y_cingulate == "ad", y_cingulate == "pd", y_cingulate == "adpd"]

# Plot UMAP
for data in zip(
    (embedding_frontal, embedding_cingulate),
    (cond_frontal, cond_cingulate),
    ("Frontal", "Cingulate"),
):
    plt.scatter(
        data[0][:, 0],
        data[0][:, 1],
        s=5,
        c=np.select(data[1], choices, 0),
        cmap="Spectral",
    )
    plt.gca().set_aspect("equal", "datalim")
    cbar = plt.colorbar(boundaries=np.arange(5) - 0.5, ticks=np.arange(4))
    cbar.ax.set_yticklabels(["Control", "AD", "PD", "ADPD"])
    plt.title(f"UMAP Plot - {data[2]}")
    plt.savefig(f"reports/figures/UMAP_{data[2]}.png", dpi=600)
    plt.close()

# Reducer for tSNE
tsne_frontal = TSNEVisualizer(decompose=None, random_state=1, perplexity=10)
tsne_frontal.fit(X_frontal, y_frontal)
tsne_frontal.poof(outpath="reports/figures/tsne_frontal.png")

# Reducer for tSNE
tsne_cingulate = TSNEVisualizer(decompose=None, random_state=1, perplexity=10)
tsne_cingulate.fit(X_cingulate, y_cingulate)
tsne_cingulate.poof(outpath="reports/figures/tsne_cingulate.png")
