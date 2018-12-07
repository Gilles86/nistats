"""
Test functions for models.regression
"""

import numpy as np

from nistats.regression import OLSModel, ARModel, SimpleRegressionResults

from nose.tools import assert_equal, assert_true
from numpy.testing import assert_array_almost_equal, assert_array_equal


RNG = np.random.RandomState(20110902)
X = RNG.standard_normal((40, 10))
Y = RNG.standard_normal((40,))


def test_OLS():
    model = OLSModel(design=X)
    results = model.fit(Y)
    assert_equal(results.df_resid, 30)


def test_AR():
    model = ARModel(design=X, rho=0.4)
    results = model.fit(Y)
    assert_equal(results.df_resid, 30)


def test_OLS_degenerate():
    Xd = X.copy()
    Xd[:, 0] = Xd[:, 1] + Xd[:, 2]
    model = OLSModel(design=Xd)
    results = model.fit(Y)
    assert_equal(results.df_resid, 31)


def test_AR_degenerate():
    Xd = X.copy()
    Xd[:, 0] = Xd[:, 1] + Xd[:, 2]
    model = ARModel(design=Xd, rho=0.9)
    results = model.fit(Y)
    assert_equal(results.df_resid, 31)

def test_simple_results():
    model = OLSModel(X)
    results = model.fit(Y)
    residfull = results.resid
    predictedfull = results.predicted
    
    simple_results = SimpleRegressionResults(results)
    assert_array_equal(results.predicted, simple_results.predicted(X))
    assert_array_equal(results.resid, simple_results.resid(Y, X))
