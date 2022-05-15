import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def Ohlc(df=pd.DataFrame, rangeslider=True):
    fig = go.Figure(data=go.Ohlc(x=df.index,
                                 open=df.Open,
                                 high=df.High,
                                 low=df.Low,
                                 close=df.Close,
                                 increasing_line_color='red',
                                 decreasing_line_color='blue'))
    fig.update(layout_xaxis_rangeslider_visible=rangeslider)
    fig.show()


def plot_indicators(plot_title, df=pd.DataFrame, indicator_num=1, eSI_period=2):
    indicators = {1: "MACD",
                  2: "방향성 지표(ADX)",
                  3: "Stochastic",
                  4: "상대강도지수(RSI)",
                  5: "거래량(Volume)",
                  6: "OBV",
                  7: "매집/분산지표(A/D)",
                  8: "강도지수(SI)"}

    fig = make_subplots(rows=3,
                        cols=1,
                        vertical_spacing=0.025,
                        specs=[[{"rowspan":2}],
                               [{}],
                               [{}]],
                        shared_xaxes=True,
                        shared_yaxes=False)

    price_trace = go.Ohlc(x=df.index,
                          open=df.Open,
                          high=df.High,
                          low=df.Low,
                          close=df.Close,
                          increasing_line_color="red",
                          decreasing_line_color="blue",
                          name="Stock_Price")
    EMA_trace = go.Scatter(x=df.index,
                           y=df[df.columns[6]].shift(-3),
                           name="{} 지수이동평균".format(df.columns[6][4:]))
    EMA_half_trace = go.Scatter(x=df.index,
                                y=df[df.columns[7]].shift(-3),
                                name="{} 지수이동평균".format(df.columns[7][4:]))
    fig.append_trace(price_trace,
                     row=1,
                     col=1)
    fig.add_trace(EMA_trace,
                  row=1,
                  col=1)
    fig.add_trace(EMA_half_trace,
                  row=1,
                  col=1)

    if indicator_num == 1:
        print(indicators[indicator_num])
        MACD_trace = go.Scatter(x=df.index,
                                y=df.MACD_Line,
                                name="MACD 선")
        Signal_trace = go.Scatter(x=df.index,
                                y=df.Signal_Line,
                                name="시그널 선")
        MACD_hist = df.MACD_Line - df.Signal_Line
        MACD_hist_trace = go.Bar(x=df.index,
                            y=MACD_hist,
                            name="MACD 히스토그램")

        fig.append_trace(MACD_trace,
                         row=3,
                         col=1)
        fig.add_trace(Signal_trace,
                      row=3,
                      col=1)
        fig.add_trace(MACD_hist_trace,
                      row=3,
                      col=1)

        fig.update_layout(height=800,
                          width=1500,
                          xaxis_rangeslider_visible=False,
                          xaxis3_rangeslider_visible=True,
                          xaxis3_type="date",
                          title="{}".format(plot_title))
        fig.show()

    elif indicator_num == 2:
        print(indicators[indicator_num])
        plus_di_13_trace = go.Scatter(x=df.index,
                                y=df["+DI_13"],
                                name="+DI_13 선")
        minus_di_13_trace = go.Scatter(x=df.index,
                                  y=df["-DI_13"],
                                  name="-DI_13 선")
        ADX_trace = go.Scatter(x=df.index,
                               y=df.ADX,
                               name="ADX")

        fig.append_trace(plus_di_13_trace,
                         row=3,
                         col=1)
        fig.add_trace(minus_di_13_trace,
                      row=3,
                      col=1)
        fig.add_trace(ADX_trace,
                      row=3,
                      col=1)

        fig.update_layout(height=800,
                          width=1500,
                          xaxis_rangeslider_visible=False,
                          xaxis3_rangeslider_visible=True,
                          xaxis3_type="date",
                          title="{}".format(plot_title))
        fig.show()

    elif indicator_num == 3:
        print(indicators[indicator_num])
        K_trace = go.Scatter(x=df.index,
                             y=df["%K"],
                             name="%K선")
        D_trace = go.Scatter(x=df.index,
                             y=df["%D"],
                             name="%D선")

        fig.append_trace(K_trace,
                         row=3,
                         col=1)
        fig.add_trace(D_trace,
                      row=3,
                      col=1)

        fig.update_layout(height=800,
                          width=1500,
                          xaxis_rangeslider_visible=False,
                          xaxis3_rangeslider_visible=True,
                          xaxis3_type="date",
                          title="{}".format(plot_title))
        fig.show()

    elif indicator_num == 4:
        print(indicators[indicator_num])
        RSI_trace = go.Scatter(x=df.index,
                               y=df["RSI"],
                               name="상대강도지수(RSI)")


        fig.append_trace(RSI_trace,
                         row=3,
                         col=1)

        fig.update_layout(height=800,
                          width=1500,
                          xaxis_rangeslider_visible=False,
                          xaxis3_rangeslider_visible=True,
                          xaxis3_type="date",
                          title="{}".format(plot_title))
        fig.show()

    elif indicator_num == 5:
        print(indicators[indicator_num])
        volume_trace = go.Bar(x=df.index,
                              y=df["Volume"],
                              name="거래량",
                              marker={'color':'blue'})


        fig.append_trace(volume_trace,
                         row=3,
                         col=1)

        fig.update_layout(height=800,
                          width=1500,
                          xaxis_rangeslider_visible=False,
                          xaxis3_rangeslider_visible=True,
                          xaxis3_type="date",
                          title="{}".format(plot_title))
        fig.show()

    elif indicator_num == 6:
        print(indicators[indicator_num])
        obv_trace = go.Scatter(x=df.index,
                               y=df["OBV"],
                               name="OBV")

        fig.append_trace(obv_trace,
                         row=3,
                         col=1)

        fig.update_layout(height=800,
                          width=1500,
                          xaxis_rangeslider_visible=False,
                          xaxis3_rangeslider_visible=True,
                          xaxis3_type="date",
                          title="{}".format(plot_title))
        fig.show()

    elif indicator_num == 7:
        print(indicators[indicator_num])
        AD_trace = go.Scatter(x=df.index,
                              y=df["A/D"],
                              name="매집/분산지표")

        fig.append_trace(AD_trace,
                         row=3,
                         col=1)

        fig.update_layout(height=800,
                          width=1500,
                          xaxis_rangeslider_visible=False,
                          xaxis3_rangeslider_visible=True,
                          xaxis3_type="date",
                          title="{}".format(plot_title))
        fig.show()

    elif indicator_num == 8:
        print(indicators[indicator_num])
        SI_trace = go.Scatter(x=df.index,
                              y=df["eSI_{}".format(eSI_period)],
                              name="강도지수")

        fig.append_trace(SI_trace,
                         row=3,
                         col=1)

        fig.update_layout(height=800,
                          width=1500,
                          xaxis_rangeslider_visible=False,
                          xaxis3_rangeslider_visible=True,
                          xaxis3_type="date",
                          title="{}".format(plot_title))
        fig.show()

    else:
        print("해당하는 지표가 없습니다.")
        return
