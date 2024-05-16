import yfinance as yf
import pandas as pd
import requests
from io import StringIO
from alpha_vantage.fundamentaldata import FundamentalData
import os


def get_all_data(ticker, debug=True):
    ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', 'BJQ9A6ATDD7QU4QG')
    fd = FundamentalData(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')
    stock = yf.Ticker(ticker)
    results = {}

    # Fetch stock history for RSI
    try:
        history = stock.history(period="1y")
        if not history.empty:
            delta = history['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            results['rsi'] = 100 - (100 / (1 + rs)).iloc[-1]
        if debug:
            print(f"{ticker} RSI: {results.get('rsi', 'No data')}")
    except Exception as e:
        print(f"Error calculating RSI for {ticker}: {e}")

    # Fetch PEG Ratio
    try:
        data, _ = fd.get_company_overview(ticker)
        if not data.empty and 'PEGRatio' in data.columns and data['PEGRatio'].iloc[0] not in [None, 'None', '']:
            results['peg_ratio'] = float(data['PEGRatio'].iloc[0])
        if debug:
            print(f"{ticker} PEG Ratio: {results.get('peg_ratio', 'No data')}")
    except Exception as e:
        print(f"Error fetching PEG Ratio for {ticker}: {e}")

    # Fetch Free Cash Flow
    try:
        data, _ = fd.get_cash_flow_annual(ticker)
        if not data.empty and 'freeCashFlow' in data.columns and data['freeCashFlow'].iloc[0] not in [None, 'None', '']:
            results['free_cash_flow'] = float(data['freeCashFlow'].iloc[0])
        if debug:
            print(f"{ticker} Free Cash Flow: {results.get('free_cash_flow', 'No data')}")
    except Exception as e:
        print(f"Error fetching free cash flow for {ticker}: {e}")

    return results