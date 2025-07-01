import subprocess
import os
import sys
from typing import Dict, Any, Optional
from pathlib import Path

def load_qwen_math_model_and_respond(
    prompt: str, 
    model_path: str = "./models/qwen2.5-math-1.5b-instruct-q8_0.gguf",
    llamacpp_binary: str = "./llama-main"
) -> Dict[str, Any]:
    """
    Loads the Qwen2.5-Math model via llama.cpp and generates a response to the given prompt.
    
    This function implements direct binary execution of llama.cpp with optimized inference 
    parameters for mathematical reasoning tasks. The implementation bypasses Python 
    bindings for maximum performance and memory efficiency.
    
    Parameters:
    -----------
    prompt : str
        Input text prompt for mathematical reasoning or general queries
    model_path : str, default="./models/qwen2.5-math-1.5b-instruct-q8_0.gguf"
        File system path to the GGUF quantized model file
    llamacpp_binary : str, default="./llama-main"
        Path to the compiled llama.cpp main executable
    
    Returns:
    --------
    Dict[str, Any]
        Response dictionary containing:
        - 'success': bool indicating operation status
        - 'response': str containing model output
        - 'error': Optional[str] containing error message if failed
        - 'inference_stats': Dict with performance metrics
    
    Technical Implementation:
    ------------------------
    - Direct subprocess execution of llama.cpp binary
    - Memory-mapped model loading for optimal RAM utilization
    - Context window management with sliding window attention
    - Temperature and sampling parameter optimization for mathematical accuracy
    """
    
    # Step 1: Validate binary and model file existence
    if not os.path.exists(llamacpp_binary):
        return {
            'success': False,
            'response': None,
            'error': f"llama.cpp binary not found at {llamacpp_binary}",
            'inference_stats': {}
        }
    
    if not os.path.exists(model_path):
        return {
            'success': False,
            'response': None,
            'error': f"Model file not found at {model_path}",
            'inference_stats': {}
        }
    
    try:
        # Step 2: Format prompt with Qwen2.5 instruction template
        # Qwen2.5-Math uses specific formatting for optimal mathematical reasoning
        formatted_prompt = f"<|im_start|>system\nYou are a helpful assistant specialized in mathematics. Provide step-by-step solutions with clear explanations.<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
        
        # Step 3: Configure llama.cpp inference parameters
        # Optimized for mathematical reasoning accuracy over creative generation
        inference_cmd = [
            llamacpp_binary,
            "--model", model_path,
            "--prompt", formatted_prompt,
            "--ctx-size", "4096",          # Context window: 4K tokens for complex problems
            "--n-predict", "1024",         # Maximum generation length
            "--temp", "0.1",               # Low temperature for deterministic mathematical reasoning
            "--top-p", "0.9",              # Nucleus sampling threshold
            "--top-k", "20",               # Top-k sampling for controlled vocabulary
            "--repeat-penalty", "1.1",     # Repetition penalty for coherent solutions
            "--threads", str(os.cpu_count()), # Utilize all available CPU cores
            "--batch-size", "512",         # Batch size for token processing
            "--no-display-prompt",         # Suppress prompt echo in output
            "--log-disable",               # Disable verbose logging
            "--seed", "42"                 # Reproducible generation seed
        ]
        
        # Step 4: Execute inference with performance monitoring
        inference_result = subprocess.run(
            inference_cmd,
            capture_output=True,
            text=True,
            timeout=180,  # 3-minute timeout for complex mathematical derivations
            cwd=os.path.dirname(os.path.abspath(llamacpp_binary))
        )
        
        # Step 5: Parse stderr for performance metrics
        stderr_output = inference_result.stderr
        inference_stats = {}
        
        # Extract key performance indicators from llama.cpp output
        for line in stderr_output.split('\n'):
            if 'llama_print_timings' in line:
                continue
            elif 'load time' in line:
                # Extract model loading time: "load time = 1234.56 ms"
                try:
                    load_time = float(line.split('=')[1].strip().split()[0])
                    inference_stats['model_load_time_ms'] = load_time
                except (ValueError, IndexError):
                    pass
            elif 'sample time' in line:
                # Extract sampling time and rate
                try:
                    parts = line.split('=')[1].strip().split()
                    sample_time = float(parts[0])
                    if len(parts) > 3:
                        sample_rate = float(parts[3].rstrip('(').rstrip(')'))
                        inference_stats['sample_time_ms'] = sample_time
                        inference_stats['sample_rate_tokens_per_sec'] = sample_rate
                except (ValueError, IndexError):
                    pass
            elif 'prompt eval time' in line:
                # Extract prompt evaluation metrics
                try:
                    parts = line.split('=')[1].strip().split()
                    prompt_eval_time = float(parts[0])
                    if len(parts) > 3:
                        prompt_eval_rate = float(parts[3].rstrip('(').rstrip(')'))
                        inference_stats['prompt_eval_time_ms'] = prompt_eval_time
                        inference_stats['prompt_eval_rate_tokens_per_sec'] = prompt_eval_rate
                except (ValueError, IndexError):
                    pass
            elif 'eval time' in line:
                # Extract generation evaluation time
                try:
                    parts = line.split('=')[1].strip().split()
                    eval_time = float(parts[0])
                    if len(parts) > 3:
                        eval_rate = float(parts[3].rstrip('(').rstrip(')'))
                        inference_stats['eval_time_ms'] = eval_time
                        inference_stats['eval_rate_tokens_per_sec'] = eval_rate
                except (ValueError, IndexError):
                    pass
        
        # Step 6: Validate and process response
        if inference_result.returncode != 0:
            return {
                'success': False,
                'response': None,
                'error': f"llama.cpp execution failed with return code {inference_result.returncode}: {stderr_output}",
                'inference_stats': inference_stats
            }
        
        raw_response = inference_result.stdout.strip()
        
        # Remove any residual prompt formatting artifacts
        response_text = raw_response
        if "<|im_start|>" in response_text:
            # Clean up any leaked formatting tokens
            response_text = response_text.split("<|im_start|>")[-1]
            if response_text.startswith("assistant\n"):
                response_text = response_text[10:]  # Remove "assistant\n"
        
        # Validate non-empty response
        if not response_text:
            return {
                'success': False,
                'response': None,
                'error': "Model generated empty response - check prompt formatting or model compatibility",
                'inference_stats': inference_stats
            }
        
        return {
            'success': True,
            'response': response_text,
            'error': None,
            'inference_stats': {
                **inference_stats,
                'model_path': model_path,
                'quantization': 'Q8_0',
                'context_size': 4096,
                'max_tokens': 1024,
                'temperature': 0.1,
                'cpu_threads': os.cpu_count()
            }
        }
        
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'response': None,
            'error': "Inference timeout exceeded - mathematical computation too complex or model unresponsive",
            'inference_stats': {}
        }
    
    except FileNotFoundError:
        return {
            'success': False,
            'response': None,
            'error': f"llama.cpp binary not executable or missing dependencies at {llamacpp_binary}",
            'inference_stats': {}
        }
    
    except Exception as e:
        return {
            'success': False,
            'response': None,
            'error': f"Unexpected error during llama.cpp execution: {str(e)}",
            'inference_stats': {}
        }

