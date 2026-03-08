"""
LangGraph agent for equity research analysis.
"""
import logging
from typing import Dict, Any, Optional

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END

from .state import AgentState
from ..rag.vector_store import VectorStoreManager
from ..tools.yahoo_finance import YahooFinanceTool
from ..tools.web_search import WebSearchTool

logger = logging.getLogger(__name__)


class EquityResearchAgent:
    """AI agent for equity research analysis using LangGraph."""

    def __init__(
        self,
        vector_store_manager: VectorStoreManager,
        model_name: str = "gpt-4-turbo-preview",
        temperature: float = 0.1
    ):
        """
        Initialize the equity research agent.

        Args:
            vector_store_manager: Vector store manager for RAG
            model_name: LLM model to use
            temperature: Temperature for generation
        """
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        self.vector_store_manager = vector_store_manager
        self.yahoo_finance = YahooFinanceTool()
        self.web_search = WebSearchTool()

        # Build the graph
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        workflow = StateGraph(AgentState)

        # Add nodes
        workflow.add_node("route", self._route_node)
        workflow.add_node("retrieve_rag", self._retrieve_rag_node)
        workflow.add_node("fetch_financial", self._fetch_financial_node)
        workflow.add_node("search_web", self._search_web_node)
        workflow.add_node("analyze", self._analyze_node)
        workflow.add_node("respond", self._respond_node)

        # Set entry point
        workflow.set_entry_point("route")

        # Add edges based on routing decisions
        workflow.add_conditional_edges(
            "route",
            self._route_decision,
            {
                "rag": "retrieve_rag",
                "finance": "fetch_financial",
                "web_search": "search_web",
                "analyze": "analyze",
                "respond": "respond",
                "end": END
            }
        )

        # Connect nodes back to router for iterative processing
        workflow.add_edge("retrieve_rag", "route")
        workflow.add_edge("fetch_financial", "route")
        workflow.add_edge("search_web", "route")
        workflow.add_edge("analyze", "respond")
        workflow.add_edge("respond", END)

        return workflow.compile()

    def _route_node(self, state: AgentState) -> AgentState:
        """Route to the appropriate next action."""
        # Increment iteration count
        state["iteration_count"] = state.get("iteration_count", 0) + 1

        # Check max iterations
        if state["iteration_count"] >= state.get("max_iterations", 5):
            state["next_action"] = "analyze"
            return state

        # Determine what information we still need
        has_rag = state.get("rag_context") is not None
        has_finance = state.get("financial_data") is not None
        has_web = state.get("web_search_results") is not None

        # Priority: RAG -> Financial Data -> Web Search -> Analyze
        if not has_rag:
            state["next_action"] = "rag"
        elif state.get("ticker") and not has_finance:
            state["next_action"] = "finance"
        elif not has_web:
            state["next_action"] = "web_search"
        else:
            state["next_action"] = "analyze"

        return state

    def _route_decision(self, state: AgentState) -> str:
        """Make routing decision based on state."""
        return state.get("next_action", "end")

    def _retrieve_rag_node(self, state: AgentState) -> AgentState:
        """Retrieve relevant documents from RAG system."""
        try:
            query = state["question"]
            retriever = self.vector_store_manager.as_retriever(
                search_kwargs={"k": 4}
            )
            docs = retriever.get_relevant_documents(query)

            # Format retrieved documents
            context = "\n\n".join([
                f"[Source: {doc.metadata.get('source', 'Unknown')}]\n{doc.page_content}"
                for doc in docs
            ])

            state["rag_context"] = context
            state["intermediate_steps"] = state.get("intermediate_steps", []) + [
                {"action": "rag_retrieval", "result": f"Retrieved {len(docs)} documents"}
            ]

            logger.info(f"Retrieved {len(docs)} documents from RAG system")
        except Exception as e:
            logger.error(f"Error in RAG retrieval: {e}")
            state["rag_context"] = "Error retrieving documents from RAG system."

        return state

    def _fetch_financial_node(self, state: AgentState) -> AgentState:
        """Fetch financial data from Yahoo Finance."""
        try:
            ticker = state.get("ticker")
            if not ticker:
                state["financial_data"] = None
                return state

            # Get stock info
            stock_info = self.yahoo_finance.get_stock_info(ticker)
            summary = self.yahoo_finance.get_key_metrics_summary(ticker)

            state["financial_data"] = {
                "stock_info": stock_info,
                "summary": summary
            }
            state["intermediate_steps"] = state.get("intermediate_steps", []) + [
                {"action": "financial_data_fetch", "result": f"Fetched data for {ticker}"}
            ]

            logger.info(f"Fetched financial data for {ticker}")
        except Exception as e:
            logger.error(f"Error fetching financial data: {e}")
            state["financial_data"] = None

        return state

    def _search_web_node(self, state: AgentState) -> AgentState:
        """Search the web for additional context."""
        try:
            query = state["question"]
            ticker = state.get("ticker")

            # Search for company news if ticker is available
            if ticker:
                company_name = state.get("financial_data", {}).get("stock_info", {}).get("name", "")
                if company_name:
                    results = self.web_search.search_company_news(company_name, ticker)
                else:
                    results = self.web_search.search(query)
            else:
                results = self.web_search.search(query)

            state["web_search_results"] = results
            state["intermediate_steps"] = state.get("intermediate_steps", []) + [
                {"action": "web_search", "result": "Completed web search"}
            ]

            logger.info("Completed web search")
        except Exception as e:
            logger.error(f"Error in web search: {e}")
            state["web_search_results"] = "Error performing web search."

        return state

    def _analyze_node(self, state: AgentState) -> AgentState:
        """Analyze gathered information from multiple perspectives."""
        try:
            question = state["question"]
            rag_context = state.get("rag_context", "No RAG context available.")
            financial_data = state.get("financial_data", {})
            web_results = state.get("web_search_results", "No web search results.")

            # Define equity research perspectives
            perspectives = [
                "Financial Performance and Valuation",
                "Business Model and Competitive Position",
                "Risk Factors and Challenges",
                "Growth Opportunities and Future Outlook"
            ]

            state["perspectives"] = perspectives

            # For now, we'll prepare the context for final response
            # In a more sophisticated implementation, we could analyze each perspective separately
            state["intermediate_steps"] = state.get("intermediate_steps", []) + [
                {"action": "analysis", "result": "Completed multi-perspective analysis"}
            ]

            logger.info("Completed analysis")
        except Exception as e:
            logger.error(f"Error in analysis: {e}")

        return state

    def _respond_node(self, state: AgentState) -> AgentState:
        """Generate final response based on analysis."""
        try:
            question = state["question"]
            rag_context = state.get("rag_context", "")
            financial_data = state.get("financial_data", {})
            web_results = state.get("web_search_results", "")
            perspectives = state.get("perspectives", [])

            # Prepare financial summary
            financial_summary = ""
            if financial_data:
                financial_summary = financial_data.get("summary", "")

            # Create prompt for response generation
            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are an expert equity research analyst. Provide comprehensive analysis from multiple perspectives:
