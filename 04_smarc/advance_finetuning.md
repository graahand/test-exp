# Advance Data Preparation, visualization and Finetuning (Trelis Research)

## 1. Document Ingestion 

converting pdfs to md. 

it can be done using three different techniques, 
1. marker-pdf - most accurate (python package) [marker-pdf](https://pypi.org/project/marker-pdf/)
*better results compared to rest two* 

2. markitdown(microsoft) fast and cheap. (github package)
3. gemini flash (google api key required)

 
## 2. Chunks the markdown/extracted data. 

1. sentence recognition (nltk for indentifying sentences boundaries but simple technique to identify the period and chunking at sentence level can be done.)

2. regex-based recognition for tables and csv. 

will only works with the marker-pdf results where the tables are intact. 


3. chunk sizing 

smaller chunks and bigger chunks(they provides better context)

but the contextualization can be improved by instead feeding the summary of the entire document(recommended (trellis research))

################################################################################################

Any given model can be finetuned with two different methods,

1. transformers.Trainer (requires high amount of VRAM)
2. Parameter efficient finetuning (peft library for this method)


## PEFT Finetuning

''' from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
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
    )

    # 2. Wrap model with PEFT
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()  # should show only LoRA layers

    # 3. Prepare data
    data = load_dataset("json", data_files="my_math_data.jsonl")
    def tokenize_fn(example):
        return tokenizer(example["text"], truncation=True, max_length=1024)

    tokenized = data.map(tokenize_fn, batched=True, remove_columns=["text"])
    data_collator = DataCollatorForLanguageModeling(tokenizer, mlm=False)

    # 4. Training args (much lighter)
    training_args = TrainingArguments(
        output_dir="outputs/lora-finetune",
        per_device_train_batch_size=4,
        gradient_accumulation_steps=8,
        learning_rate=3e-4,
        fp16=True,
        num_train_epochs=3,
        logging_steps=50,
        save_steps=200,
        save_total_limit=2,
    )

    # 5. Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized["train"],
        data_collator=data_collator,
    )

    # 6. Train!
    trainer.train()
    # 7. Save only the LoRA adapters
    model.save_pretrained("lora_adapters_math")
'''



{{Error encountered}}
    ValueError: Target modules {'o_proj', 'k_proj', 'v_proj', 'q_proj'} not found in the base model. Please check the target modules and try again.


##### Troubleshoot

inspect the actual module names to know what are the name for model's attention layers. 

with following
    [# for name, module in model.named_modules():
     if "qkv" in name or "attn" in name.lower():
         print(name, module)]


it gave following modules for the *interlm_math_plus* model

"wqkv": fused query, key, value projection.  (you are reshaping what model attends to)

"wo" : attention output projection (refine how attended information are merged back into the network).



