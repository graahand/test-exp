## Axolotl (alternative to hugginface/transformer)

It is a tool to full finetune model, parameter efficient finetuning and alignment techniques with support for multiple model architectures like llama, mixtral, phi, qwen, mixtral-moe, gemma, gpt-j, pythia etc. 

Support includes fp16/fp32, lora, qlora, gptq and flash attn. pre-training, finetuning and preference-based post-training (DPO, ORPO AND PRMs) 

Its installation requires **packaging==23.2, setuptools==75.8.0, wheel, ninja along with flash-attn and deepspeed.**

YAML file based finetuning technique. 

### Dataset Format required for pre-training. 

```python
{"text": "first row"}
{"text": "second row"}
...
```
in **.jsonl format.** 

```python
Dataset.load_dataset
```
it loads various formats of dataset including *jsonl, csv, arrow, parquet, sql and Webdataset*

### Dataset Format required for SFT

SFT means training model to respond to an instruction or chat input. (chatbots like GPT and Gemini)

Formats supported are **Conversation Dataset and Instruction Dataset** along with *tokenized dataset*

#### Conversation dataset 

It usually contain **role and content** key. 

its called chat_templates which is a Jinja2 template which formats a list of messages into a prompt. 


#### <|im_start|> and <|im_end|>

they are **de**limit**ers** which is a prompt that separates different speakers which  allow model to identify which portion belongs to whom. 

##### Sharegpt format

{"conversations": [{"from": "...", "value": "..."}]}

##### OpenAI format

{"messages": [{"role": "...", "content": "..."}]}

possible roles are *user, system, assistant*

{{**What do you want to mask?** }}

we can bring our own custom template via: 

**chat_template_jinja: # your template**

#### Instruction Dataset

used for training instruction following models. 

common format

```{"instruction": "...", "input": "...", "output": "..."}```

its called alpaca instruction dataset format. 

but custom instruction prompt are welcomed. 

## RLHF

RLHF means language model optimized through human feedback which means


### Methods for RLHF

#### DPO 

Direct Preference Optimization


#### IPO

Identity preference optimization

#### KTO

Kahneman-Tversky Optimization

#### GRPO

Group relative policy optimization

#### ORPO

Odds ratio preference optimization



