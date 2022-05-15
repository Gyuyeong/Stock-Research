import pandas as pd
import numpy as np
from get_stock_data import get_stock_historical_data

# 추세추종지표: EMA, MACD, ADX_ATR 함수들이다.
def EMA(dataframe=pd.DataFrame, period=22):
    """
    지수이동평균을 구하는 함수이다.
    :param dataframe: 분석이 필요한 종목의 주가 데이터
    :param period: 산출 기간. 길수록 장기 추세를 포착하기 좋다. 일일 데이터는 22,
    주간 데이터는 26을 추천한다.
    :return: EMA값이 추가된 주가 데이터. pandas DataFrame이 반환된다.
    """
    df = dataframe.copy()

    eMov = df.Close.ewm(span=period).mean()

    df["eMov{}".format(period)] = eMov

    return df


def MACD(dataframe=pd.DataFrame):
    """
    MACD 선과 히스토그램을 그릴 수 있게끔 값들을 계산해주는 함수이다.
    :param dataframe: 분석이 필요한 종목의 주가 데이터
    :return: MACD선과 히스토그램을 작성하기 위한 값들이 추가된 pd.DataFrame
    """
    df = dataframe.copy()

    eMov26 = df.Close.ewm(span=26).mean()
    eMov12 = df.Close.ewm(span=12).mean()

    macd_line = eMov12 - eMov26
    signal_line = macd_line.ewm(span=9).mean()

    df["MACD_Line"] = macd_line
    df["Signal_Line"] = signal_line

    return df


def ADX_ATR(dataframe=pd.DataFrame, ADX_period=13, ATR_period=13):
    """
    ADX는 평균 방향성 지표이다. ATR은 평균 실제 거래 범위이다. ADX와 +DI_13, -DI_13,
    그리고 ATR을 계산해 주는 함수이다. 아래에 있는 함수들은 모두 내부 함수들로 이 함수의
    보조 함수들이기 때문에 이렇게 작성했다. get_DM, get_TR, get_DI, ADX, ATR이
    이에 해당한다.
    :param dataframe: 분석이 필요한 종목의 주가데이터
    :param period: ATR을 산출하는 기간
    :return: ATR, +DI_13, -DI_13, ATR이 들어있는 DataFrame을 반환한다.
    """
    def get_DM(dataframe=pd.DataFrame):
        df = dataframe.copy()

        high_dm = df.High.diff()
        low_dm = df.Low.diff()
        high_dm[high_dm < 0] = 0
        low_dm[low_dm > 0] = 0

        dm = high_dm + low_dm

        plus_dm = dm.copy()
        minus_dm = dm.copy()

        plus_dm[plus_dm < 0] = 0
        minus_dm[minus_dm > 0] = 0
        plus_dm.fillna(0, inplace=True)
        minus_dm.fillna(0, inplace=True)

        df["plus_dm"] = plus_dm.apply(abs)
        df["minus_dm"] = minus_dm.apply(abs)

        return df

    def get_TR(dataframe=pd.DataFrame):
        df = dataframe.copy()
        df["Close_yest"] = df.Close.shift(1)
        df["Close_yest"].fillna(df["Close"][0], inplace=True)

        a1 = abs(df.High - df.Low)
        a2 = abs(df.High - df["Close_yest"])
        a3 = abs(df.Low - df["Close_yest"])

        TR_candidates = pd.concat([a1, a2, a3], axis=1)
        df["TR"] = TR_candidates.apply(max, axis=1)

        df.drop(["Close_yest"], axis=1, inplace=True)

        return df

    def get_DI(dataframe=pd.DataFrame):
        df = dataframe.copy()
        df = get_TR(get_DM(df))

        plus_di = df["plus_dm"] / df["TR"] * 100
        minus_di = df["minus_dm"] / df["TR"] * 100

        df["plus_di"] = plus_di.fillna(0)
        df["minus_di"] = minus_di.fillna(0)

        df.drop(["plus_dm", "minus_dm"], axis=1, inplace=True)

        return df

    def ADX(dataframe=pd.DataFrame):
        df = dataframe.copy()

        df = get_DI(df)
        plus_eDI_13 = df["plus_di"].ewm(span=13).mean()
        minus_eDI_13 = df["minus_di"].ewm(span=13).mean()

        DX = abs(((plus_eDI_13 - minus_eDI_13) / (plus_eDI_13 + minus_eDI_13))) * 100

        ADX = DX.ewm(span=ADX_period).mean()
        df["+DI_13"] = plus_eDI_13
        df["-DI_13"] = minus_eDI_13
        df["ADX"] = ADX.fillna(0)

        df.drop(["plus_di", "minus_di"], axis=1, inplace=True)

        return df

    def ATR(dataframe=pd.DataFrame):
        df = dataframe.copy()

        ATR = df["TR"].ewm(span=ATR_period).mean()
        df["ATR"] = ATR

        df.drop(["TR"], axis=1, inplace=True)

        return df

    return ATR(ADX(dataframe))


