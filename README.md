# FAES_BIOF509_FINAL

Predicting neurodegeneration from global proteomics

Project based on the [_drivendata/cookiecutter-data-science_](https://github.com/drivendata/cookiecutter-data-science) project structure

[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![GPL License](https://badges.frapsoft.com/os/gpl/gpl.svg?v=103)](https://opensource.org/licenses/GPL-3.0/)

## About

Alzheimer's and Parkinson's disease are the two most common forms of neurodegeneration, yet good biomarkers for diagnosis and prevention are hard to come by. Deep proteomics offers an opportunity to identify marker's of the disease, The dataset provided Ping L., et al., smapled post-mortem brain tissues from 40 patient, 10 with Alzheimer's, 10 with Parkinson's, 10 with co-daignoses, and 10 controls. Between the anterior cingulate gyrus and the frontal cortex, they identified 11840 proteins across 10230 genes, representing 65% of the brain proteome. 

## Features

### Introducing the CleanFrame

I found that there were at least two things I did to every pandas DataFrame that pandas didn't have a default function for:

1. Cleaning my column names
1. Filtering a DataFrame based on the value of a specific column

So I subclassed the pd.core.frame.DataFrame and added them! CleanFrame.clean_cols() does a number of common tidying operations, such as stripping whitespace, removing spaces, lower-casing, etc., in one step. CleanFrame.filter_by_val() filters the dataframe based on the vals in a given column. It allows the user to choose whether to keep or discard the filtered values. In traditional pandas fashion, both return new dataframes, but allow users the option to perform the action in-place.

## Challenges

1. Dimensionality - 40 samples (10 per group) and ~12000 features
1. Data Wrangling - the published data is not in particularly great in structure

## Plan

1. Data wrangling
1. Exploratory data visualisation - volcano plot, tSNE
1. Dimensionality reduction/feature selection
1. Machine learning - comparison between classification and clustering
1. Validation - Leave-one-out, as sample is so small

## Citation
"Global quantitative analysis of the human brain proteome in Alzheimer’s and Parkinson’s Disease"
doi:10.1038/sdata.2018.36

