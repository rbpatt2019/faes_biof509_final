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
