# Adobe India Hackathon 2025: Connecting the Dots (Round 1B)

This repository contains the solution for Round 1B of the hackathon: *Persona-Driven Document Intelligence*. The objective is to build a system that acts as an intelligent document analyst, extracting and prioritizing the most relevant sections from a collection of PDFs based on a specific user persona and their "job-to-be-done."

## My Approach

This solution is designed to understand the semantic meaning behind a user's request and match it to the content within a library of documents. The system uses a state-of-the-art Natural Language Processing (NLP) pipeline based on text embeddings and similarity search.

The entire process is broken down into the following key steps:

1.  *Foundation - Document Parsing (from Round 1A)*: The system first leverages the logic from Round 1A to parse every PDF in the document collection. It extracts a structured list of all sections (e.g., text under H1, H2, H3 headings) and their corresponding raw text content. This creates a clean, searchable knowledge base.

2.  *Core Technology - Semantic Search via Text Embeddings: To go beyond simple keyword matching, the solution uses **text embeddings*. An embedding is a numerical vector representation of text that captures its semantic meaning. Text passages with similar meanings will have vectors that are "close" to each other in multi-dimensional space.

3.  *Model Selection*: A lightweight, high-performance Sentence-Transformer model (**all-MiniLM-L6-v2**) is used to generate these embeddings. This model was specifically chosen because it:
    *   Offers excellent performance in semantic search tasks.
    *   Is small (under 100MB), easily meeting the <1GB size constraint.
    *   Is highly optimized to run efficiently on a CPU, respecting the hardware constraints.

4.  *Relevance Ranking via Cosine Similarity*:
    *   The system first generates an embedding for the user's Job-to-be-Done query.
    *   Next, it generates an embedding for every extracted section from all the PDFs.
    *   *Cosine Similarity* is then calculated between the query vector and each section vector. This metric measures the "angle" between vectors, providing a relevance score from -1 to 1. A higher score indicates a closer semantic match.
    *   The sections are then ranked in descending order based on their similarity score, fulfilling the primary "Section Relevance" requirement.

5.  *Granular Sub-Section Analysis*: To provide deeper, more focused insights, the system performs a second analysis pass on the top-ranked sections:
    *   For the most relevant sections identified in the previous step, the text is further broken down into individual sentences.
    *   The same similarity search process is repeated, comparing the user's Job-to-be-Done vector against the embeddings of each sentence.
    *   This allows the system to pinpoint and rank the most relevant individual sentences or small paragraphs within a broader section, directly addressing the "Sub-Section Relevance" scoring criterion.

This two-pass approach is highly efficient, as it avoids the computational expense of analyzing every sentence in every document, focusing only on the most promising areas.

## Models & Libraries Used

*   *Language*: Python 3.9
*   *Core Libraries*:
    *   **PyMuPDF**: For the initial, robust PDF parsing and section extraction.
    *   **sentence-transformers**: The primary framework for loading the embedding model and performing semantic search.
    *   **torch**: The backend deep learning framework for sentence-transformers.
    *   **numpy**: For efficient numerical operations on the embedding vectors.
*   *Pre-trained Model*:
    *   **all-MiniLM-L6-v2**: A sentence-embedding model that provides a state-of-the-art balance of speed, size, and accuracy for semantic search on CPU.

## How to Build and Run the Solution

The solution is fully containerized using Docker for portability and must be run on an AMD64 architecture. The container is designed to run completely offline.

*Prerequisites:*
*   Docker must be installed and running.

### 1. Build the Docker Image

Navigate to the root directory of this project (where the Dockerfile is located) and run the following command in your terminal:

```sh
docker build --platform linux/amd64 -t mysolutionname:somerandomidentifier .