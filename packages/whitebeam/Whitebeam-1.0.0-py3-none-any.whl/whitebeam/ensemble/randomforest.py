# random forests
# Whitebeam | Kieran Molloy | Lancaster University 2020

"""
This class implements RandomForests:
- https://www.stat.berkeley.edu/~breiman/randomforest2001.pdf
"""


from whitebeam.base.regr import RegTree
import numpy as np

class RandomForests():

    def __init__(self,
                base_estimator,
                base_params,
                n_estimators=100):
        self.base_estimator = base_estimator
        self.base_params = base_params.copy()
        self.n_estimators = n_estimators
        self.estimators = []

    def fit(self, X, y):

        X = X.astype(np.float)
        y = y.astype(np.float)
        if "random_state" not in self.base_params:
            self.base_params["random_state"] = 1
 
        whitebeam_tmp = RegTree()
        whitebeam_tmp.init_cnvs(X)
        xdim, cnvs, cnvsn = whitebeam_tmp.get_cnvs()
        for i in range(self.n_estimators):
            self.base_params["random_state"] += 1
            estimator = self.base_estimator(**self.base_params)
            estimator.set_cnvs(xdim, cnvs, cnvsn)
            estimator.fit(X, y, init_cnvs=False)
            self.estimators.append(estimator)

    def predict(self, X):
        n, m = X.shape
        y_hat = np.zeros(n) 
        k = len(self.estimators)
        for estimator in self.estimators:
            y_hat += estimator.predict(X) 
        y_hat /= k
        return y_hat

    def dump(self, columns=[]): 
        return [estimator.dump(columns) 
                for estimator in self.estimators]
      





