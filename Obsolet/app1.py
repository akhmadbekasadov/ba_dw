# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

testwerte=[1,2,3,2,4,1,6,3,6,8]
app.layout = html.Div(children=[
    html.H1(children='BA'),

    html.Div(children='''
        Dash: Simple Dash Server.
    '''),

    dcc.Graph(
        id='Live Data',
        figure={
            'data': [
                {'x': [5], 'y': [testwerte], 'type': 'line', 'name': 'SF'},
                #{'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'line', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug = True, host = '192.168.178.45', port = 80)
