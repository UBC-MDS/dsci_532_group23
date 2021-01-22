import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from .. import charts as ch
from .. import data_processing as dp
from ..__init__ import getlog

log = getlog(__name__)
log.warning('LOGGING WARNING TEST')
log.error('LOGGING ERROR TEST')
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

df = dp.df_clean()

log.warning('Everything init')

@app.callback(
    Output('world_map', 'figure'),
    Input('energy_dropdown', 'value'),
    Input('year_slider', 'value'))
def update_map_energy(energy_type, year, *args, **kw):
    """Update world_map chart based on energy_type dropdown and year_slider"""

    # not necessary, but can be used to check which input triggered callback, eg slider or dropdown
    ctx = dash.callback_context
    key = ctx.triggered[0]['prop_id'].split('.')[0] # energy_dropdown

    # NOTE not sure why but callback gets triggered with nothing at start
    if key == '':
        log.info('Empty callback triggered.')
        energy_type = 'total'
        year = '1980'
    
    if year is None:
        year = '1980'

    print(energy_type, year)
    return ch.world_map(df=df, energy_type=energy_type, year=str(year))

def run(app):

    # set default chart
    fig = ch.world_map(df=df, year='2018', energy_type='all_renewable')

    # Energy type dropdown, using uniqe energy_type values
    energy_types = [{'label': val.replace('_', ' ').title(), 'value': val} for val in df.energy_type.unique()]
    energy_dropdown = dcc.Dropdown(
            id='energy_dropdown',
            options=energy_types,
            value='total',
            multi=False,
            style={'width': '200px'})
        
    year_slider = dcc.Slider(
        id='year_slider',
        min=1980,
        max=2018,
        marks={year: str(year) for year in range(1980, 2019, 2)}
    )

    app.layout = html.Div([
        html.Div([energy_dropdown], style={
            # 'display': 'inline-block',
            # 'position': 'absolute',
            # 'right': 0,
            # 'float': 'right',
            # 'margin': '20px',
            'margin-bottom': '20px',
            'margin-left': 'auto',
            'horizontal-align': 'right',
            # 'border': '3px solid green',
            }),
        dcc.Graph(
            id='world_map',
            figure=fig),
        html.Div([year_slider], style={'margin-top': '20px'}),
        # html.Div(id='dd-output-container')
    ])

    return app
    # app.run_server(debug=True)

if __name__ == '__main__':
    app = run(app)
    log.info(f'app layout: {app.layout}')
    app.run_server(debug=True)
