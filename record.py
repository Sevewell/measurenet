import os
from datetime import datetime
import subprocess
import random

os.chdir('measurenet')


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

    now = datetime.now().strftime('%Y%m%d%H%M%S')

    if not os.path.isdir('data/' + host):
        os.makedirs('data/' + host)
    with open('data/{}/{}.csv'.format(host, now[:8]), 'a') as f:
        f.write('{},{},{}\n'.format(now, size, rtt))


host = 'www.amazon.co.jp'
size = int(random.uniform(1, 10) * 1024)

text = Ping(host, size)
rtt = Parse(text)

Record(host, size, rtt)

