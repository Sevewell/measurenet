#!/usr/lib/python3

import measure
import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import timedelta

app = dash.Dash(__name__)

host = 'www.amazon.co.jp'
term_hours = 1

def serve_layout():

    data = measure.Get(host, term_hours)

    return html.Div(children=[

        html.H1(children='Measurement Speed Internet'),
        html.Div(children='自宅インターネット回線の速度を測ります。'),
        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {
                        'x': [d + timedelta(hours=9) for d in data['time']],
                        'y':data['mbps'],
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
                        'x': [s / 1024 for s in data['size']],
                        'y': data['rtt'],
                        'type': 'scatter',
                        'mode': 'markers'
                    }
                ],
                'layout': {
                    'title': '送信サイズ（KB）とRTTの関係',
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