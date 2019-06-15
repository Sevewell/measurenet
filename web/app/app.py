#!/usr/lib/python3

import measure
import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)

host = 'www.amazon.co.jp'
term_days = 1

def serve_layout():

    data = measure.Get(host, term_days)

    return html.Div(children=[

        html.H1(children='Measurement Speed Internet'),
        html.Div(children='''
            Dash: A web application framework for Python.
        '''),
        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x':data['time'], 'y':data['mbps'], 'type': 'scatter', 'name': 'mbps'}
                ],
                'layout': {
                    'title': 'Dash Data Visualization'
                }
            }
        )

    ])

app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8000)