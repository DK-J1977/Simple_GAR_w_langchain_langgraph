# Usage Guide

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/DK-J1977/Simple_GAR_w_langchain_langgraph.git
cd Simple_GAR_w_langchain_langgraph

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 2. Choose Your Interface

#### Option A: Jupyter Notebooks (Recommended)

Start Jupyter and open the main notebook:
```bash
jupyter notebook equity_research_agent.ipynb
```

Or explore examples:
```bash
jupyter notebook examples.ipynb
```

**Benefits:**
- Interactive, cell-by-cell execution
- Visual feedback and results
- Easy to modify and experiment
- Perfect for exploratory analysis
- No command-line arguments needed

#### Option B: Command Line Interface

Run the CLI scripts directly:
```bash
# Basic usage
python main.py --pdf "Salesforce, Inc. files (10-K) Basic annual filing, for period end 31-Jan-26 (CRM-US).pdf" --ticker CRM

# Interactive mode
python main.py --pdf path/to/pdf --ticker CRM --interactive

# Examples
python examples.py
```

**Benefits:**
- Scriptable and automatable
- Quick one-off analyses
- Can be integrated into larger workflows

## Command Line Options

### Required Options

- `--pdf PATH`: Path to PDF file or directory containing PDFs

### Optional Options

- `--ticker SYMBOL`: Stock ticker symbol (e.g., CRM, AAPL, MSFT) - When provided, Yahoo Finance data is automatically fetched and added to the RAG system
- `--question "QUESTION"`: Custom question to ask the agent
- `--interactive`: Start interactive Q&A session
- `--use-existing`: Use existing vector store (skip PDF processing)
- `--log-level LEVEL`: Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

## Usage Examples

## Jupyter Notebook Usage

### Main Notebook (equity_research_agent.ipynb)

The main notebook provides a complete interactive interface:

1. **Setup Cell**: Import dependencies and load environment
2. **Configuration Cell**: Set PDF path, ticker, and options
3. **RAG Initialization**: Process PDFs and create vector store
4. **Agent Initialization**: Create the equity research agent
5. **Analysis Options**:
   - Single question analysis
   - Custom questions
   - Interactive Q&A sessions
   - Manual interactive mode

**Example Workflow:**
```python
# Cell 1: Setup
import os
from dotenv import load_dotenv
from src.agent.equity_research_agent import EquityResearchAgent
# ... (imports)

# Cell 2: Configuration
PDF_PATH = "path/to/10k.pdf"
TICKER = "CRM"
USE_EXISTING_VECTOR_STORE = False

# Cell 3: Initialize RAG
vector_store_manager = initialize_rag_system(PDF_PATH, USE_EXISTING_VECTOR_STORE)

# Cell 4: Initialize Agent
agent = EquityResearchAgent(vector_store_manager)

# Cell 5: Ask Questions
result = agent.run("What are the key revenue drivers?", ticker=TICKER)
print(result['answer'])
```

### Examples Notebook (examples.ipynb)

Contains 7 comprehensive examples:

**Example 1: Basic Usage**
- Process PDF
- Create vector store
- Ask single question

**Example 2: Comprehensive Analysis**
- Use predefined workflows
- Comprehensive summary
- Financial analysis

**Example 3: Interactive Q&A**
- Multiple related questions
- Context-aware responses

**Example 4: Specific Analyses**
- Risk assessment
- Growth analysis
- Investment thesis

**Example 5: Yahoo Finance Tool**
- Independent tool usage
- Stock information
- Key metrics

**Example 6: Web Search Tool**
- Company news search
- Industry trends

**Example 7: Yahoo Finance RAG Integration**
- Create financial documents
- Add to vector store
- Demonstrate persistence

### Benefits of Notebooks

1. **Iterative Development**: Test and refine queries easily
2. **Visual Results**: See outputs inline with code
3. **Experimentation**: Modify parameters and retry without reprocessing
4. **Documentation**: Markdown cells explain each step
5. **Persistence**: Vector store cached between runs
6. **Debugging**: Inspect intermediate results and state

## Command Line Usage Examples

### Example 1: Single Question Analysis

```bash
python main.py \
  --pdf "Salesforce, Inc. files (10-K) Basic annual filing, for period end 31-Jan-26 (CRM-US).pdf" \
  --ticker CRM \
  --question "What are the key revenue drivers for Salesforce?"
```

### Example 2: Interactive Mode

```bash
python main.py \
  --pdf "Salesforce, Inc. files (10-K) Basic annual filing, for period end 31-Jan-26 (CRM-US).pdf" \
  --ticker CRM \
  --interactive
```

