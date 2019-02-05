import sys
from datetime import datetime
import os
from matplotlib import pyplot
from matplotlib import dates
import matplotlib
matplotlib.use('Agg')


host = sys.argv[1]


def Get(host):

    files = os.listdir('./data/{}'.format(host))
    files.sort()
    data = []
    for filename in files:
        with open('./data/{}/{}'.format(host, filename), 'r') as f:
            data += [line.strip().split(',') for line in f]

    timeseries = [datetime.strptime(row[0], '%Y%m%d%H%M%S') for row in data]
    size = [int(row[1]) / 1024 for row in data]
    Mbps = [float(row[2]) for row in data]

    return timeseries, size, Mbps


def Plot(timeseries, mbps):

    fig = pyplot.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(timeseries, mbps)

    if not os.path.isdir('png'):
        os.makedirs('png')
    fig.savefig('png/{}_plot.png'.format(host))

    fig.clf()


def Hist(mbps):

    fig = pyplot.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.hist(mbps, bins=20)

    if not os.path.isdir('png'):
        os.makedirs('png')
    fig.savefig('png/{}_hist.png'.format(host))

    fig.clf()


def Scatter(size, mbps):

    fig = pyplot.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(size, mbps)

    if not os.path.isdir('png'):
        os.makedirs('png')
    fig.savefig('png/{}_scatter.png'.format(host))

    fig.clf()


timeseries, size, mbps = Get(sys.argv[1])
Plot(timeseries, mbps)
Hist(mbps)
Scatter(size, mbps)
