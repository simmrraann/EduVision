from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

def load_llm():
    model_id = "gpt2"  # Or mistralai/Mistral-7B-Instruct-v0.1
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id)
    generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
    return generator

generator = load_llm()

def generate_output(prompt: str):
    try:
        result = generator(prompt, max_length=100, num_return_sequences=1)
        return result[0]['generated_text']
    except Exception as e:
        return f"Error generating text: {e}"