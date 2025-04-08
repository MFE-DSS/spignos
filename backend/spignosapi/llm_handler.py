from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

MODEL_PATH = "/absolute/path/to/PycharmProjects/spignos/local_models/mistral"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH)
llm_pipeline = pipeline("text-generation", model="./llm_models/mistral", local_files_only=True)

def generate_response(prompt: str) -> str:
    response = llm_pipeline(prompt, max_new_tokens=100, do_sample=True)
    return response[0]["generated_text"]
