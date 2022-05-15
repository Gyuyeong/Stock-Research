import investpy
from datetime import datetime as dt
import re

import numpy as np
import pandas as pd
import os
import mplfinance as mpf
import plotly.graph_objects as go
import matplotlib.pyplot as plt


# Need to find a way to always pick out the stock you want rather than
# having multiple choices and the user having to browse.
def get_stock_code_from_name(stock):
    """
    대한민국 주식 이름으로 종목코드를 찾는 함수이다. 한국 종목의 경우, 이 함수를 먼저
    사용해서 코드를 먼저 검색한 다음 아래에 있는 함수들을 사용해야 애로사항이 덜 생긴다.
    stock: 종목 이름을 입력한다. 이름에 따라 하나의 결과만 나올 수 있고
           여러개의 결과가 나올 수 있다. 여러개가 나올 경우 조금 더
           구체적으로 검색하든가 코드번호를 찾으면 된다.
    return: 검색결과가 하나일 경우, 그 종목의 코드번호를 반환한다. 여러개일 경우,
            검색결과들만 보여주고 따로 반환하는 값은 없다.
    """
    df = pd.read_csv('종목코드_20210920.csv', encoding='euc-kr')
    target_df = df.loc[df['한글 종목약명'].str.contains(stock)]
    if target_df.shape[0] != 1:
        print(target_df[['단축코드', '한글 종목약명']])
        return
    else:
        print(target_df[['단축코드', '한글 종목약명']])
        return target_df.iloc[0, 1]


def get_stock_information(stock, country='south korea'):
    """
    stock: Enter the name of the stock you want to search, 종목코드를 넣어도 된다. 한국종목의 경우 코드를 넣는게 좋다.
    country: Enter the country name. Default is 'south korea'
    return: Returns the information of the stock.
    prevClose: 최근 종가, Investing.com 사이트 특성상 하루 정도의 딜레이가 있는 듯하다.
    dailyRange: 그날 최고치-최저치 범위
    revenue: 매출액
    open: 시가
    52weekRange: 1년 주가변동폭, 코드 내에서는 weekRange라고밖에 안나와있다. 혼동하지 말기.
    eps: Earning Per Share: 주당순이익
    Volume: 주식거래량
    marketCap: 시가총액
    dividend: 배당(률)
    avgVolume (3m): 3개월 평균 주식거래량
    P/E ratio: PER, Price Earning Ratio, 주가수익비율, 주가 / EPS == 시가총액 / 순이익
    beta: 베타계수(상관성), 특정 표준과 관련된 주식의 상대적 변동성을 측정한 값. 공분산 / 분산
    oneYearReturn: 1년 투자대비 수익률
    sharesOutstanding: 회사가 주식 발행 후 재취득하지 않은 주식수.
    nextEarningDate: 다음 실적발표일
    """

    if (country == 'south korea') & (stock[0].isdigit() is False):
        stock_code = get_stock_code_from_name(stock)
        if stock_code is None:
            print('원하시는 종목의 코드를 찾아서 넣어주세요')
            return
        else:
            search_result = investpy.search_quotes(text=stock_code,
                                                   products=['stocks'],
                                                   countries=[country],
                                                   n_results=1)
    else:
        search_result = investpy.search_quotes(text=stock,
                                               products=['stocks'],
                                               countries=[country],
                                               n_results=1)
    information = search_result.retrieve_information()
    print(information)
    return information


