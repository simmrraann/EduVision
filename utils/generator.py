from llm_engine import generate_output

def generate_flashcards(text):
    prompt = f"Generate flashcards based on the following content:\n\n{text}"
    return generate_output(prompt)

def generate_mcqs(text):
    prompt = f"Create 3 MCQs from the following:\n\n{text}"
    return generate_output(prompt)

def generate_fill_in_blanks(text):
    prompt = f"Convert this into 3 fill-in-the-blanks questions:\n\n{text}"
    return generate_output(prompt)
