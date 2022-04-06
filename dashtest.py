from dash import Dash, html, dcc
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
df = df.loc[df['nome'] == 'Abílio Santana']
df = df[[ 'valorDocumento', 'tipoDespesa']].groupby('tipoDespesa').sum().reset_index()
df = df.sort_values(by='valorDocumento', ascending=False)
df = df.head(10)



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

    dcc.Graph(
        id='example-graph-2',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)