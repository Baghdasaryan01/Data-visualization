import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

# Load and clean the data
data = pd.read_csv("C:/Users/HP/Desktop/DATA__VIZUALI/world-data-2023.csv")

# Clean country names
data["Country"] = data["Country"].str.replace("S�����������", "")
data["Country"] = data["Country"].replace("", np.nan)
data = data.dropna(subset=['Country'])

# List of numerical variables for conversion
NumericalVariables = [
    'Density\n(P/Km2)', 'Agricultural Land( %)', 'Land Area(Km2)', 'Armed Forces size', 'Birth Rate',
    'Co2-Emissions', 'CPI', 'CPI Change (%)', 'Fertility Rate', 'Forested Area (%)', 'Gasoline Price',
    'GDP', 'Gross primary education enrollment (%)', 'Gross tertiary education enrollment (%)',
    'Infant mortality', 'Life expectancy', 'Maternal mortality ratio', 'Minimum wage',
    'Out of pocket health expenditure', 'Physicians per thousand', 'Population',
    'Population: Labor force participation (%)', 'Tax revenue (%)', 'Total tax rate',
    'Unemployment rate', 'Urban_population'
]

# Clean and convert numerical variables
for variable in NumericalVariables:
    if data[variable].dtype == 'object':
        data[variable] = data[variable].str.replace(',', '').str.replace('%', '').str.replace('$', '')
        data[variable] = data[variable].astype(float)

# Fill missing numerical data with column mean
for variable in NumericalVariables:
    data[variable].fillna(data[variable].mean(), inplace=True)

# Create a new column for GDP per capita
data['GDP per capita'] = data['GDP'] / data['Population']

# Create Dash app
app = dash.Dash(__name__)
server = app.server

# App layout
app.layout = html.Div([
    html.H1("World Data Dashboard"),

    dcc.Dropdown(
        id='country-filter',
        options=[{'label': country, 'value': country} for country in data['Country']],
        value=[],
        multi=True,
        placeholder="Select countries"
    ),

    html.Div([
        dcc.Graph(id='choropleth-map', style={'display': 'inline-block'}),
        dcc.Graph(id='scatter-plot', style={'display': 'inline-block'})
    ]),

    html.Div([
        dcc.Graph(id='bar-chart', style={'display': 'inline-block'}),
        dcc.Graph(id='bubble-chart', style={'display': 'inline-block'})
    ]),

    html.Div([
        dcc.Graph(id='pie-chart', style={'display': 'inline-block'}),
        dcc.Graph(id='gdp-per-capita-bar-chart', style={'display': 'inline-block'})
    ]),

    html.Div([
        dcc.Graph(id='line-chart', style={'display': 'inline-block'}),
        dcc.Graph(id='urban-population-line-chart', style={'display': 'inline-block'})
    ]),

    html.Div([
        dcc.Graph(id='violin-plot', style={'display': 'inline-block'}),
        dcc.Graph(id='treemap', style={'display': 'inline-block'})
    ]),

    html.Div([
        dcc.Graph(id='top-10-gdp-per-capita', style={'display': 'inline-block'}),
        dcc.Graph(id='top-10-population', style={'display': 'inline-block'})
    ]),

    dcc.Graph(id='3d-scatter-plot'),
    dcc.Graph(id='minimum-wage-chart')
])

