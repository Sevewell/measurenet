import os
from datetime import datetime, timedelta, timezone
import subprocess
import random
import sched
import time
import csv

def Ping(host, size):

    command = ['ping', '-s', str(size), '-c', '1', host]

    process = subprocess.run(command, stdout=subprocess.PIPE)
    text = process.stdout.decode('UTF-8')

    print(text)
    return text


def Parse(text):

    # 100%パケットロスだったらNoneを返す
    if '100% packet loss' in text:
        return None

    rtt = [line for line in text.split('\n')][-2].split(' ')[-2].split('/')[1]

    return rtt


def Size(size_max):

    size = size_max
    while size >= size_max:
        size = random.expovariate(0.5)
    
    return int(size * 1024)


def Record(host, size, rtt):

    #jst = timezone(timedelta(hours=+9), 'JST')
    now = datetime.now().isoformat()

    directory = 'data/{}/{}.csv'.format(host, now.split('T')[0])

    if not os.path.exists('./data/{}'.format(host)):
        os.makedirs('data/' + host)

    if not os.path.exists(directory):
        rows = [
            ['datetime','size','rtt'],
            [now, size, rtt]
        ]
    else:
        rows = [
            [now, size, rtt]
        ]

    with open(directory, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def Main():

    global host
    global size
    text = Ping(host, size)
    rtt = Parse(text)
    Record(host, size, rtt)


host = '10.254.30.254'

s = sched.scheduler(time.time, time.sleep)

while True:
    size = int(random.uniform(1, 60) * 1024)
    s.enter(60, 1, Main)
    s.run()
