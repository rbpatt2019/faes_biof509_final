"""A script for visualising data before feature engineering and training

Two plots are used here - volcano and UMAP

The volcano plot allows for a visualisation of those genes that are differentially expressed
and the significance of those changes.

UMAP is an alternative to tSNE plotting and is a dimensionality reduction technique 
for visualising clusters

This would probably be better structured in some kind of visualising class with methods
but am currently too short on time
"""

import src.visualization.volcano
