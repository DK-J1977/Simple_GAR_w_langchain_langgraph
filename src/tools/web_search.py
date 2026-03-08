"""
Web search tool using DuckDuckGo for internet searches.
"""
import logging
from typing import List, Dict, Any, Optional

try:
    from duckduckgo_search import DDGS
except ImportError as e:
    logging.error(f"Required library not installed: {e}")
    raise

logger = logging.getLogger(__name__)


class WebSearchTool:
    """Tool for performing web searches."""

    def __init__(self, max_results: int = 5):
        """
        Initialize web search tool.

        Args:
            max_results: Maximum number of search results to return
        """
        self.max_results = max_results

    def search(self, query: str, max_results: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Perform a web search.

        Args:
            query: Search query
            max_results: Maximum number of results (overrides default)

        Returns:
            List of search results
        """
        results_limit = max_results if max_results is not None else self.max_results

        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=results_limit))
                return results
        except Exception as e:
            logger.error(f"Error performing web search for '{query}': {e}")
            return []

    def search_news(self, query: str, max_results: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Search for news articles.

        Args:
            query: Search query
            max_results: Maximum number of results

        Returns:
            List of news results
        """
        results_limit = max_results if max_results is not None else self.max_results

        try:
            with DDGS() as ddgs:
                results = list(ddgs.news(query, max_results=results_limit))
                return results
        except Exception as e:
            logger.error(f"Error searching news for '{query}': {e}")
            return []

    def format_search_results(self, results: List[Dict[str, Any]]) -> str:
        """
        Format search results as text.

        Args:
            results: List of search results

        Returns:
            Formatted text string
        """
        if not results:
            return "No search results found."

        formatted = "Search Results:\n\n"
        for i, result in enumerate(results, 1):
            title = result.get('title', 'N/A')
            body = result.get('body', result.get('description', 'N/A'))
            url = result.get('href', result.get('url', 'N/A'))

            formatted += f"{i}. {title}\n"
            formatted += f"   {body}\n"
            formatted += f"   URL: {url}\n\n"

        return formatted

    def search_company_news(self, company_name: str, ticker: Optional[str] = None) -> str:
        """
        Search for company-specific news.

        Args:
            company_name: Name of the company
            ticker: Optional stock ticker

        Returns:
            Formatted news results
        """
        query = f"{company_name}"
        if ticker:
            query += f" {ticker}"
        query += " stock news"

        results = self.search_news(query)
        return self.format_search_results(results)

    def search_industry_trends(self, industry: str) -> str:
        """
        Search for industry trends and news.

        Args:
            industry: Industry name

        Returns:
            Formatted search results
        """
        query = f"{industry} industry trends analysis"
        results = self.search(query)
        return self.format_search_results(results)
