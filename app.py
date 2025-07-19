from llm_engine import generate_output
from dotenv import load_dotenv
import os
import json
from flask import Flask, request, render_template, jsonify, redirect, url_for, session
from utils.ocr import extract_text_from_image
from utils.parser import extract_text_from_pdf
from utils.generator import generate_flashcards, generate_mcqs, generate_fill_in_blanks, generate_mindmap, generate_summary, generate_study_schedule
from utils.database import get_due_flashcards
from utils.spaced import update_flashcard_review

api_key = os.getenv("OPENAI_API_KEY")
load_dotenv()

app = Flask(__name__)
app.secret_key = 'mindmorph_secret_key_2025'  # Required for sessions

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            file = request.files["file"]
            if file.filename.endswith(".pdf"):
                uploaded_text = extract_text_from_pdf(file)
            elif file.filename.endswith((".png", ".jpg", ".jpeg")):
                file.save("temp.png")
                uploaded_text = extract_text_from_image("temp.png")
            elif file.filename.endswith(".txt"):
                uploaded_text = file.read().decode('utf-8')
            else:
                return "Unsupported file format. Please upload a PDF, image, or text file."

            # Generate all content and store in session
            session['uploaded_text'] = uploaded_text
            session['flashcards'] = generate_flashcards(uploaded_text)
            session['mcqs'] = generate_mcqs(uploaded_text)
            session['fill_in_blanks'] = generate_fill_in_blanks(uploaded_text)
            session['mindmap'] = generate_mindmap(uploaded_text)
            session['summary'] = generate_summary(uploaded_text)
            session['schedule'] = generate_study_schedule(uploaded_text)
            
            # Redirect to output options page
            return redirect(url_for('output_options'))
            
        except Exception as e:
            return f"Error processing file: {str(e)}"
    
    return render_template("index.html")

@app.route("/output-options")
def output_options():
    if 'uploaded_text' not in session:
        return redirect(url_for('index'))
    return render_template("output_options.html")

@app.route("/flashcards")
def flashcards_page():
    if 'flashcards' not in session:
        return redirect(url_for('index'))
    return render_template("flashcards.html", flashcards=session['flashcards'])

@app.route("/mcqs")
def mcqs_page():
    if 'mcqs' not in session:
        return redirect(url_for('index'))
    return render_template("mcqs.html", mcqs=session['mcqs'])

@app.route("/fillintheblanks")
def fill_in_blanks_page():
    if 'fill_in_blanks' not in session:
        return redirect(url_for('index'))
    return render_template("fill_in_blanks.html", fill_in_blanks=session['fill_in_blanks'])

@app.route("/mindmap")
def mindmap_page():
    if 'mindmap' not in session:
        return redirect(url_for('index'))
    return render_template("mindmap.html", mindmap=session['mindmap'])

@app.route("/summary")
def summary_page():
    if 'summary' not in session:
        return redirect(url_for('index'))
    return render_template("summary.html", summary=session['summary'])

@app.route("/schedule")
def schedule_page():
    if 'schedule' not in session:
        return redirect(url_for('index'))
    return render_template("schedule.html", schedule=session['schedule'])

@app.route("/upload", methods=["GET"])
def upload_page():
    return render_template("upload.html")

# API endpoints for AJAX calls (if needed)
@app.route('/generate_flashcards', methods=['POST'])
def flashcards():
    try:
        data = request.json.get('text', session.get('uploaded_text', ''))
        if not data:
            return jsonify({'error': 'No text available. Please upload a document first.'})
        
        result = generate_flashcards(data)
        return jsonify({'output': result})
    except Exception as e:
        return jsonify({'error': f'Error generating flashcards: {str(e)}'})

@app.route('/generate_mcqs', methods=['POST'])
def mcqs():
    try:
        data = request.json.get('text', session.get('uploaded_text', ''))
        if not data:
            return jsonify({'error': 'No text available. Please upload a document first.'})
        
        result = generate_mcqs(data)
        return jsonify({'output': result})
    except Exception as e:
        return jsonify({'error': f'Error generating MCQs: {str(e)}'})

@app.route('/generate_fillups', methods=['POST'])
def fill_in_blanks():
    try:
        data = request.json.get('text', session.get('uploaded_text', ''))
        if not data:
            return jsonify({'error': 'No text available. Please upload a document first.'})
        
        result = generate_fill_in_blanks(data)
        return jsonify({'output': result})
    except Exception as e:
        return jsonify({'error': f'Error generating fill-in-blanks: {str(e)}'})

@app.route('/generate_mindmap', methods=['POST'])
def mindmap():
    try:
        data = request.json.get('text', session.get('uploaded_text', ''))
        if not data:
            return jsonify({'error': 'No text available. Please upload a document first.'})
        
        result = generate_mindmap(data)
        return jsonify({'output': result})
    except Exception as e:
        return jsonify({'error': f'Error generating mindmap: {str(e)}'})

@app.route('/generate_schedule', methods=['POST'])
def schedule():
    try:
        data = request.json.get('text', session.get('uploaded_text', ''))
        if not data:
            return jsonify({'error': 'No text available. Please upload a document first.'})
        
        result = generate_study_schedule(data)
        return jsonify({'output': result})
    except Exception as e:
        return jsonify({'error': f'Error generating schedule: {str(e)}'})

@app.route('/generate_summary', methods=['POST'])
def summary():
    try:
        data = request.json.get('text', session.get('uploaded_text', ''))
        if not data:
            return jsonify({'error': 'No text available. Please upload a document first.'})
        
        result = generate_summary(data)
        return jsonify({'output': result})
    except Exception as e:
        return jsonify({'error': f'Error generating summary: {str(e)}'})

@app.route('/chatbot', methods=['POST'])
def chatbot():
    try:
        data = request.json
        question = data.get('question', '')
        context = data.get('context', session.get('uploaded_text', ''))
        
        if not context:
            return jsonify({'error': 'No document context available. Please upload a document first.'})
        
        prompt = f"Based on the following document content, answer this question: {question}\n\nDocument content:\n{context}"
        result = generate_output(prompt)
        return jsonify({'response': result})
    except Exception as e:
        return jsonify({'error': f'Error in chatbot: {str(e)}'})

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

@app.route("/clear-session")
def clear_session():
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)