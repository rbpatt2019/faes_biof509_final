#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import pytest

import src.data.CleanFrame as cf

def test_clean_col_defaults():
    test = cf.CleanFrame({" A B ": [1, 2], " C D ": [3, 4]})
    assert all(test.clean_cols().columns == ["a_b", "c_d"]) # Expected results
    test.clean_cols()
    assert all(test.columns == [' A B ', ' C D ']) # Insure is not in place

def test_clean_col_type_check():
    test = cf.CleanFrame({" A B ": [1, 2], " C D ": [3, 4]})
    # Test that wrong values raise a value error
    with pytest.raises(ValueError):
        test.clean_cols(strip=1)
        test.clean_cols(spaces="a")
        test.clean_cols(lower=[True, False])
        test.clean_cols(upper=(True, False))
        test.clean_cols(inplace={1: False, "a": True})
        test.clean_cols(strip=1)

def test_filter_by_val_defaults():
    test = cf.CleanFrame({"A": [1, 2], "B": [3, 4]})
    # Expected results
    assert all(test.filter_by_val(col="A", vals=[1]) == cf.CleanFrame({'A': [1], 'B': [3]}))
    # Insure operation is not inplace
    test.filter_by_val(col='A', vals=[1])
    assert all(test == cf.CleanFrame({"A": [1, 2], "B": [3, 4]}))

def test_filter_by_val_type_check():
    test = cf.CleanFrame({"A": [1, 2], "B": [3, 4]})
    with pytest.raises(ValueError):
        test.filter_by_val(col=1)
        test.filter_by_val(col=['a', 'b', 'c'])
        test.filter_by_val(col=False)
        test.filter_by_val(vals=1)
        test.filter_by_val(vals='a')
        test.filter_by_val(vals=False)
        test.filter_by_val(inplace=1)
        test.filter_by_val(keep='a')
        test.filter_by_val(inplace=(1, 2, 3))
        test.filter_by_val(inplace=[True, False])
