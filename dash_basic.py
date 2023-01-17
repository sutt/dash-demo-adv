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


app = dash.Dash(__name__)

conn = pymssql.connect(server,username, password, database)
cursor = conn.cursor()

query = f"SELECT * FROM {table}"

df = pd.read_sql(query, conn)

cols = ['Weight', 'MPG.city', 'MPG.highway']
for col in cols:
    df[col] = df[col].astype('int')

print(df.shape)
print(df.dtypes)

df2 = df[['Weight', 'MPG.city', 'MPG.highway']]


# construct figures
fig = px.scatter(df2, x='Weight', y='MPG.city', title='My first plot')
fig2 = px.scatter(df2, x='Weight', y='MPG.highway', title='MPG (highway) vs Weight')
fig2 = px.bar(df['Weight'])

# put figures into dashboard's html
app.layout = html.Div(children=[
    html.H1(children='Hello Dash. Wills Dashboard!.'),
    html.H1(children='Description of my project here.'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='first-graph',
        figure=fig
    ),

    dcc.Graph(
            id='example-graph',
            figure=fig2
    )
])

# run the app
if __name__ == '__main__':
    app.run_server(debug=True )
