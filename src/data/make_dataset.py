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
import src.data.CleanFrame as cf

hold = pd.read_csv('data/external/cingulate_batch 1__Proteins.txt', usecols=['Master', 'Accession', 'Exp. q-value', 'Sum PEP Score', 'Abundance Ratio: (F1, 127N) / (F1, 126)', 'Abundance Ratio: (F1, 127N) / (F1, 126)', 'Abundance Ratio: (F1, 128N) / (F1, 126)', 'Abundance Ratio: (F1, 128C) / (F1, 126)', 'Abundance Ratio: (F1, 129N) / (F1, 126)', 'Abundance Ratio: (F1, 129C) / (F1, 126)', 'Abundance Ratio: (F1, 130N) / (F1, 126)', 'Abundance Ratio: (F1, 130C) / (F1, 126)'], sep=None, engine='python')
