if __name__ == "__main__":
    # Frontal cortex data
    frontal = make_data(
        "data/raw/f*",
        usecols=[2, 5, 9, 10, 72, 73, 74, 75, 76, 77, 78, 79],
        names=[
            "master",
            "accession",
            "q_score",
            "pep_score",
            "AD1",
            "AD2",
            "Control1",
            "Control2",
            "PD1",
            "PD2",
            "ADPD1",
            "ADPD2",
        ],
        index_col=1,
        axis=1,
        join="inner",
        keys=[1, 2, 3, 4, 5],
    )
    pd.to_pickle(frontal, "data/interim/frontal_full.pkl")
#And again with the cingulate data...
