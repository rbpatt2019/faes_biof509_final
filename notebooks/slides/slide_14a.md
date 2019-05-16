## UMAP Plots

```python
class CleanFrame(pd.core.frame.DataFrame):
    def umap(
        self,
        X_list,
        y_name,
        plt_comp=(0, 1),
        title="UMAP Plot",
        title_size=12,
        label_size=8,
        show=True,
        save=False,
        path="report/figures/umap.png",
        **kwargs,
    ):
        # Type check inputs
        # Reducer for umap
        X, y = self[X_list], self[y_name]
        reducer = umap.UMAP(random_state=1, **kwargs)
        embedding = reducer.fit_transform(X)

        # Create conditions/choices for colors, leave first for default
        # Plot UMAP
        plt.scatter(
            embedding[:, plt_comp[0]],
            embedding[:, plt_comp[1]],
            s=5,
            c=np.select(conditions, choices, 0),
            cmap="Spectral",
        )

        # Plot settings
        # Same as volcano

        # Show or save
        if save:
            plt.savefig(path, dpi=600)
        if show:
            plt.show()

```
