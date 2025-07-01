# AI MATHS 


## flow for ai math

queries are accepted via two different modality,

text and image.

the text is converted to latex format and then only passed to the model.

the image is first processed using nougat-base-latex model and then passed to the llm.

the chosen llm for now is interlm-math-2-plus-7b, qwen family (2.5 and 3).

############################################################## can be files as well need a function that returns latex from image. need a function that converts text to latex format. need a function that loads and allow communication with the model.

## 7b model internlm

We unify *chain-of-thought reasoning, reward modeling, formal reasoning, data augmentation, and code interpreter* in a unified seq2seq format and supervise our model to be a versatile math reasoner, verifier (reinforcement learning), prover, and augmenter.


**ORM: OUTCOME REWARD MODELS**



## math benchmarks

1. gsm8k:linguistically diverse grade school math word problems (openai and surgeai, authored by expert human problem writers to ensure quality.)

2. MATH  : maths problem solving abilities (algebra, geometry, calculus, number theory)

4. mathbench-zh:maths theory understanding, bilingual questions (chinese and english), 

5. minif2f (formal 2 formatl): formal maths questions (undergraduate and highschool), questions formalized using LEAN (proof assistant)


**stochastic**: *random or chance of happening*


[latex-formulas, 552k datasets](https://huggingface.co/datasets/OleehyO/latex-formulas)


query of CC (common crawl) (data collection method [paper link](https://arxiv.org/abs/2401.14624), a llm guided approach to mie large-scale, high-quality data from public corpora(key techniques including query bootstrapping, bm25 retrieval))


{{MathJax (latext to text rendering for frontend)}}


################################################
Model required for solving geometrical questions. 



qwen2.5-math-7b is good model and better than internlm2-math-plus-7b in terms of maths word problem not tested with latex questions related to calculus.

there is another model especially for chatting i.e  qwen2.5-math-7b-Instruct whihch is specially finetuned for chatting purpose. 


## Planning


ai maths already uses gemini-flash api with daily requests limits. the performance of this model and the results generated are not evaluated. 

currently the model only generates the answer to any of the question provided via text and image modality. 

the existing system also doesn't consume extensive amount of resources because of the use of api. 

if we are to replace the geminin-flash or add any new model alongside it, then the resources required will substantially increase because of the nature of AI models. 

AI models (especially llms) are very resource intensive and heavily rely on GPU for efficient and fast computation. Our existing server configuration is not sufficient for loading such model with concurrent users. 

This requires deploying the model elsewhere in the cloud with GPU configuration like AWS, Azure or Google Cloud. 


experimented models includes qwen2.5-math-7b-instruct and interlm-math-plus-7b where the internlm was tested with word problems from class 10 maths where it performed poor, whereas the qwen family of the model performed better with the word problems, it requires testing with the calculus and algebraic problems.

regarding the modalities of input accepted by the model, text input will be easily interpreted by the model but when dealing with the image, questions from the image needs to be extracted using another model named (nougat-base-latex) which converts the maths question from the image to its latex representation which can be directly passed to the model such that it provides the response in same latex format. 

The latex format output needs to be converted to readable text for showing the results in AI maths website, one of such tool is {{MathJax (latext to text rendering for frontend)}}.


testing locally with the integrated web ui will be next step towards its next phase development. 



### How ollama uses the model such that they can run easily on consumer hardware?

ollama allow running any hugging face model as long as the model is available in GGUF format which means quantized. 

Ollama is suitable for small-scale deployment (e.g., teams ≤5 users) but struggles with high-concurrency scenarios, where solutions like OpenLLM offer 8x higher throughput and lower latency.

it can be done with this as well vLLM or Hugging Face Transformers with BitsAndBytes

#### Quantized models in hugging face 

*bnb-4bit*: 4-bit quantization implemented by bitsandbytes library. (good)
*gguf*: model file format optimized for local inference with frameworks like ollama and llama.cpp. 
*gptq-int4*: (generalized post-training quantization), a 4-bit quantization designed to preserve better accuracy than normal quantization. 
*gptq-int8*:same as above but uses 8-bit integers for quantization. 
*awq*:(adaptive weight quantization) new quantization, which adapts quantization parameters per weight group for better accuracy with 4-bit quantization. 
*q4f16_1-mlc*: 40bit quantization and 16-bit floating points for some part. 

*q5_k_m_gguf*: 5-bit quantization (k means quantization kernel), (m means mixed quantization)
*q6_k-gguf*: (ollama supported)(excellent accuracy)
*q4_k_m_gguf*: (good accuracy)(ollama supported)
*q4_k_s_gguf*: 4-bit quantization (s for small)
*q8_0-gguf*: 8-bit quantization without any schemes (0 means default quantization) (max accuracy,high usage ram)
*i1_gguf*: 1-bit quantization with extreme compression level. 

**Perplexity increase (PPL) is a measure of how much worse the quantized model predicts compared to the original FP16 model. For example, q6_k-gguf with +0.0044 PPL is almost indistinguishable from full precision.**
(lower perplexity means better performance) [its a exponentiation of average negative log-likelihood of predicted tokens.]




##### k-quantization / k-scheme

The "K" refers to a quantization strategy that groups or clusters model weights into a limited set of representative values (sometimes called centroids), but it is not the same as k-means clustering. Instead, it is a specialized quantization approach designed for LLM weights.

*the most important weights are quantized with higher precision, while less critical weights use lower precision.*

*The "K" quantization uses different bit-width representations (e.g., 4-bit, 5-bit, 6-bit)*


