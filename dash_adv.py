# Run this app with:
#  >conda activate base
#  >pip install dash (if not done previously)
#  >python dash_basic.py
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import pymssql

# for later iterations:
# import pymssql

from config import database
from config import table
from config import username
from config import password
from config import server

import random
from dash.dependencies import Input, Output


app = dash.Dash(__name__)

def get_data_sql():
    conn = pymssql.connect(server,username, password, database)
    cursor = conn.cursor()
    query = f"SELECT * FROM {table}"
    df = pd.read_sql(query, conn)
    return df

def get_data_full():
    df = pd.read_csv(f'data/Cars93.csv')
    return df

def get_data_sample():
    i = random.randint(0,2)
    df = pd.read_csv(f'data/sample-{i}')
    print(i)
    return df

def trim_cols(df):
    cols = ['Weight', 'MPG.city', 'MPG.highway']
    for col in cols:
        df[col] = df[col].astype('int')
    df2 = df[['Weight', 'MPG.city', 'MPG.highway']]
    return df2


def make_figure_1():
    df = get_data_sample()
    df2 = trim_cols(df)
    fig = px.scatter(
                df2, 
                x='Weight', 
                y='MPG.city', 
                title='My first plot',
    )
    return fig

def make_figure_2(opacity=0.2):
    df = get_data_full()
    df2 = trim_cols(df)
    fig = px.scatter(
                df2, 
                x='Weight', 
                y='MPG.city', 
                title=f'Second Plot with opacity of {opacity}',
                opacity=opacity,
    )
    return fig

# put figures into dashboard's html
app.layout = html.Div(children=[
    html.H1(children='Hello Dash. Wills Dashboard!.'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='fig-1',
        figure=make_figure_1()
    ),

    dcc.Interval(
        id='interval-component',
        interval=5*1000, # in milliseconds
        n_intervals=0
    ),
    
    dcc.Input(
        value="0.2",
        id='opacity-input',
        
    ),

    dcc.Graph(
            id='fig-2',
            figure=make_figure_2()
    ),
])

@app.callback(
    Output('fig-1', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_figure_1(n_intervals=None):
    return make_figure_1()

@app.callback(
    Output('fig-2', 'figure'),
    Input('opacity-input', 'value')
)
def update_opactiy(opacity_value):
    try:
        opacity_float = float(opacity_value)
    except:
        opacity_float = 1.0
    if (opacity_float > 1.0) or (opacity_float < 0.0):
        opacity_float = 1.0
    
    return make_figure_2(opacity_float)


if __name__ == '__main__':
    app.run_server(debug=True )
