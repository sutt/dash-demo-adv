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
app.callback

def get_data_sql():
    conn = pymssql.connect(server,username, password, database)
    cursor = conn.cursor()
    query = f"SELECT * FROM {table}"
    df = pd.read_sql(query, conn)
    return df

def get_data_full():
    df = pd.read_csv(f'data/Cars93.csv')
    return df

def get_data_sample(i):
    # i = random.randint(0,2)
    df = pd.read_csv(f'data/sample-{i}')
    print(i)
    return df

def trim_cols(df):
    cols = ['Weight', 'MPG.city', 'MPG.highway']
    for col in cols:
        df[col] = df[col].astype('int')
    df2 = df[['Weight', 'MPG.city', 'MPG.highway']]
    return df2


def make_figure_1(sample_num=0):
    df = get_data_sample(sample_num % 3)
    df2 = trim_cols(df)
    fig = px.scatter(
                df2, 
                x='Weight', 
                y='MPG.city', 
                title=f'sample num: {sample_num % 3}',
    )
    return fig

def make_figure_2(opacity=0.2, height=500):
    df = get_data_full()
    df2 = trim_cols(df)
    print(f"====make_figure_2 is being called with opacity: {opacity} | height: {height}")
    fig = px.scatter(
                df2, 
                x='Weight', 
                y='MPG.city', 
                title=f'Second Plot with opacity of {opacity}',
                opacity=opacity,
                height=height,
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
        interval=1*1000, # in milliseconds
        n_intervals=0
    ),
    


    dcc.Input(
        value="0.2",
        id='opacity-input',
        
    ),

    dcc.Input(
        value="500",
        id='height-input',
        
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
    print(f"n_intervals {n_intervals}")
    return make_figure_1(sample_num=n_intervals)

# @app.callback(
#     Output('fig-2', 'figure'),
#     Input('opacity-input', 'value')
# )
# def update_opactiy(opacity_value):
#     try:
#         opacity_float = float(opacity_value)
#     except:
#         opacity_float = 0.5
#     if (opacity_float > 1.0) or (opacity_float < 0.0):
#         opacity_float = 1.0
    
#     return make_figure_2(opacity_float)

@app.callback(
    Output('fig-2', 'figure'),
    Input('height-input', 'value'),
    Input('opacity-input', 'value'),
)
def update_height(height_value, opacity_value):
    print(height_value, opacity_value)
    
    try:
        opacity_float = float(opacity_value)
    except:
        opacity_float = 0.5
    if (opacity_float > 1.0) or (opacity_float < 0.0):
        opacity_float = 1.0
    
    try:
        height_value = int(height_value)
    except:
        height_value = 500
    
    return make_figure_2(opacity=opacity_float ,height=height_value)




if __name__ == '__main__':
    app.run_server(debug=True )
