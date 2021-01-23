import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from . import charts as ch
from . import data_processing as dp
from .__init__ import getlog

log = getlog(__name__)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

df = dp.df_clean()

@app.callback(
    Output('world_map', 'figure'),
    Output('bar_top', 'figure'),
    Input('energy_dropdown', 'value'),
    Input('year_slider', 'value'),
    Input('cb_percapita', 'value'))
def update_map_energy(energy_type, year, percapita, *args, **kw):
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

    print('cb_percapita', percapita)
    energy_col = 'energy_per_capita' if percapita else 'energy'

    return ch.multi_plots(
        df=df,
        energy_type=energy_type,
        year=str(year),
        energy_col=energy_col)

@app.callback(
    Output('single_country', 'figure'),
    Input('country_dropdown', 'value'))
def update_single_country(country, *args, **kw):
    """Update single_countries chart based on country dropdown"""

    # not necessary, but can be used to check which input triggered callback, eg slider or dropdown
    ctx = dash.callback_context
    key = ctx.triggered[0]['prop_id'].split('.')[0] # energy_dropdown

    # NOTE not sure why but callback gets triggered with nothing at start
    if key == '':
        log.info('Empty countries callback triggered.')
        country = 'World'

    return ch.single_country(df=df, country=country)

def wrap_elements(items):
    """Wrap dropdown with some html stuff"""
    if not isinstance(items, list): items = [items]
    return html.Div([*items], style={
            'margin-bottom': '20px',
            'margin-left': 'auto',
            'horizontal-align': 'right',
            'width': '200px'
            # 'border': '3px solid green',
            })

def make_app():
    """Add layout to global app"""

    # set default charts
    fig_world_map, fig_bar_top = ch.multi_plots(df=df)
    fig_single_country = ch.single_country(df=df, country='World')

    # per-capita checkbox
    cb_percapita = dcc.Checklist(
        id='cb_percapita',
        options=[
            {'label': 'Per-Capita Values', 'value': 'pc'},
        ],
        value=['pc']
    )  

    # Energy type dropdown, using uniqe energy_type values
    energy_types = [{'label': val.replace('_', ' ').title(), 'value': val} for val in df.energy_type.unique()]
    energy_dropdown = dcc.Dropdown(
            id='energy_dropdown',
            options=energy_types,
            value='total')
    
    # year slider
    year_slider = dcc.Slider(
        id='year_slider',
        min=1980,
        max=2018,
        marks={year: str(year) for year in range(1980, 2019, 2)})

    # country dropdown
    countries = [{'label': val, 'value': val} for val in df.country.unique()]
    country_dropdown = dcc.Dropdown(
            id='country_dropdown',
            options=countries,
            value='World')

    multi_plots = html.Div([
        html.Div([
            dcc.Graph(id='world_map', figure=fig_world_map)]),
        html.Div([
            dcc.Graph(id='bar_top', figure=fig_bar_top)]),
        ],
        className='row')

    app.layout = html.Div([

        
        wrap_elements([cb_percapita, energy_dropdown]),
        multi_plots,
        html.Div([year_slider],
            style={'margin-top': '20px', 'margin-bottom': '20px'}),
        wrap_elements(country_dropdown),
        dcc.Graph(
            id='single_country',
            figure=fig_single_country,
            style={'margin-bottom': '40px'}),
    ], style={'width': 1200, 'margin-left': '40px'})

    return app # this returns the global app
