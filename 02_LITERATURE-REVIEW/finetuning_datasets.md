# Domain Specific Dataset Curation for Effective Finetuning

[[axolotl]]

# LLM Finetuning Datasets & Methodologies: Comprehensive Technical Guide

(referenced from claude.ai)

## Models Consideration

Qwen2.5-7B, llama2-7b and llama3.2-3b

## Quantization

qlora 4-bit quantization for 7b models and standard lora for 3b models. 


## Datasets

### Instruction tuning datasets

#### Multi Domain datasets

[Alpaca-52k ](https://huggingface.co/datasets/tatsu-lab/alpaca)

its can be used for general reasoning and creative writing with  4-6 hours of training 3b model. 

[Ultrachat-200k](https://huggingface.co/datasets/HuggingFaceH4/ultrachat_200k)

multi-turn conversation dataset. *complex reasoning chain* and *natural dialogue*

[anon8231489123/ShareGPT_Vicuna_unfiltered](https://huggingface.co/datasets/anon8231489123/ShareGPT_Vicuna_unfiltered/blob/main/ShareGPT_V3_unfiltered_cleaned_split_no_imsorry.json) ([text](https://huggingface.co/datasets/anon8231489123/ShareGPT_Vicuna_unfiltered/blob/main/ShareGPT_V3_unfiltered_cleaned_split.json))

chatgpt conversation 90k. for human like behavior finetuning. 

#### Enhance instruction datasets

[microsoft/orca-math-word-problems-200k](http://huggingface.co/datasets/microsoft/orca-math-word-problems-200k)

for mathematical reasoning with step-by-step solutions. 

upto grade 12. 

format: problem statement....reasoning......final answer. 

### Maths Dataset

1. GSM8K contains 8500 grade school maths problem including basic arithmetic through pre-algebra. 


2. [hendrycks/competition_math](taken down)

 12,500 competition-level problems (algebra, theory, calculus and number theory)

 ### Conversational Assistant Datasets

1. PersonaChat [bavard/personachat_truecased](https://huggingface.co/datasets/bavard/personachat_truecased)
        Contains 160k dialogue with personality traits. good for **human-like engagement patterns training objective.**
2. Empathetic dialogues [empathetic_dialogues](discarded)

    25k conversations

    for emotional understanding and assistant like behavior development. 

3. BlenderBot3-Dialog [facebook/blended_skill_talk](https://www.kaggle.com/datasets/thedevastator/multi-modal-conversation-data)
    
    76k conversations
    knowlege, empathy, personality and consistency. 


### Specific Assistant Behavior Datasets

1. Assistant Conversations by Anthropic [Anthropic/hh-rlhf](https://huggingface.co/datasets/Anthropic/hh-rlhf)

    161k human-assitant dialogues. 
    helpful, harmless and honest response, RLHF-ready format. 

2. OpenAssistant Conversations [OpenAssistant/oasst1](https://huggingface.co/datasets/OpenAssistant/oasst1)

    161k human-generated conversations. 
    include multiple languages (might contain nepali as well)


### Nepali TTS Development

    OpenSLR Nepali [openslr/43](https://openslr.org/43/)
   


   ## Can we finetune a vision language model on Maths Dataset/pictures?

### InternLM-Math [internlm/internlm2-math-plus-7b](https://huggingface.co/internlm/internlm2-math-plus-7b)

7b and 20b models which are pre-trained with ~100B math-related tokens and *SFT* with
~2M bilingual math supervised data. 

{{minhash and exact number match used for decontaminate possible test set leakage.}}

InternLM-Math is solver, prover, verifier and augmentor. 

It was evaluated for formal math reasoning with this evaluation set [MiniF2F-test](https://github.com/openai/miniF2F)

the dataset contains maths problems (theorem proving) from olympiads as well as high-school and undergraduate maths classes. 


In informal maths reasoning MATH, MATH-Python and GSM8K are used as evaluation set. 

InternLM-Math-7b performance: **34.6, 50.9, 78.1**

the 7b model outperforms the deepseek-7b-rl model 


InternLM-Math will be combined with Lean 3 (for theorem proving and maths problem solving). 

[Lean 3](https://lean-lang.org/doc/reference/latest/Elaboration-and-Compilation/) is a interactive theorem prover and functional programming language  based on dependent kernel theory which means types can depend on terms, enabling expressive formalization of mathematics and programs

#### How does test-set leakage happens?

future data used for training in time series. 

and improper cross-validation and its repeated use during hyperparameter tuning. 

information from test fold influence the training process of the model causing data leakage. 



## Mixture of Experts
    a machine learning architecture where llm is divided into multiple networks called experts and the **gated network** dynamically selects and routes input to one or few relevant experts. 

    Models like Mixtral-8x7b, Youtube Recommendation system, Z-code, Switch Transformer are based on MOE. 


    Different modes or methods of MOE are Top-k routing, 
    top-1 routing (only one exper per input token), 
    expert choice routing (expert decides which input they can handle best), 
    sparse activation/routing (only subset of experts are activated)

    **Capacity factor** is the hyperparameter that influences how many tokens each expert can handle during training and inference. 


    

