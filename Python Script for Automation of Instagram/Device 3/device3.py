import os
import time
from threading import Thread, Lock

# Device Serial Number
device_serial = "device_serial_3"  # Replace with your actual device serial number

# List of GramAddict Commands for the Device
commands = [
    "gramaddict run --config accounts/account1_device3/config.yml",
    "gramaddict run --config accounts/account2_device3/config.yml",
    "gramaddict run --config accounts/account3_device3/config.yml"
]

# Configuration Variables
DELAY_BETWEEN_BOTS = 300  # Delay in seconds between consecutive bot executions (5 minutes)
MAX_RETRIES = 3           # Maximum number of retries for a bot if it crashes
DELAY_BETWEEN_RETRIES = 120  # Delay in seconds between retries (2 minutes)

def log(message):
    """Logs a message with a timestamp."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def run_bot(command, device, device_index, active_threads, lock):
    """
    Runs a GramAddict bot on a specific ADB device.
    If the bot stops unexpectedly, it retries running the bot up to MAX_RETRIES times.
    """
    retries = 0
    while retries <= MAX_RETRIES:
        full_command = f"adb -s {device} shell {command}"
        log(f"Starting bot on device {device}: {command} (Attempt {retries + 1})")
        exit_code = os.system(full_command)

        if exit_code == 0:
            log(f"Bot for '{command}' on device {device} finished successfully.")
            break  # Exit the retry loop on successful completion
        else:
            retries += 1
            log(f"Bot for '{command}' on device {device} stopped unexpectedly with exit code {exit_code}.")
            if retries <= MAX_RETRIES:
                log(f"Retrying in {DELAY_BETWEEN_RETRIES} seconds... (Retry {retries}/{MAX_RETRIES})")
                time.sleep(DELAY_BETWEEN_RETRIES)
            else:
                log(f"Maximum retries reached for '{command}' on device {device}. Moving to the next command.")
    
    # Delay before starting the next bot
    log(f"Waiting for {DELAY_BETWEEN_BOTS} seconds before starting the next bot.")
    time.sleep(DELAY_BETWEEN_BOTS)
    
    with lock:
        if commands:
            new_command = commands.pop(0)
            active_threads[device_index] = Thread(target=run_bot, args=(new_command, device, device_index, active_threads, lock))
            active_threads[device_index].start()
        else:
            log(f"No more commands to run for device {device}.")

def main():
    active_threads = []
    lock = Lock()

    # Start the first bot
    if commands:
        command = commands.pop(0)
        thread = Thread(target=run_bot, args=(command, device_serial, 0, active_threads, lock))
        thread.start()
        active_threads.append(thread)
        log(f"Initialized bot execution for device {device_serial}.")
    else:
        log(f"No commands found for device {device_serial}.")

    # Join all threads to ensure the script waits for them to finish
    for thread in active_threads:
        thread.join()
    log(f"All bot executions completed for device {device_serial}.")

if __name__ == "__main__":
    main()
