import plotly.express as px
import plotly.graph_objs as go
import plotly.offline as py
import seaborn as sns
from matplotlib import pyplot
from plotly.subplots import make_subplots

# TODO need to make all values use total energy OR energy_per_capita
y_title = lambda x: 'BTU per Capita' if 'capita' in x else 'Quadrillion BTU'

def multi_plots(df, year='1980', energy_type='renewables', energy_col='energy_per_capita', **kw):
    """Return world_map with bar_top 10"""

    # filter df, both use same data
    df = filter_df(df, energy_type=energy_type, year=year)
    fig2 = top_bar(df=df, energy_col=energy_col)
    fig1 = world_map(df=df, energy_col=energy_col)

    return fig1, fig2

def filter_df(df, energy_type='renewables', year='1980'):
    """Filter df before sending to top_n and world_map"""
    # NOTE filtering 1e9 because it removes some small countries with unusually high per-capita values and messes up color scale on world_map
    return df.loc[year] \
        .pipe(lambda df: df[
            (df.energy_type == energy_type) &
            (df.country_code != 'WORL') &
            (df.energy_per_capita < 1e9)])

# def get_title()

def top_bar(df, energy_type='renewables', year='1980', n=10, energy_col='energy_per_capita'):
    """Horizontal bar chart of top 10 countries per energy_type/year"""

    # filter top n, sort
    df = df.sort_values([energy_col]) \
        .iloc[-1 * n:, :]

    trace = go.Bar(
        x=df[energy_col],
        y=df.country,
        orientation='h',
        marker=dict(colorscale='Viridis') # NOTE this isn't actually viridis
    )

    fig = go.Figure(data=[trace])

    xaxis = dict(
        title=y_title(energy_col))

    fig.update_layout(
        xaxis=xaxis,
        title_text = f'Top {n} Energy Consumers',
        margin=dict(t=30, b=0, r=0, l=100),
        width=400
    )

    return fig

def world_map(df, year='1980', energy_type='renewables', energy_col='energy_per_capita', **kw):
    """Create main world map plot of energy consumption"""  

    map_trace = go.Choropleth(
        locations=df.country_code,
        z=df[energy_col],
        locationmode='ISO-3',
        colorscale='viridis',
        # reversescale=True
        colorbar_title=y_title(energy_col))

    fig = go.Figure(data=[map_trace])

    fig.update_layout(
        title_text = 'World Energy Consumption',
        margin=dict(t=30, b=0, r=0, l=20),
        width=800
        # geo_scope='usa', # limite map scope to USA
    )

    return fig

def single_country(df, country='Canada'):
    """Return line chart for single country with full history and all energy types"""
    fig = go.Figure()
    df = df[df.country == country]
    x = df.index.to_timestamp()

    xaxis = dict(
        ticktext=df.index.strftime('%Y'),
        tickvals=x,
        tickangle=270,
        showgrid=False)

    energy_types = ['coal', 'natural_gas', 'petroleum', 'nuclear', 'renewables']

    # loop energy types and add traces
    for energy in energy_types:
        df2 = df[df.energy_type == energy]

        trace = go.Scatter(
            name=energy,
            x=df2.index.to_timestamp(),
            y=df2.energy)

        fig.add_trace(trace)

    fig.update_layout(
        xaxis=xaxis,
        margin=dict(t=30, b=0, r=0, l=0),
        title=f'Energy Consumption ({country})',
        yaxis=dict(
            title='Energy Consumption (Quad BTU)',
            showgrid=False
        ),
        width=800,
        height=300,
        plot_bgcolor='white'
    )

    return fig
