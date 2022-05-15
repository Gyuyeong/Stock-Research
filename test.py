from get_stock_data import get_stock_information
from get_stock_data import get_stock_historical_data
from get_stock_data import draw_plotly_stock_chart
from get_stock_data import draw_simple_stock_chart
from get_stock_data import draw_plotly_stock_chart
import matplotlib.pyplot as plt

from ta.trend import ADXIndicator

from news_scraper import get_us_stock_news

from financeAnalysisTools import EMA
from financeAnalysisTools import MACD
from financeAnalysisTools import ADX_ATR
from financeAnalysisTools import stochastic
from financeAnalysisTools import OBV
from financeAnalysisTools import RSI
from financeAnalysisTools import A_D
from financeAnalysisTools import SI
from financeAnalysisTools import eSI
from financeAnalysisTools import process_stock_data

from dataPlottingTools import Ohlc
from dataPlottingTools import plot_indicators

# draw_plotly_stock_chart("삼성바이오", '01/01/2021')

# get_stock_information('선익')

# print(get_stock_historical_data('005930', '01/01/2020', interval='Monthly').head())
# print(get_stock_historical_data('005930', '01/01/2020', interval='Daily').head())
# print(get_stock_historical_data('005930', '01/01/2020', interval='Weekly').head())

# draw_simple_stock_chart('Disney', '01/01/2021', country='united states')

# get_us_stock_news("Amazon")

daily = get_stock_historical_data('005930',
                                          from_date='01/01/2020',
                                          interval='Daily')
# google_weekly = get_stock_historical_data('Amazon',
#                                            from_date='01/01/2020',
#                                            country='United States',
#                                            interval='Weekly')

daily = process_stock_data(daily)

plot_indicators(daily)




