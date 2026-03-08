# Equity Research AI Agent with LangChain and LangGraph

A sophisticated AI agent for equity research analysis that combines RAG (Retrieval Augmented Generation), Yahoo Finance data, and web search to provide comprehensive investment analysis from multiple perspectives.

## Features

- **RAG System**: Process PDF documents (10-K filings, annual reports) with support for text and tables
- **Yahoo Finance RAG Integration**: Automatically fetches financial data and adds it to the RAG vector store when a ticker symbol is provided, making it accessible for all subsequent queries
- **Financial Data Integration**: Fetch real-time stock data, financial metrics, and analyst recommendations from Yahoo Finance
- **Web Search**: Access current news and market information via DuckDuckGo search
- **Multi-Perspective Analysis**: Analyze companies from four key perspectives:
  1. Financial Performance and Valuation
  2. Business Model and Competitive Position
  3. Risk Factors and Challenges
  4. Growth Opportunities and Future Outlook
- **Interactive Q&A**: Ask follow-up questions recursively using knowledge from RAG and external sources, with Yahoo Finance data persisting in the vector store
- **LangGraph Workflow**: Orchestrated agent workflow with intelligent routing and tool selection

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Equity Research Agent                    │
│                      (LangGraph Workflow)                    │
└──────────────┬──────────────┬──────────────┬────────────────┘
               │              │              │
               ▼              ▼              ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │   RAG    │   │  Yahoo   │   │   Web    │
        │  System  │   │ Finance  │   │  Search  │
        └──────────┘   └──────────┘   └──────────┘
               │
               ▼
        ┌──────────┐
        │   PDF    │
        │Processor │
        │(text &   │
        │ tables)  │
        └──────────┘
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/DK-J1977/Simple_GAR_w_langchain_langgraph.git
cd Simple_GAR_w_langchain_langgraph
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Usage

### Option 1: Jupyter Notebooks (Recommended)

The easiest way to use the Equity Research Agent is through Jupyter notebooks:

#### Main Notebook
```bash
jupyter notebook equity_research_agent.ipynb
```

Features:
- Interactive interface with clear section-by-section execution
- Single question analysis
- Custom questions
- Interactive Q&A sessions
- Configuration management

#### Examples Notebook
```bash
jupyter notebook examples.ipynb
```

Contains 7 example use cases:
1. Basic usage with single question
2. Comprehensive analysis with workflows
3. Interactive Q&A session
4. Specific analyses (risk, growth, investment thesis)
5. Yahoo Finance tool (independent usage)
6. Web search tool (independent usage)
7. Yahoo Finance RAG integration

### Option 2: Command Line Interface

You can also use the CLI scripts directly:

#### Basic Usage

Process a PDF and run analysis with a default question:
```bash
python main.py --pdf "Salesforce, Inc. files (10-K) Basic annual filing, for period end 31-Jan-26 (CRM-US).pdf" --ticker CRM
```

#### Custom Question

Ask a specific question:
```bash
python main.py --pdf path/to/pdf --ticker CRM --question "What are the key revenue drivers for this company?"
```

#### Interactive Mode

Start an interactive Q&A session:
```bash
python main.py --pdf path/to/pdf --ticker CRM --interactive
```

#### Use Existing Vector Store

Skip PDF reprocessing and use existing vector store:
```bash
python main.py --use-existing --ticker CRM --interactive
```

## Python API Usage

```python
import os
from dotenv import load_dotenv

from src.rag.pdf_processor import PDFProcessor
from src.rag.vector_store import VectorStoreManager
from src.agent.equity_research_agent import EquityResearchAgent
from src.agent.workflows import EquityResearchWorkflows

# Load environment variables
load_dotenv()

# Initialize RAG system
pdf_processor = PDFProcessor()
pdf_data = pdf_processor.process_pdf("path/to/10k.pdf")

vector_store_manager = VectorStoreManager()
documents = vector_store_manager.create_documents_from_pdf_data(pdf_data)
vector_store_manager.create_vector_store_chroma(documents)

# Initialize agent
agent = EquityResearchAgent(vector_store_manager)

# Run analysis
result = agent.run(
    question="Provide a comprehensive equity research summary",
    ticker="CRM"
)
print(result['answer'])

# Use predefined workflows
workflows = EquityResearchWorkflows(agent)

# Comprehensive summary
summary = workflows.comprehensive_summary(ticker="CRM")
print(summary['answer'])

# Financial analysis
financial = workflows.financial_analysis(ticker="CRM")
print(financial['answer'])

# Interactive Q&A
questions = [
    "What are the main revenue streams?",
    "What are the biggest risks?",
    "What are the growth opportunities?"
]
responses = workflows.q_and_a_session(questions, ticker="CRM")
for response in responses:
    print(f"Q: {response['question']}")
    print(f"A: {response['answer']}\n")
```

## Project Structure

