
# LIBRARIES

import dash
from matplotlib.pyplot import margins
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


import plotly.io as pio

# VARIABLES
df = pd.read_csv('db_publicdata.csv')

# DROPDOWN OPTIONS
dfdep = list(df["nome"].unique())
dfdep.sort()


# DATA TO PLOT


#firstplot = df.loc[df['nome'] == 'Abílio Santana']
firstplot = df[['valorDocumento', 'tipoDespesa']
               ].groupby('tipoDespesa').sum().reset_index()
#firstplot = firstplot.sort_values(by='valorDocumento', ascending=True)
#firstplot = firstplot.head(10)

# PLOTS
#fig = px.bar(df, x="tipoDespesa", y="valorDocumento", text_auto=True, orientation='h')


fig = px.bar(df, x="valorDocumento", y="tipoDespesa",
             text_auto=True, orientation='h', height=400, width=1000)
#fig.update_yaxes(visible=False, showticklabels=False)


# LAYOUT
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Dados Abertos", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Page 1", href="/page-1", active="exact"),
                dbc.NavLink("Page 2", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        # page 1 begin
        return html.Div([
            html.Div(children=[
                        html.Label('Deputados'),
                        dcc.Dropdown(dfdep, id='dropdown',
                                     value='Abílio Santana', multi=False),

                        ], style={'width': '100%', 'height': '300px', 'background-color': '#00ff00',  'align-items': 'center', 'border-radius': '30px', 'margin': '1%', 'padding': '1%'}),

            html.Div(children=[
                html.Label('2'),

            ], style={'width': '100%', 'height': '300px', 'background-color': '#0000ff', 'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center', 'align-items': 'center', 'border-radius': '30px', 'margin': '1%', 'padding': '1%'}),

            html.Div(children=[
                html.Label('3'),

            ], style={'width': '100%', 'height': '300px', 'background-color': '#ffff00', 'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center', 'align-items': 'center', 'border-radius': '30px', 'margin': '1%', 'padding': '1%'}),
        ], style={'width': '100%', 'height': '100%', 'background-color': '#ff0000', 'display': 'flex'}), html.Div(children=[

            dcc.Graph(id='graph_1', figure=fig, style={
                      "height": "100%", "width": "100%"}),
        ], style={'width': '100%', 'height': '400px', 'background-color': '#00ffff', 'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center', 'align-items': 'center'}),

        # page 1 end


# END
    elif pathname == "/page-1":
        return html.P("This is the content of page 1. Yay!")
    elif pathname == "/page-2":
        return html.P("Oh cool, this is page 2!")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )
# dropdown callback


@app.callback(
    Output('graph_1', 'figure'),
    Input('dropdown', 'value')
)
def update_output(value):
    if value == 'Todos':
        fig = px.bar(df, x="valorDocumento", y="tipoDespesa",
                     text_auto=True, orientation='h')
    else:
        dffilter = df.loc[df['nome'] == value,
                          ['valorDocumento', 'tipoDespesa']]
        dffilter = dffilter[['valorDocumento', 'tipoDespesa']].groupby(
            'tipoDespesa').sum().reset_index()
        fig = px.bar(dffilter, x="valorDocumento", y="tipoDespesa",
                     text_auto=True, orientation='h')

    return fig


if __name__ == "__main__":
    app.run_server(port=8888)
