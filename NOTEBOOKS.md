# Jupyter Notebooks Guide

This guide provides detailed information about using the Jupyter notebooks included in this repository.

## Overview

The repository includes two Jupyter notebooks that provide an interactive interface to the Equity Research AI Agent:

1. **`equity_research_agent.ipynb`** - Main interactive notebook for running analyses
2. **`examples.ipynb`** - Comprehensive examples demonstrating all features

## Getting Started

### Prerequisites

1. Install all dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your OpenAI API key:
```bash
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=your_api_key_here
```

3. Start Jupyter:
```bash
jupyter notebook
```

Your browser will open automatically with the Jupyter interface.

## Main Notebook: equity_research_agent.ipynb

### Structure

The notebook is organized into clear sections:

1. **Setup and Imports** - Load all required libraries
2. **Configuration** - Set your PDF path, ticker symbol, and options
3. **Initialize RAG System** - Process PDFs and create/load vector store
4. **Initialize Agent** - Create the equity research agent
5. **Run Analysis** - Multiple analysis options
6. **Manual Interactive Mode** - Alternative interactive interface
7. **View Conversation History** - Debugging and inspection
8. **Quick Reference** - Common questions and tips

### How to Use

#### Basic Workflow

1. **Run Setup Cell** (Cell 1)
   - Imports all dependencies
   - Loads environment variables
   - Sets up logging
   - Confirms successful setup

2. **Configure Parameters** (Cell 2)
   - Set `PDF_PATH` to your document
   - Set `TICKER` symbol (e.g., "CRM")
   - Set `USE_EXISTING_VECTOR_STORE = True` to skip reprocessing

3. **Initialize RAG** (Cell 3)
   - Processes PDFs (or loads existing vector store)
   - Creates document chunks
   - Builds vector database
   - Takes 30-60 seconds for new PDFs

4. **Initialize Agent** (Cell 4)
   - Quick setup of the equity research agent
   - Ready to answer questions

5. **Ask Questions** (Cells 5-8)
   - Choose from multiple analysis options
   - Run cells to get answers
   - Modify questions as needed

#### Analysis Options

**Option A: Single Question Analysis**
- Default comprehensive analysis
- Covers financial performance, business model, risks, growth

**Option B: Custom Questions**
- Ask your own specific questions
- Examples:
  - "What are the main revenue streams?"
  - "Analyze the competitive landscape"
  - "What are the key risks?"

**Option C: Interactive Q&A Session**
- Ask multiple related questions
- Context is maintained across questions
- Perfect for deep-dive analysis

**Option D: Manual Interactive Mode**
- Command-line style interaction within notebook
- Type questions and get immediate answers
- Type 'exit' or 'quit' to end session

### Tips for Best Results

1. **First Run**: Set `USE_EXISTING_VECTOR_STORE = False`
2. **Subsequent Runs**: Set `USE_EXISTING_VECTOR_STORE = True` to skip PDF processing
3. **Ask Specific Questions**: More specific questions get better answers
4. **Use Follow-ups**: Build on previous questions for deeper insights
5. **Experiment**: Modify and rerun cells as needed

### Common Use Cases

#### Use Case 1: Quick Analysis
```python
# Cell 2: Configuration
PDF_PATH = "company-10k.pdf"
TICKER = "AAPL"
USE_EXISTING_VECTOR_STORE = False

# Run cells 3-4 to initialize

# Cell 5: Get comprehensive summary
result = agent.run(
    "Provide a comprehensive equity research summary",
    ticker=TICKER
)
```

#### Use Case 2: Focused Research
```python
# Ask specific questions
questions = [
    "What were total revenues?",
    "What is the profit margin?",
    "What are the main growth drivers?"
]

for q in questions:
    result = agent.run(q, ticker=TICKER)
    print(f"Q: {q}")
    print(f"A: {result['answer']}\n")
```

#### Use Case 3: Comparative Analysis
```python
# First company
result1 = agent.run("Analyze financial performance", ticker="CRM")

# Switch ticker and ask similar question
result2 = agent.run("Analyze financial performance", ticker="MSFT")
```

## Examples Notebook: examples.ipynb

### Structure

The examples notebook contains 7 complete examples:

**Example 1: Basic Usage**
- Complete workflow from PDF to answer
- Shows fundamental operations
- Creates vector store

**Example 2: Comprehensive Analysis with Workflows**
- Uses `EquityResearchWorkflows` class
- Runs predefined analysis templates
- Comprehensive summary and financial analysis

**Example 3: Interactive Q&A Session**
- Multiple related questions
- Shows conversation context
- Using `q_and_a_session` workflow

**Example 4: Specific Analysis Types**
- Risk assessment
- Growth analysis
- Investment thesis
- Targeted, focused analyses

**Example 5: Yahoo Finance Tool**
- Independent tool usage (no agent needed)
- Stock information and metrics
- Direct financial data access

**Example 6: Web Search Tool**
- Search for company news
- Industry trends
- Recent developments

**Example 7: Yahoo Finance RAG Integration**
- Convert financial data to documents
- Add to vector store
- Demonstrate persistence and retrieval

### How to Use Examples

