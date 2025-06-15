from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from peft import get_peft_config, get_peft_model, LoraConfig, TaskType
from datasets import load_dataset
from transformers import DataCollatorForLanguageModeling

model_name = "internlm/internlm2-math-plus-7b"
tokenizer  = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model      = AutoModelForCausalLM.from_pretrained(
    model_name,
    trust_remote_code=True,
    device_map="auto",
    torch_dtype="auto",
)

# 1. Define LoRA config
peft_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    inference_mode=False,
    r=16,                # rank
    lora_alpha=32,
    lora_dropout=0.05,
    target_modules=['wqkv', 'wo']
)

# 2. Wrap model with PEFT
model = get_peft_model(model, peft_config)
model.print_trainable_parameters()  # should show only LoRA layers


# for name, module in model.named_modules():
#     if "qkv" in name or "attn" in name.lower():
#         print(name, module)

