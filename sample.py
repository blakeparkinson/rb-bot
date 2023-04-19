import sys

from src.trading_bots.base import TradeBot
from src.trading_bots.utilities import ROBINHOOD_PASS
from src.trading_bots.utilities import ROBINHOOD_USER, QR_CODE
from src.trading_bots.simple_moving_average import TradeBotSimpleMovingAverage
from src.trading_bots.volume_weighted_average_price import TradeBotVWAP
from src.trading_bots.twitter_sentiments import TradeBotTwitterSentiments
from src.trading_bots.base import OrderType

tickers = ["AAPL", "MSFT", "AMZN", "GOOG", "GOOGL", "FB", "TSLA", "NVDA", "JPM", "JNJ", 
           "V", "PG", "MA", "UNH", "HD", "PYPL", "DIS", "BAC", "INTC", "ASML", 
           "KO", "NFLX", "CMCSA", "VZ", "ADBE", "CRM", "ORCL", "PEP", "NKE", "WMT", 
           "PFE", "ABT", "CVX", "MCD", "TMO", "CSCO", "NEE", "ACN", "UNP", "XOM", 
           "AMGN", "HON", "ABBV", "QCOM", "MDT", "MRK", "BA", "BMY", "WFC", "LOW", 
           "HDB", "NVS", "BHP", "TGT", "TXN", "CVS", "MMM", "MCHP", "C", "COST", 
           "SHOP", "BLK", "BAJAJ-AUTO.NS", "BP", "AMAT", "TOT", "HSBC", "SBUX", "PM", 
           "TMUS", "UNM", "MO", "CME", "SPGI", "MAA", "MCO", "GLD", "BRK-B", "GS", 
           "FDX", "ADSK", "TEL", "APD", "ETN", "SRE", "WELL", "PSA", "CCI", "SYY", 
           "GSX", "LUV", "DUK", "PNC", "BKNG", "TROW", "TFC", "MMC", "CMI", "SPG", 
           "DHR", "ZTS", "LOW", "KHC", "EOG", "DE", "MS", "ETR", "EXC", "EL", 
           "COP", "EMR", "FDL", "NEE", "APH", "AMP", "ANTM", "VFC", "DD", "CL", 
           "RE", "ALL", "BAX", "DUK", "D", "SO", "AVGO", "CAT", "AXP", "RTX", 
           "SAP", "WFC", "GLW", "ICE", "ZM", "REGN", "BUD", "RTN", "GILD", "BAH", 
           "CCL", "CVNA", "FITB", "MKC", "FISV", "LVS", "WBA", "GIS", "VRTX", "FIS", 
           "WEC", "GD", "HES", "RTX", "DXC", "FE", "GWW", "KO", "PEG", "WEC", 
           "MKTX", "BBY", "LIN", "MNST", "ELAN", "BIIB", "TM", "ADP", "CTSH", "CI", 
           "PCAR", "CINF", "WM", "BR", "HIG", "TIF", "SBAC", "ADI", "DLR", "CTAS"]


# Usage: python sample.py <company_ticker>

def main():

    if len(sys.argv) != 2:
        raise Exception("Must run as python sample.py [company_ticker]")
        
    args = sys.argv[1:]
    ticker = args[0]

    tb0 = TradeBot(ROBINHOOD_USER, ROBINHOOD_PASS, QR_CODE)
    tb1 = TradeBotSimpleMovingAverage(ROBINHOOD_USER, ROBINHOOD_PASS, QR_CODE)
    tb2 = TradeBotVWAP(ROBINHOOD_USER, ROBINHOOD_PASS, QR_CODE)
    # tb3 = TradeBotTwitterSentiments(ROBINHOOD_USER, ROBINHOOD_PASS)

    current_positions = tb0.get_current_positions()

    keys = list(current_positions.keys())
    for key in keys:
        rec1 = tb1.make_order_recommendation(key)
        rec2 = tb2.make_order_recommendation(key)
        if rec1 == OrderType.SELL_RECOMMENDATION and rec2 == OrderType.SELL_RECOMMENDATION:
            print(current_positions[key])
            try:
                tb0.place_sell_order(key, float(current_positions[key]["equity"]))
                print (f"Sold {key} at ${tb0.get_current_market_price(key)}")
            except:
                continue
        else:
            print (f"Did not sell {key} at ${tb0.get_current_market_price(key)}")
    
    # print(f"TwitterSentiments : {tb3.make_order_recommendation(ticker)}")


    current_cash=tb0.get_current_cash_position()
    print(f"Current cash: {current_cash}")
    if current_cash:
        for ticker in tickers:
            try:
                rec1 = tb1.make_order_recommendation(ticker)
                rec2 = tb2.make_order_recommendation(ticker)
            except:
                print(f"Error with {ticker}")
                continue
            if rec1 == OrderType.BUY_RECOMMENDATION and rec2 == OrderType.BUY_RECOMMENDATION:
                print(f"Buying {ticker}")
                tb0.place_buy_order(ticker, current_cash)
                print (f"Bought {ticker} at ${tb0.get_current_market_price(ticker)}")



if __name__ == "__main__":
    main()
