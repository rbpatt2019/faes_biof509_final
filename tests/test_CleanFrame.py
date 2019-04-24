#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import pytest

import src.data.CleanFrame as cf

def test_type_CleanFrame():
    assert isinstance(cf.CleanFrame(), pd.core.frame.DataFrame)

def test_clean_col_defaults():
    test = cf.CleanFrame({" A B ": [1, 2], " C D ": [3, 4]})
    assert all(test.clean_cols().columns == ["a_b", "c_d"])
    assert all(test.clean_cols().columns != test.columns)

def test_clean_col_type_check():
    test = cf.CleanFrame({" A B ": [1, 2], " C D ": [3, 4]})
    with pytest.raises(ValueError):
        test.clean_cols(strip=1)
        test.clean_cols(spaces="a")
        test.clean_cols(lower=[True, False])
        test.clean_cols(upper=(True, False))
        test.clean_cols(inplace={1: False, "a": True})
        test.clean_cols(strip=1)

    # def clean_cols(
    #     self,
    #     strip=True,
    #     spaces=True,
    #     space_char="_",
    #     lower=True,
    #     upper=False,
    #     inplace=False,
    # ):
