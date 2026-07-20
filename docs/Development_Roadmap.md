# Development Roadmap & Future Improvements

This project was built to demonstrate an advanced AI agent architecture, but there is always room for growth. If you wish to extend this project further, here are the recommended next steps.

## Phase 1: Advanced Retrieval
- **Hybrid Search**: Currently, we use dense vector similarity. Add sparse keyword search (BM25) and combine them with Reciprocal Rank Fusion (RRF) for better retrieval of exact names/dates.
- **Cross-Encoder Reranking**: Replace the heuristic reranker in `src/retrieval/reranker.py` with a machine learning cross-encoder model (e.g., `cross-encoder/ms-marco-MiniLM-L-6-v2`) for state-of-the-art relevance scoring.

## Phase 2: System Scalability
- **Redis Caching**: Replace the simple in-memory dictionary cache (`src/retrieval/cache.py`) with Redis. This allows caching to work across multiple server instances.
- **FastAPI Migration**: Port the Flask API to FastAPI. This provides native async support, which is much better for handling long-running LLM calls, plus automatic OpenAPI (Swagger) documentation.
- **Dockerization**: Create a `Dockerfile` and `docker-compose.yml` to package the app, making deployment to AWS or Google Cloud seamless.

## Phase 3: User Experience
- **Streaming Responses**: Instead of waiting for the full quiz to generate, stream the JSON back to the frontend chunk by chunk using Server-Sent Events (SSE).
- **Authentication**: Add user login (JWT or OAuth) so users can save their quiz history and track their high scores over time.
- **Database Integration**: Use PostgreSQL to store generated quizzes, user scores, and analytics.

## Phase 4: AI Capabilities
- **Multi-Agent Architecture**: Split the single orchestrator agent into a team of agents using LangGraph (e.g., a Researcher Agent, a Writer Agent, and an Editor Agent).
- **Dynamic Difficulty Calibration**: If a user answers 5 "Hard" questions correctly, automatically increase the complexity of the next generation.
- **Image Generation**: Use an image generation model to create unique, AI-generated thumbnail images for each generated quiz.
