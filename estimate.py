import measure
import sys
from scipy import stats

class Intercept:

    def __init__(self, param, dist_prior):

        self.param = param
        self.dist_prior = dist_prior

    def Likelihood(hypothesis=False):

        if hypothesis:
            param = self.dist_prior.rvs()
        else:
            param = self.param

        return self.dist_prior.pdf(param)


def GetParameterLinear(intercept, coefficient, sample):



host = sys.argv[1]
