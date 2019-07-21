import os
import datetime
import pandas
import numpy
from scipy import stats
import pymc3
import arviz
from matplotlib import pyplot

def Load(host):

    files = os.listdir('./data/{}'.format(host))
    datas = [pandas.read_csv('./data/{}/{}'.format(host, f), parse_dates=True) for f in files]
    data = pandas.concat(datas)

    return data

host = 'www.amazon.co.jp'
directory = './data/{}'
term_hours = 3

data = Load(host)
data = data.dropna()

data['size'] = data['size'] / 1024
print(data.describe())
data = data.sort_values(by=['rtt'])
data = data.drop(213)
print(data)
pyplot.hist(data['rtt'])
pyplot.show()

with pymc3.Model() as linear_model:

    alpha = pymc3.HalfCauchy('alpha', 5)
    beta = pymc3.HalfCauchy('beta', 5)

    mu = pymc3.Deterministic('mu', alpha + beta*data['size'])
    sigma = pymc3.HalfCauchy('sigma', 5)

    rtt = pymc3.Normal('rtt', mu=mu, sigma=sigma, observed=data['rtt'])

    trace = pymc3.sample(tune=1000, chains=4)

    pymc3.traceplot(trace, var_names=['alpha', 'beta', 'sigma'])
    pyplot.savefig('trace.png')
    pyplot.clf()

    posterior = numpy.array([numpy.random.choice(s) for s in pymc3.sample_posterior_predictive(trace)['rtt'].T])
    pyplot.scatter(data['size'], data['rtt'], alpha=0.2)
    pyplot.scatter(data['size'], posterior, alpha=0.2)
    #pyplot.ylim(0,20)
    pyplot.savefig('posterior.png')
    pyplot.clf()

    exit()

    print(trace['alpha'].shape)
    print(trace['beta'].shape)
    print(trace['sigma'].shape)
    size_sample = 500
    sizes = numpy.random.uniform(1, 60, size=size_sample)
    alphas = numpy.random.choice(trace['alpha'], size=size_sample, replace=True)
    betas = numpy.random.choice(trace['beta'], size=size_sample, replace=True)
    sigmas = numpy.random.choice(trace['sigma'], size=size_sample, replace=True)
    rtts = stats.lognorm.rvs(sigmas, loc=0, scale=numpy.exp(alphas + betas*sizes))
    pyplot.scatter(sizes, rtts)
    pyplot.savefig('check.png')

#arviz.plot_autocorr(trace)
