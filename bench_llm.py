import os
import subprocess
import csv
import argparse
from pathlib import Path
import time

output_csv = "benchmark_results.csv"
command_template = "./bin/llama-cli -m {model_path} -p \"{prompt}\" -c {context} -b {batch} -t {threads}"
base_timeout = 300  # Base timeout for each benchmark in seconds

# Run benchmark with resource monitoring
def run_benchmark(model_path, batch, context, threads, prompt):
    command = command_template.format(model_path=model_path, batch=batch, context=context, threads=threads, prompt=prompt)

    try:
        print(f"Starting benchmark for model: {model_path}, batch: {batch}, context: {context}, threads: {threads}")
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Wait for the process to complete
        stdout, stderr = process.communicate(timeout=base_timeout + context // 500)

        # Ensure the process is completely terminated
        if process.poll() is None:
            process.terminate()
            process.wait()

        if process.returncode != 0:
            with open("error.log", "a") as error_log:
                error_log.write(f"Command: {command}\nError: {stderr}\n")
            return None, None, None, None, None, None

        print(f"Completed benchmark for model: {model_path}, batch: {batch}, context: {context}, threads: {threads}")

        # Extract tokens per second and evaluation time from stderr
        tokens_per_second = "N/A"
        prompt_eval_time = "N/A"
        for line in stderr.splitlines():
            if "eval time" in line and "tokens per second" in line:
                tokens_per_second = line.split(",")[-1].strip().split()[0] + " tokens per second"
            if "prompt eval time" in line and "tokens per second" in line:
                prompt_eval_time = line.split(",")[-1].strip().split()[0] + " tokens per second"

        # Extract output text from stdout
        output_text = "N/A"
        for line in stdout.splitlines():
            if line.endswith("[end of text]"):
                output_text = line.strip()

        return tokens_per_second, prompt_eval_time, None, None, output_text

    except subprocess.TimeoutExpired:
        print(f"Timeout: Benchmark for model {model_path}, batch: {batch}, context: {context}, threads: {threads} took too long.")
        process.terminate()
        process.wait()  # Ensure the process is completely terminated
        return None, None, None, None, None

def main():
    parser = argparse.ArgumentParser(description="Benchmark llama.cpp models with different batch sizes, context lengths, and thread counts.")
    parser.add_argument("-m", "--models", nargs="+", required=True, help="List of model file paths.")
    parser.add_argument("-b", "--batches", nargs="+", type=int, help="List of batch sizes (default: 512).", default=[512])
    parser.add_argument("-c", "--contexts", nargs="+", type=int, help="List of context lengths (default: 4096).", default=[4096])
    parser.add_argument("-t", "--threads", nargs="+", type=int, help="Number of threads to use (default: 4).", default=[4], choices=[1, 2, 3, 4])
    parser.add_argument("-p", "--prompt", type=str, required=True, help="Prompt to use for benchmarking.")
    args = parser.parse_args()

    results = []

    for model_path in args.models:
        for batch in args.batches:
            for context in args.contexts:
                for threads in args.threads:
                    tokens_per_second, prompt_eval_time, _, _, output_text = run_benchmark(model_path, batch, context, threads, args.prompt)
                    if tokens_per_second is not None:
                        results.append({
                            "Model": model_path,
                            "Threads": threads,
                            "Context Size": context,
                            "Batch Size": batch,
                            "Prompt Eval Time": prompt_eval_time,
                            "Evaluation Time": tokens_per_second,
                            "Output": output_text
                        })

    # Write results to CSV
    with open(output_csv, mode="w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Model", "Threads", "Context Size", "Batch Size", "Prompt Eval Time", "Evaluation Time",  "Output"])
        writer.writeheader()
        writer.writerows(results)

    # Print results to terminal without the Output column
    print(f"\nBenchmark Results:\n")
    print(f"{'Model':<30} {'Context Size':<15} {'Batch Size':<15} {'Threads':<10}{'Prompt Eval Time':<20} {'Evaluation Time':<20} ")
    print("-" * 160)
    for row in results:
        print(f"{row['Model']:<30} {row['Context Size']:<15} {row['Batch Size']:<15} {row['Threads']:<10}  {row['Prompt Eval Time']:<20} {row['Evaluation Time']:<20}")

if __name__ == "__main__":
    main()
