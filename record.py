from matplotlib import dates
from matplotlib import pyplot
import json
import subprocess
from datetime import datetime
import os
import matplotlib
matplotlib.use('Agg')
import random

os.chdir('measurenet')


def Ping(target):

    command = [
        'ping',
        '-s', str(target['size']),
        '-c', str(target['count']),
        '-i', str(target['interval']),
        target['host']
    ]

    process = subprocess.run(command, stdout=subprocess.PIPE)
    text = process.stdout.decode('UTF-8')

    print(text)
    return text


def Parse(text, size):

    # 100%パケットロスだったらNoneを返す
    avg = [line for line in text.split('\n')][-2].split(' ')[-2].split('/')[1]
    bit = size * 8 * 2
    bps = bit / (float(avg) / 1000)
    Mbps = bps / 1000 / 1000

    return Mbps


def Plot(host):

    files = os.listdir('./data/{}'.format(host))
    files.sort()
    data = []
    for filename in files:
        with open('./data/{}/{}'.format(host, filename), 'r') as f:
            data += [line.strip().split() for line in f]

    timeseries = [datetime.strptime(row[0], '%Y%m%d%H%M%S') for row in data]
    Mbps = [float(row[1]) for row in data]

    fig = pyplot.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(timeseries, Mbps)

    if not os.path.isdir('png'):
        os.makedirs('png')
    fig.savefig('png/{}.png'.format(host))

    fig.clf()


with open('./ping.json', 'r') as f:
    conf_ping = json.load(f)

for target in conf_ping.values():

    if target['size'] == None:
        target['size'] = random.randint(1, 50) * 1024
    text = Ping(target)
    Mbps = Parse(text, target['size'])

    if not os.path.isdir('data/' + target['host']):
        os.makedirs('data/' + target['host'])

    now = datetime.now().strftime('%Y%m%d%H%M%S')

    with open('data/{}/{}.log'.format(target['host'], now[:8]), 'a') as f:
        f.write('{},{},{}\n'.format(now, target['size'], Mbps))
