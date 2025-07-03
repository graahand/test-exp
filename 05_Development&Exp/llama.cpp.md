# llama.cpp

[[05_ai_maths#ollama, llama.cpp and gguf for efficient inference and deployment]]

### homebrew installation in ubuntu (required for llama.cpp pre-built binary installation)


    sudo apt-get install build-essential procps curl file git

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    brew install llama.cpp


what is the difference between:
*llama-server -hf bartowski/Qwen2.5-Math-7B-Instruct-GGUF:Q6_K_L* and 
*llama-cli -hf bartowski/Qwen2.5-Math-7B-Instruct-GGUF:Q6_K_L* ?

    

