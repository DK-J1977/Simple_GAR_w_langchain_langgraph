"""
Predefined workflows for common equity research tasks.
"""
import logging
from typing import List, Dict, Any, Optional

from .equity_research_agent import EquityResearchAgent

logger = logging.getLogger(__name__)


class EquityResearchWorkflows:
    """Predefined workflows for equity research analysis."""

    def __init__(self, agent: EquityResearchAgent):
        """
        Initialize workflows with an agent.

        Args:
            agent: EquityResearchAgent instance
        """
        self.agent = agent

    def comprehensive_summary(self, ticker: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a comprehensive equity research summary from multiple perspectives.

        Args:
            ticker: Optional stock ticker symbol

        Returns:
            Analysis result
        """
        question = """
        Provide a comprehensive equity research summary analyzing the company from the following perspectives:

        1. Financial Performance and Valuation:
           - Revenue and earnings trends
           - Profitability metrics
           - Valuation ratios (P/E, P/S, etc.)
           - Financial health indicators

        2. Business Model and Competitive Position:
           - Core business operations
           - Revenue streams
           - Competitive advantages
           - Market position

        3. Risk Factors and Challenges:
           - Key risks facing the business
           - Industry headwinds
           - Competitive threats
           - Operational challenges

        4. Growth Opportunities and Future Outlook:
           - Growth drivers
           - New market opportunities
           - Strategic initiatives
           - Industry trends
        """

        return self.agent.run(question, ticker=ticker)

    def financial_analysis(self, ticker: Optional[str] = None) -> Dict[str, Any]:
        """
        Focus on financial performance analysis.

        Args:
            ticker: Optional stock ticker symbol

        Returns:
            Analysis result
        """
        question = """
        Analyze the company's financial performance:
        - Revenue and earnings trends over recent periods
        - Profit margins and profitability metrics
        - Cash flow analysis
        - Balance sheet strength
        - Key financial ratios and valuation metrics
        - Year-over-year and quarter-over-quarter comparisons
        """

        return self.agent.run(question, ticker=ticker)

    def competitive_analysis(self, ticker: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze competitive position and market dynamics.

        Args:
            ticker: Optional stock ticker symbol

        Returns:
            Analysis result
        """
        question = """
        Analyze the company's competitive position:
        - Core business model and value proposition
        - Key competitors and market share
        - Competitive advantages and moats
        - Industry dynamics and trends
        - Strategic positioning
        """

        return self.agent.run(question, ticker=ticker)

    def risk_assessment(self, ticker: Optional[str] = None) -> Dict[str, Any]:
        """
        Assess risks and challenges.

        Args:
            ticker: Optional stock ticker symbol

        Returns:
            Analysis result
        """
        question = """
        Identify and analyze key risks and challenges:
        - Business and operational risks
        - Financial risks
        - Market and competitive risks
        - Regulatory and legal risks
        - Macroeconomic risks
        - Mitigation strategies
        """

        return self.agent.run(question, ticker=ticker)

    def growth_analysis(self, ticker: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze growth opportunities and outlook.

        Args:
            ticker: Optional stock ticker symbol

        Returns:
            Analysis result
        """
        question = """
        Analyze growth opportunities and future outlook:
        - Key growth drivers
        - Addressable market opportunities
        - Product and service pipeline
        - Strategic initiatives and investments
        - Industry tailwinds
        - Long-term growth prospects
        """

        return self.agent.run(question, ticker=ticker)

    def sector_analysis(self, sector: str, ticker: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze the company within its sector context.

        Args:
            sector: Sector name
            ticker: Optional stock ticker symbol

        Returns:
            Analysis result
        """
        question = f"""
        Analyze the company within the {sector} sector:
        - Sector trends and dynamics
        - Company position within the sector
        - Sector-specific metrics and comparisons
        - Industry tailwinds and headwinds
        - Regulatory environment
        - Competitive landscape within the sector
        """

        return self.agent.run(question, ticker=ticker)

    def q_and_a_session(
        self,
        questions: List[str],
        ticker: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Conduct a Q&A session with multiple questions.

        Args:
            questions: List of questions to ask
            ticker: Optional stock ticker symbol

        Returns:
            List of analysis results
        """
        return self.agent.run_conversation(questions, ticker=ticker)

    def investment_thesis(self, ticker: Optional[str] = None) -> Dict[str, Any]:
        """
        Develop an investment thesis.

        Args:
            ticker: Optional stock ticker symbol

        Returns:
            Analysis result
        """
        question = """
        Develop a comprehensive investment thesis:
        - Executive summary of the investment opportunity
        - Key strengths and competitive advantages
        - Financial highlights and valuation
        - Growth catalysts
        - Key risks and mitigants
        - Recommendation rationale
        """

        return self.agent.run(question, ticker=ticker)
