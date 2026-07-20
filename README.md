# AI-Powered Sports Quiz Agent

This project is a functional Python web application that generates interactive sports quizzes using Retrieval-Augmented Generation (RAG). It combines local historic facts (via ChromaDB) and live web search (via DuckDuckGo) to generate grounded questions using Google Gemini.

## 1. Setup Environment

First, open your terminal, navigate to this project folder, and activate the virtual environment:

**For macOS/Linux:**
```bash
source venv/bin/activate
```

**For Windows:**
```bash
venv\Scripts\activate
```

## 2. Install Dependencies

Ensure all required packages are installed:
```bash
pip install -r requirements.txt
```

## 3. Configure API Key

Ensure you have a `.env` file in the root of the project with your Google Gemini API Key:
```text
GOOGLE_API_KEY=your_api_key_here
```

## 4. Run the Application

Start the backend server by running:
```bash
python app.py
```

## 5. Access the Web App

Once the server is running, open your web browser and go to:
**http://localhost:8080**

You will see the clean Genially-style User Interface where you can configure and generate your quiz!
