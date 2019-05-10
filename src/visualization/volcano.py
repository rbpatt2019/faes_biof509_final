"""A script for making volcano plots

The volcano plot allows for a visualisation of those genes that are differentially expressed
and the significance of those changes.

This would probably be better structured in some kind of visualising class with methods
but am currently too short on time
"""

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
    df.columns = df.columns.str.rstrip('12')
    columns = df.columns.unique()
    for col in columns:
        df[f'mean_{col}'] = df[col].mean(axis=1)
    df = df.drop(columns=columns)
    df['mean_q_score'] = df['mean_q_score'].replace(0, 0.000001)
    return df

# Read in the data
frontal = cf.CleanFrame(pd.read_pickle("data/interim/frontal_full.pkl"))
cingulate = cf.CleanFrame(pd.read_pickle("data/interim/cingulate_full.pkl"))

# Prep data
frontal_volc = prep_volcano(frontal)
cingulate_volc = prep_volcano(cingulate)

# Save volcano data
pd.to_pickle(frontal_volc, "data/interim/frontal_volc.pkl")
pd.to_pickle(cingulate_volc, "data/interim/cingulate_volc.pkl")

# Plot data
data = ['mean_ad', 'mean_pd', 'mean_adpd']
for df in zip((frontal_volc, cingulate_volc), ('Frontal', 'Cingulate')):
    for col in ('mean_ad', 'mean_pd', 'mean_adpd'):
        df[0].volcano(col, 'mean_q_score', is_log=False, title=f'{df[1]} {col}')
        plt.savefig(f"reports/figures/{df[1]}_{col}.png", dpi=600)
        plt.close()

print("Volcano Plots Made!")
