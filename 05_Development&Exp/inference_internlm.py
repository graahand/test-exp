# Inference with InternLM2-Math-Plus-7B

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("internlm/internlm2-math-plus-7b", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    "internlm/internlm2-math-plus-7b",
    torch_dtype=torch.float16,         # Use bfloat16 or float16 for speed (if on GPU)
    device_map="auto",                 # Automatically assign to available devices
    trust_remote_code=True
)

# Set model to eval mode
model.eval()

# Inference function
def generate_response(prompt, max_new_tokens=256, temperature=0.2, top_p=0.9):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id  # prevent warning if input ends early
        )
    return tokenizer.decode(output[0], skip_special_tokens=True).strip()

# Example usage
prompt = "Solve the equation: 2x + 3 = 11."
response = generate_response(prompt)
print("Response:\n", response)
