import os
from datetime import datetime, timedelta, timezone
import subprocess
import random
import sched
import time

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

    if not os.path.isdir('data/' + host):
        os.makedirs('data/' + host)
    with open('data/{}/{}.csv'.format(host, now.split('T')[0]), 'a') as f:
        f.write('{},{},{}\n'.format(now, size, rtt))

def Main():

    global host
    global size
    text = Ping(host, size)
    rtt = Parse(text)
    Record(host, size, rtt)


host = 'www.amazon.co.jp'

s = sched.scheduler(time.time, time.sleep)

while True:
    size = int(random.uniform(1, 10) * 1024)
    s.enter(60, 1, Main)
    s.run()
