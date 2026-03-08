"""
Main application entry point for the Equity Research AI Agent.
"""
import os
import argparse
import logging
from pathlib import Path
from dotenv import load_dotenv

from src.rag.pdf_processor import PDFProcessor
from src.rag.vector_store import VectorStoreManager
from src.agent.equity_research_agent import EquityResearchAgent
from src.utils.logging_config import setup_logging

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


def initialize_rag_system(pdf_path: str, use_existing: bool = False) -> VectorStoreManager:
    """
    Initialize the RAG system with PDF documents.

    Args:
        pdf_path: Path to PDF file or directory
        use_existing: Whether to load existing vector store

    Returns:
        Initialized VectorStoreManager
    """
    vector_store_manager = VectorStoreManager()

    persist_dir = "./chroma_db"

    # Check if we should load existing vector store
    if use_existing and os.path.exists(persist_dir):
        logger.info("Loading existing vector store...")
        vector_store_manager.load_vector_store_chroma(persist_dir)
        return vector_store_manager

    # Process PDF(s)
    logger.info(f"Processing PDF(s) from {pdf_path}...")
    pdf_processor = PDFProcessor()

    if os.path.isfile(pdf_path):
        pdf_data = pdf_processor.process_pdf(pdf_path)
        all_pdf_data = [pdf_data]
    elif os.path.isdir(pdf_path):
        all_pdf_data = pdf_processor.process_directory(pdf_path)
    else:
        raise ValueError(f"Invalid path: {pdf_path}")

    # Create documents for vector store
    all_documents = []
    for pdf_data in all_pdf_data:
        documents = vector_store_manager.create_documents_from_pdf_data(pdf_data)
        all_documents.extend(documents)

    logger.info(f"Created {len(all_documents)} document chunks from {len(all_pdf_data)} PDF(s)")

    # Create vector store
    vector_store_manager.create_vector_store_chroma(all_documents, persist_dir)

    return vector_store_manager


def run_analysis(agent: EquityResearchAgent, question: str, ticker: str = None):
    """
    Run analysis with the agent.

    Args:
        agent: EquityResearchAgent instance
        question: Question to answer
        ticker: Optional stock ticker
    """
    logger.info(f"Running analysis for: {question}")
    if ticker:
        logger.info(f"Stock ticker: {ticker}")

    result = agent.run(question, ticker=ticker)

    print("\n" + "="*80)
    print("EQUITY RESEARCH ANALYSIS")
    print("="*80)
    print(f"\nQuestion: {result['question']}")
    if result['ticker']:
        print(f"Ticker: {result['ticker']}")
    print(f"\n{result['answer']}")
    print("\n" + "="*80)

    return result


def run_interactive_mode(agent: EquityResearchAgent, ticker: str = None):
    """
    Run the agent in interactive Q&A mode.

    Args:
        agent: EquityResearchAgent instance
        ticker: Optional stock ticker
    """
    print("\n" + "="*80)
    print("INTERACTIVE EQUITY RESEARCH AGENT")
    print("="*80)
    print("\nAsk questions about the company and financial data.")
    print("Type 'exit' or 'quit' to end the session.\n")

    while True:
        try:
            question = input("Your question: ").strip()

            if question.lower() in ['exit', 'quit', 'q']:
                print("Ending session. Goodbye!")
                break

            if not question:
                continue

            result = agent.run(question, ticker=ticker)

            print(f"\n{result['answer']}\n")
            print("-" * 80 + "\n")

        except KeyboardInterrupt:
            print("\n\nSession interrupted. Goodbye!")
            break
        except Exception as e:
            logger.error(f"Error during interactive session: {e}")
            print(f"\nError: {e}\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Equity Research AI Agent using LangChain and LangGraph"
    )

    parser.add_argument(
        "--pdf",
        type=str,
        default=".",
        help="Path to PDF file or directory containing PDFs (default: current directory)"
    )

    parser.add_argument(
        "--ticker",
        type=str,
        help="Stock ticker symbol (e.g., CRM for Salesforce)"
    )

    parser.add_argument(
        "--question",
        type=str,
        help="Question to ask the agent"
    )

    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive Q&A mode"
    )

    parser.add_argument(
        "--use-existing",
        action="store_true",
        help="Use existing vector store instead of reprocessing PDFs"
    )

    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level (default: INFO)"
    )

    args = parser.parse_args()

    # Setup logging
    setup_logging(level=args.log_level)

    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        logger.error("OPENAI_API_KEY not found in environment variables.")
        logger.error("Please set it in a .env file or export it as an environment variable.")
        return

    try:
        # Initialize RAG system
        vector_store_manager = initialize_rag_system(args.pdf, args.use_existing)

        # Initialize agent
        logger.info("Initializing equity research agent...")
        agent = EquityResearchAgent(vector_store_manager)

        # Run in appropriate mode
        if args.interactive:
            run_interactive_mode(agent, ticker=args.ticker)
        elif args.question:
            run_analysis(agent, args.question, ticker=args.ticker)
        else:
            # Default example question
            default_question = "Provide a comprehensive equity research summary analyzing the company's financial performance, business model, risks, and growth opportunities."
            run_analysis(agent, default_question, ticker=args.ticker)

    except Exception as e:
        logger.error(f"Error running application: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
