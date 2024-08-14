import subprocess
import time
import os

def run_command(command):
    """Runs a single command and returns the result."""
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        stdout, stderr = process.communicate()
        return process.returncode, stdout, stderr
    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")
        return -1, "", str(e)
    except Exception as e:
        print(f"Exception: {e}")
        return -1, "", str(e)

def run_bot(run_duration):
    """Runs multiple commands in a loop for a certain amount of time."""
    # Commands to run
    commands = [
        [r"C:\Users\user\AppData\Local\Programs\Python\Python312\Scripts\gramaddict.exe", "run", "--config", r"C:\Users\user\accounts\sehnazz602019\config.yml"],
        [r"C:\Users\user\AppData\Local\Programs\Python\Python312\Scripts\gramaddict.exe", "run", "--config", r"C:\Users\user\accounts\sehnazz602019\config.yml"],
        [r"C:\Users\user\AppData\Local\Programs\Python\Python312\Scripts\gramaddict.exe", "run", "--config", r"C:\Users\user\accounts\sehnazz602019\config.yml"]
    ]

    start_time = time.time()  # Record the start time
    end_time = start_time + run_duration  # Calculate end time
    
    while time.time() < end_time:
        for command in commands:
            if time.time() >= end_time:
                break  # Exit the loop if time is up

            print(f"Running command: {' '.join(command)}")
            returncode, stdout, stderr = run_command(command)
            
            # Print stdout and stderr for debugging
            print("Standard Output:", stdout)
            print("Standard Error:", stderr)
            
            if returncode != 0:
                print(f"Command failed with return code {returncode}.")
                break  # Exit the loop if any command fails
        
        # Optional: Add a delay before starting the commands again
        if time.time() < end_time:
            print("Restarting commands loop in 5 seconds...")
            time.sleep(60)  # Wait before restarting the loop

def main():
    run_duration = 60 * 480   # Example: run for 10 minutes (600 seconds)
    run_bot(run_duration)

if __name__ == "__main__":
    main()
