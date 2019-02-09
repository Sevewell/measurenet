import measure
import sys
from datetime import datetime
import os
from matplotlib import pyplot
from matplotlib import dates
import matplotlib
matplotlib.use('Agg')


def Plot(timeseries, mbps):

    fig = pyplot.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(timeseries, mbps)

    fig.savefig('plot.png')

    fig.clf()


def Hist(mbps):

    fig = pyplot.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.hist(mbps, bins=20)

    fig.savefig('hist.png')

    fig.clf()


def Scatter(size, mbps, host):

    size_k = [s / 1024 for s in size]

    fig = pyplot.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(size_k, mbps)

    fig.savefig('scatter.png')

    fig.clf()


if __name__ == "__main__":

    host = sys.argv[1]
    timeseries, size, mbps = measure.Get(host)

    directory = 'png/' + host
    if not os.path.isdir(directory):
        os.makedirs(directory)
    os.chdir(directory)

    Plot(timeseries, mbps)
    Hist(mbps)
    Scatter(size, mbps, host)
