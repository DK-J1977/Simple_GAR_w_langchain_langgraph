"""
Yahoo Finance tool for fetching financial data.
"""
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

try:
    import yfinance as yf
    import pandas as pd
except ImportError as e:
    logging.error(f"Required library not installed: {e}")
    raise

logger = logging.getLogger(__name__)


class YahooFinanceTool:
    """Tool for fetching financial data from Yahoo Finance."""

    def __init__(self):
        """Initialize Yahoo Finance tool."""
        pass

    def get_stock_info(self, ticker: str) -> Dict[str, Any]:
        """
        Get comprehensive stock information.

        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT')

        Returns:
            Dictionary containing stock information
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            # Extract key metrics
            result = {
                'ticker': ticker,
                'name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': info.get('marketCap', 'N/A'),
                'current_price': info.get('currentPrice', 'N/A'),
                'previous_close': info.get('previousClose', 'N/A'),
                'open': info.get('open', 'N/A'),
                'day_high': info.get('dayHigh', 'N/A'),
                'day_low': info.get('dayLow', 'N/A'),
                'volume': info.get('volume', 'N/A'),
                'average_volume': info.get('averageVolume', 'N/A'),
                '52_week_high': info.get('fiftyTwoWeekHigh', 'N/A'),
                '52_week_low': info.get('fiftyTwoWeekLow', 'N/A'),
                'pe_ratio': info.get('trailingPE', 'N/A'),
                'forward_pe': info.get('forwardPE', 'N/A'),
                'eps': info.get('trailingEps', 'N/A'),
                'dividend_yield': info.get('dividendYield', 'N/A'),
                'beta': info.get('beta', 'N/A'),
                'analyst_recommendation': info.get('recommendationKey', 'N/A'),
                'target_price': info.get('targetMeanPrice', 'N/A')
            }

            return result
        except Exception as e:
            logger.error(f"Error fetching stock info for {ticker}: {e}")
            return {'error': str(e), 'ticker': ticker}

    def get_financial_statements(self, ticker: str) -> Dict[str, Any]:
        """
        Get financial statements (income statement, balance sheet, cash flow).

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dictionary containing financial statements
        """
        try:
            stock = yf.Ticker(ticker)

            result = {
                'ticker': ticker,
                'income_statement': None,
                'balance_sheet': None,
                'cash_flow': None
            }

            # Get financial statements
            try:
                result['income_statement'] = stock.financials.to_dict() if stock.financials is not None else None
            except:
                pass

            try:
                result['balance_sheet'] = stock.balance_sheet.to_dict() if stock.balance_sheet is not None else None
            except:
                pass

            try:
                result['cash_flow'] = stock.cashflow.to_dict() if stock.cashflow is not None else None
            except:
                pass

            return result
        except Exception as e:
            logger.error(f"Error fetching financial statements for {ticker}: {e}")
            return {'error': str(e), 'ticker': ticker}

    def get_historical_data(
        self,
        ticker: str,
        period: str = "1y",
        interval: str = "1d"
    ) -> Dict[str, Any]:
        """
        Get historical price data.

        Args:
            ticker: Stock ticker symbol
            period: Time period (e.g., '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', 'max')
            interval: Data interval (e.g., '1m', '5m', '1h', '1d', '1wk', '1mo')

        Returns:
            Dictionary containing historical data
        """
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period, interval=interval)

            if hist.empty:
                return {'error': 'No historical data available', 'ticker': ticker}

            # Convert to dict and format
            result = {
                'ticker': ticker,
                'period': period,
                'interval': interval,
                'data': hist.to_dict('index'),
                'summary': {
                    'start_date': str(hist.index[0]),
                    'end_date': str(hist.index[-1]),
                    'num_records': len(hist),
                    'latest_close': float(hist['Close'].iloc[-1]),
                    'period_return': float((hist['Close'].iloc[-1] / hist['Close'].iloc[0] - 1) * 100)
                }
            }

            return result
        except Exception as e:
            logger.error(f"Error fetching historical data for {ticker}: {e}")
            return {'error': str(e), 'ticker': ticker}

    def get_analyst_recommendations(self, ticker: str) -> Dict[str, Any]:
        """
        Get analyst recommendations.

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dictionary containing analyst recommendations
        """
        try:
            stock = yf.Ticker(ticker)
            recommendations = stock.recommendations

            if recommendations is None or recommendations.empty:
                return {'error': 'No recommendations available', 'ticker': ticker}

            result = {
                'ticker': ticker,
                'recommendations': recommendations.to_dict('index')
            }

            return result
        except Exception as e:
            logger.error(f"Error fetching analyst recommendations for {ticker}: {e}")
            return {'error': str(e), 'ticker': ticker}

    def get_key_metrics_summary(self, ticker: str) -> str:
        """
        Get a text summary of key financial metrics.

        Args:
            ticker: Stock ticker symbol

        Returns:
            Formatted text summary
        """
        info = self.get_stock_info(ticker)

        if 'error' in info:
            return f"Error fetching data for {ticker}: {info['error']}"

        summary = f"""
Financial Summary for {info['name']} ({ticker}):

Company Information:
- Sector: {info['sector']}
- Industry: {info['industry']}

Stock Performance:
- Current Price: ${info['current_price']}
- Previous Close: ${info['previous_close']}
- Day Range: ${info['day_low']} - ${info['day_high']}
- 52 Week Range: ${info['52_week_low']} - ${info['52_week_high']}

Valuation Metrics:
- Market Cap: ${info['market_cap']:,} if isinstance(info['market_cap'], (int, float)) else {info['market_cap']}
- P/E Ratio: {info['pe_ratio']}
- Forward P/E: {info['forward_pe']}
- EPS: {info['eps']}

Trading Metrics:
- Volume: {info['volume']:,} if isinstance(info['volume'], (int, float)) else {info['volume']}
- Average Volume: {info['average_volume']:,} if isinstance(info['average_volume'], (int, float)) else {info['average_volume']}
- Beta: {info['beta']}

Additional Information:
- Dividend Yield: {info['dividend_yield']}
- Analyst Recommendation: {info['analyst_recommendation']}
- Target Price: ${info['target_price']}
"""
        return summary.strip()

    def compare_stocks(self, tickers: List[str]) -> str:
        """
        Compare multiple stocks.

        Args:
            tickers: List of stock ticker symbols

        Returns:
            Comparison text
        """
        comparison = "Stock Comparison:\n\n"

        for ticker in tickers:
            info = self.get_stock_info(ticker)
            if 'error' not in info:
                comparison += f"{ticker} ({info['name']}):\n"
                comparison += f"  Price: ${info['current_price']}, P/E: {info['pe_ratio']}, "
                comparison += f"Market Cap: {info['market_cap']}, Sector: {info['sector']}\n\n"

        return comparison
