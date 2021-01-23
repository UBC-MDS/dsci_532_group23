import plotly.express as px
import plotly.graph_objs as go
import plotly.offline as py
import seaborn as sns
from matplotlib import pyplot
from plotly.subplots import make_subplots
import ipywidgets as ipw

def multi_plots(df, **kw):
    """Return world_map with bar_top 10"""

    # filter df, both use same data
    df = filter_df(df, **kw)
    fig2 = top_bar(df=df)
    fig1 = world_map(df=df)

    return fig1, fig2

def filter_df(df, energy_type='renewables', year='1980'):
    """Filter df before sending to top_n and world_map"""
    return df.loc[year] \
        .pipe(lambda df: df[
            (df.energy_type == energy_type) &
            (df.country_code != 'WORL') &
            (df.energy_per_capita < 1e9)])

def top_bar(df, energy_type='renewables', year='1980', n=10):

    # filter top n, sort
    df = df.sort_values(['energy_per_capita']) \
        .iloc[-1 * n:, :]

    trace = go.Bar(
        x=df.energy_per_capita,
        y=df.country,
        orientation='h',
        # color_continuous_scale='Viridis',
        marker=dict(
            # color='Viridis',
            colorscale='Viridis'
            )
    )

    fig = go.FigureWidget(data=[trace])

    xaxis = dict(
        title='BTU per Capita'
    )

    fig.update_layout(
        xaxis=xaxis,
        title_text = f'Top {n} Energy Consumers',
        margin=dict(t=30, b=0, r=0, l=100),
        width=400
    )

    return fig

def world_map(df, year='1980', energy_type='renewables', **kw):
    """Create main world map plot of energy consumption"""

    map_trace = go.Choropleth(
        locations=df.country_code,
        z=df.energy_per_capita,
        locationmode='ISO-3',
        colorscale='viridis',
        # reversescale=True
        colorbar_title='BTU per Capita',
    )

    fig = go.FigureWidget(data=[map_trace])

    fig.update_layout(
        title_text = 'World Energy Consumption',
        margin=dict(t=30, b=0, r=0, l=20),
        yaxis=dict(title='BTU per Capita'),
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