def get_stock_historical_data(stock, from_date, to_date='{}'.format(dt.today()), country='south korea', interval='Daily'):
    """
    stock: Enter the name of the stock you want to search
    from_date: Enter the start date of the stock you want to browse. Has to be inserted as Strings. i.e. '01/01/2020'
    to_date: Default is Today
    country: Default country is 'south korea'
    interval: 'Daily', 'Weekly', 'Monthly'
    return: Returns the prices of the stock in a chronological order.
    """

    if to_date.__contains__('-'):
        date_elements = '{}'.format(dt.today())[:10].split('-')
        to_date = date_elements[2] + '/' + date_elements[1] + '/' + date_elements[0]

    if (country == 'south korea') & (stock[0].isdigit() is False):
        stock_code = get_stock_code_from_name(stock)

        if stock_code is None:
            print('원하시는 종목의 코드를 찾아서 넣어주세요')
            return
        else:
            historical_data = investpy.get_stock_historical_data(stock=stock_code,
                                                      country=country,
                                                      from_date=from_date,
                                                      to_date=to_date,
                                                      as_json=False,
                                                      order='ascending',
                                                      interval=interval)
    elif (country == 'united states') or (country == 'United States'):
        search_result = investpy.search_quotes(text=stock,
                                               products=['stocks'],
                                               countries=[country],
                                               n_results=1)
        search_result = str(search_result)
        search_match = re.search('(?<="symbol": ")(\w+)"', search_result)
        search_symbol = search_match.group(1)
        print(search_symbol)
        historical_data = investpy.get_stock_historical_data(stock=search_symbol,
                                                             country=country,
                                                             from_date=from_date,
                                                             to_date=to_date,
                                                             as_json=False,
                                                             order='ascending',
                                                             interval=interval)

    else:
        historical_data = investpy.get_stock_historical_data(stock=stock,
                                                             country=country,
                                                             from_date=from_date,
                                                             to_date=to_date,
                                                             as_json=False,
                                                             order='ascending',
                                                             interval=interval)

    return historical_data


def get_per(stock, country='south korea'):
    """
    PER(주당순이익률)를 계산해주는 함수.
    stock: 원하는 주식을 입력한다.
    country: 나라를 입력한다. 기본값은 'south korea'이다.
    return: PER값을 반환한다.
    """
    information = get_stock_information(stock, country)
    prevClose = information['prevClose']
    eps = information['eps']
    per = prevClose/eps
    print(per)
    return per


def draw_simple_stock_chart(stock, from_date, to_date='{}'.format(dt.today()), country='south korea'):
    """
    mplfinance를 이용한 간단한 주식차트를 그려주는 함수이다.
    :param stock: 한국주식의 경우, 코드를 찾아주고 돌려준다. 단 검색결과가 여러개일 경우
                  직접 찾아야한다.
    :param from_date: 언제부터
    :param to_date: 언제까지. 기본값은 오늘
    :param country: 국가, 기본값은 'south korea'이다. 주로 'united states'를
                    찾지 않을까?
    :return: 그래프를 그려준다. 따로 반환하는 값은 없다.
    """
    if (country == 'south korea') & (stock[0].isdigit() is False):
        stock_code = get_stock_code_from_name(stock)
        if stock_code is None:
            print('원하시는 종목의 코드를 찾아서 넣어주세요')
            return
        else:
            df = get_stock_historical_data(stock_code, from_date, to_date, country)

    else:
        df = get_stock_historical_data(stock, from_date, to_date, country)
        print(df.head())

    colorset = mpf.make_marketcolors(up='tab:red',
                                     down='tab:blue',
                                     volume='tab:blue')
    s = mpf.make_mpf_style(marketcolors=colorset)

    mpf.plot(df, type='candle', volume=True, style=s)


def draw_plotly_stock_chart(stock, from_date, to_date='{}'.format(dt.today()), country='south korea'):
    """
    plotly로 주가차트를 그려주는 함수이다.
    :param stock: 주식. 한국주식의 경우 코드를 찾아준다.
    :param from_date: 언제부터
    :param to_date: 언제까지, 기본값은 오늘
    :param country: 국가, 기본값은 'south korea'
    :return: 그래프를 그려준다. 따로 반환값은 없다.
    """
    if (country == 'south korea') & (stock[0].isdigit() is False):
        stock_code = get_stock_code_from_name(stock)
        if stock_code is None:
            print('원하시는 종목의 코드를 찾아서 넣어주세요')
            return
        else:
            df = get_stock_historical_data(stock_code, from_date, to_date, country)
    else:
        df = get_stock_historical_data(stock, from_date, to_date, country)
        print(df.head())

    candle = go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
    )
    fig = go.Figure(data=candle)
    fig.show()


if __name__ == '__main__':
    # draw_simple_stock_chart('roblox', '01/01/2021', country='united states')
    # draw_plotly_stock_chart('costco', '01/01/2021', country='united states')
    # print(investpy.search_quotes('171090', countries=['south korea'], products=['stocks'], n_results=1))
    data = investpy.get_stock_historical_data(stock='323990',
                                              country='south korea',
                                              from_date='01/01/2020',
                                              to_date='01/01/2021',
                                              as_json=False,
                                              order='ascending',
                                              interval='Weekly')
    info = investpy.get_stock_information("323990")

    print(data.head())
