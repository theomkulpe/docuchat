This is an intelligent web application where users can upload PDFs or enter webpage URLs, and in return, receive detailed, AI-generated responses based on the content.

# PDF and Webpage Text Extraction and Querying Application

This project is a web-based application where users can upload PDF files or input a webpage URL. The app extracts the text, splits it into meaningful chunks, and allows users to query the content using AI models. The system leverages state-of-the-art embedding techniques, vector databases, and large language models to provide intelligent responses.

## Features

- Upload PDF files or input webpage URLs for processing.
- Text extraction from PDF and webpage sources.
- Chunked text processing with LangChain's RecursiveCharacterTextSplitter.
- Similarity search using FAISS vector store and HuggingFace embeddings.
- Query the content and get AI-generated answers with Groq's LLM integration.

## Technologies Used

- **Flask**: Backend framework to handle API requests.
- **React**: Frontend for user interaction.
- **LangChain**: Text splitting and management.
- **FAISS**: Vector database for document search and retrieval.
- **HuggingFace**: Pre-trained models for generating text embeddings.
- **Groq**: Cloud-based LLM model for generating intelligent responses.
- **Docker** (optional): For containerizing the application.
