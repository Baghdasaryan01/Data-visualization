import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Load data
mouse_data = pd.read_csv("C:/Users/HP/Desktop/PYTHON/Homework_dash_mouse/Mouse_metadata.csv")
study_results = pd.read_csv("C:/Users/HP/Desktop/DATA__VIZUALI/Study_results.csv")
merged_df = pd.merge(mouse_data, study_results, on='Mouse ID')

# Define app and external stylesheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Design parameters
colors = {
    'light-blue': '#7FAB8',
    'light-grey': '#F7EFED',
    'dark-blue': '#33546D'
}

drug_colors = {
    'Placebo': '#29304E',
    'Capomulin': '#27706B',
    'Ramicane': '#71AB7F',
    'Ceftamin': '#9F4440',
    'Infubinol': '#FFD37B',
    'Ketapril': '#FEADB9',
    'Naftisol': '#B3AB9E',
    'Propriva': '#ED5CD4',
    'Stelasyn': '#97C1DF',
    'Zoniferol': '#8980D4'
}

# App layout
app.layout = html.Div(style={'backgroundColor': colors['light-grey']}, children=[
    html.H1('Mouse Study Dashboard', style={'textAlign': 'center', 'border': f'3px solid {colors["dark-blue"]}' }),

    # Row 1: Weight Histogram and Distribution Chart
    html.Div(style={'display': 'flex'}, children=[
        html.Div(style={'border': f'1px solid {colors["dark-blue"]}', 'margin': '10px', 'width': '50%'}, children=[
            dcc.Checklist(
                id='weight-histogram-checklist',
                options=[{'label': drug, 'value': drug} for drug in np.unique(mouse_data['Drug Regimen'])],
                value=['Placebo'],
                labelStyle={'display': 'inline-block'}
            ),
            dcc.Graph(id='weight-histogram')
        ]),
        html.Div(style={'border': f'1px solid {colors["dark-blue"]}', 'margin': '10px', 'width': '50%'}, children=[
            dcc.RadioItems(
                id='overlay-drug-radio',
                options=[{'label': drug, 'value': drug} for drug in np.unique(mouse_data['Drug Regimen'])],
                value='Placebo',
                labelStyle={'display': 'inline-block'}
            ),
            dcc.Graph(id='weight-distribution-chart', figure={})
        ])
    ]),

    # Row 2: Survival Function Chart and Survival Function over Time Chart
    html.Div(style={'display': 'flex'}, children=[
        html.Div(style={'border': f'1px solid {colors["dark-blue"]}', 'margin': '10px', 'width': '50%'}, children=[
            dcc.Checklist(
                id='drug-group-checklist',
                options=[
                    {'label': 'Lightweight', 'value': 'lightweight'},
                    {'label': 'Heavyweight', 'value': 'heavyweight'},
                    {'label': 'Placebo', 'value': 'placebo'}
                ],
                value=['placebo'],
                labelStyle={'display': 'inline-block'}
            ),
            dcc.Graph(id='survival-function-chart', figure={})
        ]),
        html.Div(style={'border': f'1px solid {colors["dark-blue"]}', 'margin': '10px', 'width': '50%'}, children=[
            dcc.Graph(id='survival-function-time-chart', figure={}),
            dcc.Checklist(
                id='drug-group-time-checklist',
                options=[
                    {'label': 'Lightweight', 'value': 'lightweight'},
                    {'label': 'Heavyweight', 'value': 'heavyweight'},
                    {'label': 'Placebo', 'value': 'placebo'}
                ],
                value=['placebo'],
                labelStyle={'display': 'inline-block'}
            )
        ])
    ])
])


# Callbacks
@app.callback(
    Output('weight-histogram', 'figure'),
    [Input('weight-histogram-checklist', 'value')]
)
def update_weight_histogram(drug_names):
    traces = []
    for drug in drug_names:
        traces.append(go.Histogram(
            x=merged_df[merged_df['Drug Regimen'] == drug]['Weight (g)'],
            name=drug,
            opacity=0.9,
            marker=dict(color=drug_colors[drug])
        ))
    return {
        'data': traces,
        'layout': {
            'barmode': 'stack',
            'xaxis': {'title': 'Mouse Weight', 'showgrid': False},
            'yaxis': {'title': 'Number of Mice', 'showgrid': False},
            'autosize': False,
            'paper_bgcolor': colors['light-grey'],
            'plot_bgcolor': colors['light-grey'],
            'margin': {'l': 40, 'b': 40, 't': 10, 'r': 10},
            'legend': {'x': 0, 'y': 1},
        }
    }

