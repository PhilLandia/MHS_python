import math
import logging
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from time import time
import multiprocessing
import pandas as pd

def integrate_chunk(f, start, end, n_iter):
    logging.info(f"Task started for interval [{start}, {end}]")
    acc = 0
    chunk_step = (end - start) / n_iter
    for i in range(n_iter):
        acc += f(start + i * chunk_step) * chunk_step
    logging.info(f"Task finished for interval [{start}, {end}]")
    return acc

def integrate(f, a, b, *, n_jobs=1, n_iter=10000000, executor_type='thread'):
    logging.info(f"Starting integration with {n_jobs} jobs using {executor_type} executor.")

    step = (b - a) / n_iter
    chunks = [(a + i * (b - a) / n_jobs, a + (i + 1) * (b - a) / n_jobs) for i in range(n_jobs)]
    chunk_iters = n_iter // n_jobs

    if executor_type == 'thread':
        Executor = ThreadPoolExecutor
    elif executor_type == 'process':
        Executor = ProcessPoolExecutor
    else:
        raise ValueError("Invalid executor_type. Use 'thread' or 'process'.")

    with Executor(max_workers=n_jobs) as executor:
        futures = [executor.submit(integrate_chunk, f, start, end, chunk_iters) for start, end in chunks]
        results = [future.result() for future in futures]

    return sum(results)

if __name__ == "__main__":
    logging.basicConfig(filename='integration.log', level=logging.INFO,
                        format='%(asctime)s - %(message)s')

    n_iter = 1000000  # Reduced for demonstration purposes
    cpu_count = multiprocessing.cpu_count()
    jobs = list(range(1, cpu_count * 2 + 1))

    thread_results = []
    process_results = []

    for n_jobs in jobs:
        start_time = time()
        integrate(math.cos, 0, math.pi / 2, n_jobs=n_jobs, n_iter=n_iter, executor_type='thread')
        thread_duration = time() - start_time

        start_time = time()
        integrate(math.cos, 0, math.pi / 2, n_jobs=n_jobs, n_iter=n_iter, executor_type='process')
        process_duration = time() - start_time

        thread_results.append((n_jobs, thread_duration))
        process_results.append((n_jobs, process_duration))

    thread_df = pd.DataFrame(thread_results, columns=['n_jobs', 'time']).assign(executor='thread')
    process_df = pd.DataFrame(process_results, columns=['n_jobs', 'time']).assign(executor='process')
    results_df = pd.concat([thread_df, process_df])

    results_df.to_csv('execution_times.csv', index=False)

    print("Comparison data saved to 'execution_times.csv'.")
