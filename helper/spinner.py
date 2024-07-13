import sys
import time
import threading

# Define the spinner animation function
def spinner_animation(stop_event):
    spinner = ['|', '/', '-', '\\']
    while not stop_event.is_set():
        for symbol in spinner:
            if stop_event.is_set():
                break
            sys.stdout.write(f'\r{symbol}')
            sys.stdout.flush()
            time.sleep(0.1)

def process_items(items):
    # Create an Event object to control the spinner thread
    stop_event = threading.Event()

    # Start the spinner in a separate thread
    spinner_thread = threading.Thread(target=spinner_animation, args=(stop_event,))
    spinner_thread.start()

    # Process the items (main loop)
    for item in items:
        # Simulate processing time
        time.sleep(1)  # Replace with actual processing code
        print(f"\rProcessing item: {item}")

    # Stop the spinner
    stop_event.set()
    spinner_thread.join()

if __name__ == "__main__":
    items = ["Item1", "Item2", "Item3", "Item4", "Item5", "Item6", "Item7", "Item8", "Item9", "Item10"]
    print("Loading...", end=' ')
    process_items(items)
    print("\nTask completed!")
