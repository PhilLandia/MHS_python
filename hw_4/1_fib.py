import time
import threading
import multiprocessing


def fibonacci(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def run_synchronous(n, runs):
    start_time = time.time()
    for _ in range(runs):
        fibonacci(n)
    return time.time() - start_time

def run_threads(n, runs):
    start_time = time.time()
    threads = []
    for _ in range(runs):
        thread = threading.Thread(target=fibonacci, args=(n,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    return time.time() - start_time

def run_processes(n, runs):
    start_time = time.time()
    processes = []
    for _ in range(runs):
        process = multiprocessing.Process(target=fibonacci, args=(n,))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    return time.time() - start_time

if __name__ == "__main__":
    n = 600000
    runs = 10

    sync_time = run_synchronous(n, runs)

    threads_time = run_threads(n, runs)

    processes_time = run_processes(n, runs)

    with open("fibonacci_timing_results.txt", "w") as file:
        file.write(f"Synchronous execution time: {sync_time:.2f} seconds\n")
        file.write(f"Threads execution time: {threads_time:.2f} seconds\n")
        file.write(f"Processes execution time: {processes_time:.2f} seconds\n")

    print(sync_time, threads_time, processes_time)
