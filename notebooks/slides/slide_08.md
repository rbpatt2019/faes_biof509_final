## Volcano Plots

```python
class CleanFrame(pd.core.frame.DataFrame):
    def volcano(
        self,
        x,
        y,
        is_log=True,
        fold_cut=0.585,
        q_cut=1.301,
        title="Volcano Plot",
        title_size=12,
        label_size=8,
        show=True,
        save=False,
        path="reports/figures/volcano.png",
    ):

        # Type check inputs
        # Log, if necessary
        # Create red, black green custom color map
        cmap = LinearSegmentedColormap.from_list(
            "Volcano", [(1, 0, 0), (0, 0, 0), (0, 1, 0)], N=3
        )

        # Establish colors
        conditions = [(y >= q_cut) & (x >= fold_cut), (y >= q_cut) & (x <= -fold_cut)]
        choices = [2, 0]
        colors = np.select(conditions, choices, default=1)

        # Plot data
        plt.scatter(x, y, c=colors, cmap=cmap, s=2, alpha=0.7)
        plt.axvline(fold_cut, linestyle="--", color="gray", linewidth=1)
        plt.axvline(-fold_cut, linestyle="--", color="gray", linewidth=1)
        plt.axhline(q_cut, linestyle="--", color="gray", linewidth=1)

        # Plot settings
        sns.despine(offset=5, trim=False)
        # And others...

        # Show or save
        if save:
            plt.savefig(path, dpi=600)
        if show:
            plt.show()

```