# Callback to update all graphs based on country selection
@app.callback(
    [Output('choropleth-map', 'figure'),
     Output('scatter-plot', 'figure'),
     Output('bar-chart', 'figure'),
     Output('bubble-chart', 'figure'),
     Output('pie-chart', 'figure'),
     Output('gdp-per-capita-bar-chart', 'figure'),
     Output('line-chart', 'figure'),
     Output('urban-population-line-chart', 'figure'),
     Output('violin-plot', 'figure'),
     Output('treemap', 'figure'),
     Output('top-10-gdp-per-capita', 'figure'),
     Output('top-10-population', 'figure'),
     Output('3d-scatter-plot', 'figure'),
     Output('minimum-wage-chart', 'figure')],
    [Input('country-filter', 'value')]
)
def update_graphs(selected_countries):
    if selected_countries:
        filtered_df = data[data['Country'].isin(selected_countries)]
    else:
        filtered_df = data

    fig_choropleth = px.choropleth(
        filtered_df,
        locations="Country",
        locationmode="country names",
        color="Density\n(P/Km2)",
        hover_name="Country",
        color_continuous_scale=px.colors.sequential.Plasma,
        title="Population Density by Country"
    )

    fig_scatter = px.scatter(
        filtered_df,
        x="Birth Rate",
        y="Co2-Emissions",
        text="Country",
        title="Birth Rate vs. CO2 Emissions",
        labels={"Birth Rate": "Birth Rate (per 1000 people)", "Co2-Emissions": "CO2 Emissions (kt)"}
    )

    fig_bar = px.bar(
        filtered_df,
        x="Country",
        y="Armed Forces size",
        title="Armed Forces Size by Country",
        labels={"Armed Forces size": "Armed Forces Size"}
    )

    fig_bubble = px.scatter(
        filtered_df,
        x="Land Area(Km2)",
        y="Population",
        size="Co2-Emissions",
        color="Country",
        hover_name="Country",
        title="Population vs. Land",
        labels={"Land Area(Km2)": "Land Area (Km2)", "Population": "Population"}
    )

    fig_pie = px.pie(
        filtered_df,
        values='Agricultural Land( %)',
        names='Country',
        title='Agricultural Land Distribution'
    )

    fig_gdp_per_capita = px.bar(
        filtered_df,
        x="Country",
        y="GDP per capita",
        title="GDP per Capita by Country",
        labels={"GDP per capita": "GDP per Capita (USD)"}
    )

    fig_line = px.line(
        filtered_df,
        x='Country',
        y='Life expectancy',
        title='Life Expectancy by Country'
    )

    fig_urban_population_line = px.line(
        filtered_df,
        x='Country',
        y='Urban_population',
        title='Urban Population (%) by Country',
        labels={"Urban_population": "Urban Population (%)"}
    )

    fig_violin = px.violin(
        filtered_df,
        y='Life expectancy',
        box=True,
        title='Life Expectancy Violin Plot'
    )

    fig_treemap = px.treemap(
        filtered_df,
        path=['Country', 'Life expectancy'],
        values='Population',
        title='Population Treemap'
    )

    top_10_gdp_per_capita = filtered_df.nlargest(10, 'GDP per capita')
    top_10_population = filtered_df.nlargest(10, 'Population')

    fig_top_10_gdp_per_capita = px.bar(
        top_10_gdp_per_capita,
        x="Country",
        y="GDP per capita",
        title="Top Countries by GDP per Capita",
        labels={"GDP per capita": "GDP per Capita (USD)"}
    )

    fig_top_10_population = px.scatter(
        top_10_population,
        x="Country",
        y="Population",
        size="Population",
        color="Country",
        hover_name="Country",
        title="Top Countries by Population",
        labels={"Population": "Population"}
    )

    fig_3d_scatter = px.scatter_3d(
        filtered_df,
        x='Life expectancy',
        y='GDP',
        z='Population',
        color='Country',
        hover_name='Country',
        title='Life Expectancy, GDP, and Population Relationship'
    )

    fig_minimum_wage = px.bar(
        filtered_df,
        x="Country",
        y="Minimum wage",
        title="Minimum Wage by Country",
        labels={"Minimum wage": "Minimum Wage (USD)"}
    )

    return (
        fig_choropleth, fig_scatter, fig_bar, fig_bubble, fig_pie, fig_gdp_per_capita, fig_line,
        fig_urban_population_line, fig_violin, fig_treemap, fig_top_10_gdp_per_capita, fig_top_10_population,
        fig_3d_scatter, fig_minimum_wage
    )


if __name__ == '__main__':
    app.run_server(debug=True)
