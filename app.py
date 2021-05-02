# -*- coding: utf-8 -*-
"""
Dashboard using Dash and Plotly 
@author: Prakhar
"""

#importing modules 
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import dash_table
import dash_bootstrap_components as dbc
import os

#Bootstrap component
BS = "https://stackpath.bootstrapcdn.com/bootswatch/4.5.0/lux/bootstrap.min.css"
USERNAME_PASSWORD = {'hello': 'world'}

#Launching application
app = dash.Dash(external_stylesheets=[BS])
server = app.server

loc = os.path.join('./','query_cleaned.csv')

app.title =  'Dashboard'
#OYO Logo
LOGO = "https://logos-download.com/wp-content/uploads/2019/11/OYO_Rooms_Logo.png"
server = app.server

#laoding the data
data = pd.read_csv(loc)
print(loc)
ds = data[['lead_id','lead_source', 'hub', 'city', 'cluster','latitude','longitude']]
df = ds.head(10000)

# API keys and datasets
mapbox_access_token = "pk.eyJ1IjoicHJha2hhcjE4NzQiLCJhIjoiY2thZHozazVrMDNydTJxcXAweDJyampkOSJ9.T_RDTOD6sej7MhmE8zAzSA"
map_data = pd.read_csv(loc)
# Selecting only required columns
map_data = map_data[['lead_id','lead_source','latitude','longitude']].drop_duplicates()
map_data = map_data.head(10000)
#  Layouts
layout_table = dict(
    autosize=True,
    height=500,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
)
layout_table['font-size'] = '12'
layout_table['margin-top'] = '20'

layout_map = dict(
    autosize=True,
    height=500,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
    title='Locations in selected city',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(
            lon=-73.91251,
            lat=40.7342
        ),
        zoom=10,
    )
)

dropdown = html.Div(
    [
        html.Div([
        dcc.Dropdown(
            id='name-dropdown',
            options=[{'label':name, 'value':name} for name in df.city.unique()]
            ),
            ],style={'width': '75%', 'display': 'inline-block',
                     'marginLeft': 10, 'marginRight': 10, 
                     'marginTop': 10, 'marginBottom': 10}),

    ]
)
nav_item = dbc.NavItem(dbc.NavLink("OYO Website", href="https://www.oyorooms.com/"))

navbar = dbc.Navbar(
    
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("OYO DASHBOARD", className="ml-2")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
    
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    [nav_item,
                     ], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
            dbc.NavbarToggler(id="navbar-toggler3"),
        ]
    ),
    color="dark",
    dark=True,
    className="mb-5",
)
#Setup table
table = dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in df.columns],
                    data=df.to_dict('records'),
                            css = ["https://cdn.datatables.net/1.10.21/css/jquery.dataTables.min.css"]                            
                            ,sort_action="native",
                            sort_mode="multi",
                            column_selectable="single",
                            row_selectable="multi",
                            row_deletable=True,
                            selected_columns=[],
                            selected_rows=[],
                            page_action="native",
                            page_current= 0,
                            page_size= 10,
                               
                            
                            )



@app.callback(
               Output('table', 'data'),
               [Input('name-dropdown', 'value')]
            )
def update_figure(value):
    
    dff = df.copy
    dff = df[df["city"] == value]

    return dff.to_dict('records')

mapplot = html.Div(
                        [
                            html.P('lead_source:'),
                            dcc.Dropdown(
                                id='lead_id',
                                options= [{'label': str(item),
                                                      'value': str(item)}
                                                     for item in set(map_data['lead_id'])],
                                multi=True,
                                value=list(set(map_data['lead_source']))
                        )
                    ],
                    className='six columns',
                    style={'margin-top': '10'}
                )
 

def gen_map(map_data):
    # groupby returns a dictionary mapping the values of the first field
    # 'classification' onto a list of record dictionaries with that
    # classification value.
    return {
        "data": [{
                "type": "scattermapbox",
                "lat": list(map_data['latitude']),
                "lon": list(map_data['longitude']),
                "hoverinfo": "text",
                "mode": "markers",
                "marker": {
                    "size": 6,
                    "opacity": 0.7
                }
        }],
        "layout": layout_map
    }                            

@app.callback(
    Output('map-graph', 'figure'),
    [Input('datatable', 'rows'),
     Input('datatable', 'selected_row_indices')])
def map_selection(rows, selected_row_indices):
    aux = pd.DataFrame(rows)
    temp_df = aux.ix[selected_row_indices, :]
    if len(selected_row_indices) == 0:
        return gen_map(aux)
    return gen_map(temp_df)




"""Layout"""
app.layout = html.Div(
                      [navbar,dropdown,table,mapplot]
                     )



if __name__ == "__main__":
    app.run_server()