1. Financial Performance and Valuation
2. Business Model and Competitive Position
3. Risk Factors and Challenges
4. Growth Opportunities and Future Outlook

Use the provided context to give a detailed, well-structured response."""),
                ("user", """Question: {question}

Context from Company Documents (SEC Filings, Reports):
{rag_context}

Financial Data from Yahoo Finance:
{financial_data}

Recent News and Web Search:
{web_results}

Please provide a comprehensive equity research analysis addressing the question from multiple perspectives.""")
            ])

            # Generate response
            chain = prompt | self.llm
            response = chain.invoke({
                "question": question,
                "rag_context": rag_context[:4000] if rag_context else "No document context available.",
                "financial_data": financial_summary[:2000] if financial_summary else "No financial data available.",
                "web_results": web_results[:2000] if web_results else "No web results available."
            })

            state["final_answer"] = response.content

            # Update conversation history
            state["conversation_history"] = state.get("conversation_history", []) + [
                {"role": "user", "content": question},
                {"role": "assistant", "content": response.content}
            ]

            logger.info("Generated final response")
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            state["final_answer"] = f"Error generating response: {str(e)}"

        return state

    def run(
        self,
        question: str,
        ticker: Optional[str] = None,
        max_iterations: int = 5
    ) -> Dict[str, Any]:
        """
        Run the agent with a question.

        Args:
            question: Question to answer
            ticker: Optional stock ticker symbol
            max_iterations: Maximum iterations for the agent

        Returns:
            Dictionary containing the final answer and metadata
        """
        initial_state = AgentState(
            question=question,
            ticker=ticker,
            rag_context=None,
            financial_data=None,
            web_search_results=None,
            analysis_type="question",
            perspectives=[],
            current_perspective=None,
            intermediate_steps=[],
            final_answer=None,
            conversation_history=[],
            next_action=None,
            iteration_count=0,
            max_iterations=max_iterations
        )

        # Run the graph
        final_state = self.graph.invoke(initial_state)

        return {
            "question": question,
            "ticker": ticker,
            "answer": final_state.get("final_answer"),
            "intermediate_steps": final_state.get("intermediate_steps", []),
            "conversation_history": final_state.get("conversation_history", [])
        }

    def run_conversation(
        self,
        questions: list,
        ticker: Optional[str] = None
    ) -> list:
        """
        Run a conversation with multiple questions recursively.

        Args:
            questions: List of questions to ask
            ticker: Optional stock ticker symbol

        Returns:
            List of responses
        """
        responses = []

        for question in questions:
            result = self.run(question, ticker=ticker)
            responses.append(result)

        return responses
