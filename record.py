import os
from datetime import datetime
import subprocess
import json
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


with open('./ping.json', 'r') as f:
    conf_ping = json.load(f)

for target in conf_ping.values():

    if target['size'] == None:
        target['size'] = random.randint(1, 60) * 1024
    text = Ping(target)
    Mbps = Parse(text, target['size'])

    if not os.path.isdir('data/' + target['host']):
        os.makedirs('data/' + target['host'])

    now = datetime.now().strftime('%Y%m%d%H%M%S')

    with open('data/{}/{}.log'.format(target['host'], now[:8]), 'a') as f:
        f.write('{},{},{}\n'.format(now, target['size'], Mbps))