```
Simple_GAR_w_langchain_langgraph/
├── equity_research_agent.ipynb  # Main Jupyter notebook interface
├── examples.ipynb               # Examples and demonstrations notebook
├── main.py                      # CLI entry point
├── examples.py                  # CLI examples script
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── README.md                    # This file
├── USAGE.md                     # Detailed usage guide
│
├── src/
│   ├── rag/                     # RAG system
│   │   ├── __init__.py
│   │   ├── pdf_processor.py    # PDF text & table extraction
│   │   └── vector_store.py     # Vector store management
│   │
│   ├── tools/                   # Agent tools
│   │   ├── __init__.py
│   │   ├── yahoo_finance.py    # Yahoo Finance integration
│   │   └── web_search.py       # Web search tool
│   │
│   ├── agent/                   # LangGraph agent
│   │   ├── __init__.py
│   │   ├── state.py            # Agent state definitions
│   │   ├── equity_research_agent.py  # Main agent logic
│   │   └── workflows.py        # Predefined workflows
│   │
│   └── utils/                   # Utilities
│       ├── __init__.py
│       └── logging_config.py   # Logging setup
│
└── chroma_db/                   # Vector store (generated)
```

## Components

### RAG System

**PDF Processor** (`src/rag/pdf_processor.py`):
- Extracts text from PDF documents using PyPDF and pdfplumber
- Extracts tables from PDFs with structure preservation
- Processes individual files or entire directories

**Vector Store Manager** (`src/rag/vector_store.py`):
- Creates and manages ChromaDB/FAISS vector stores
- Chunks documents intelligently with overlap
- Provides similarity search and retrieval capabilities

### Tools

**Yahoo Finance Tool** (`src/tools/yahoo_finance.py`):
- Fetches real-time stock information
- Retrieves financial statements (income, balance sheet, cash flow)
- Gets historical price data
- Accesses analyst recommendations

**Web Search Tool** (`src/tools/web_search.py`):
- Performs web searches via DuckDuckGo
- Searches for company news
- Retrieves industry trends

### Agent

**Equity Research Agent** (`src/agent/equity_research_agent.py`):
- LangGraph-based workflow orchestration
- Intelligent routing between tools
- Multi-step reasoning and analysis
- Conversation history management
- Automatic integration of Yahoo Finance data into RAG vector store

**Workflows** (`src/agent/workflows.py`):
- Predefined analysis templates
- Comprehensive summary
- Financial analysis
- Competitive analysis
- Risk assessment
- Growth analysis
- Investment thesis

## Example Analyses

### 1. Comprehensive Summary
Analyzes the company from four perspectives: financial performance, business model, risks, and growth opportunities.

### 2. Financial Analysis
Deep dive into revenue trends, profitability, cash flow, and valuation metrics.

### 3. Competitive Analysis
Evaluates market position, competitive advantages, and industry dynamics.

### 4. Risk Assessment
Identifies and analyzes business, financial, market, and regulatory risks.

### 5. Growth Analysis
Examines growth drivers, market opportunities, and future outlook.

## Requirements

- Python 3.8+
- OpenAI API key
- Internet connection (for Yahoo Finance and web search)

## Key Dependencies

- langchain & langgraph: LLM framework and workflow orchestration
- langchain-openai: OpenAI integration
- chromadb: Vector database
- pypdf & pdfplumber: PDF processing
- yfinance: Yahoo Finance data
- duckduckgo-search: Web search

## Environment Variables

Create a `.env` file with:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Advanced Features

### Yahoo Finance Data in RAG System
When you provide a ticker symbol (e.g., `--ticker CRM`), the agent automatically:
1. Fetches comprehensive financial data from Yahoo Finance
2. Converts it into document format with metadata
3. Adds it to the RAG vector store alongside PDF documents
4. Makes it available for retrieval in all subsequent queries

This means Yahoo Finance data is treated as another source of truth in the RAG system, allowing the agent to retrieve and cite specific financial metrics, historical data, and analyst recommendations just like it would retrieve information from PDF documents.

### Recursive Q&A
The agent maintains conversation history and can answer follow-up questions that reference previous context. Yahoo Finance data persists in the vector store across multiple questions in the same session.

### Multi-Source Analysis
Each analysis combines information from:
1. Company documents (SEC filings, PDFs)
2. Real-time financial data from Yahoo Finance (added to RAG)
3. Recent news and web sources

### Customizable Workflows
Create custom analysis workflows by extending the `EquityResearchWorkflows` class.

## Troubleshooting

**Issue**: OpenAI API key error
- **Solution**: Ensure `OPENAI_API_KEY` is set in `.env` file

**Issue**: PDF processing fails
- **Solution**: Check PDF is not password-protected and is readable

**Issue**: Yahoo Finance data unavailable
- **Solution**: Verify ticker symbol is correct and check internet connection

**Issue**: Vector store not found
- **Solution**: Run without `--use-existing` flag to create new vector store

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## License

MIT License

## Acknowledgments

- Built with LangChain and LangGraph
- Financial data from Yahoo Finance
- PDF processing with PyPDF and pdfplumber
