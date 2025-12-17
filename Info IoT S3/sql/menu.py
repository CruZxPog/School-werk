#		     █████████                  █████                    
#			 ███░░░░░███                ░░███                    
#			░███    ░███  ████████    ███████  ████████   ██████ 
#			░███████████ ░░███░░███  ███░░███ ░░███░░███ ███░░███
#			░███░░░░░███  ░███ ░███ ░███ ░███  ░███ ░░░ ░███████ 
#			░███    ░███  ░███ ░███ ░███ ░███  ░███     ░███░░░  
#			█████   █████ ████ █████░░████████ █████    ░░██████ 
#			░░░░░   ░░░░░ ░░░░ ░░░░░  ░░░░░░░░ ░░░░░      ░░░░░░ 

# Vergeet de bronnen niet toe te voegen!
# Bronnen:
# chatgpt.com (26/10)
# copilot.github.com (26/10)
# https://docs.python.org/3/library/subprocess.html#subprocess.run (26/10)
# https://docs.python.org/3/library/pathlib.html#pathlib.Path (26/10)

import sys
import subprocess # https://docs.python.org/3/library/subprocess.html#subprocess.run (26/10)
from pathlib import Path # https://docs.python.org/3/library/pathlib.html#pathlib.Path (26/10)

SCRIPTS = {
    "1": ("Add sensor reading", "add_sensor_reading.py"),
    "2": ("View sensor readings", "view_sensor_readings.py"),
    "3": ("Maintenance check", "maintenance_check.py"),
    "4": ("Customer report", "customer_report.py"),
}

def print_menu():
    print("----------------------")
    for key, (label, _) in sorted(SCRIPTS.items()):
        print(f"{key}. {label}")
    print("0. Exit")

def check_env_file():
    env_path = Path(".env")
    if not env_path.exists():
        print("Warning: .env not found in current directory.")
        sys.exit(1)

def run_script(script_filename):
    if not Path(script_filename).exists():
        print(f"Error: {script_filename} not found next to menu.py")
        return
    try:
        # Use the current Python interpreter to preserve the active venv
        result = subprocess.run([sys.executable, script_filename], check=False)
        if result.returncode != 0:
            print(f"{script_filename} exited with code {result.returncode}")
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    except Exception as error:
        print(f"Failed to run {script_filename}: {error}")

def main():
    check_env_file()
    while True:
        print_menu()
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye.")
            break
        if choice in SCRIPTS:
            label, filename = SCRIPTS[choice]
            print(f"\nRunning: {label}\n")
            run_script(filename)
            input("\nPress Enter to go back to the menu...")
        else:
            print("Invalid choice.")
            input("Press Enter to try again...")

if __name__ == "__main__":
    main()
