import multiprocessing
import time
from datetime import datetime
import codecs

def log_message(message):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

def process_a(input_queue, output_queue):
    while True:
        message = input_queue.get()
        if message == "STOP":
            log_message("Process A: Stopping.")
            output_queue.put("STOP")
            break
        lower_message = message.lower()
        log_message(f"Process A: Received '{message}', transformed to '{lower_message}'.")
        output_queue.put(lower_message)
        time.sleep(5)

def process_b(input_queue, main_queue):
    while True:
        message = input_queue.get()
        if message == "STOP":
            log_message("Process B: Stopping.")
            main_queue.put("STOP")
            break
        encoded_message = codecs.encode(message, 'rot_13')
        log_message(f"Process B: Received '{message}', encoded to '{encoded_message}'.")
        print(f"{encoded_message}")
        main_queue.put(encoded_message)

def main():
    log_message("Main process: Starting.")
    input_queue = multiprocessing.Queue()
    intermediate_queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()

    process_a_proc = multiprocessing.Process(target=process_a, args=(input_queue, intermediate_queue))
    process_b_proc = multiprocessing.Process(target=process_b, args=(intermediate_queue, output_queue))

    process_a_proc.start()
    process_b_proc.start()

    try:
        while True:
            user_input = input("Enter a message (or 'STOP' to terminate): ").strip()
            if user_input:
                input_queue.put(user_input)
                if user_input == "STOP":
                    break

        process_a_proc.join()
        process_b_proc.join()

    except KeyboardInterrupt:
        log_message("Main process: Interrupted. Stopping child processes.")
        input_queue.put("STOP")
        intermediate_queue.put("STOP")

    while not output_queue.empty():
        result = output_queue.get()
        log_message(f"Main process: Received final output '{result}' from Process B.")

    log_message("Main process: Terminated.")

if __name__ == "__main__":
    main()
