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

    print(target['host'])
    print(text)
    return text


def Parse(text, size):

    # 100%パケットロスだったらNoneを返す

    packet_loss = [line for line in text.split('\n')][-3].split(', ')[-2].split(' ')[0]
    rtt = [line for line in text.split('\n')][-2].split(' ')[-2].split('/')

    parsed = {
        'packet_loss':packet_loss,
        'rtt_avg':rtt[1],
        'rtt_dev':rtt[3]
    }

    return parsed


with open('./ping.json', 'r') as f:
    conf_ping = json.load(f)

config = {
    'host':'www.amazon.co.jp',
    'size':None,
    'count':10,
    'interval':60
}

if config['size'] == None:
    config['size'] = random.randint(1, 60) * 1024
text = Ping(config)
info = Parse(text, config['size'])

if not os.path.isdir('data/' + config['host']):
    os.makedirs('data/' + config['host'])

now = datetime.now().strftime('%Y%m%d%H%M%S')

with open('data/{}/{}.csv'.format(config['host'], now[:8]), 'a') as f:
    f.write('{},{},{},{},{}\n'.format(now, config['size'], info['packet_loss'], info['rtt_avg'], info['rtt_dev']))
