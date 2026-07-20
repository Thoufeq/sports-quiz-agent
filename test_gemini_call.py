import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv('.env')

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    temperature=0.4,
    google_api_key=os.environ['GOOGLE_API_KEY'],
)

try:
    response = llm.invoke([
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content="Write a short sentence."),
    ])
    print("SUCCESS")
    print(response.content)
except Exception as e:
    print("ERROR")
    print(e)
