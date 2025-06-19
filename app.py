from llm_engine import generate_output
from dotenv import load_dotenv
import os
api_key = os.getenv("OPENAI_API_KEY")
load_dotenv()

from flask import Flask, request, render_template
from utils.ocr import extract_text_from_image
from utils.parser import extract_text_from_pdf
from utils.generator import generate_flashcards, generate_mcqs, generate_fill_in_blanks

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    if request.method == "POST":
        file = request.files["file"]
        if file.filename.endswith(".pdf"):
            text = extract_text_from_pdf(file)
        else:
            file.save("temp.png")
            text = extract_text_from_image("temp.png")

        flashcards = generate_flashcards(text)
        mcqs = generate_mcqs(text)
        blanks = generate_fill_in_blanks(text)

        output = {
            "flashcards": flashcards,
            "mcqs": mcqs,
            "blanks": blanks
        }
        return render_template("index.html", output=output)
    
    return render_template("index.html")


@app.route("/upload", methods=["GET"])
def upload_page():
    return render_template("upload.html")

    return render_template("index.html", output=output)

@app.route('/generate_flashcards', methods=['POST'])
def flashcards():
    data = request.json['text']
    prompt = f"Create 5 flashcards (Q&A) from the following content:\n{data}"
    result = generate_output(prompt)
    return jsonify({'output': result})

@app.route('/generate_mcqs', methods=['POST'])
def mcqs():
    data = request.json['text']
    prompt = f"Generate 5 MCQs with 4 options each and correct answers:\n{data}"
    result = generate_output(prompt)
    return jsonify({'output': result})

@app.route('/generate_fillups', methods=['POST'])
def fill_in_blanks():
    data = request.json['text']
    prompt = f"Create 5 fill-in-the-blank questions from the following text:\n{data}"
    result = generate_output(prompt)
    return jsonify({'output': result})

@app.route('/generate_mindmap', methods=['POST'])
def mindmap():
    data = request.json['text']
    prompt = f"List main concepts and their subpoints from this content for mind mapping:\n{data}"
    result = generate_output(prompt)
    return jsonify({'output': result})

@app.route('/generate_schedule', methods=['POST'])
def schedule():
    data = request.json['text']
    prompt = f"Generate a 7-day spaced repetition study plan based on this content:\n{data}"
    result = generate_output(prompt)
    return jsonify({'output': result})


if __name__ == "__main__":
    app.run(debug=True)

from utils.database import get_due_flashcards
from utils.spaced import update_flashcard_review

@app.route("/review", methods=["GET", "POST"])
def review():
    if request.method == "POST":
        card_id = int(request.form["card_id"])
        quality = int(request.form["quality"])
        update_flashcard_review(card_id, quality)

    due_cards = get_due_flashcards()
    if due_cards:
        card = due_cards[0]  # Show one card at a time
        return render_template("review.html", card=card)
    else:
        return render_template("review_done.html")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        
        if file.filename.endswith(".pdf"):
            text = extract_text_from_pdf(file)
        elif file.filename.endswith((".png", ".jpg", ".jpeg")):
            file.save("temp.png")
            text = extract_text_from_image("temp.png")
        else:
            return "Unsupported file format. Please upload a PDF or image."

        flashcards = generate_flashcards(text)
        mcqs = generate_mcqs(text)
        blanks = generate_fill_in_blanks(text)

        output = {
            "flashcards": flashcards,
            "mcqs": mcqs,
            "blanks": blanks
        }

        return render_template("index.html", output=output)
    
    return render_template("index.html")