import openai
import os
from dotenv import load_dotenv

from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

openai.api_key = os.getenv("OPENAI_API_KEY")

print("Loaded API Key:", os.getenv("OPENAI_API_KEY"))

def generate_flashcards(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Generate flashcards based on the following content:\n\n{text}"}
        ]
    )

    return response.choices[0].message.content


def generate_mcqs(text):
    prompt = f"Create 3 MCQs from the following:\n\n{text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

def generate_fill_in_blanks(text):
    prompt = f"Convert this into 3 fill-in-the-blanks questions:\n\n{text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']