from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "gpt2"
AutoTokenizer.from_pretrained(model_id)
AutoModelForCausalLM.from_pretrained(model_id)