"""
Example script demonstrating the Equity Research AI Agent API usage.
"""
import os
from dotenv import load_dotenv

from src.rag.pdf_processor import PDFProcessor
from src.rag.vector_store import VectorStoreManager
from src.agent.equity_research_agent import EquityResearchAgent
from src.agent.workflows import EquityResearchWorkflows
from src.utils.logging_config import setup_logging


def example_basic_usage():
    """Example: Basic usage with a single question."""
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Usage")
    print("="*80)

    # Initialize RAG system
    pdf_processor = PDFProcessor()
    pdf_data = pdf_processor.process_pdf("Salesforce, Inc. files (10-K) Basic annual filing, for period end 31-Jan-26 (CRM-US).pdf")

    vector_store_manager = VectorStoreManager()
    documents = vector_store_manager.create_documents_from_pdf_data(pdf_data)
    vector_store_manager.create_vector_store_chroma(documents, persist_directory="./chroma_db")

    # Initialize agent
    agent = EquityResearchAgent(vector_store_manager)

    # Ask a question
    result = agent.run(
        question="What are Salesforce's main business segments and revenue streams?",
        ticker="CRM"
    )

    print(f"\nQuestion: {result['question']}")
    print(f"\nAnswer:\n{result['answer']}")


def example_comprehensive_analysis():
    """Example: Comprehensive analysis using workflows."""
    print("\n" + "="*80)
    print("EXAMPLE 2: Comprehensive Analysis with Workflows")
    print("="*80)

    # Load existing vector store
    vector_store_manager = VectorStoreManager()
    vector_store_manager.load_vector_store_chroma("./chroma_db")

    # Initialize agent and workflows
    agent = EquityResearchAgent(vector_store_manager)
    workflows = EquityResearchWorkflows(agent)

    # Run comprehensive summary
    print("\n--- Comprehensive Summary ---")
    summary = workflows.comprehensive_summary(ticker="CRM")
    print(summary['answer'][:500] + "...\n")

    # Run financial analysis
    print("\n--- Financial Analysis ---")
    financial = workflows.financial_analysis(ticker="CRM")
    print(financial['answer'][:500] + "...\n")


def example_interactive_qa():
    """Example: Interactive Q&A session."""
    print("\n" + "="*80)
    print("EXAMPLE 3: Interactive Q&A Session")
    print("="*80)

    # Load existing vector store
    vector_store_manager = VectorStoreManager()
    vector_store_manager.load_vector_store_chroma("./chroma_db")

    # Initialize agent and workflows
    agent = EquityResearchAgent(vector_store_manager)
    workflows = EquityResearchWorkflows(agent)

    # Ask multiple related questions
    questions = [
        "What were Salesforce's total revenues in the most recent fiscal year?",
        "How does this compare to the previous year?",
        "What are the key drivers of revenue growth?"
    ]

    responses = workflows.q_and_a_session(questions, ticker="CRM")

    for i, response in enumerate(responses, 1):
        print(f"\nQuestion {i}: {response['question']}")
        print(f"Answer: {response['answer'][:300]}...\n")
        print("-" * 80)


def example_specific_analyses():
    """Example: Run specific analysis types."""
    print("\n" + "="*80)
    print("EXAMPLE 4: Specific Analysis Types")
    print("="*80)

    # Load existing vector store
    vector_store_manager = VectorStoreManager()
    vector_store_manager.load_vector_store_chroma("./chroma_db")

    # Initialize agent and workflows
    agent = EquityResearchAgent(vector_store_manager)
    workflows = EquityResearchWorkflows(agent)

    # Risk assessment
    print("\n--- Risk Assessment ---")
    risks = workflows.risk_assessment(ticker="CRM")
    print(risks['answer'][:500] + "...\n")

    # Growth analysis
    print("\n--- Growth Analysis ---")
    growth = workflows.growth_analysis(ticker="CRM")
    print(growth['answer'][:500] + "...\n")

    # Investment thesis
    print("\n--- Investment Thesis ---")
    thesis = workflows.investment_thesis(ticker="CRM")
    print(thesis['answer'][:500] + "...\n")


def example_yahoo_finance_only():
    """Example: Using Yahoo Finance tool independently."""
    print("\n" + "="*80)
    print("EXAMPLE 5: Yahoo Finance Tool (Independent Usage)")
    print("="*80)

    from src.tools.yahoo_finance import YahooFinanceTool

    yf_tool = YahooFinanceTool()

    # Get stock info
    print("\n--- Stock Information ---")
    info = yf_tool.get_stock_info("CRM")
    print(f"Company: {info['name']}")
    print(f"Sector: {info['sector']}")
    print(f"Current Price: ${info['current_price']}")
    print(f"Market Cap: ${info['market_cap']:,}" if isinstance(info['market_cap'], (int, float)) else f"Market Cap: {info['market_cap']}")
    print(f"P/E Ratio: {info['pe_ratio']}")

    # Get key metrics summary
    print("\n--- Key Metrics Summary ---")
    summary = yf_tool.get_key_metrics_summary("CRM")
    print(summary[:500] + "...")


def example_web_search_only():
    """Example: Using web search tool independently."""
    print("\n" + "="*80)
    print("EXAMPLE 6: Web Search Tool (Independent Usage)")
    print("="*80)

    from src.tools.web_search import WebSearchTool

    search_tool = WebSearchTool(max_results=3)

    # Search for company news
    print("\n--- Company News Search ---")
    news = search_tool.search_company_news("Salesforce", "CRM")
    print(news[:500] + "...")


def main():
    """Run all examples."""
    # Setup
    load_dotenv()
    setup_logging(level="INFO")

    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please set it in a .env file or export it as an environment variable.")
        return

    # Run examples
    print("\n" + "="*80)
    print("EQUITY RESEARCH AI AGENT - EXAMPLES")
    print("="*80)

    try:
        # Example 1: Basic usage (processes PDF and creates vector store)
        # Uncomment to run:
        # example_basic_usage()

        # Example 2-4: Using existing vector store
        # Make sure to run Example 1 first, or use --use-existing with main.py
        # example_comprehensive_analysis()
        # example_interactive_qa()
        # example_specific_analyses()

        # Example 5-6: Independent tool usage (no vector store needed)
        example_yahoo_finance_only()
        example_web_search_only()

        print("\n" + "="*80)
        print("Examples completed!")
        print("="*80)

    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
