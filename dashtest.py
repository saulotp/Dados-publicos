from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv('db_publicdata.csv')
# df = pd.DataFrame({
#    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#    "Amount": [4, 1, 2, 2, 4, 5],
#    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    html.Div(test='''
        Dash: A web application framework for your data.
    '''),

    dcc.Dropdown(df['nome'], value='Todos', id='dropdown-deputados'),
    dcc.Graph(id='example-graph',  figure=fig)
])


@app.callback(
    Output('dd-output-container', 'test'),
    Input('dropdown-deputados', 'value')
)
def update_output(value):
    return 'You have selected "{}"'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)


#dfmall = dfmain.loc[dfmain['ID Loja'] == 'Shopping Morumbi']
# df['valorDocumento'].nlargest(n=10)
