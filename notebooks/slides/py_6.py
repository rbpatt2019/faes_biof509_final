def filter_by_val(self, col="", vals=[], keep=True, inplace=False):
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
