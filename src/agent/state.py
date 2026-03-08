"""
Agent state definitions for LangGraph.
"""
from typing import TypedDict, List, Dict, Any, Optional, Annotated
from operator import add


class AgentState(TypedDict):
    """State for the equity research agent."""

    # Input
    question: str
    ticker: Optional[str]

    # Context and retrieval
    rag_context: Optional[str]
    financial_data: Optional[Dict[str, Any]]
    web_search_results: Optional[str]

    # Analysis and output
    analysis_type: Optional[str]  # 'summary', 'question', 'comparison'
    perspectives: List[str]  # Different analytical perspectives
    current_perspective: Optional[str]

    # Response generation
    intermediate_steps: Annotated[List[Dict[str, Any]], add]
    final_answer: Optional[str]

    # Conversation history for recursive Q&A
    conversation_history: Annotated[List[Dict[str, str]], add]

    # Control flow
    next_action: Optional[str]  # 'rag', 'finance', 'web_search', 'analyze', 'respond'
    iteration_count: int
    max_iterations: int
    finance_data_fetched: bool  # Track if Yahoo Finance data has been added to RAG