# 다음은 전환점을 포착해주는 오실레이터의 역할을 해주는 지표들이다. MACD 히스토그램,
# 스토캐스틱, 상대강도지수가 이에 속한다.
def stochastic(dataframe=pd.DataFrame):
    """
    스토캐스틱은 종가와 최근 '고가 - 저가' 거래 범위의 관계를 추적한다. 해당 함수는
    느린 스토캐스틱을 구현한다.
    :param dataframe: 분석이 필요한 종복의 주가 데이터
    :return: 스토캐스틱에 필요한 %K와 %D가 포함된 DataFrame을 반환한다.
    """
    df = dataframe.copy()

    Hn = df.High.rolling(window=5).max()
    Ln = df.Low.rolling(window=5).min()
    raw_stochastic = (df.Close - Ln) / (Hn - Ln) * 100

    # %K
    averaged_raw_stochastic = raw_stochastic.ewm(span=3).mean()
    # %D
    averaged_once_more = averaged_raw_stochastic.ewm(span=3).mean()

    df["%K"] = averaged_raw_stochastic
    df["%D"] = averaged_once_more

    return df


def RSI(dataframe = pd.DataFrame, period=7):
    """
    상대강도지수를 계산하는 함수이다.
    :param dataframe: 분석이 필요한 종목의 주가 데이터
    :param period: 산출 기간이다. 7, 9일처럼 짧은 기간을 산출하면 매수 신호가 더
    뚜렷하게 보인다. 
    :return: 상대강도지수를 계산한 DataFrame
    """
    df = dataframe.copy()

    up = np.where(df.Close.diff() > 0, df.Close.diff(), 0)
    down = np.where(df.Close.diff() < 0, df.Close.diff() * (-1), 0)

    average_up = pd.Series(up).rolling(window=period, min_periods=period).mean()
    average_down = pd.Series(down).rolling(window=period, min_periods=period).mean()

    RSI = 100 - (100) / (1 + (average_up / average_down))
    RSI.index = df.index

    df["RSI"] = RSI

    return df


# 거래량과 관련된 지표들이다.
def OBV(dataframe=pd.DataFrame):
    """
    OBV는 거래량 누계로 종가의 전일 대비 등락에 따라 그날의 거래량을 더하거나 뺀 값들이다.
    패자들이 느끼는 고통의 강도를 반영한 것이다.
    :param dataframe: 분석이 필요한 종목의 주가 데이터
    :return: OBV 값이 계산된 DataFrame
    """
    df = dataframe.copy()

    obv = pd.Series(index=df.index, dtype="float")
    obv.iloc[0] = df.Volume.iloc[0]

    for i in range(1, df.shape[0]):
        if df.Close.iloc[i] > df.Close.iloc[i - 1]:
            obv.iloc[i] = obv.iloc[i - 1] + df.Volume.iloc[i]

        elif df.Close.iloc[i] < df.Close.iloc[i - 1]:
            obv.iloc[i] = obv.iloc[i - 1] - df.Volume.iloc[i]
        else:
            obv.iloc[i] = obv.iloc[i - 1]

    df["OBV"] = obv

    return df


def A_D(dataframe=pd.DataFrame):
    """
    매집/분산지표이다. OBV보다 미세하게 조정할 수 있다는 장점이 있다.
    :param dataframe: 분석이 필요한 종목의 주가 데이터
    :return: 매집/분산지표가 계산된 DataFrame
    """
    df = dataframe.copy()

    A_D = (df.Close - df.Open) / (df.High - df.Low) * df.Volume

    df["A/D"] = A_D.fillna(0)

    return df


def SI(dataframe=pd.DataFrame):
    """
    강도지수
    :param dataframe: 분석이 필요한 종목의 주가 데이터
    :return: 강도지수가 계산된 DataFrame
    """
    df = dataframe.copy()

    SI = df.Close.diff() * df.Volume

    df["SI"] = SI.fillna(0)

    return df


def eSI(dataframe=pd.DataFrame, period=2):
    """
    강도지수를 평활화하는 함수.
    :param dataframe:
    :param period: 산출하는 기간. 단기, 중/장기 모두 활용 방법이 있다.
    :return:
    """
    df = dataframe.copy()

    SI = df.Close.diff() * df.Volume

    SI.fillna(0, inplace=True)

    eSI = SI.ewm(span=period).mean()

    df["eSI_{}".format(period)] = eSI

    return df


def process_stock_data(dataframe=pd.DataFrame, EMA_period=22, ADX_period=13, ATR_period=13, RSI_period=7, eSI_period=2):
    df = dataframe.copy()

    df = EMA(df, EMA_period)
    df = EMA(df, int(EMA_period / 2))
    df = MACD(df)
    df = ADX_ATR(df, ADX_period, ATR_period)
    df = stochastic(df)
    df = RSI(df, RSI_period)
    df = OBV(df)
    df = A_D(df)
    df = eSI(df, eSI_period)


    # return eSI(A_D(OBV(RSI(stochastic(ADX_ATR(MACD(EMA(df, EMA_period)), ADX_period, ATR_period)), RSI_period))), eSI_period)
    return df