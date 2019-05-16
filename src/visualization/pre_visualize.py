"""A script for visualising data before feature engineering and training

2 plots are used here - volcano and UMAP 

The volcano plot allows for a visualisation of those genes that are differentially expressed
and the significance of those changes.

UMAP is an alternative to tSNE plotting and is a dimensionality reduction technique 
for visualising clusters
"""

import matplotlib.pyplot as plt
import pandas as pd

import src.data.CleanFrame as cf


def prep_volcano(cf):
    """Prep data for volcano plots

    Cleans off unnecessary columns information then aggregates by means
    """
    cf_clean = cf.copy()
    cf_clean.columns = cf_clean.columns.droplevel(0)
    cf_clean.columns = cf_clean.columns.str.rstrip("12")
    columns = cf_clean.columns.unique()
    for col in columns:
        cf_clean[f"mean_{col}"] = cf_clean[col].mean(axis=1)
    cf_clean = cf_clean.drop(columns=columns)
    cf_clean["mean_q_score"] = cf_clean["mean_q_score"].replace(0, 0.000001)
    return cf_clean


def prep_umap(cf, col="label", vals=["q_score", "pep_score"]):
    """Prep data for umap plots

    Cleans off unnecessary columns information then aggregates by means
    """
    cf_clean = (
        cf.T.reset_index()
        .rename_axis(columns=None)
        .rename(columns={"level_0": "batch", "level_1": "label"})
        .filter_by_val(col=col, vals=vals, keep=False)
        .sort_values(by=["label"])
        .reset_index()
        .drop(columns=["index"])
    )
    cf_clean["label"] = cf_clean["label"].str.extract("(\D+)", expand=False)
    cf_clean["label"] = cf_clean["label"].astype("category")
    return cf_clean


if __name__ == "__main__":

    # Read in the data
    frontal = cf.CleanFrame(pd.read_pickle("data/interim/frontal_full.pkl"))
    cingulate = cf.CleanFrame(pd.read_pickle("data/interim/cingulate_full.pkl"))

    # Prep data
    frontal_volc = prep_volcano(frontal)
    cingulate_volc = prep_volcano(cingulate)
    frontal_umap = prep_umap(frontal)
    cingulate_umap = prep_umap(cingulate)

    # Save data
    pd.to_pickle(frontal_volc, "data/interim/frontal_volc.pkl")
    pd.to_pickle(cingulate_volc, "data/interim/cingulate_volc.pkl")
    pd.to_pickle(frontal_umap, "data/interim/frontal_umap.pkl")
    pd.to_pickle(cingulate_umap, "data/interim/cingulate_umap.pkl")

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

    for data in zip((frontal_umap, cingulate_umap), ("Frontal", "Cingulate")):
        for col in ("label", "batch"):
            data[0].umap(
                (x for x in data[0].columns if x not in ["label", "batch"]),
                col,
                title=f"{data[1]} {col}",
                show=False,
                save=True,
                path=f"reports/figures/{data[1]}_{col}.png",
            )
            plt.close()

    # Examine their summary data
    data = (
        cf.CleanFrame(
            pd.read_excel(
                "references/TMT_Summary_Data.xlsx",
                sheet_name=sheet,
                header=(0, 2),
                index=0,
            )
        )
        for sheet in ("frontal cortex", "anterior cingulate gyrus")
    )

    # Clean Data
    titles = (
        "Frontal Cortex TMT Summary Data.#",
        "Anterior Cingulate Gyrus TMT Summary Data.#",
    )
    data_prep = (
        prep_umap(item[0], col="batch", vals=[item[1]]) for item in zip(data, titles)
    )

    # Drop NaNs
    data_clean = (cf.loc[:, (cf != 0).all()].dropna(axis=1) for cf in data_prep)

    # Plot data
    paths = (
        "reports/figures/Frontal_sum_umap.png",
        "reports/figures/Cingulate_sum_umap.png",
    )
    for item in zip(data_clean, paths):
        item[0].umap(
            [i for i in item[0].columns if i not in ["batch", "label"]],
            "label",
            show=False,
            save=True,
            path=item[1],
        )
        plt.close()
