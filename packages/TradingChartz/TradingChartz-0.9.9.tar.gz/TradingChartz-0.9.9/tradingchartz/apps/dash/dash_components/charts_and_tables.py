# external standard
import os
import pandas as pd
import datetime as dt
from pandas_datareader import get_data_yahoo as yahoo_data
from dateutil.relativedelta import relativedelta

# external dash
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_html_components as html

# internal import
import tradingchartz.apps.dash.helpers.helper_functions as hf


def generate_ohlc_graph(fig,
                        df) -> go.Figure:
    fig.add_trace(
        go.Candlestick(x=df.index.strftime('%Y-%m-%d'),
                       open=df['Open'],
                       high=df['High'],
                       low=df['Low'],
                       close=df['Close'],
                       name='OHLC')
    )
    fig.update(layout_xaxis_rangeslider_visible=False)
    fig.update_xaxes(type='category')
    # # fig.update_layout(
    # #                   xaxis=dict(
    # #                       rangeselector=dict(
    # #                           buttons=list([
    # #                               dict(count=5,
    # #                                    label="5d",
    # #                                    step="day",
    # #                                    stepmode="backward"),
    # #                               dict(count=1,
    # #                                    label="1m",
    # #                                    step="month",
    # #                                    stepmode="backward"),
    # #                               dict(count=6,
    # #                                    label="6m",
    # #                                    step="month",
    # #                                    stepmode="backward"),
    # #                               dict(count=1,
    # #                                    label="YTD",
    # #                                    step="year",
    # #                                    stepmode="todate"),
    # #                               dict(count=1,
    # #                                    label="1y",
    # #                                    step="year",
    # #                                    stepmode="backward"),
    # #                               dict(step="all")
    # #                           ])
    # #                       ),
    # #                       range=[(min(df.index.date) - dt.timedelta(1)), (max(df.index.date) + dt.timedelta(1))],
    # #                   ),
    #                   margin=dict(l=20, r=20, t=20, b=20))
    return fig


def add_signals_to_chart(fig: go.Figure,
                         signal_df: pd.DataFrame,
                         ohlc_df: pd.DataFrame) -> go.Figure:
    for pattern in signal_df.columns:
        up_signal, down_signal = hf.df_bifurcate_positive_and_negative_signals(signal_df[pattern])
        if not up_signal.empty:
            fig.add_trace(
                go.Scatter(
                    x=up_signal.index.strftime('%Y-%m-%d'),
                    y=ohlc_df.loc[up_signal.index, 'High'],
                    mode='markers',
                    name=pattern,
                    marker_symbol='triangle-up',
                    marker=dict(
                        color='darkgreen',
                        size=10)
                )
            )
        if not down_signal.empty:
            fig.add_trace(
                go.Scatter(
                    x=down_signal.index.strftime('%Y-%m-%d'),
                    y=ohlc_df.loc[down_signal.index, 'Low'],
                    mode='markers',
                    name=pattern,
                    marker_symbol='triangle-down',
                    marker=dict(
                        color='orange',
                        size=10)
                )
            )
    return fig


def triple_barrier_setter_template():
    return [html.Div("**Only for long signals"),
            dbc.Row(
                [
                    dbc.Col(dbc.Label("Upper Barrier")),
                    dbc.Col(dbc.Input(id="tb-upper", placeholder="Profit Booking", type="float")),
                ], no_gutters=True),
            dbc.Row(
                [
                    dbc.Col(dbc.Label("Lower Barrier")),
                    dbc.Col(dbc.Input(id="tb-lower", placeholder="Stop Loss", type="float")),
                ], no_gutters=True),
            dbc.Row(
                [
                    dbc.Col(dbc.Label("Vertical Barrier")),
                    dbc.Col(dbc.Input(id="tb-vertical", placeholder="Time Horizon", type="float")),
                ], no_gutters=True),
            ]


