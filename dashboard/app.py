import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Load data
df = pd.read_csv('../data/processed/mental_health_clean.csv')

# 50 states only
states_50 = ['AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA',
             'HI','ID','IL','IN','IA','KS','KY','LA','ME','MD',
             'MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ',
             'NM','NY','NC','ND','OH','OK','OR','PA','RI','SC',
             'SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']

df = df[df['LocationAbbr'].isin(states_50)]

# Initialize app
app = dash.Dash(__name__)
server = app.server

# Layout
app.layout = html.Div([

    # Title
    html.H1("US Mental Health Trends Dashboard (2019-2022)",
            style={'textAlign': 'center', 'color': '#2c3e50',
                   'fontFamily': 'Arial', 'marginBottom': '20px'}),

    # Dropdowns row
    html.Div([
        html.Div([
            html.Label("Select Condition:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='condition-dropdown',
                options=[{'label': q, 'value': q} for q in sorted(df['Question'].unique())],
                value=df['Question'].unique()[0]
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.Label("Select State:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='state-dropdown',
                options=[{'label': s, 'value': s} for s in sorted(states_50)],
                value='NY'
            )
        ], style={'width': '48%', 'display': 'inline-block', 'marginLeft': '2%'})
    ], style={'padding': '20px'}),

    # Charts
    html.Div([
        dcc.Graph(id='trend-chart', style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(id='map-chart', style={'width': '48%', 'display': 'inline-block'})
    ]),

    # Bottom charts
    html.Div([
        dcc.Graph(id='demographic-chart', style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(id='covid-chart', style={'width': '48%', 'display': 'inline-block'})
    ])

], style={'fontFamily': 'Arial', 'backgroundColor': '#f9f9f9'})


# Callbacks
@app.callback(
    Output('trend-chart', 'figure'),
    Output('map-chart', 'figure'),
    Output('demographic-chart', 'figure'),
    Output('covid-chart', 'figure'),
    Input('condition-dropdown', 'value'),
    Input('state-dropdown', 'value')
)
def update_charts(selected_condition, selected_state):

    # Chart 1 — Trend line for selected state
    filtered = df[(df['Question'] == selected_condition) &
                  (df['LocationAbbr'] == selected_state)]
    trend = filtered.groupby('YearStart')['DataValue'].mean().reset_index()
    trend['YearStart'] = trend['YearStart'].astype(str)

    trend_fig = px.line(trend, x='YearStart', y='DataValue',
                        markers=True,
                        title=f'{selected_condition}<br>{selected_state} Trend',
                        labels={'DataValue': 'Prevalence Rate (%)', 'YearStart': 'Year'},
                        color_discrete_sequence=['#e74c3c'])
    trend_fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')

    # Chart 2 — Choropleth map
    map_data = df[df['Question'] == selected_condition]
    map_data = map_data.groupby('LocationAbbr')['DataValue'].mean().reset_index()

    map_fig = px.choropleth(map_data,
                            locations='LocationAbbr',
                            locationmode='USA-states',
                            color='DataValue',
                            scope='usa',
                            color_continuous_scale='Reds',
                            range_color=[10, 20],
                            title=f'{selected_condition}<br>All States',
                            labels={'DataValue': 'Prevalence Rate (%)'})
    map_fig.update_layout(margin=dict(l=0, r=0, t=50, b=0))

    # Chart 3 — Demographic breakdown
    demo_data = df[(df['Question'] == selected_condition) &
                   (df['StratificationCategory1'].isin(['Sex', 'Age', 'Race/Ethnicity']))]
    demo_data = demo_data.groupby(['StratificationCategory1', 'Stratification1'])['DataValue'].mean().reset_index()

    demo_fig = px.bar(demo_data, x='Stratification1', y='DataValue',
                      color='StratificationCategory1',
                      title=f'{selected_condition}<br>By Demographics',
                      labels={'DataValue': 'Prevalence Rate (%)', 'Stratification1': 'Group'},
                      color_discrete_sequence=px.colors.qualitative.Set2)
    demo_fig.update_layout(xaxis_tickangle=-45, plot_bgcolor='white', paper_bgcolor='white')

    # Chart 4 — Pre vs During COVID
    df['Period'] = df['YearStart'].apply(lambda x: 'Pre-COVID (2019)' if x <= 2019 else 'During COVID (2020-2022)')
    covid_data = df[df['Question'] == selected_condition]
    covid_data = covid_data.groupby('Period')['DataValue'].mean().reset_index()

    covid_fig = px.bar(covid_data, x='Period', y='DataValue',
                       color='Period',
                       title=f'{selected_condition}<br>Pre vs During COVID',
                       labels={'DataValue': 'Avg Prevalence Rate (%)'},
                       color_discrete_map={
                           'Pre-COVID (2019)': '#3498db',
                           'During COVID (2020-2022)': '#e74c3c'
                       })
    covid_fig.update_layout(showlegend=False, plot_bgcolor='white', paper_bgcolor='white')

    covid_fig.update_xaxes(categoryorder='array',
                           categoryarray=['Pre-COVID (2019)', 'During COVID (2020-2022)'])


    return trend_fig, map_fig, demo_fig, covid_fig


# Run
if __name__ == '__main__':
    app.run(debug=True)