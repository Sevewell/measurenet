import random
import math
import datetime
import os


def Calc(size, rtt):

    bit = size * 8 * 2
    bps = bit / (rtt / 1000)
    Mbps = bps / 1000 / 1000

    return Mbps


def SliceDataByTerm(data, term):

    now = datetime.datetime.now()
    start = now - datetime.timedelta(days=term)

    index = None
    for i, row in enumerate(data):
        if row[0] > start:
            index = i
            break

    return data[index:]


def Get(host, term):

    files = os.listdir('./data/{}'.format(host))
    files.sort()
    data = []
    for filename in files:
        with open('./data/{}/{}'.format(host, filename), 'r') as f:
            data += [line.strip().split(',') for line in f]

    for row in data:
        row[0] = datetime.datetime.strptime(row[0], '%Y%m%d%H%M%S')

    # 欲しい期間に絞る
    data = SliceDataByTerm(data, term)

    timeseries = [row[0] for row in data]
    size = [float(row[1]) for row in data]
    rtt = [float(row[2]) if row[2] != 'None' else None for row in data]
    Mbps = [Calc(s, t) if t != None else None for s, t in zip(size, rtt)]

    result = {
        'time': timeseries,
        'size': size,
        'rtt': rtt,
        'mbps': Mbps
    }

    return result


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