def daily_recommendation_twitter_template(symbol: str,
                                          name: str = None,
                                          end_date: dt.date = dt.date.today(),
                                          entry: float = None,
                                          sl: float = None,
                                          rr: float = None,
                                          sl_min: float = .02,
                                          sl_max: float = .1,
                                          conviction: int = 4) -> go.Figure:
    """
    Generates daily twitter template chart for given Symbol
    :param symbol: str - ticker
    :param name: str - Optional(default value from constituents file)
                    Full name of company or any other information to be added
    :param end_date: Optional (default value as today) dt.date - Date T
    :param entry: float - Optional (default Close of T)
    :param sl: float - Optional(default set min of Low for T adn T-1)
    :param rr: float - Optional(default set to 2) risk reward ratio too determine TP from SL
    :param sl_min: float - Optional(default 0.02) to set cap for sl e.g. for 2% min sl use 0.02
    :param sl_max: float - Optional(default 0.10) to set floor for sl e.g. for 10% max sl use 0.1
    :param conviction: int - Optional(default 4 stars) to add no. of stars
    :return: Fig - Twitter template
    """
    index_constituents = pd.read_csv(os.path.join(os.path.dirname(__file__), '../../../data/NIFTY500_constituents.csv'))
    index_constituents.set_index('Symbol', inplace=True)
    if name is None:
        name = f"{index_constituents.loc[symbol, 'Company Name']} ({index_constituents.loc[symbol, 'Industry']})"
    start_date = end_date - relativedelta(months=1)
    df = yahoo_data(symbol + '.NS', start=start_date, end=end_date).round(2)
    star = '⭐'
    conviction_star = conviction * star
    df.index = df.index.strftime('%d-%b')
    if entry is None:
        entry = round(df.Close.iloc[-1], 2)
    if sl is None:
        sl = round(max(min(min(df.Low.iloc[-2:]), (1-sl_min)*entry), (1-sl_max)*entry), 2)
    if rr is None:
        rr = 2
    tp = round((entry + rr*(entry-sl)), 2)
    data = [dict(type='candlestick',
                 open=df.Open,
                 high=df.High,
                 low=df.Low,
                 close=df.Close,
                 opacity=.5,
                 x=df.index,
                 yaxis='y2',
                 name=symbol,
                 increasing=dict(fillcolor='rgba(0,0,0,0)', line={'width': 1}),
                 decreasing=dict(fillcolor='rgba(0,0,0,0)', line={'width': 1})),
            dict(x=df.index,
                 y=df.Volume,
                 opacity=.1,
                 marker=dict(color='Grey'),
                 type='bar', yaxis='y',
                 name='Volume')]
    fig = go.Figure(data=data)
    fig.add_shape(type='line',
                  x0=0,
                  y0=sl,
                  x1=1,
                  y1=sl,
                  opacity=.7,
                  line=dict(color='Red', dash="dashdot", width=.75),
                  xref='paper',
                  yref='y2'
                  )
    fig.add_shape(type='line',
                  x0=0,
                  y0=tp,
                  x1=1,
                  y1=tp,
                  opacity=.7,
                  line=dict(color='Green', dash="dashdot", width=.75),
                  xref='paper',
                  yref='y2',
                  )
    fig.add_shape(type='line',
                  x0=0,
                  y0=entry,
                  x1=1,
                  y1=entry,
                  opacity=.7,
                  line=dict(color='Grey', dash="dashdot", width=.75),
                  xref='paper',
                  yref='y2'
                  )
    fig.add_annotation(x=1, y=tp,
                       font=dict(
                           family="Courier New, monospace",
                           size=12,
                           color="white"
                       ),
                       xref='paper',
                       yref='y2',
                       text=f"<b>TP:{tp}</b>",
                       xanchor='left',
                       yanchor='middle',
                       bgcolor="green",
                       showarrow=False)
    fig.add_annotation(x=1, y=entry,
                       font=dict(
                           family="Courier New, monospace",
                           size=12,
                           color='white'
                       ),
                       xref='paper',
                       yref='y2',
                       xanchor='left',
                       yanchor='middle',
                       bgcolor="grey",
                       text=f"<b>En:{entry}</b>",
                       showarrow=False)
    fig.add_annotation(x=1, y=sl,
                       font=dict(
                           family="Courier New, monospace",
                           size=12,
                           color="white"
                       ),
                       xref='paper',
                       yref='y2',
                       text=f"<b>SL:{sl}</b>",
                       # yshift=-10,
                       xanchor='left',
                       yanchor='middle',
                       bgcolor="red",
                       showarrow=False)
    fig.update_layout(
        title_text=f'<b><span style="font-size:17px">{symbol} | Date: {end_date.strftime("%d-%b")} </b></span><br>'
              f'<b><span style="font-size:12px";>{name}</span><br>'
              f'<b><span style="font-size:12px;color:blue">Entry(En): {entry} | Stop Loss(SL): {sl} | Take Profit(TP): {tp}<span></b><br>'
              f'<b><span style="font-size:12px; color:black; class="emoji">Conviction: {conviction_star}</span>',
        xaxis=go.layout.XAxis(rangeslider=dict(visible=False), dtick=5),
        title = dict(xanchor="left",
                     y=.95),
        yaxis=dict(domain=[0, 0.2], showticklabels=False, side='right', overlaying='y', showgrid=False),
        yaxis2=dict(domain=[0, 1], side='right', overlaying='y', showgrid=False),
        autosize=False,
        width=500,
        height=400,
        margin=dict(
            l=10,
            r=90,
            b=20,
            t=100,
            pad=1
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig
