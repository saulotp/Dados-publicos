from click import option
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import plotly.io as pio
pio.renderers.default = "notebook_connected"




app = Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv('db_publicdata.csv')
dfdep = df.loc[df['nome'] == 'Abílio Santana']
dfdep = dfdep[[ 'valorDocumento', 'tipoDespesa']].groupby('tipoDespesa').sum().reset_index()
dfdep = dfdep.sort_values(by='valorDocumento', ascending=False)
dfdep = dfdep.head(10)

## dropdown options
options = list(df['nome'].unique())
options.append('Todos')




fig = px.bar(df, x="tipoDespesa", y="valorDocumento", text_auto=True)
fig.update_yaxes(visible=False, showticklabels=False)

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Hello Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    
    

    html.Div(children='Dash: A web application framework for your data.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    dcc.Dropdown(options, value='todos', id='demo-dropdown'),
    html.Div(id='dd-output-container'),
    dcc.Graph(
        id='example-graph-2',
        figure=fig
    )
])

@app.callback(
    Output('dd-output-container', 'children'),
    Input('demo-dropdown', 'value')
)

def update_output(value):
    return f'You have selected {value}'

if __name__ == '__main__':
    app.run_server(debug=True)