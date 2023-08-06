from sklearn.datasets import make_hastie_10_2
from sklearn.model_selection import train_test_split

import numpy as np

def createSomeData():

    n_samples = 100000
    test_size = 0.2

    # Hastie_10_2
    # X_i ~ Gaussian
    # sum of X_i^2 > Chi-squire(10, 0.5) 9.34, then 1, otherwise -1
    X, y_org = make_hastie_10_2(n_samples=n_samples) 
    z = np.random.randn(n_samples)
    y = y_org * z
    y[y > 0] = 1
    y[y <= 0] = 0
    X = np.hstack((X, z.reshape(n_samples,1)))
    n, m = X.shape
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)

    return X_train, X_test, y_train, y_test

                                            