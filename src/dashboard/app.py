import dash
import dash_core_components as dcc
import dash_html_components as html

from .. import charts as ch
from .. import data_processing as dp
from ..__init__ import getlog

log = getlog(__name__)

# log.info('THIS IS THE LOGGING')

"""
TODO
- callback on country click
- slider bar
- energy type dropdown
- find country population data

"""

def run():
    app = dash.Dash(__name__)

    # app.layout = html.Div('I am NOT alive!!')

    # load dataframe and create world map chart
    df = dp.df_clean()
    fig = ch.world_map(df=df, year='2018', energy_type='petroleum')

    app.layout = html.Div([
        dcc.Graph(figure=fig)
    ])

    app.run_server(debug=True)

if __name__ == '__main__':
    run()
