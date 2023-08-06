import numpy as np
from test_distributions import Dataset
import pandas as pd

class RaschDichotomous:
    """
    The dichotomous Rasch Model describes two groups
    1. test items
    2. students
    Each test item is described by a parameter deltaj
    Each student is described by a parameter thetai

    Input:
    each row is a student
    each column is whether the student answered the question correctly

    A student takes a test and answers all the questions
    The total number answered correctly is then a proxy for
    the student's skill in the tested area. The total number of
    students who answered a question correctly is a proxy for
    how difficult the question is.
    """
    def __init__(self, data):
        """
        :param data: each row is a student, each column a question
        """
        self.data = data



    def set_prox_estimates(self):
        epsilon = 1e-6
        item_scores = self.data.sum(axis=0) / len(self.data.columns)
        delta_hat = np.log((1-item_scores+epsilon)/(item_scores+epsilon))
        avg_delta = np.mean(delta_hat)
        delta_hat_centered = delta_hat - avg_delta

        student_scores = self.data.sum(axis=1) / len(self.data)
        theta_hat = np.log(student_scores+epsilon/(1-student_scores+epsilon))


        self._delta = delta_hat_centered
        self._theta = theta_hat

    def _calculate_p(self):
        expand_delta = np.repeat(self._delta.to_numpy().reshape((-1, 1)), len(self._theta), axis=1)
        expand_theta = np.repeat(self._theta.to_numpy().reshape(1, -1), len(self._delta), axis=0)

        cross_diff = np.exp(expand_theta - expand_delta) / (1 + np.exp(expand_theta - expand_delta))

        return np.exp(cross_diff) / (1+np.exp(cross_diff))

    def _fit_delta_newton_raphson(self, iterations=100):

        #assume prox estimates set
        s = self.data.to_numpy().sum(axis=0)
        i = 0
        while i < iterations:

            p = self._calculate_p()

            A = (p.sum(axis=1) - s)/-(p*(1-p)).sum(axis=1)

            if np.all(np.abs(A) < 0.01): break;

            self._delta -= A
            i += 1

    def _fit_theta_newton_raphson(self, iterations=100):

        r = self.data.to_numpy().sum(axis=1)
        i = 0
        while i<iterations:
            p = self._calculate_p()
            A = (r - p.sum(axis=0))/-(p*(1-p)).sum(axis=0)

            if np.all(np.abs(A) < 0.01): break;

            self._theta -= A
            i += 1

    def fit(self):
        self.set_prox_estimates()
        self._fit_delta_newton_raphson()
        self._fit_theta_newton_raphson()

def test():
    dataset = Dataset(10, 20)
    ability, grades = dataset.get_dataset()
    df = pd.DataFrame(grades)
    print('data:', df)

    rasch = RaschDichotomous(df)
    rasch.set_prox_estimates()
    print('delta:', rasch._delta)
    print('theta:', rasch._theta)
    rasch.fit()

    print('delta:', rasch._delta)
    print('theta:', rasch._theta)

if __name__=='__main__':
    test()