In interactive mode, you can ask multiple follow-up questions:
```
Your question: What were the total revenues last year?
[Agent provides answer with data from 10-K and Yahoo Finance RAG data]

Your question: How does this compare to competitors?
[Agent provides competitive analysis, retrieving financial metrics from RAG]

Your question: What are the main risks?
[Agent analyzes risks from 10-K filing]

Your question: What is the current stock price and P/E ratio?
[Agent retrieves this from Yahoo Finance data stored in RAG]
```

**Note**: When you provide a ticker symbol with `--ticker`, Yahoo Finance data is automatically fetched on the first query and added to the RAG vector store. This data persists for all subsequent questions in the session, allowing the agent to retrieve specific financial metrics just like it retrieves information from PDF documents.

### Example 3: Use Existing Vector Store

After first run, you can skip PDF reprocessing:

```bash
python main.py \
  --use-existing \
  --ticker CRM \
  --question "Analyze the competitive landscape"
```

### Example 4: Process Multiple PDFs

```bash
# Put all PDFs in a directory
mkdir financial_docs
mv *.pdf financial_docs/

# Process entire directory
python main.py \
  --pdf financial_docs \
  --ticker CRM \
  --interactive
```

## Python API Examples

### Example 1: Basic API Usage

```python
from dotenv import load_dotenv
from src.rag.pdf_processor import PDFProcessor
from src.rag.vector_store import VectorStoreManager
from src.agent.equity_research_agent import EquityResearchAgent

load_dotenv()

# Setup RAG
pdf_processor = PDFProcessor()
pdf_data = pdf_processor.process_pdf("path/to/10k.pdf")

vector_store = VectorStoreManager()
docs = vector_store.create_documents_from_pdf_data(pdf_data)
vector_store.create_vector_store_chroma(docs)

# Create agent and ask question
agent = EquityResearchAgent(vector_store)
result = agent.run(
    question="What are the company's main revenue streams?",
    ticker="CRM"
)
print(result['answer'])
```

### Example 2: Using Predefined Workflows

```python
from src.agent.workflows import EquityResearchWorkflows

# Create workflows
workflows = EquityResearchWorkflows(agent)

# Comprehensive analysis
summary = workflows.comprehensive_summary(ticker="CRM")
print(summary['answer'])

# Financial focus
financial = workflows.financial_analysis(ticker="CRM")
print(financial['answer'])

# Risk analysis
risks = workflows.risk_assessment(ticker="CRM")
print(risks['answer'])

# Growth analysis
growth = workflows.growth_analysis(ticker="CRM")
print(growth['answer'])

# Investment thesis
thesis = workflows.investment_thesis(ticker="CRM")
print(thesis['answer'])
```

### Example 3: Multi-Question Session

```python
questions = [
    "What were the total revenues in fiscal year 2025?",
    "What is the year-over-year growth rate?",
    "What are the main drivers of revenue growth?",
    "What are the biggest risks to future growth?"
]

responses = workflows.q_and_a_session(questions, ticker="CRM")

for response in responses:
    print(f"\nQ: {response['question']}")
    print(f"A: {response['answer']}\n")
```

### Example 4: Using Individual Tools

```python
from src.tools.yahoo_finance import YahooFinanceTool
from src.tools.web_search import WebSearchTool

# Yahoo Finance
yf = YahooFinanceTool()
stock_info = yf.get_stock_info("CRM")
print(f"Current Price: ${stock_info['current_price']}")
print(f"P/E Ratio: {stock_info['pe_ratio']}")

# Get financial statements
financials = yf.get_financial_statements("CRM")

# Historical data
hist = yf.get_historical_data("CRM", period="1y")

# Web Search
search = WebSearchTool()
news = search.search_company_news("Salesforce", "CRM")
print(news)
```

## Advanced Features

### Custom Analysis Perspectives

You can modify the agent to analyze from custom perspectives:

```python
# Modify in src/agent/equity_research_agent.py
perspectives = [
    "ESG and Sustainability",
    "Technology and Innovation",
    "M&A and Strategic Initiatives",
    "International Expansion"
]
```

### Custom LLM Settings

```python
agent = EquityResearchAgent(
    vector_store_manager,
    model_name="gpt-4-turbo-preview",  # or "gpt-3.5-turbo"
    temperature=0.1  # Lower = more focused, Higher = more creative
)
```

### Custom Vector Store Settings

```python
vector_store = VectorStoreManager(
    embedding_model="text-embedding-3-small",  # or "text-embedding-3-large"
    chunk_size=1000,  # Smaller = more precise, Larger = more context
    chunk_overlap=200
)
```

## Analysis Types

### 1. Comprehensive Summary
Analyzes from four key perspectives:
- Financial Performance and Valuation
- Business Model and Competitive Position
- Risk Factors and Challenges
- Growth Opportunities and Future Outlook

### 2. Financial Analysis
- Revenue and earnings trends
- Profitability metrics
- Cash flow analysis
- Valuation ratios

### 3. Competitive Analysis
- Market position
- Competitive advantages
- Industry dynamics
- Strategic positioning

