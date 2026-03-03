# RAG (Retrieval-Augmented Generation)

A sophisticated document-based question-answering system that combines PDF processing, semantic search, and AI-powered answer generation.

## Overview

This project implements a complete Retrieval-Augmented Generation (RAG) pipeline that:
- **Extracts** text and structured content from PDF documents
- **Processes** documents using OCR for image-based content
- **Embeds** document chunks into vector space using sentence transformers
- **Retrieves** relevant context using FAISS vector search
- **Generates** accurate answers using the Groq LLaMA API

Perfect for building intelligent document Q&A systems, knowledge base chatbots, and academic research assistants.

## Features

✨ **Advanced PDF Processing**
- Multi-format text extraction using pdfplumber
- OCR support for image-heavy and scanned PDFs
- Smart document structuring with Unit and Section tagging

🔍 **Intelligent Retrieval**
- FAISS vector indexing for fast similarity search
- Keyword filtering for pre-filtering candidates
- Query expansion strategies
- Chunk-based retrieval with configurable overlap

🤖 **AI-Powered Responses**
- LLaMA 3.1 via Groq API for answer generation
- Two-stage retrieval: ranking and final answer generation
- Strict academic mode (refuses to guess beyond provided context)
- JSON-formatted output

🌐 **Multi-Language Support**
- JavaScript/Node.js interface via `ask.js`
- Python backend for core processing
- Seamless cross-language communication
