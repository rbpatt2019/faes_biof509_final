# Reducer for tSNE
tsne_frontal = TSNEVisualizer(decompose=None, random_state=1, perplexity=10)
tsne_frontal.fit(X_frontal, y_frontal)
tsne_frontal.poof(outpath='reports/figures/tsne_frontal.png')
