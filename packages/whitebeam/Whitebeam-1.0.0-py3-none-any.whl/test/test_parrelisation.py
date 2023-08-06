from whitebeam.base.regr import RegTree
from whitebeam.base.xgb import XGBTree

from sklearn.datasets import make_friedman1
from sklearn.datasets import make_friedman2
from sklearn.datasets import make_friedman3

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import PolynomialFeatures

import numpy as np
import time
from collections import Counter

import pytest

def test_regression_parallelisation(): 

    n_samples = 10000
    max_depth = 5
    test_size = 0.2
    X, y = make_friedman1(n_samples=n_samples) 
    poly = PolynomialFeatures(degree=3)
    X = poly.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                        test_size=test_size)

    model_p1 = RegTree(max_depth=max_depth, n_jobs=1)
    model_p2 = RegTree(max_depth=max_depth, n_jobs=2)

    start = time.time()
    model_p1.fit(X_train, y_train)
    time_fit_p1 = time.time() - start

    start = time.time()
    model_p2.fit(X_train, y_train)
    time_fit_p2 = time.time() - start

    assert time_fit_p2 < 5

def test_xgboost_parallelisation(): 

    n_samples = 10000
    max_depth = 5
    test_size = 0.2
    X, y = make_friedman1(n_samples=n_samples) 
    poly = PolynomialFeatures(degree=3)
    X = poly.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                        test_size=test_size)

    model_p1 = XGBTree(max_depth=max_depth, n_jobs=1)
    model_p2 = XGBTree(max_depth=max_depth, n_jobs=2)

    start = time.time()
    model_p1.fit(X_train, y_train)
    time_fit_p1 = time.time() - start

    start = time.time()
    model_p2.fit(X_train, y_train)
    time_fit_p2 = time.time() - start

    assert time_fit_p2 < 5