### 4. Risk Assessment
- Business and operational risks
- Financial risks
- Market risks
- Regulatory risks

### 5. Growth Analysis
- Growth drivers
- Market opportunities
- Strategic initiatives
- Industry trends

### 6. Investment Thesis
- Executive summary
- Key strengths
- Valuation highlights
- Growth catalysts
- Risk factors

## Data Sources

The agent combines information from three sources:

1. **Company Documents (RAG)**
   - SEC filings (10-K, 10-Q)
   - Annual reports
   - Investor presentations
   - Any PDF documents you provide

2. **Financial Data (Yahoo Finance) - Integrated into RAG**
   - Real-time stock prices
   - Financial statements
   - Key metrics and ratios
   - Analyst recommendations
   - Historical price data
   - **Automatically added to RAG vector store when ticker is provided**
   - **Persists across queries for retrieval alongside PDF documents**

3. **Web Search (DuckDuckGo)**
   - Recent news articles
   - Industry analysis
   - Market updates
   - Competitive intelligence

## How Yahoo Finance RAG Integration Works

When you provide a ticker symbol (e.g., `--ticker CRM`):

1. **First Query**: The agent fetches comprehensive financial data from Yahoo Finance and converts it into document format with metadata (source, ticker, content type, timestamp)
2. **RAG Integration**: These documents are added to the vector store alongside your PDF documents
3. **Subsequent Queries**: The agent can retrieve Yahoo Finance data through the RAG system, just like it retrieves information from PDFs
4. **Benefits**:
   - Financial data is searchable and retrievable based on semantic similarity
   - The agent can cite specific financial metrics with source attribution
   - Data persists throughout the conversation session
   - Reduces redundant API calls to Yahoo Finance

## Tips for Best Results

1. **Provide Complete Documents**: Include full 10-K filings for comprehensive analysis
2. **Use Correct Tickers**: Ensure ticker symbols match the documents
3. **Ask Specific Questions**: More specific questions get better answers
4. **Leverage Interactive Mode**: Follow-up questions can clarify and expand on initial answers
5. **Review Source Documents**: The agent cites sources - review them for verification

## Troubleshooting

### Issue: "OPENAI_API_KEY not found"
**Solution**: Create a `.env` file with `OPENAI_API_KEY=your_key_here`

### Issue: PDF processing fails
**Solution**:
- Ensure PDF is not password-protected
- Try installing additional dependencies: `pip install camelot-py[cv]`

### Issue: "Vector store not found"
**Solution**: Remove `--use-existing` flag to create new vector store

### Issue: Yahoo Finance data unavailable
**Solution**:
- Check ticker symbol is correct
- Verify internet connection
- Yahoo Finance may have rate limits

### Issue: Out of memory
**Solution**:
- Reduce `chunk_size` in VectorStoreManager
- Process PDFs one at a time
- Use FAISS instead of ChromaDB for large documents

## Performance Optimization

### For Large PDFs
```python
vector_store = VectorStoreManager(
    chunk_size=500,  # Smaller chunks
    chunk_overlap=50
)
```

### For Multiple PDFs
Process incrementally:
```python
for pdf_file in pdf_files:
    pdf_data = pdf_processor.process_pdf(pdf_file)
    docs = vector_store.create_documents_from_pdf_data(pdf_data)
    # Add to existing vector store
    vector_store.vector_store.add_documents(docs)
```

### For Faster Responses
```python
agent = EquityResearchAgent(
    vector_store_manager,
    model_name="gpt-3.5-turbo",  # Faster, cheaper
    temperature=0.0
)
```

## Example Output

### Comprehensive Summary Output

```
================================================================================
EQUITY RESEARCH ANALYSIS
================================================================================

Question: Provide a comprehensive equity research summary

Ticker: CRM

COMPREHENSIVE EQUITY RESEARCH ANALYSIS: SALESFORCE, INC.

1. FINANCIAL PERFORMANCE AND VALUATION

Revenue Performance:
- FY2025 revenue reached $35.5 billion, representing 11% YoY growth
- Subscription revenue comprises 94% of total revenue
- Strong recurring revenue model with high renewal rates

Profitability Metrics:
- Operating margin: 18.5%
- Net income: $4.1 billion
- Free cash flow: $10.2 billion

Valuation:
- Current P/E ratio: 42.5x
- Forward P/E: 28.3x
- EV/Revenue: 5.2x

2. BUSINESS MODEL AND COMPETITIVE POSITION

[Detailed analysis continues...]

3. RISK FACTORS AND CHALLENGES

[Detailed risk analysis...]

4. GROWTH OPPORTUNITIES AND FUTURE OUTLOOK

[Detailed growth analysis...]
```

## Support

For issues or questions:
- Check the [README.md](README.md)
- Review the [examples.py](examples.py) file
- Open an issue on GitHub
