# Central Quality Inspection System

this system is aims to identify design flaws using AI


aspect ratio (ratio of height and width): done ()
resolution (number of pixels in width and height): no problem ()
logo placement (WORKING A4)
text/typo (text extract)
blur detection (dekhauna layek)

margin(space between the image/design edge and the last elements closest to the edge of the image/design)


text, typos and grammar (text extraction is done first with doctr(document text recognition)) and as expected it didn't worked well out of the box and needs preprocessing which isn't feasible at all keeping in mind that the designs can be of any types (creativity, subjective)

color code for web usage and print usage (cmyk and rgb, no problem)

### needs to be done

1. font checker (different ING colleges have different fonts they use, apex and kavya have different primary font, rest of the ing's colleges primary font and typeface is roboto) also there are numerous secondary fonts for each colleges. (when to use primary font, when to use secondary font?)

2. logo placement works or not? (not known)

3. blur detection (can it be done with any vision language model guided with appropriate prompt.) needs an experimentation. 

4. if the algorithms or models are not working properly for text extraction, here also vision language model can rescue (i already worked on such project where vlm (moondream2 and qwen-vl-3b/7b) is used for text extraction (fyp))


5. a guidelines report is essential (kimi_ai allow 50 files upload, uploading the files shared from icreate to write down the actual guidelines)

6. font confirmation

7. typos and grammar mistakes (gramformer, pyaspeller, python-language-tools, )



1. logo 



finetuning vlm with all the information about the guidelines. 

how to finetune??

dataset should contain following: 
    design image
    what text is written? exact
    what font is used? 
    does it contain any unwanted blur or not?
    logo placement correct or not? 
    check whether the design templates are not distorted, cropped or scaled differently or oddly? 
    

## experimentation 1

without finetuning and careful prompting, text extraction can be done, font classification is only possible with a trained CNN. logo placement done through algorithm and pre-defined criteria. 

**model usage** [[05_ai_maths#How ollama uses the model such that they can run easily on consumer hardware?]]

segmentation of any use? for blur detection?? 


## Information to be extracted from the shared CQIS folder

1. primary and secondary fonts/typeface of each ing college.
2. Logo placement guide for A4, A3, A5,digital collaterals (margins), color theme and do/don't regarding the logo (text color, background color) 
3. story guide (consult to niraj dai , what does story means? is it social media story? if yes then write down the criteria in words)
4. write down the criteria for standees (every ING colleges) like margin and logo placement and any other essential details. 


5. Dataset format for vision language model: 
    a. design template/image
    b. which typeface used (primary and secondary)
    c. what text is written in the image and is it correct (typos/grammar)? any text overflow or weird line breaks inside the designs. 
    d. any distorted, pixelated or unnecessarily/mistakenly blurred region in the image
    e. logo placement and margin for A4, A3, A5, digital collaterals, social media cover pages and standee (30x72)
    f. color guidelines (logos, background, text color)

inclusion of positive cases and negative cases in dataset and requires minimal human intervention.


    image_id:01,
    image_path: img.png,
    typeface used: roboto, (can model learn to identify?)
    blur/pixelated_regions_present: yes (co-ordinates)/no, (can model learn)
    text_written: islington college, congratulations graduates!!, 
    grammar check: positive/negative,
    logo_placement: co-ordinates() (can model extract accurately) 
    logo_margin: 30px (can model learn?) 
    type_of_templates:A4/A3/A5 (i don't know whether the model can learn to identify size of template), 
    logo_color_check: positive/negative
    logo_background_check: positive/negative


##  can a vision language model like qwen can learn these things after finetuning? if  yes then how many positive and negative samples required, help me with the data collection and preparation.?


### convolutional neural network for typeface classification

data collection by generating the typeface/font text to image from font file like  .ttf or .otf which are easily available.

generate the images using using openly available tool/model that can be run with  the resources from our pc. 

real world samples will be very valuable.

required samples for each typeface is at least 1000. 

here is the link to the dataset which needs some exploration and can be useful for this task. its a font recognition dataset by Adobe. train data is around 18gb with 2383 font classes. pretrained model is DeepFont produced along with the dataset by adobe research. 

feasiblity and initial reports required fast. 

for now research on vlms is on hold. 
(https://www.kaggle.com/datasets/luisgoncalo/adobe-visual-font-recognition?select=train.bcf)






















