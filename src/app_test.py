import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd
import plotly.express as px

# Read in global data
energy_data = pd.read_csv("data/world_energy.csv")
energy_data = energy_data.query('energy_type != "total" & energy_type != "all_renewable"')
country_code_list = list(set(energy_data.country_code.unique()) - set("WORL")) 
# Disabling MaxRowsError
alt.data_transformers.disable_max_rows()
# Setup app and layout/frontend
app = dash.Dash(__name__,  external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
app.layout = html.Div([
    html.Iframe(
        id='lineplot',
        style={'border-width': '0', 'width': '100%', 'height': '400px'}),
    dcc.Dropdown(
        id='xcol-widget',
        value='year',  # REQUIRED to show the plot on the first page load
       options=[{'label': col, 'value': col} for col in country_code_list])])

# Set up callbacks/backend
@app.callback(
    Output('lineplot', 'srcDoc'),
    Input('xcol-widget', 'value'))

def plot_altair(xcol):
    chart = alt.Chart(energy_data.query('country_code == "AFG"')).mark_line().encode(
        x=xcol,
        y='mean(energy)',
        color = "energy_type:O",
        tooltip = 'energy_type').interactive()
    return chart.to_html()



if __name__ == '__main__':
    app.run_server(debug=True)