# Computational efficiency analysis function
def analyze_inference_performance(stats: Dict[str, Any]) -> Dict[str, str]:
    """
    Analyzes llama.cpp inference performance metrics for optimization insights.
    
    Parameters:
    -----------
    stats : Dict[str, Any]
        Performance statistics from inference execution
    
    Returns:
    --------
    Dict[str, str]
        Performance analysis with optimization recommendations
    """
    analysis = {}
    
    if 'eval_rate_tokens_per_sec' in stats:
        eval_rate = stats['eval_rate_tokens_per_sec']
        if eval_rate > 50:
            analysis['generation_speed'] = "Optimal - High throughput inference"
        elif eval_rate > 20:
            analysis['generation_speed'] = "Good - Acceptable inference speed"
        else:
            analysis['generation_speed'] = "Suboptimal - Consider increasing batch size or reducing context"
    
    if 'model_load_time_ms' in stats:
        load_time = stats['model_load_time_ms']
        if load_time < 1000:
            analysis['model_loading'] = "Excellent - Fast model initialization"
        elif load_time < 5000:
            analysis['model_loading'] = "Good - Reasonable loading time"
        else:
            analysis['model_loading'] = "Slow - Consider SSD storage or memory mapping optimization"
    
    return analysis

# Example usage demonstrating mathematical reasoning capabilities
if __name__ == "__main__":
    # Verify model and binary paths exist
    model_file = "./models/qwen2.5-math-1.5b-instruct-q8_0.gguf"
    binary_path = "./llama-main"
    
    if not os.path.exists(model_file) or not os.path.exists(binary_path):
        print("Error: Missing required files")
        print(f"Model file: {model_file} - {'✓' if os.path.exists(model_file) else '✗'}")
        print(f"Binary: {binary_path} - {'✓' if os.path.exists(binary_path) else '✗'}")
        print("\nDownload instructions:")
        print("1. Compile llama.cpp: git clone https://github.com/ggerganov/llama.cpp && cd llama.cpp && make")
        print("2. Download model: wget https://huggingface.co/bartowski/Qwen2.5-Math-1.5B-Instruct-GGUF/resolve/main/Qwen2.5-Math-1.5B-Instruct-Q8_0.gguf")
        sys.exit(1)
    
    # Mathematical reasoning test case
    test_prompt = """
    Find the derivative of f(x) = 3x^4 - 2x^3 + 5x^2 - 7x + 1.
    Then evaluate this derivative at x = 2.
    Show all steps clearly.
    """
    
    result = load_qwen_math_model_and_respond(test_prompt, model_file, binary_path)
    
    if result['success']:
        print("Mathematical Solution:")
        print("=" * 50)
        print(result['response'])
        print("\nPerformance Metrics:")
        print("=" * 50)
        for key, value in result['inference_stats'].items():
            print(f"{key}: {value}")
        
        # Performance analysis
        analysis = analyze_inference_performance(result['inference_stats'])
        if analysis:
            print("\nPerformance Analysis:")
            print("=" * 50)
            for metric, assessment in analysis.items():
                print(f"{metric}: {assessment}")
    else:
        print(f"Execution failed: {result['error']}")
        sys.exit(1)