import os
from datetime import datetime
import subprocess
import random

os.chdir('measurenet')


def Ping(host, size_kb):

    command = ['ping', '-s', str(int(size_kb * 1024)), '-c', '1', host]

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

    size_kb = size_max
    while size_kb >= size_max:
        size_kb = random.expovariate(0.5)
    
    return size_kb


def Record(host, size, rtt):

    now = datetime.now().strftime('%Y%m%d%H%M%S')

    if not os.path.isdir('data/' + host):
        os.makedirs('data/' + host)
    with open('data/{}/{}.csv'.format(host, now[:8]), 'a') as f:
        f.write('{},{},{}\n'.format(now, size, rtt))


host = 'www.amazon.co.jp'
size = Size(30)

text = Ping(host, size)
rtt = Parse(text)

Record(host, size, rtt)

