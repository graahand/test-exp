# What is Transformers?
It is a library of pretrained natural language processing, computer vision, audio and multimodal models for inference and training. The main features of transformer library are: 
```
pip install 'transformers[torch]'
```
### Pipeline
It includes the inference class for many machine learning tasks like text generation,  image generation, automatic speech recognition, document answering and so on. ((run inference with pipeline))
```
from transformer import pipeline
pipeline = pipeline('text-generation', 'model/name', device='cuda')
pipeline("The malaria is caused due to", max_length=50)
```
## Trainer
It includes the trainer configuration for that supports mixed precision, torch.compile, Flash Attention and distributed training for PyTorch models.((finetune the model with trainer)) 
```
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from datasets import load_dataset

from transformers import DataCollatorWithPadding

from transformers import TrainingArguments

from transformers import Trainer

  

model = AutoModelForSequenceClassification.from_pretrained("distilbert/distilbert-base-uncased")

tokenizer = AutoTokenizer("distilbert/distilbert-base-uncased")

dataset = load_dataset("rotten_tomatoes")

  

# Converting to Tensors

def tokenize_dataset(dataset):

    return tokenizer(dataset['text'])

dataset = dataset.map(tokenize_dataset, batched=True)

  

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

  
  

training_args = TrainingArguments(

    output_dir='./output_directory_class',

    learning_rate=2e-5,

    per_device_train_batch_size=8,

    per_device_eval_batch_size=8,

    num_train_epochs=2,

)

  

trainer = Trainer(

    model=model,

    args=training_args,

    train_dataset=dataset['train'],

    eval_dataset=dataset['test'],

    tokenizer=tokenizer,

    data_collator=data_collator,

)

  

trainer.train()
```
### Generate
It allow the fast text generation with large language models and vision language models, including support for streaming and multiple decoding strategies. 

---
#### Accelerate Library
Accelerate library automate the device placement, distributed process orchestration and mixed-precision handling across CPU, GP and TPU.  Its API wraps model, optimizer and data loader so that the training loop scales seamlessly on any hardware with minimal code change. 
##### Process Orchestration
Process orchestration means coordinating training processes across devices and nodes, launching, synchronizing and managing inter-process communication to ensure parallel workloads share gradients, configuration, monitoring and automatic scaling efficiently without manual boilerplate. ((infrastructure-level code for initializing devices, spawning processes, managing precision scaling)) [[#Accelerate Library]]

---
#### Timm Library
'timm' is a deep learning library that contains the SOTA computer vision models, layers, optimizers, utilities, data loaders, augmentations and training/validation scripts with ability to reproduce ImageNet training results. [[#Accelerate Library]]
%%  pip install timm %%
```
import timm
import torch

model = timm.create_model('resnet50')
x = torch.randn(1, 3, 224, 224)
model(x).shape
```
---
### Pretrained Models
Each Hugging Face's pre-trained models inherits from three base classes: 
- **PretrainedConfig**: Model attributes ((number of heads, vocabulary size))
- **PretrainedModel** ((model architecture defined with configuration file, pretrained models only return raw hidden states. Model head need to be used to convert raw hidden states, *LlamaForCausalLM*))
- **Preprocessor** ((class for converting raw inputs into numerical inputs to the model, *PreTrainedTokenizer*, *ImageProcessingMixin*))
**AutoClass** API is recommended to use for loading models and preprocessors to automatically infer to appropriate architecture for each task.  

> [!NOTE]
> PyTorch loads weights in *torch.float32*  by default.

---

> [!MobileBERT ] MobileBERT
> MobileBERT introduces an inverted-bottleneck structure to maintain a balance between self-attention and feed-forward networks, achieving a 4.3x size reduction and a 5.5x speedup compared to the base version of BERT. 


> [!BabyLLaMA] BabyLLaMA
> BabyLLaMA distill knowledge from multiple teachers (LLaMA, GPT) into a 58M-parameter  model and a 345M-parameter model respectively, demonstrating that distillation can exceed teacher model's performance particularly under data-constrained conditions. 

## FlashAttention
*Reformer improves the complexity of the self-attention from 0(N2)  to 0(N log N) by replacing the dot product attention with one which uses locality-sensitivity hashing.*

Mixed Precision Training is a technique for enhancing pre-training efficiency of SLMs and LLMs. This approach leverages low-precision representations for forward and pass and backward propagation while maintaining high precision for updates. Few notable works are Automatic Mixed Precision, Brain Floating Point (BFLOAT16).
NVIDIA's latest hopper architecture supports 8-bit-floating (FP8) precision enabling greater computational efficiency for large-scale language models. 
### Hessian Metrics
The **Hessian** is a matrix that tells you how a function bends. While the gradient tells you the direction of steepest ascent or descent, the Hessian tells you how the steepness itself changes. In machine learning, especially deep learning, it helps us understand how our loss function behaves around minima and how our model might generalize. 
### Monolithic Multi-Modal Model
Monolithic multimodal models are single, unified neural networks trained to process and integrate multiple data types (e.g., text, image, audio) within one architecture. Unlike modular systems that use separate models for each modality, monolithic models share parameters and jointly learn cross-modal representations, enabling richer understanding and generation across modalities with end-to-end training and shared context.
### Gradient Clipping
Gradient clipping limits how large the gradients can get during backpropagation. If they exceed a threshold, they’re scaled down to prevent instability or exploding gradients. This stabilizes training, especially in deep or recurrent neural networks, by avoiding extreme parameter updates that can cause divergence or NaN losses. It ensures smoother, more controlled learning steps.
 ### Universal Login Distillation Loss
 Universal Logit Distillation Loss is a knowledge distillation technique where a student model learns from the logits (pre-softmax outputs) of a teacher model, using a unified, modality-agnostic loss. It’s designed to work across different tasks or modalities (e.g., vision, language, audio), hence the term "universal".
 
> [!NOTE] Title
> **Logits**: Raw output from the last layer of a model before applying softmax.

### BFLOAT16
BFLOAT16 is a compact floating-point format that keeps the range of FP32 but with lower precision. It speeds up training while avoiding common issues like overflow seen in FP16. That’s why it’s widely used in TPUs and supported in modern deep learning frameworks
**BFLOAT16 keeps the same 8-bit exponent as FP32**, so it can represent large and small values just like FP32.

#### GPU Generation and Supported Precision 

| Generation    | Precision Support                |
| ------------- | -------------------------------- |
| Volta (V100)  | FP16, FP32                       |
| Turing (T4)   | FP16, INT8                       |
| Ampere (A100) | FP16, BFLOAT16, TF32, INT8, FP64 |
| Hopper (H100) | FP8, FP16, BFLOAT16, INT8, FP64  |
### Mixture of Experts
Mixture of Experts (MoE) is a neural network architecture that splits the model into multiple “experts” (sub-networks), and during inference or training, only a small number of them are activated based on the input.
#### Usage of MoE
- GShard (Google): Scaled to 600B+ parameters.
- Switch Transformer: Efficient MoE with only 1 expert per token.
- GPT-MoE variants: Sparse expert-based large language models.
- Vision Models: Used in sparse ViT and multimodal architectures.