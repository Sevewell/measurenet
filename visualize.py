import measure
import sys
from datetime import datetime
import os
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot
from matplotlib import dates


def PlotRTT(ax, timeseries, value):

    ax.plot(timeseries, value)
    ax.set_ylim([0, 50])
    ax.set_xlabel('Date')
    ax.set_ylabel('RTT')
    ax.xaxis.set_major_formatter(dates.DateFormatter('%m%d'))


def PlotMbps(ax, timeseries, value):

    ax.plot(timeseries, value)
    #ax.set_ylim([0, 50])
    ax.set_xlabel('Date')
    ax.set_ylabel('Mbps')
    ax.xaxis.set_major_formatter(dates.DateFormatter('%m%d'))


def Hist(name, value):

    fig = pyplot.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.hist(value, bins=20, density=True)

    fig.savefig('{}_hist.png'.format(name))

    fig.clf()


def ScatterRTT(ax, size, rtt):

    size_k = [s / 1024 for s in size]

    ax.scatter(size_k, rtt, s=1, alpha=0.5)
    ax.set_xlim([0, 11])
    ax.set_ylim([0, 30])
    ax.set_xlabel('size(kb)')
    ax.set_ylabel('RTT')


def ScatterMbps(ax, size, Mbps):

    size_k = [s / 1024 for s in size]

    ax.scatter(size_k, Mbps, s=1, alpha=0.5)
    ax.set_xlim([0, 11])
    ax.set_ylim([0, 25])
    ax.set_xlabel('size(kb)')
    ax.set_ylabel('Mbps')


def HistMissing(ax, data):

    size_value = [s for r,s in zip(data['rtt'], data['size']) if r != None]
    size_missing = [s for r,s in zip(data['rtt'], data['size']) if r == None]

    ax.hist(size_value, range=(0, 15000), bins=25, alpha=0.5, density=True)
    ax.hist(size_missing, range=(0, 15000), bins=25, alpha=0.5, density=True)


if __name__ == "__main__":

    host = sys.argv[1]
    data = measure.Get(host)

    directory = 'png/' + host
    if not os.path.isdir(directory):
        os.makedirs(directory)
    os.chdir(directory)

    fig = pyplot.figure(figsize=(16,9))

    PlotRTT(fig.add_subplot(2,2,1), data['time'], data['rtt'])
    ScatterRTT(fig.add_subplot(2,2,2), data['size'], data['rtt'])
    PlotMbps(fig.add_subplot(2,2,3), data['time'], data['mbps'])
    ScatterMbps(fig.add_subplot(2,2,4), data['size'], data['mbps'])

    fig.savefig('Dashboard.png')

    fig = pyplot.figure()
    HistMissing(fig.add_subplot(1,1,1), data)
    fig.savefig('Missing.png')