@app.callback(
    Output('weight-distribution-chart', 'figure'),
    [Input('overlay-drug-radio', 'value')]
)
def update_weight_distribution(selected_drug):
    traces = []
    overall_distribution = go.Histogram(
        x=mouse_data['Weight (g)'],
        name='All mice',
        opacity=0.5,
        marker=dict(color='gray')
    )
    traces.append(overall_distribution)
    if selected_drug:
        selected_distribution = go.Histogram(
            x=mouse_data[mouse_data['Drug Regimen'] == selected_drug]['Weight (g)'],
            name=selected_drug,
            opacity=0.9,
            marker=dict(color=drug_colors[selected_drug])
        )
        traces.append(selected_distribution)
    return {
        'data': traces,
        'layout': {
            'barmode': 'overlay',
            'xaxis': {'title': 'Mouse Weight'},
            'yaxis': {'title': 'Number of Mice'},
            'autosize': False,
            'paper_bgcolor': colors['light-grey'],
            'plot_bgcolor': colors['light-grey'],
            'margin': {'l': 40, 'b': 40, 't': 10, 'r': 10},
            'legend': {'x': 0, 'y': 1},
        }
    }

@app.callback(
    Output('survival-function-chart', 'figure'),
    [Input('drug-group-checklist', 'value')]
)
def update_survival_function(selected_group):
    traces = []
    for drug in selected_group:
        if drug == 'lightweight':
            drugs_of_interest = ['Ramicane', 'Capomulin']
        elif drug == 'heavyweight':
            drugs_of_interest = ['Ceftamin', 'Infubinol', 'Ketapril', 'Naftisol', 'Propriva', 'Stelasyn', 'Zoniferol']
        else:
            drugs_of_interest = ['Placebo']

        for d in drugs_of_interest:
            drug_data = merged_df[merged_df['Drug Regimen'] == d]
            traces.append(go.Histogram(
                x=drug_data['Weight (g)'],
                name=f'{d} - {drug}',
                opacity=0.6,
                marker=dict(color=drug_colors[d])
            ))

    return {
        'data': traces,
        'layout': {
            'barmode': 'overlay',
            'xaxis': {'title': 'Mouse Weight (g)', 'showgrid': False},
            'yaxis': {'title': 'Number of Mice', 'showgrid': False},
            'autosize': False,
            'paper_bgcolor': colors['light-grey'],
            'plot_bgcolor': colors['light-grey'],
            'margin': {'l': 40, 'b': 40, 't': 10, 'r': 10},
            'legend': {'x': 0, 'y': 1},
        }
    }

@app.callback(
    Output('survival-function-time-chart', 'figure'),
    [Input('drug-group-time-checklist', 'value')]
)
def update_survival_function_time(selected_group):
    traces = []
    for drug in selected_group:
        if drug == 'lightweight':
            drugs_of_interest = ['Ramicane', 'Capomulin']
        elif drug == 'heavyweight':
            drugs_of_interest = ['Ceftamin', 'Infubinol', 'Ketapril', 'Naftisol', 'Propriva', 'Stelasyn', 'Zoniferol']
        else:
            drugs_of_interest = ['Placebo']

        for d in drugs_of_interest:
            drug_data = merged_df[merged_df['Drug Regimen'] == d]
            timepoints = sorted(drug_data['Timepoint'].unique())
            mice_alive = [len(drug_data[drug_data['Timepoint'] == tp]) for tp in timepoints]
            traces.append(go.Scatter(
                x=timepoints,
                y=mice_alive,
                mode='lines',
                name=f'{d} - {drug}',
                line=dict(color=drug_colors[d])
            ))

    return {
        'data': traces,
        'layout': {
            'xaxis': {'title': 'Time', 'showgrid': False},
            'yaxis': {'title': 'Number of Mice Alive', 'showgrid': False},
            'autosize': False,
            'paper_bgcolor': colors['light-grey'],
            'plot_bgcolor': colors['light-grey'],
            'margin': {'l': 40, 'b': 40, 't': 10, 'r': 10},
            'legend': {'x': 0, 'y': 1},
        }
    }


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8085)
