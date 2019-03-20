import measure
import sys
from datetime import datetime
import os
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot
from matplotlib import dates


def Plot(timeseries, mbps):

    fig = pyplot.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(timeseries, mbps)
    ax.set_ylabel('Mbps')
    ax.xaxis.set_major_formatter(dates.DateFormatter('%m/%d'))

    fig.savefig('plot.png')

    fig.clf()


def Hist(name, value):

    fig = pyplot.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.hist(value, bins=20, density=True)

    fig.savefig('{}_hist.png'.format(name))

    fig.clf()


def ScatterRTT(size, rtt):

    size_k = [s / 1024 for s in size]

    fig = pyplot.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(size_k, rtt)
    ax.set_xlabel('size(kb)')
    ax.set_ylabel('rtt')

    fig.savefig('scatter_rtt.png')

    fig.clf()


def ScatterMbps(size, mbps):

    size_k = [s / 1024 for s in size]

    fig = pyplot.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(size_k, mbps)
    ax.set_xlabel('size(kb)')
    ax.set_ylabel('Mbps')

    fig.savefig('scatter_mbps.png')

    fig.clf()


if __name__ == "__main__":

    host = sys.argv[1]
    data = measure.Get(host)

    directory = 'png/' + host
    if not os.path.isdir(directory):
        os.makedirs(directory)
    os.chdir(directory)

    Plot(data['time'], data['mbps'])
    Hist('Mbps', data['mbps'])
    Hist('rtt', data['rtt'])
    ScatterRTT(data['size'], data['rtt'])
    ScatterMbps(data['size'], data['mbps'])
