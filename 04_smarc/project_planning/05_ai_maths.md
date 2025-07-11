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

**ollama run hf.com/modelprovider/modelname**

############################################################################################################################################

## ollama, [llama.cpp](https://github.com/ggml-org/llama.cpp) and gguf for efficient inference and deployment 

ollama provides the way to infer and finetune numerous large language models with different modalities like llama3, moondream2 and so on. Additionally, it also allow running the models from huggingface allowing the flexibility of testing different models with consumer grade hardware (without cpu as well). But ollama is not preferred solution for deployment purpose as the concurrency directly affect the throughput from the ollama. 
    ollama run hf.com/model_provider/model_name-gguf

yes, ollama can be used for experimentation, llama.cpp can handle much more concurrent user requests along with running quantized models efficiently. llama.cpp is the way to run the large language models and deployment of those models on edge devices and the servers with cpus.
    llama-cli -hf modelprovide/modelname-gguf

## vllm (llm serving engine)

used for fast llm inference and serving. provides sota serving throughput (means how the model server can process the inference requests) 

**(pagedattention)**, allow quantization (gptq, int4, int8 and awq),OpenAI-compatible API server

        pip install vllm --extra-index-url https://download.pytorch.org/whl/cu128
        
        vllm serve DevQuasar/Qwen.Qwen2.5-VL-3B-Instruct-GGUF --port 8000 --host 0.0.0.0
        
*vLLM not supporting loading GGUF models directly from a remote Hugging Face repository*


        huggingface-cli download Qwen/Qwen2.5-7B-Instruct-GGUF --include "*.gguf" --local-dir ./Qwen.Qwen2.5-VL-3B-Instruct-GGUF --local-dir-use-symlinks False

        huggingface-cli download Qwen/Qwen2.5-7B-Instruct-GGUF qwen2.5-7b-instruct-q3_k_m.gguf --local-dir ./Qwen.Qwen2.5-VL-3B-Instruct-GGUFhuggingface-cli download Qwen/Qwen2.5-7B-Instruct-GGUF qwen2.5-7b-instruct-q3_k_m.gguf --local-dir ./Qwen.Qwen2.5-VL-3B-Instruct-GGUF

        vllm serve ./Qwen.Qwen2.5-VL-3B-Instruct-GGUF/qwen2.5-7b-instruct-q3_k_m.gguf --port 8000 --host 0.0.0.0

## openllm and sglang

[openllm](https://github.com/bentoml/OpenLLM)

[philosophy of openllm](https://www.bentoml.com/blog/from-ollama-to-openllm-running-llms-in-the-cloud) {must read}


openllm allow running the open-weights models as openai-compatible api endpoints with single command.
(also a chatui)
 
 openllm's python client is used for sending the requests and receiving  the raw response from the model. (its like a ollama but for cloud deployment)

OpenLLM’s current primary focus is on GPU-based inference, and it does not actively support CPU-only inference out of the box yet. 

    pip install openllm
    openllm hello
    openllm serve modelname 
 

[sgland](https://github.com/sgl-project/sglang)

sglang is a fast serving framework for llm and vlms. 

#### attributes of sglang

1. *radixattention for prefix caching*: caching the previously generated outputs
2. *zero-overhead cpu scheduler*: cpu inference support. 
3. *speculative decoding*: predicts possible new words ahead of time for response generation. 
4. *continuos batching*: group multiple requests together
5. *paged attention*: 


### openai-compatible api server


*An API that accepts and returns requests/responses in OpenAI’s JSON format*



This server implements an API compatible with OpenAI's API, allowing clients designed for OpenAI models to interact seamlessly with this local model instead.

**exposes an OpenAI-like API endpoint**

but qwen family is incompatible. 


### open-source model and local deployment

there are two options for using the large language models like qwen, llama, other any openai models in our application. first one is using using their hosted api endpoints (cloud based services) (paying for per/million tokens, the model is hostel in their own cloud) and second one is running the model locally in the server and use your own local api endpoint (http://localhost:2000) to serve the application with that model which can be done with the tools like llama.cpp, vllm, openllm and sglang. (provides full control over data, no api usage fee, scaling issue with limited hardware, slower inference speed depending on the infrastructure)

qwen allow commercial use. 

When running locally, you do not need an API key for your own server, but you need to set up your own API interface if you want to serve multiple users or integrate with other applications

    [vllm serve (from the vLLM project) — which starts a server exposing an OpenAI-compatible API endpoint on your local machine or server.

    llama-server (from llama.cpp) — which similarly runs a local HTTP server to serve model inference requests.

    Likewise, SGLang provides a runtime and server you can launch to serve models with an OpenAI-compatible API.]


**cpu-inference optimized frameworks**

CTranslate2
intel llm runtime





# Scaling LLMs

triton, vllm

business case] First, since the implication seems to be that this is for a business purpose, you should establish the business case for it. What's the market, what's the size of your market, how will you present it to your market.

[scalability] Second, you need to consider how many you're going to deploy. Just 'cause you can run one instance on your machine doesn't mean that you can deal with 10 people simultaneously trying to access it.

[Security] Third, you need to consider security. Can malicious forces take your machine and use it for their purposes?

[Liability] Fourth, what are the liability issues for the use of your product? What about the models you're using? Are there licenses that you need to comply with?re reading this post, this is to ask your very honest opinions and suggestions to help e-learning platforms to grow in Nepal.

5 months back we launched an online learning platform for early-professionals - edtraa.com , which provides career-ready courses from the top mentors of your desired industry. Nepal has seen massive failures in the e-learning segment yet we took a leap to start our venture. Being very honest, we currently have exactly 509 students in our platform as we are growin



Platforms like (digitalocean,runpod, lambda labs) provides raw GPU access where we need to manage our own environment whereas Azure/AWS are fully managed AI/ML services with enterprise grade features. 

## GPUs

V100, A100, H100. 



not only a model for answering the maths questions answer rather a complete product that offers question answering, reflective analysis and report from results and progress report uploaded by the students. Self evaluation through generated test papers. 


1. Multi-subject question answering (Nepali, social, english, maths, optional maths, science and computer science)
2. Curriculum aligned content ensuring relevance and accuracy. 
3. Generated question papers, past exam papers for practice covering all mentioned subjects. (how student written answers to the questions can be evaluated insted of just using mcq) 
4. AI powered grading and performance analytics for tests and assignments. 
5. Reflective learning reports.
6. llms for 24/7 study support.
7. career awareness and  guidance regarding emerging tech subjects. 
8. 


reflective pedagody (Gibbs Reflective Cycle)