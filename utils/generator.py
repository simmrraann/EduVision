from llm_engine import generate_output, generate_structured_output
import json

def generate_flashcards(text):
    """Generate structured flashcards from text content"""
    # Use the first 1000 characters for better results
    content = text[:1000] if len(text) > 1000 else text
    
    prompt = f"""Create 5 high-quality flashcards from the following content. 
    Each flashcard should have a clear question and detailed answer.
    Format as JSON array with 'question' and 'answer' fields.
    
    Content: {content}
    
    Example format:
    [
        {{"question": "What is...?", "answer": "It is..."}},
        {{"question": "How does...?", "answer": "It works by..."}}
    ]"""
    
    try:
        result = generate_structured_output(prompt, "json")
        # Try to parse and validate JSON
        parsed = json.loads(result)
        if isinstance(parsed, list) and len(parsed) > 0:
            return parsed
        else:
            return [{"question": "Sample Question", "answer": "Sample Answer"}]
    except:
        # Fallback to simple text format
        simple_result = generate_output(f"Create 3 flashcards (Q&A format) from: {content}")
        return [{"question": "Generated Question", "answer": simple_result}]

def generate_mcqs(text):
    """Generate multiple choice questions from text content"""
    prompt = f"""Create 5 multiple choice questions from the following content.
    Each question should have 4 options (A, B, C, D) with one correct answer.
    Format as JSON array with 'question', 'options', and 'correct_answer' fields.
    
    Content: {text[:1000]}
    
    Example format:
    [
        {{
            "question": "What is...?",
            "options": {{
                "A": "Option 1",
                "B": "Option 2", 
                "C": "Option 3",
                "D": "Option 4"
            }},
            "correct_answer": "A"
        }}
    ]"""
    
    try:
        result = generate_structured_output(prompt, "json")
        parsed = json.loads(result)
        if isinstance(parsed, list) and len(parsed) > 0:
            return parsed
        else:
            return [{"question": "Sample MCQ", "options": {"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"}, "correct_answer": "A"}]
    except:
        simple_result = generate_output(f"Create 3 MCQs from: {text[:500]}")
        return [{"question": "Generated MCQ", "options": {"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"}, "correct_answer": "A"}]

def generate_fill_in_blanks(text):
    """Generate fill-in-the-blank questions from text content"""
    prompt = f"""Create 5 fill-in-the-blank questions from the following content.
    Each question should have a sentence with a blank space and the correct answer.
    Format as JSON array with 'sentence' and 'answer' fields.
    
    Content: {text[:1000]}
    
    Example format:
    [
        {{"sentence": "The capital of France is _____.", "answer": "Paris"}},
        {{"sentence": "Water is composed of _____ and oxygen.", "answer": "hydrogen"}}
    ]"""
    
    try:
        result = generate_structured_output(prompt, "json")
        parsed = json.loads(result)
        if isinstance(parsed, list) and len(parsed) > 0:
            return parsed
        else:
            return [{"sentence": "Sample sentence with _____.", "answer": "blank"}]
    except:
        simple_result = generate_output(f"Create 3 fill-in-blank questions from: {text[:500]}")
        return [{"sentence": "Generated sentence with _____.", "answer": "answer"}]

def generate_mindmap(text):
    """Generate mindmap structure from text content"""
    prompt = f"""Create a mindmap structure from the following content.
    Identify main topics and their subtopics.
    Format as JSON with hierarchical structure.
    
    Content: {text[:1000]}
    
    Example format:
    {{
        "Main Topic": {{
            "Subtopic 1": ["Point 1", "Point 2"],
            "Subtopic 2": ["Point 3", "Point 4"]
        }}
    }}"""
    
    try:
        result = generate_structured_output(prompt, "json")
        parsed = json.loads(result)
        return parsed
    except:
        simple_result = generate_output(f"List main topics from: {text[:500]}")
        return {"Main Topic": {"Subtopic": ["Point 1", "Point 2"]}}

def generate_summary(text):
    """Generate AI summary from text content"""
    prompt = f"""Create a comprehensive summary of the following content.
    Include key points, main ideas, and important details.
    Keep it concise but informative.
    
    Content: {text[:1500]}"""
    
    return generate_output(prompt)

def generate_study_schedule(text):
    """Generate spaced repetition study schedule"""
    prompt = f"""Create a 7-day spaced repetition study plan based on this content.
    Include daily topics, review sessions, and practice activities.
    Format as JSON with daily schedules.
    
    Content: {text[:1000]}
    
    Example format:
    {{
        "Day 1": ["Topic 1", "Initial Review"],
        "Day 2": ["Topic 2", "Review Day 1"],
        "Day 3": ["Topic 3", "Review Day 1 & 2"],
        "Day 7": ["Final Review", "Practice Test"]
    }}"""
    
    try:
        result = generate_structured_output(prompt, "json")
        parsed = json.loads(result)
        return parsed
    except:
        simple_result = generate_output(f"Create study schedule for: {text[:500]}")
        return {"Day 1": ["Study", "Review"], "Day 7": ["Final Review"]}
