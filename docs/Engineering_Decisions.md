# Engineering Decisions

This document explains the rationale behind the key architectural choices in this project. It is designed to help you discuss these decisions confidently in technical interviews.

### Why ChromaDB instead of Pinecone?
- **Cost & Independence**: ChromaDB runs entirely locally on disk. It requires no API keys, no cloud accounts, and incurs no monthly costs. Pinecone is an excellent managed service, but for a portfolio project, showing that you can self-manage a vector database is a stronger engineering signal.
- **Persistence**: We use Chroma's `PersistentClient` to save vectors to the `chroma_db` folder, ensuring data survives server restarts.

### Why MiniLM-L6-v2 for Embeddings?
- **Efficiency**: With only 22 million parameters, it runs extremely fast on CPU.
- **Quality**: Despite its small size, it produces excellent 384-dimensional semantic vectors and is widely used in production RAG systems where latency and cost are concerns.
- **Privacy**: No data is sent to external APIs (like OpenAI or Cohere) for embedding.

### Why DuckDuckGo Search?
- **Zero Configuration**: It requires no API key, unlike Google Custom Search or Bing Search API.
- **Supplemental Context**: Web search is used to catch recent events (e.g., "Latest Wimbledon winner") that a static knowledge base misses.

### Why a Query Planner?
- **Agentic Behavior**: A naive RAG system uses the user's raw query to search the DB. A smart agent *plans* its queries. The Query Planner decides whether to search the web, the DB, or both based on the user's intent.

### Why a Reranker?
- **Noise Reduction**: Vector similarity search (Cosine similarity) is good but imperfect. Web search has no similarity score at all. The Reranker sits *after* the Context Merger and scores all chunks (DB + Web) using heuristics (keyword density, source reliability). This ensures only the highest-quality context reaches the LLM.

### Why a Fact Checker instead of just a JSON Validator?
- **Anti-Hallucination**: LLMs hallucinate. By building a Fact Checker that verifies the generated answers against the retrieved context, we guarantee a higher level of factual accuracy. If the check fails, the agent automatically retries with specific error feedback.

### Why Structured JSON only?
- **Separation of Concerns**: The backend API should not be concerned with presentation (Markdown/HTML). Returning structured JSON allows the frontend to render the data in an interactive UI (like the one-question-at-a-time quiz interface) rather than just dumping text on a screen.

### Why move the Reranker AFTER the Context Merger?
- In standard pipelines, reranking happens right after retrieval. However, since we use two sources (ChromaDB and Web), moving the reranker *after* the merger allows us to evaluate all evidence together and select the best overall context.
