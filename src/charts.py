import plotly.express as px
import plotly.graph_objs as go
import plotly.offline as py
import seaborn as sns
from matplotlib import pyplot
from plotly.subplots import make_subplots


def world_map(df, year='2018', energy_type='all_renewable', **kw):
    """Create main world map plot of energy consumption"""

    # filter 
    # NOTE filtering everyting less than 1e9.. some small countries have weird per capita values
    df = df.loc[year] \
        .pipe(lambda df: df[
            (df.energy_type == energy_type) &
            (df.country_code != 'WORL') &
            (df.energy_per_capita < 1e9)
            ])

    map_trace = go.Choropleth(
        locations=df.country_code,
        z=df.energy_per_capita,
        locationmode='ISO-3',
        colorscale='viridis',
        # reversescale=True
        # colorbar_title = "Millions USD",
    )

    fig = go.Figure(data=[map_trace])

    fig.update_layout(
        title_text = 'World Energy Consumption',
        margin=dict(t=30, b=0, r=0, l=20),
        # geo_scope='usa', # limite map scope to USA
    )

    return fig

def chart_single_country(df, country='Canada'):
    fig = go.Figure()

    df = df[df.country == country]

    x = df.index.to_timestamp()

    xaxis = dict(
        ticktext=df.index.strftime('%Y'),
        tickvals=x,
        tickangle=270,
        showgrid=False,
    )

    # traces = []
    energy_types = ['coal', 'natural_gas', 'petroleum', 'nuclear', 'renewables']
    for energy in energy_types:
        df2 = df[df.energy_type == energy]

        trace = go.Scatter(
            name=energy,
            x=df2.index.to_timestamp(),
            y=df2.energy,
        )

        fig.add_trace(trace)

    # fig.append_trace(traces)

    fig.update_layout(
        xaxis=xaxis,
        margin=dict(t=30, b=0, r=0, l=0),
        title='Energy Consumption (Canada)',
        yaxis=dict(
            title='Energy Consumption (Quad BTU)',
            showgrid=False
        ),
        width=800,
        height=300,
        plot_bgcolor='white'
    )

    return fig
