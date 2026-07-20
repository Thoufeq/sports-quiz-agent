# API Reference

The backend exposes a RESTful JSON API via Flask.

## Base URL
`http://localhost:5000`

---

## `POST /api/generate`

Generates a sports quiz using the AI agent pipeline.

### Request Body (JSON)
```json
{
  "sport": "Cricket",
  "difficulty": "Hard",
  "num_questions": 5
}
```

### Response (Success 200 OK)
```json
{
  "success": true,
  "quiz": {
    "sport": "Cricket",
    "difficulty": "Hard",
    "questions": [
      {
        "id": 1,
        "question": "Which bowler took the first hat-trick in Cricket World Cup history?",
        "options": ["Wasim Akram", "Chetan Sharma", "Brett Lee", "Shane Warne"],
        "correct_answer": "Chetan Sharma",
        "explanation": "Chetan Sharma of India took the first hat-trick in World Cup history against New Zealand in the 1987 World Cup.",
        "source": "Document 2 | Cricket_World_Cup_History.pdf",
        "confidence": 0.95,
        "difficulty": "Hard"
      }
    ]
  },
  "sources": {
    "historical": ["Cricket_World_Cup_History.pdf"],
    "web": ["latest ICC cricket rankings 2026"]
  },
  "activity_log": [
    {
      "step": "Intent analyzed",
      "detail": "Sport: Cricket, Difficulty: Hard, Questions: 5",
      "duration_ms": 1,
      "status": "success"
    },
    {
      "step": "ChromaDB searched",
      "detail": "8 chunks retrieved",
      "duration_ms": 150,
      "status": "success"
    }
  ],
  "metadata": {
    "total_duration_ms": 2450,
    "chunks_retrieved": 13,
    "chunks_after_rerank": 5,
    "cache_hit": false,
    "generation_attempts": 1,
    "overall_confidence": 0.92
  }
}
```

---

## `GET /api/sports`

Returns configuration data for the frontend.

### Response (200 OK)
```json
{
  "sports": [
    "Cricket",
    "Football",
    "Basketball",
    "Tennis",
    "Badminton",
    "Formula 1",
    "Olympics"
  ],
  "difficulties": ["Easy", "Medium", "Hard"],
  "question_range": {
    "min": 3,
    "max": 10,
    "default": 5
  }
}
```

---

## `GET /api/health`

Basic health check endpoint.

### Response (200 OK)
```json
{
  "status": "ok",
  "model": "gemini-2.5-flash"
}
```
