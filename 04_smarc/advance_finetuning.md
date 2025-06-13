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

