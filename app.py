from flask import Flask, render_template, request, jsonify
from src.generator import compile_quiz_data
from src.database import setup_and_populate_db
import os
import json

app = Flask(__name__)
setup_and_populate_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.json
    sport = data.get("sport")
    difficulty = data.get("difficulty")
    num_questions = data.get("num_questions", 3)
    
    try:
        quiz_text, context_used = compile_quiz_data(sport, difficulty, num_questions)
        try:
            quiz_json = json.loads(quiz_text)
        except json.JSONDecodeError:
            import re
            json_match = re.search(r'\{[\s\S]*\}', quiz_text)
            if json_match:
                quiz_json = json.loads(json_match.group(0))
            else:
                return jsonify({"success": False, "error": "Failed to parse LLM JSON output"})
                
        return jsonify({
            "success": True,
            "quiz": quiz_json,
            "metadata": {
                "context": context_used
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
