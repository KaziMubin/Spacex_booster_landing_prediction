# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                 {'label': 'All Sites', 'value': 'All'},
                                                 {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                 {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                 {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                 {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                             ],
                                             value='All',
                                             placeholder="place holder here",
                                             searchable=True
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0', 1000: '1000', 2000: '2000', 3000: '3000',
                                                       4000: '4000', 5000: '5000', 6000: '6000', 7000: '7000',
                                                       8000: '8000', 9000: '9000', 10000: '10000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))
def get_pie_chart(entered_site, payload_mass):
    filtered_df = spacex_df.copy()
    double_filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= payload_mass[0]) &
                                     (filtered_df['Payload Mass (kg)'] <= payload_mass[1])]
    print(payload_mass)
    if entered_site == 'All':
        pie_fig = px.pie(filtered_df, values='class', names='Launch Site', title='All Site')
        scatter_fig = px.scatter(double_filtered_df, x=double_filtered_df['Payload Mass (kg)'],
                                 y=double_filtered_df['class'], color=double_filtered_df['Booster Version Category'])
        return pie_fig, scatter_fig
    else:
        current_site = double_filtered_df[double_filtered_df['Launch Site'] == entered_site]
        print(current_site)
        pie_fig = px.pie(current_site, names='class', title=entered_site)
        scatter_fig = px.scatter(current_site, x=current_site['Payload Mass (kg)'], y=current_site['class'],
                                 color=current_site['Booster Version Category'])
        return pie_fig, scatter_fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
