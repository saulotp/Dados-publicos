import hvplot.pandas
import pandas as pd
import numpy as np
import panel as pn
pn.extension('tabulator')


df = pd.read_csv(
    "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv")

# print(df.head())
# cache data to improve dashboard performance
if 'data' not in pn.state.cache.keys():

    df = pd.read_csv(
        'https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv')

    pn.state.cache['data'] = df.copy()

else:

    df = pn.state.cache['data']

# Fill NAs with 0s and create GDP per capita column
df = df.fillna(0)
df['gdp_per_capita'] = np.where(
    df['population'] != 0, df['gdp'] / df['population'], 0)
# Make DataFrame Pipeline Interactive
idf = df.interactive()


# Define Panel widgets
year_slider = pn.widgets.IntSlider(
    name='Year slider', start=1750, end=2020, step=5, value=1850)

# Radio buttons for CO2 measures
yaxis_co2 = pn.widgets.RadioButtonGroup(
    name='Y axis',
    options=['co2', 'co2_per_capita', ],
    button_type='success'
)

continents = ['World', 'Asia', 'Oceania', 'Europe',
              'Africa', 'North America', 'South America', 'Antarctica']

co2_pipeline = (
    idf[
        (idf.year <= year_slider) &
        (idf.country.isin(continents))
    ]
    .groupby(['country', 'year'])[yaxis_co2].mean()
    .to_frame()
    .reset_index()
    .sort_values(by='year')
    .reset_index(drop=True)
)

co2_plot = co2_pipeline.hvplot(
    x='year', by='country', y=yaxis_co2, line_width=2, title="CO2 emission by continent")


# Radio buttons for GDP measures
yaxis_gdp = pn.widgets.RadioButtonGroup(
    name='Y axis',
    options=['gdp', 'gdp_per_capita', ],
    button_type='success'
)


gdp_pipeline = (
    idf[
        (idf.year <= year_slider) &
        (idf.country.isin(continents))
    ]
    .groupby(['country', 'year'])[yaxis_gdp].mean()
    .to_frame()
    .reset_index()
    .sort_values(by='year')
    .reset_index(drop=True)
)


gdp_plot = gdp_pipeline.hvplot(
    x='year', by='country', y=yaxis_gdp, line_width=2, title="GDP by continent")
