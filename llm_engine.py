import os
import openai
from dotenv import load_dotenv
import json
import random

load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_output(prompt: str, model="gpt-3.5-turbo"):
    """
    Generate output using OpenAI API with fallback to local model
    """
    try:
        if openai.api_key and openai.api_key.startswith("sk-"):
            # Use OpenAI API
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant that creates educational content. Always respond in a clear, structured format."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            return response.choices[0].message.content
        else:
            # Fallback to local model or generate sample content
            return generate_fallback_content(prompt)
            
    except Exception as e:
        # Fallback to local model or generate sample content
        return generate_fallback_content(prompt)

def generate_fallback_content(prompt: str):
    """
    Generate fallback content when OpenAI is not available
    """
    prompt_lower = prompt.lower()
    
    # Sample content based on prompt type
    if "flashcard" in prompt_lower:
        return json.dumps([
            {
                "question": "What is machine learning?",
                "answer": "Machine learning is a subset of AI that enables computers to learn from data without explicit programming."
            },
            {
                "question": "What are the three types of machine learning?",
                "answer": "Supervised learning, unsupervised learning, and reinforcement learning."
            },
            {
                "question": "What is supervised learning?",
                "answer": "Supervised learning uses labeled data to train models to make predictions on new, unseen data."
            },
            {
                "question": "What is a neural network?",
                "answer": "A neural network is a computational model inspired by biological neurons, consisting of interconnected nodes organized in layers."
            },
            {
                "question": "What is overfitting in machine learning?",
                "answer": "Overfitting occurs when a model learns the training data too well but fails to generalize to new, unseen data."
            }
        ])
    
    elif "mcq" in prompt_lower or "multiple choice" in prompt_lower:
        return json.dumps([
            {
                "question": "What is machine learning?",
                "options": {
                    "A": "A type of computer hardware",
                    "B": "A subset of artificial intelligence",
                    "C": "A programming language",
                    "D": "A database system"
                },
                "correct_answer": "B"
            },
            {
                "question": "Which of the following is NOT a type of machine learning?",
                "options": {
                    "A": "Supervised Learning",
                    "B": "Unsupervised Learning",
                    "C": "Reinforcement Learning",
                    "D": "Manual Programming"
                },
                "correct_answer": "D"
            },
            {
                "question": "What is the main purpose of neural networks?",
                "options": {
                    "A": "To store data",
                    "B": "To process and learn patterns from data",
                    "C": "To display graphics",
                    "D": "To connect to the internet"
                },
                "correct_answer": "B"
            },
            {
                "question": "What is overfitting?",
                "options": {
                    "A": "When a model is too simple",
                    "B": "When a model learns training data too well",
                    "C": "When data is missing",
                    "D": "When the computer is too slow"
                },
                "correct_answer": "B"
            },
            {
                "question": "Which application uses machine learning?",
                "options": {
                    "A": "Image recognition",
                    "B": "Word processing",
                    "C": "Web browsing",
                    "D": "File management"
                },
                "correct_answer": "A"
            }
        ])
    
    elif "fill" in prompt_lower or "blank" in prompt_lower:
        return json.dumps([
            {
                "sentence": "Machine learning is a subset of _____ intelligence.",
                "answer": "artificial"
            },
            {
                "sentence": "_____ learning uses labeled data for training.",
                "answer": "Supervised"
            },
            {
                "sentence": "Neural networks are inspired by biological _____.",
                "answer": "neurons"
            },
            {
                "sentence": "_____ occurs when a model learns training data too well.",
                "answer": "Overfitting"
            },
            {
                "sentence": "Deep learning uses neural networks with multiple _____.",
                "answer": "layers"
            }
        ])
    
    elif "mindmap" in prompt_lower:
        return json.dumps({
            "Machine Learning": {
                "Types": ["Supervised Learning", "Unsupervised Learning", "Reinforcement Learning"],
                "Applications": ["Computer Vision", "Natural Language Processing", "Healthcare", "Finance"],
                "Key Concepts": ["Neural Networks", "Deep Learning", "Overfitting", "Underfitting"]
            }
        })
    
    elif "summary" in prompt_lower:
        return "Machine learning is a subset of artificial intelligence that enables computers to learn from data without explicit programming. It includes three main types: supervised learning (using labeled data), unsupervised learning (finding patterns in unlabeled data), and reinforcement learning (learning through interaction). Key concepts include neural networks, deep learning, overfitting, and underfitting. Applications span computer vision, natural language processing, healthcare, and finance."
    
    elif "schedule" in prompt_lower or "plan" in prompt_lower:
        return json.dumps({
            "Day 1": ["Introduction to Machine Learning", "Basic Concepts Review"],
            "Day 2": ["Supervised Learning", "Review Day 1 Concepts"],
            "Day 3": ["Unsupervised Learning", "Review Previous Days"],
            "Day 4": ["Neural Networks", "Practice Problems"],
            "Day 5": ["Deep Learning", "Review All Concepts"],
            "Day 6": ["Applications", "Real-world Examples"],
            "Day 7": ["Final Review", "Practice Test", "Assessment"]
        })
    
    else:
        # Generic response
        return "I can help you with machine learning concepts. Please ask specific questions about flashcards, MCQs, fill-in-the-blanks, mindmaps, summaries, or study schedules."

def generate_structured_output(prompt: str, structure_type: str = "json"):
    """
    Generate structured output (JSON, markdown, etc.)
    """
    try:
        if structure_type == "json":
            prompt += "\n\nPlease format your response as valid JSON."
        
        result = generate_output(prompt)
        
        # Try to parse JSON if requested
        if structure_type == "json":
            try:
                # Find JSON in the response
                start = result.find('{')
                end = result.rfind('}') + 1
                if start != -1 and end != 0:
                    json_str = result[start:end]
                    json.loads(json_str)  # Validate JSON
                    return json_str
                else:
                    # Try array format
                    start = result.find('[')
                    end = result.rfind(']') + 1
                    if start != -1 and end != 0:
                        json_str = result[start:end]
                        json.loads(json_str)  # Validate JSON
                        return json_str
                    else:
                        return result
            except:
                return result
        
        return result
        
    except Exception as e:
        return f"Error generating structured output: {str(e)}"