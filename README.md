# Llama.cpp Benchmarking Script on Astra 

This Python script allows you to benchmark any [llama.cpp](https://github.com/ggerganov/llama.cpp) models on Synaptics Astra Machina Board.

You can benchmark any Large Language model using  [llama.cpp](https://github.com/ggerganov/llama.cpp) with different configurations of batch sizes, context lengths and thread counts. It collects Prompt Eval Time and Eval Time to a CSV file and displays them in the terminal.


## Prerequisites

- Astra SDK  `v1.2 OOBE` or higher.
- llama.cpp binary (`llama-cli`) compiled and available in the `./bin/` directory.

    Simple Steps to generate llama.cpp binary: 

    ```bash
    git clone https://github.com/ggerganov/llama.cpp
    cd llama.cpp
    cmake -B build
    cmake --build build --target llama-cli
    ```
    
- Models stored in a `models/` directory

## Usage
Run the script from same directory where `llama-cli` is stored or build 

(For eg. root@sl1680:/home/llama.cpp/build/bin#)
### Command-Line Arguments

- `-m, --models`: List of model file paths (required).
- `-b, --batches`: List of batch sizes (default: `2048`).
- `-c, --contexts`: List of context lengths (default: `4096`).
- `-t, --threads`: Number of threads to use (default: `4`, choices: `1, 2, 3, 4`).
- `-p, --prompt`: Prompt to use for benchmarking (required).

### Example Command

```bash
python3 bench_llm.py -m models/smollm2-360m-instruct-q8_0.gguf -p "Tell me about Synaptics Incorporated" -b 1024 2048 -c 512 1024 -t 4 
```

### Output

1. **CSV File**:
   Benchmark Results along with Output of LLM are saved in `benchmark_results.csv` in the following format:
   ```bash
   Model, Threads, Context Size, Batch Size, Prompt Eval Time, Evaluation Time, Output
   ```

2. **Terminal Output**:
   A summarized table without the output column(which can be accessed via csv file):
   ```
    Benchmark Results:

    Model                                    Context Size    Batch Size      Threads   Prompt Eval Time     Evaluation Time
    =============================================================================================================================
    models/smollm2-360m-instruct-q8_0.gguf   512             1024            4          36.43 t/s            23.39 t/s
    models/smollm2-360m-instruct-q8_0.gguf   1024            1024            4          36.36 t/s            23.29 t/s
    models/smollm2-360m-instruct-q8_0.gguf   512             2048            4          33.02 t/s            23.37 t/s
    models/smollm2-360m-instruct-q8_0.gguf   1024            2048            4          35.18 t/s            23.03 t/s
   ```

 
 
### Debugging
Check the `error.log` file for detailed error messages if benchmarks fail.


## Contributing

Contributions are welcome! Please fork the repository, create a new branch and submit a pull request.

## Acknowledgments

- [llama.cpp](https://github.com/ggerganov/llama.cpp) by Georgi Gerganov

 
