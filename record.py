import json
import subprocess
from datetime import datetime
import os
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot
from matplotlib import dates

os.chdir('measurenet')

conf_ping_json = open('./ping.json', 'r')
conf_ping = json.load(conf_ping_json)
conf_ping_json.close()


def Ping(host):

    command = [
        'ping',
        '-s', str(conf_ping['size']),
        '-c', str(conf_ping['count']),
        '-i', str(conf_ping['interval']),
        host
    ]

    process = subprocess.run(command, stdout=subprocess.PIPE)
    text = process.stdout.decode('UTF-8')

    print(text)
    return text


def Parse(text):

    # 100%パケットロスだったらNoneを返す
    avg = [line for line in text.split('\n')][-2].split(' ')[-2].split('/')[1]
    bit = conf_ping['size'] * 8 * 2
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

with open('host.conf', 'r') as f:
    hosts = [host.strip() for host in f]

for host in hosts:

    text = Ping(host)
    Mbps = Parse(text)

    if not os.path.isdir('data/' + host):
        os.makedirs('data/' + host)

    now = datetime.now().strftime('%Y%m%d%H%M%S')

    with open('data/{}/{}.log'.format(host, now[:8]), 'a') as f:
        f.write('{} {}\n'.format(now, Mbps))

    Plot(host)

    pyplot.close()
