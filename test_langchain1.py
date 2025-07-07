import getpass
import os


os.environ['HUGGINGFACEHUB_API_TOKEN'] = getpass.getpass(
    "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"
)


# Huggingface Endpoint 
# from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

# llm = HuggingFaceEndpoint(
#     repo_id="Qwen/Qwen2.5-0.5B-Instruct", 
#     task="text-generation",
#     max_new_tokens=512,
#     do_sample=False, 
#     repetition_penalty=1.04,
# )

# chat_model = ChatHuggingFace(llm=llm)


# HuggingfacePipeline
from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace


from transformers import BitsAndBytesConfig

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype="float16",
    bnb_4bit_use_double_quant=True,
)

llm = HuggingFacePipeline.from_model_id(
    model_id="Qwen/Qwen2.5-0.5B-Instruct",
    task="text-generation",
    pipeline_kwargs=dict(
        max_new_tokens=128,
        do_sample=False,
        repetition_penalty=1.03,
        return_full_text=False,
    ),
    model_kwargs={"quantization_config": quantization_config}

)

chat_model = ChatHuggingFace(llm=llm)


from langchain_core.messages import (
    HumanMessage, 
    SystemMessage,
)

messages = [
    SystemMessage(content="You're a helpful assistant"),
    HumanMessage(
        content="What happens when an unstoppable force meets an immovable object?"
    ),
]

ai_messages = chat_model.invoke(messages)

print(ai_messages)



