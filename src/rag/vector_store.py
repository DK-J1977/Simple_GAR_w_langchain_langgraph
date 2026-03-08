"""
Vector store module for document indexing and retrieval.
Implements RAG (Retrieval Augmented Generation) using ChromaDB and FAISS.
"""
import os
from typing import List, Dict, Any, Optional
import logging

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma, FAISS
from langchain.schema import Document

logger = logging.getLogger(__name__)


class VectorStoreManager:
    """Manage vector store for document retrieval."""

    def __init__(
        self,
        embedding_model: str = "text-embedding-3-small",
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        collection_name: str = "financial_docs"
    ):
        """
        Initialize vector store manager.

        Args:
            embedding_model: OpenAI embedding model to use
            chunk_size: Size of text chunks for splitting
            chunk_overlap: Overlap between chunks
            collection_name: Name for the vector store collection
        """
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.collection_name = collection_name
        self.vector_store = None

        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

    def create_documents_from_pdf_data(self, pdf_data: Dict[str, Any]) -> List[Document]:
        """
        Create LangChain documents from processed PDF data.

        Args:
            pdf_data: Dictionary containing PDF text and tables

        Returns:
            List of Document objects
        """
        documents = []

        # Add main text content
        if pdf_data.get('text'):
            text_chunks = self.text_splitter.split_text(pdf_data['text'])
            for i, chunk in enumerate(text_chunks):
                doc = Document(
                    page_content=chunk,
                    metadata={
                        'source': pdf_data['file_name'],
                        'file_path': pdf_data['file_path'],
                        'chunk_id': i,
                        'content_type': 'text'
                    }
                )
                documents.append(doc)

        # Add table content
        for table in pdf_data.get('tables', []):
            table_text = f"Table from page {table['page']} (Table #{table['table_number']}):\n{table['text']}"
            doc = Document(
                page_content=table_text,
                metadata={
                    'source': pdf_data['file_name'],
                    'file_path': pdf_data['file_path'],
                    'page': table['page'],
                    'table_number': table['table_number'],
                    'content_type': 'table'
                }
            )
            documents.append(doc)

        return documents

    def create_vector_store_chroma(
        self,
        documents: List[Document],
        persist_directory: Optional[str] = "./chroma_db"
    ) -> Chroma:
        """
        Create a ChromaDB vector store from documents.

        Args:
            documents: List of Document objects
            persist_directory: Directory to persist the vector store

        Returns:
            ChromaDB vector store
        """
        logger.info(f"Creating ChromaDB vector store with {len(documents)} documents...")

        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            collection_name=self.collection_name,
            persist_directory=persist_directory
        )

        logger.info("ChromaDB vector store created successfully.")
        return self.vector_store

    def create_vector_store_faiss(self, documents: List[Document]) -> FAISS:
        """
        Create a FAISS vector store from documents.

        Args:
            documents: List of Document objects

        Returns:
            FAISS vector store
        """
        logger.info(f"Creating FAISS vector store with {len(documents)} documents...")

        self.vector_store = FAISS.from_documents(
            documents=documents,
            embedding=self.embeddings
        )

        logger.info("FAISS vector store created successfully.")
        return self.vector_store

    def load_vector_store_chroma(self, persist_directory: str = "./chroma_db") -> Chroma:
        """
        Load an existing ChromaDB vector store.

        Args:
            persist_directory: Directory where vector store is persisted

        Returns:
            ChromaDB vector store
        """
        logger.info(f"Loading ChromaDB vector store from {persist_directory}...")

        self.vector_store = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
            persist_directory=persist_directory
        )

        logger.info("ChromaDB vector store loaded successfully.")
        return self.vector_store

    def save_vector_store_faiss(self, save_path: str = "./faiss_index"):
        """
        Save FAISS vector store to disk.

        Args:
            save_path: Path to save the FAISS index
        """
        if self.vector_store is None or not isinstance(self.vector_store, FAISS):
            raise ValueError("No FAISS vector store to save")

        self.vector_store.save_local(save_path)
        logger.info(f"FAISS vector store saved to {save_path}")

    def load_vector_store_faiss(self, load_path: str = "./faiss_index") -> FAISS:
        """
        Load FAISS vector store from disk.

        Args:
            load_path: Path to load the FAISS index from

        Returns:
            FAISS vector store
        """
        self.vector_store = FAISS.load_local(
            load_path,
            self.embeddings,
            allow_dangerous_deserialization=True
        )
        logger.info(f"FAISS vector store loaded from {load_path}")
        return self.vector_store

    def similarity_search(
        self,
        query: str,
        k: int = 4,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """
        Perform similarity search on the vector store.

        Args:
            query: Query text
            k: Number of results to return
            filter_dict: Optional metadata filter

        Returns:
            List of relevant documents
        """
        if self.vector_store is None:
            raise ValueError("Vector store not initialized. Create or load a vector store first.")

        if filter_dict and isinstance(self.vector_store, Chroma):
            results = self.vector_store.similarity_search(query, k=k, filter=filter_dict)
        else:
            results = self.vector_store.similarity_search(query, k=k)

        return results

    def as_retriever(self, search_kwargs: Optional[Dict[str, Any]] = None):
        """
        Get a retriever interface for the vector store.

        Args:
            search_kwargs: Optional search parameters

        Returns:
            Retriever object
        """
        if self.vector_store is None:
            raise ValueError("Vector store not initialized. Create or load a vector store first.")

        if search_kwargs is None:
            search_kwargs = {"k": 4}

        return self.vector_store.as_retriever(search_kwargs=search_kwargs)
