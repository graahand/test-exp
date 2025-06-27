# flow for ai math


queries are accepted via two different modality, 

text and image. 

the text is converted to latex format and then only passed to the model. 

the image is first processed using nougat-base-latex model and then passed to the llm.


the chosen llm for now is interlm-math-2-plus-7b, qwen family (2.5 and 3).



##############################################################
    can be files as well
    need a function that returns latex from image.
    need a function that converts text to latex format. 
    need a function that loads and allow communication with the model. 


7b model interlm
