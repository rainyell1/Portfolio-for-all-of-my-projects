import subprocess
import time
import os

def run_bot():
    """Runs the GramAddict bot and waits for it to finish."""
    gramaddict_path = r"C:\Users\user\AppData\Local\Programs\Python\Python312\Scripts\gramaddict.exe"
    config_path = r"C:\Users\user\accounts\sehnazz602019\config.yml"
    
    # Debug print statements
    print("GramAddict Path:", gramaddict_path)
    print("Config Path:", config_path)
    
    command = [gramaddict_path, "run", "--config", config_path]
    
    try:
        # Start the process and capture stdout and stderr
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        
        # Wait for the process to finish and capture the output
        stdout, stderr = process.communicate()
        
        # Print stdout and stderr for debugging
        print("Standard Output:", stdout)
        print("Standard Error:", stderr)
        
        # Return the exit code, stdout, and stderr
        return process.returncode, stdout, stderr

    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")
        return -1, "", str(e)
    except Exception as e:
        print(f"Exception: {e}")
        return -1, "", str(e)

def main():
    while True:
        returncode, stdout, stderr = run_bot()

        if returncode == 0:
            print("Bot finished successfully.")
        else:
            print(f"Bot stopped unexpectedly with return code {returncode}.")
        
        print("Restarting the bot in 5 seconds...")
        time.sleep(5)  # Wait before restarting the bot

if __name__ == "__main__":
    main()
