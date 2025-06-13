# Xtuner 

### Single turn and multi-turn converstation dataset. 

single turn dataset is effective for simple *FAQ bots and text classification related task.* 

multi turn conversation dataset is required for applications needing sustained (continuing for long time) interaction like *customer support, mental health counselling and talkbot robots.* 


#### incremental pre-training: 

    training the llama2 in nepali corpus for boosting the nepali language understanding.


**for instruction tuning reponse generation(output) loss is used for weight updates while the loss of instruction part(system input) is neglected**


*amalgamate:combine*


#### multi-turn conversation dataset sample: 

```
<|system|> You are a helpful assistant.
<|user|> What is the capital of France?
<|assistant|> Paris is the capital of France.
<|user|> What's the population?
<|assistant|> About 67 million people live in France.
<|user|> Who is the president?
<|assistant|> Emmanuel Macron is the current president.```



**xtuner uses their own method to deal with multi-turn conversation dataset**

i. concatenate the full converstaion into one sequence. 
ii. add special **<|user|> and <|assistant|>** tokens to *mark who said what.*

iii. only computed the loss for *assistant token* (loss mask used: 1 means computer loss, 0 means ignore)

iv. training becomes fast and efficient. 

