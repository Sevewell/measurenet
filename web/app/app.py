#!/usr/lib/python3

import os
import datetime
import pandas
import dash
import dash_core_components as dcc
import dash_html_components as html

def CalcMbps(data):

    bit = data['size'] * 8 * 2
    bps = bit / (data['rtt'] / 1000)
    mbps = bps / 1000 / 1000

    return mbps

def Load(host, term):

    files = os.listdir('./data/{}'.format(host))
    datas = [pandas.read_csv('./data/{}/{}'.format(host, f)) for f in files]
    data = pandas.concat(datas)

    data['datetime'] = [datetime.datetime.fromisoformat(d) for d in data['datetime']]

    # 欲しい期間に絞る
    start_datetime = datetime.datetime.now() - datetime.timedelta(hours=term)
    data = data[data['datetime'] > start_datetime]

    data['mbps'] = CalcMbps(data)

    return data

app = dash.Dash(__name__)

host = 'www.amazon.co.jp'
directory = './data/{}'
term_hours = 3

def serve_layout():

    data = Load(host, term_hours)

    return html.Div(children=[

        html.H1(children='Measurement Speed Internet'),
        html.Div(children='自宅インターネット回線の速度を測ります。'),
        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {
                        'x': data['datetime'] + datetime.timedelta(hours=9),
                        'y': data['mbps'],
                        'type': 'scatter',
                        'name': 'mbps',
                    }
                ],
                'layout': {
                    'title': 'Mbpsの推移'
                }
            }
        ),
        dcc.Graph(
            id='histgram-rtt',
            figure={
                'data': [
                    {
                        'x': data['rtt'],
                        'type': 'histogram',
                        'xbins': {
                            'start': 0,
                            'end': 20,
                            'size': 1
                        }
                    }
                ],
                'layout': {
                    'title': 'RTT',
                    'xaxis': {
                        'range': [5, 20]
                    }
                }
            },
            style={
                'float': 'left',
                'width': '50%'
            }
        ),
        dcc.Graph(
            id='scatter-size-and-rtt',
            figure={
                'data': [
                    {
                        'x': data['size'] / 1024,
                        'y': data['rtt'],
                        'type': 'scatter',
                        'mode': 'markers'
                    }
                ],
                'layout': {
                    'title': '送信サイズとRTTの関係',
                    'yaxis': {
                        'range': [0, 20]
                    }
                }
            },
            style={
                'float': 'right',
                'width': '50%'
            }
        )

    ])

app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8000)