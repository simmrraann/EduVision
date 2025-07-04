rom llm_engine import generate_output

def generate_mcqs(text):
    prompt = f"Generate 5 multiple choice questions from the following text:\n{text}"
    return generate_output(prompt)

def generate_fill_in_blanks(text):
    prompt = f"Convert the following text into 5 fill in the blanks:\n{text}"
    return generate_output(prompt)