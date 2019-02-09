import random
import math
from datetime import datetime
import os


def Calc(size, avg):

    bit = size * 8 * 2
    bps = bit / (avg / 1000)
    Mbps = bps / 1000 / 1000

    return Mbps


def Get(host):

    files = os.listdir('./data/{}'.format(host))
    files.sort()
    data = []
    for filename in files:
        with open('./data/{}/{}'.format(host, filename), 'r') as f:
            data += [line.strip().split(',') for line in f]

    timeseries = [datetime.strptime(row[0], '%Y%m%d%H%M%S') for row in data]
    size = [int(row[1]) for row in data]
    Mbps = [Calc(int(row[1]), float(row[2])) for row in data]

    return timeseries, size, Mbps


def Estimate(mbps, size, time):

    overhead = 100

    for i in range(10000):

        overhead_hypo = random.expovariate(overhead)
        print('current parameter is {}'.format(overhead))
        print('hpo parameter is {}'.format(overhead_hypo))
        varience = 0
        varience_hypo = 0

        for b, s in zip(mbps, size):
            varience += (b - ((overhead + b) / s)) ** 2
            varience_hypo += (b - ((overhead + b) / s)) ** 2

        print('current varience is {}'.format(varience))
        print('hypo varience is {}'.format(varience_hypo))

        if varience_hypo < varience:
            overhead = overhead_hypo

        print('last parameter is {}'.format(overhead))
        print()

    return overhead
