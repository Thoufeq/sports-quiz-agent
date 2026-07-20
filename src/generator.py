from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from src.config import GOOGLE_API_KEY
from src.database import query_historic_facts
from src.search import get_live_news_context

def compile_quiz_data(sport, difficulty, num_questions):
    db_query = f"{sport} history cup championships rules records"
    db_matches = query_historic_facts(sport=sport, query_text=db_query, n_results=2)
    db_context = "\n".join(db_matches) if db_matches else "No offline historic data recorded."

    web_context = get_live_news_context(sport)

    unified_context = f"=== HISTORICAL FACTS ===\n{db_context}\n\n=== LIVE INTERNET NEWS ===\n{web_context}"

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.7
    )

    system_instruction = (
        "You are an expert sports quiz creator. Your job is to write multiple-choice quizzes "
        "relying strictly on the provided Context. Avoid hallucinations. Do not use facts not "
        "found in the Context below. If facts are scarce, make do with what you have, "
        "but keep details completely accurate to the text context.\n\n"
        f"CONTEXT DETAILS:\n{unified_context}\n\n"
        "You MUST output ONLY valid JSON matching this schema:\n"
        "{\n"
        "  \"questions\": [\n"
        "    {\n"
        "      \"id\": 1,\n"
        "      \"question\": \"Question text here?\",\n"
        "      \"options\": [\"A\", \"B\", \"C\", \"D\"],\n"
        "      \"correct_answer\": \"B\",\n"
        "      \"explanation\": \"Why B is correct based on the context.\",\n"
        "      \"source\": \"Document 1 | File.pdf\",\n"
        "      \"confidence\": 0.95,\n"
        "      \"difficulty\": \"Hard\"\n"
        "    }\n"
        "  ]\n"
        "}\n"
        "Do NOT include markdown formatting like ```json or any other text before or after the JSON."
    )

    user_prompt = f"Generate exactly {num_questions} unique multiple-choice questions for the sport: {sport} at {difficulty} difficulty."

    response = llm.invoke([
        SystemMessage(content=system_instruction),
        HumanMessage(content=user_prompt)
    ])
    
    response_text = response.content
    if isinstance(response_text, list):
        text_parts = [item.get("text", "") for item in response_text if isinstance(item, dict) and "text" in item]
        response_text = "".join(text_parts)
    elif not isinstance(response_text, str):
        response_text = str(response_text)

    return response_text, unified_context
