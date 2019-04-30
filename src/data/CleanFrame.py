import pandas as pd


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

    def prep_data(self, inplace=False):
        """A function for project specific CleanFrame data tidying

        This function calls, in order:
            cf.clean_cols() to clean column names
            cf.filter_by_vals() to sort only master peptides
            pd.df.drop() to get rid of no longer necessary master column
            pd.df.dropna to get rid of any genes that do not have
            pd.df.set_index() to set Accession column to index
            pd.df.rename() to label samples
        
        Inputs
        ------
        inplace: bool
            If true, the operation occurs inplace, altering self.

        Outputs
        -------
        new_data: CleanFrame
            Only if inplace=False
            The cleaned dataframe
        """
        new_data = (
            self.clean_cols()
            .filter_by_val(col="master", vals=["IsMasterProtein"])
            .drop(columns="master")
            .dropna(axis=0)
            .set_index("accession")
            .rename(
                columns={
                    "abundance_ratio:_(f1,_127n)_/_(f1,_126)": "AD1",
                    "abundance_ratio:_(f1,_127c)_/_(f1,_126)": "AD2",
                    "abundance_ratio:_(f1,_128n)_/_(f1,_126)": "Control1",
                    "abundance_ratio:_(f1,_128c)_/_(f1,_126)": "Control2",
                    "abundance_ratio:_(f1,_129n)_/_(f1,_126)": "PD1",
                    "abundance_ratio:_(f1,_129c)_/_(f1,_126)": "PD2",
                    "abundance_ratio:_(f1,_130n)_/_(f1,_126)": "ADPD1",
                    "abundance_ratio:_(f1,_130c)_/_(f1,_126)": "ADPD2",
                }
            )
        )
        # self._update_inplace is from pandas.core.frame
        if inplace:
            self._update_inplace(new_data)
        else:
            return new_data
