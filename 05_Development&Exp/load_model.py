from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

# Load tokenizer and model explicitly
model_name = "Qwen/Qwen2.5-Math-7B"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True, torch_dtype=torch.float16)

# Create pipeline with GPU support
device = 0 if torch.cuda.is_available() else -1
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device=device,
    torch_dtype=torch.float16
)

def chat_with_model(question):
    messages = [{"role": "user", "content": f"PLEASE ANSWER IN ENGLISH ONLY: {question}"}]
    response = pipe(messages, max_new_tokens=1002, do_sample=True, temperature=0.5)
    return response[0]['generated_text'][-1]['content']

# Test with math question
math_question = "what is derivative of x^2 + 3x + 2"
print("Question:", math_question)
print("Answer:", chat_with_model(math_question))

# Interactive chat loop
while True:
    user_input = input("\nEnter your math question (or 'quit' to exit): ")
    if user_input.lower() == 'quit':
        break
   
    try:
        answer = chat_with_model(user_input)
        print("Model:", answer)
    except Exception as e:
        print(f"Error: {e}")
