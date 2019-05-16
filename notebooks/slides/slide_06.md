## Sub-classing DataFrames

```python
class CleanFrame(pd.core.frame.DataFrame):

    @property
    def _constructor(self):
        return CleanFrame

    def filter_by_val(self, col="", vals=[], keep=True, inplace=False):
        # Type check inputs
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
```
