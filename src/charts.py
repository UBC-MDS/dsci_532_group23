import plotly.graph_objs as go
import plotly.offline as py
import seaborn as sns
from matplotlib import pyplot
from plotly.subplots import make_subplots

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