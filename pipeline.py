from datetime import datetime as dt
from get_stock_data import get_stock_historical_data
from financeAnalysisTools import process_stock_data
from dataPlottingTools import plot_indicators


def plot_stock_info(stock,
                    from_date,
                    to_date='{}'.format(dt.today()),
                    country='south korea',
                    interval='Daily',
                    EMA_period=22,
                    ADX_period=13,
                    ATR_period=13,
                    RSI_period=7,
                    eSI_period=2,
                    indicator_num=1):
    """
    원하는 종목의 주가를 찾고 관련 지표를 분석해서 원하는 지표를 주가와 함께
    그래프로 나타내는 함수이다. 모든 구성요소를 한 곳에 묶은 함수이다. 이
    함수를 매인으로 활용할 것이다.
    :param stock: 찾으려는 주식의 이름.
    :param from_date: 언제부터
    :param to_date: 언제까지, 기본값은 오늘이다.
    :param country: 찾고자 하는 주식의 국가. 'south korea'가 기본값이고,
                    미국 주식은 'united states'를 입력한다. 주식이 조회가
                    안되면 국가와 주식이 매칭이 안되는 경우가 많다.
    :param interval: 일일은 'Daily', 주간은 'Weekly', 월간은 'Monthly'를 입력한다.
    :param EMA_period: 지수이동평균의 산출기간
    :param ADX_period: 평균 방향성 지표의 평균 산출 기간
    :param ATR_period: 평균 실제 거래 범위의 평균 산출 기간
    :param RSI_period: 상대 강도 지수의 산출 기간
    :param eSI_period: 강도 지수의 산출 기간
    :param indicator_num: 찾고 싶은 지수의 값을 입력한다.
                          1: "MACD",
                          2: "방향성 지표(ADX)",
                          3: "Stochastic",
                          4: "상대강도지수(RSI)",
                          5: "거래량(Volume)",
                          6: "OBV",
                          7: "매집/분산지표(A/D)",
                          8: "강도지수(SI)"
    :return: 따로 반환하는 것은 없고 그래프를 plotly로 그려준다.
    """
    df = get_stock_historical_data(stock=stock,
                                   from_date=from_date,
                                   to_date=to_date,
                                   country=country,
                                   interval=interval)
    print(df.head())
    try:
        df = process_stock_data(df,
                                EMA_period=EMA_period,
                                ADX_period=ADX_period,
                                ATR_period=ATR_period,
                                RSI_period=RSI_period,
                                eSI_period=eSI_period)

    except:
        print("\n종목 조회에 실패했습니다.")
        return

    plot_indicators(stock,
                    df,
                    indicator_num=indicator_num,
                    eSI_period=eSI_period)


if __name__ == "__main__":
    plot_stock_info(stock="005930",
                    from_date="01/01/2020",
                    interval='Weekly',
                    indicator_num=8)

    # plot_stock_info(stock='005930',
    #                 from_date="01/01/2020",
    #                 interval='Day',
    #                 indicator_num=1)
