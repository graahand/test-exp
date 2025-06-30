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