#### Running Examples Sequentially

1. **Run Setup Cell** - Load all dependencies

2. **Run Example 1** - Creates the initial vector store
   - This is required for Examples 2-4
   - Takes 30-60 seconds

3. **Run Examples 2-4** - Use existing vector store
   - These examples load the vector store created in Example 1
   - Much faster than Example 1

4. **Run Examples 5-7** - Independent examples
   - Don't require vector store
   - Can run in any order

#### Running Individual Examples

You can run examples independently:

**For Examples 2-4:**
- Make sure Example 1 has been run at least once, OR
- Run `main.py` once to create the vector store

**For Examples 5-7:**
- No prerequisites
- Run directly

#### Modifying Examples

Feel free to modify the examples:

```python
# Change the ticker
ticker = "AAPL"  # Instead of "CRM"

# Change the questions
questions = [
    "Your custom question 1",
    "Your custom question 2"
]

# Use different PDF
pdf_path = "your-document.pdf"
```

### Example Use Cases

#### Learning the System
- Run all examples in order
- Read the output and explanations
- Understand what each component does

#### Quick Testing
- Run Example 5 or 6 for immediate results
- No PDF processing required
- Test Yahoo Finance or web search

#### Research Workflow
- Run Example 2 for comprehensive analysis
- Follow with Example 4 for specific deep-dives
- Use Example 3 for follow-up questions

## Advanced Usage

### Customizing Analysis

Both notebooks can be customized:

1. **Custom LLM Settings**
```python
agent = EquityResearchAgent(
    vector_store_manager,
    model_name="gpt-4-turbo-preview",  # or "gpt-3.5-turbo"
    temperature=0.0  # More deterministic
)
```

2. **Custom Vector Store Settings**
```python
vector_store_manager = VectorStoreManager(
    embedding_model="text-embedding-3-large",
    chunk_size=500,  # Smaller chunks
    chunk_overlap=50
)
```

3. **Custom Analysis Perspectives**
Modify the perspectives in the agent code to analyze from different angles.

### Debugging

**View Agent State:**
```python
# After running a query
print(agent.state)
```

**Inspect Vector Store:**
```python
# See what's in the vector store
docs = vector_store_manager.similarity_search("financial performance", k=5)
for doc in docs:
    print(doc.page_content)
```

**Check Retrieved Context:**
```python
# See what the agent retrieved
print(result.get('rag_context', 'No RAG context'))
print(result.get('financial_data', 'No financial data'))
```

### Performance Tips

1. **Use Existing Vector Store**
   - Set `USE_EXISTING_VECTOR_STORE = True`
   - Saves 30-60 seconds per run

2. **Batch Questions**
   - Use `workflows.q_and_a_session()` for multiple questions
   - More efficient than individual queries

3. **Cache Financial Data**
   - Yahoo Finance data is added to RAG
   - Persists across queries in same session

4. **GPU Acceleration**
   - Use FAISS with GPU for large document sets
   - See `VectorStoreManager` options

## Troubleshooting

### "OPENAI_API_KEY not found"
**Solution:** Create `.env` file with your API key:
```bash
echo "OPENAI_API_KEY=your_key_here" > .env
```

### Notebook Kernel Dies
**Possible causes:**
- Out of memory (reduce chunk size)
- Large PDF (process in batches)
- API timeout (check internet connection)

**Solutions:**
```python
# Reduce memory usage
vector_store_manager = VectorStoreManager(chunk_size=500)

# Process PDFs one at a time
for pdf in pdf_files:
    pdf_data = pdf_processor.process_pdf(pdf)
    # Process individually
```

### "Vector store not found"
**Solution:** Run with `USE_EXISTING_VECTOR_STORE = False` to create it

### Import Errors
**Solution:** Reinstall dependencies:
```bash
pip install -r requirements.txt --upgrade
```

### Yahoo Finance Errors
**Solution:**
- Check ticker symbol is correct
- Verify internet connection
- Some tickers may not be available

## Best Practices

1. **Document Your Work**
   - Add markdown cells with notes
   - Save modified notebooks with descriptive names

2. **Version Control**
   - Clear output before committing: Cell → All Output → Clear
   - Create notebook copies for different analyses

3. **Incremental Testing**
   - Test with small PDFs first
   - Verify setup before processing large documents

4. **Resource Management**
   - Restart kernel if memory issues occur
   - Close unused notebooks

5. **Reproducibility**
   - Document configuration settings
   - Note API versions and models used
   - Save key results in markdown cells

## Next Steps

1. **Start Simple**: Begin with `equity_research_agent.ipynb`
2. **Learn by Example**: Explore `examples.ipynb`
3. **Customize**: Modify for your specific use case
4. **Experiment**: Try different questions and settings
5. **Integrate**: Incorporate into your research workflow

## Additional Resources

- **README.md** - Project overview and features
- **USAGE.md** - Comprehensive usage guide
- **main.py** - CLI reference implementation
- **examples.py** - API usage examples

## Support

For issues or questions:
- Check this guide first
- Review example notebooks
- Open an issue on GitHub
- Check the README.md troubleshooting section

---

Happy researching! 📊💡
