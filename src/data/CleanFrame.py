import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import umap
from matplotlib.colors import LinearSegmentedColormap

import src.data.CleanFrame as cf


class CleanFrame(pd.core.frame.DataFrame):
    """Sub-classed DataFrame with expanded method for cleaning
    
    Frequently, when loading data, a number of cleaning steps are performed that do not have direct functions in the pandas module.
    This class seeks to add those functionalities on top of pandas to expand its capacity

    Methods
    -------
    clean_cols: 
        Cleans column names by stripping white space, removing white space, and converting all characters to either lower or upper case
    filter_by_val:
        Select rows based on values in a given column
    volcano:
        In progress. Will make volcano plots!
    """

    @property
    def _constructor(self):
        return CleanFrame

    def clean_cols(
        self,
        strip=True,
        spaces=True,
        space_char="_",
        lower=True,
        upper=False,
        inplace=False,
    ):
        """Cleans column names

        Inputs
        ------
        strip: bool
            default: True
            Whether to strip leading and trailing whitespace
        spaces: bool
            default: True
            Whether to replace spaces with space_char
            Note that odd behaviour results if strip=True and spaces=False
        space_char: str
            default: '_'
            If spaces=True, then ' ' will be replaced with this value
        lower: bool
            default: True
            Whether to convert all letters to lower case
            Note that odd behaviour will results if both lower=True and upper=True
        upper: bool
            default: False
            Whether to convert all letters to upper case
            Note that odd behaviour will results if both lower=True and upper=True
        inplace: bool
            If true, the operation occurs inplace, altering self.

        Outputs
        -------
        new_data: CleanFrame
            Only if inplace=False
            The cleaned dataframe
        """

        # Type check inputs
        for i in (strip, spaces, lower, upper, inplace):
            if not (isinstance(i, bool)):
                raise ValueError(f"{i} must be a bool")
        if not isinstance(space_char, str):
            raise ValueError("space_char must be a str")

        # Operate
        new_data = self.copy(deep=True)
        if strip:
            new_data.columns = new_data.columns.str.strip()
        if spaces:
            new_data.columns = new_data.columns.str.replace(" ", space_char)
        if lower:
            new_data.columns = new_data.columns.str.lower()
        if upper:
            new_data.columns = new_data.columns.str.upper()

        # self._update_inplace is from pandas.core.frame
        if inplace:
            self._update_inplace(new_data)
        else:
            return new_data

    def filter_by_val(self, col="", vals=[], keep=True, inplace=False):
        """Keeps rows of a dataframe based on value(s) in a column(s)

        Inputs
        ------
        cols: str
            column name to be used for filtering. col must be in self.columns
        vals: list  
            Values to search for in columns
        keep: bool
            If false, drop rows where vals are in cols
            If true, drop rows where vals are NOT in cols
        inplace: bool
            If true, the operation occurs inplace, altering self.

        Outputs
        -------
        new_data: CleanFrame
            Only if inplace=False
            The cleaned dataframe
        """

        # Type check inputs
        for i in (keep, inplace):
            if not isinstance(i, bool):
                raise ValueError(f"{i} must be a bool")
        if not isinstance(col, str):
            raise ValueError("col must be a str in self.columns")
        if not isinstance(vals, (list, tuple)):
            raise ValueError("vals must be a list or tuple")

        # Operate, checking whether to keep or discard
        if keep:
            new_data = self[self[col].isin(vals)]
        else:
            new_data = self[~self[col].isin(vals)]

        # self._update_inplace is from pandas.core.frame
        if inplace:
            self._update_inplace(new_data)
        else:
            return new_data

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

        """Makes a volcano plot of the data

        Inputs
        ------
        x: str
        Column name containing fold change values
        y: str
        Column name containing q_scores
        is_log: bool, Optional
        Whether or not the passed data has already had its log taken
        If false, the appropriate log will be taken of both x and y
        fold_cut: numeric, Optional
        log2(fold_change) to consider significant
        Default is fold_change greater than 1.5
        fold_cut: numeric, Optional
        -log10(q_score) to consider significant
        Default is q_score less than 0.05
        title: str, Optional
        Plot title
        title_size: numeric, Optional
        Font size, in pts, to use for Figure title
        label_size: numeric, Optional
        Font size, in pts, to use for axes title
        show: bool, Optional
        If true, display the plot
        save: bool, Optional
        If true, save the plot
        path: str, Optional
        Where to save the plot, if save == True

        Outputs
        -------
        """

        # Type check inputs
        for i in (x, y, title, path):
            if not isinstance(i, str):
                raise ValueError(f"{i} must be a str")
        for i in (is_log, show, save):
            if not isinstance(i, bool):
                raise ValueError(f"{i} must be a bool")
        for var in (title_size, label_size):
            try:
                float(var)
            except (ValueError, TypeError) as err:
                print(f"{var} needs to be numeric")
                raise

        # Log, if necessary
        if not is_log:
            x, y = np.log2(self[x]), -np.log10(self[y])
        else:
            x, y = self[x], self[y]

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
        plt.title(title, fontdict={"fontsize": title_size}, pad=15)
        plt.gca().set_aspect("equal", "datalim")
        cbar = plt.colorbar(
            boundaries=np.arange(4) - 0.5, ticks=np.arange(3), shrink=0.33
        )
        cbar.ax.set_yticklabels(
            ["Sig. Under", "N.S.", "Sig. Over"], fontdict={"fontsize": label_size}
        )
        plt.xlabel("log2(fold_change)", fontdict={"fontsize": label_size}, labelpad=5)
        plt.ylabel("-log10(q_score)", fontdict={"fontsize": label_size}, labelpad=10)
        plt.tick_params(axis="both", labelsize=label_size)

        # Show or save
        if save:
            plt.savefig(path, dpi=600)
        if show:
            plt.show()

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
        """Makes a UMAP plot of the data

        Inputs
        ------
        X_list: iterable
            List of columns to be used as features
        y_name: str
            Column containing labels
        plt_comp: tuple
            Dimensions to be plotted
        title: str, Optional
            Plot title
        title_size: numeric, Optional
            Font size, in pts, to use for Figure title
        label_size: numeric, Otional
            Font size, in pts, to use for axes title
        show: bool, Optional
            If true, display the plot
        save: bool, Optional
            If true, save the plot
        path: str, Optional
            Where to save the plot, if save == True
        kwargs:
            Additional parameters to be passed to umap.UMAP()

        Outputs
        -------
        """
        # Type check inputs
        for i in (y_name, title, path):
            if not isinstance(i, str):
                raise ValueError(f"{i} must be a str")
        for i in (save, show):
            if not isinstance(i, bool):
                raise ValueError(f"{i} must be a bool")
        for var in (title_size, label_size):
            try:
                float(var)
            except (ValueError, TypeError) as err:
                print(f"{var} needs to be numeric")
                raise
        if not isinstance(plt_comp, tuple):
            raise ValueError(f'plt_comp must be a tuple')

        # Reducer for umap
        X, y = self[X_list], self[y_name]
        reducer = umap.UMAP(random_state=1, **kwargs)
        embedding = reducer.fit_transform(X)

        # Create conditions/choices for colors, leave first for default
        choices = np.arange(1, len(y.unique()))
        conditions = [y == item for item in y.unique()[1:]]

        # Plot UMAP
        plt.scatter(
            embedding[:, plt_comp[0]],
            embedding[:, plt_comp[1]],
            s=5,
            c=np.select(conditions, choices, 0),
            cmap="Spectral",
        )

        # Plot settings
        sns.despine(offset=5, trim=False)
        plt.title(title, fontdict={"fontsize": title_size}, pad=15)
        plt.gca().set_aspect("equal", "datalim")
        cbar = plt.colorbar(
            boundaries=np.arange(len(y.unique()) + 1) - 0.5,
            ticks=np.arange(len(y.unique())),
            shrink=0.33,
        )
        cbar.ax.set_yticklabels(list(y.unique()), fontdict={"fontsize": label_size})

        # Show or save
        if save:
            plt.savefig(path, dpi=600)
        if show:
            plt.show()
