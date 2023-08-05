# -*- coding: utf-8 -*-

__author__ = ["Markus Löning"]
__all__ = ["MatrixProfileTransformer"]

import pandas as pd
from sktime.transformations.base import _SeriesToSeriesTransformer
from sktime.utils.validation.series import check_series
from sktime.utils.validation._dependencies import _check_soft_dependencies

_check_soft_dependencies("stumpy")

import stumpy  # noqa: E402


class MatrixProfileTransformer(_SeriesToSeriesTransformer):

    _tags = {"univariate-only": True, "fit-in-transform": True}  # for unit test cases

    def __init__(self, window_length=3):
        self.window_length = window_length
        super(MatrixProfileTransformer, self).__init__()

    def transform(self, X, y=None):
        """
        Takes as input a single time series dataset and returns the matrix profile
        for that time series dataset.

        Parameters
        ----------
        X: pandas.Series
           Time series dataset(lets say of length=n)

        Returns
        -------
        Xt: pandas.Series
            Matrix Profile of time series as output with length as (n-window_length+1)
        """
        self.check_is_fitted()
        X = check_series(X, enforce_univariate=True)
        Xt = stumpy.stump(X, self.window_length)
        return pd.Series(Xt[:, 0])
