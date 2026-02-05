# Importing libraries
import sys
import time
import questionary
from questionary import Separator
import os
import ctypes
from questionary import Choice
from rich.console import Console
from rich.progress import track
import pydirectinput
import logging
import json
import keyboard

# Makes script aware of DPI
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    dpi_awareness_failed = False
    dpi_error = None
except (AttributeError, OSError) as e:
    logging.warning(f"DPI Awareness could not be set: {e}. Coordinates may be inaccurate if scaling is enabled.")
    dpi_awareness_failed = True
    dpi_error = e

# Consent function
def user_consent(dpi_awareness_failed, dpi_error):
    warning_message = ("This tool makes keystrokes and mouse movements, do you consent?")
    if dpi_awareness_failed:
        warning_message += (f"\n[CRITICAL] DPI Awareness failed: {dpi_error}. Coordinates may be inaccurate. Continue anyway?")    

    if not questionary.confirm(warning_message).ask():
        return False
    
    return True

# Kill switch function
def kill_switch():
    if keyboard.is_pressed(CONFIG["keybinds"]["kill_switch_key"]):
        pydirectinput.keyUp(CONFIG["keybinds"]["sprint_dodge_key"])
        pydirectinput.keyUp(CONFIG["keybinds"]["forward_key"])
        pydirectinput.keyUp(CONFIG["keybinds"]["left_key"])
        pydirectinput.keyUp(CONFIG["keybinds"]["right_key"])
        pydirectinput.keyUp(CONFIG["keybinds"]["back_key"])
        pydirectinput.keyUp(CONFIG["keybinds"]["esc_key"])
        pydirectinput.keyUp(CONFIG["keybinds"]["interact_key"])
        pydirectinput.keyUp(CONFIG["keybinds"]["camera_lock_on_reset_key"])
        pydirectinput.keyUp(CONFIG["keybinds"]["jump_key"])
        pydirectinput.mouseUp()
        logging.warning("Kill switch activated. Exiting\n")
        print("Kill switch activated. Exiting\n")
        sys.exit()

# Sleep function that still allows kill_switch to work
def sleep_ks(duration):
    timer = 0
    while timer < duration:
        kill_switch()
        time.sleep(0.01)
        timer = timer + 0.01

# CONFIG.json function loader
def load_config():
    default_config = {
        "execute_delay": 7,
        "ascii_art": True,
        "maximum_argument_value": 100000,
        "keybinds":
            {
                "forward_key": "w",
                "left_key": "a",
                "right_key": "d",
                "back_key": "s",
                "jump_key": "c",
                "sprint_dodge_key": "space",
                "esc_key": "esc",
                "interact_key": "e",
                "camera_lock_on_reset_key": "q",
                "kill_switch_key": "home"
            }
    }
    try:
        with open("CONFIG.json", "r") as f:
            config_code = json.load(f)
            updated_config = False
            for key in default_config:
                if key not in config_code:
                    print(f"Repairing CONFIG: Missing key '{key}' added.")
                    config_code[key] = default_config[key]
                    updated_config = True
                elif key == "keybinds":
                    for bind in default_config["keybinds"]:
                        if bind not in config_code["keybinds"]:
                            print(f"Repairing CONFIG: Missing keybind '{bind}' added.")
                            config_code["keybinds"][bind] = default_config["keybinds"][bind]
                            updated_config = True
            if updated_config:
                with open("CONFIG.json", "w") as f:
                    json.dump(config_code, f, indent=4)
    except (FileNotFoundError, json.JSONDecodeError):
        with open("CONFIG.json", "w") as f:
            json.dump(default_config, f, indent=4)
        config_code = default_config
    return config_code

CONFIG = load_config()

# Save CONFIG function
def save_config():
    with open("CONFIG.json", "w") as f:
        json.dump(CONFIG, f, indent=4)

# Rebind keybinds function
def rebind_keybinds(user_input_for_keybind_menu):
    current_key = CONFIG["keybinds"][user_input_for_keybind_menu]
    print(f"Press the key you want to bind for the {user_input_for_keybind_menu}. Current key bound: {current_key}")
    sleep_ks(0.2)
    new_key = keyboard.read_key()
    CONFIG["keybinds"][user_input_for_keybind_menu] = new_key
    save_config()
    logging.info(f"Mapped {user_input_for_keybind_menu} to {new_key}.\n")
    print(f"Mapped {user_input_for_keybind_menu} to {new_key}.\n")

# Changes execute time function
def change_execute_time():
    while True:
        try:
            new_execute_time = float(input(f"Set how much time until the script runs in seconds (default value is 7 and current value is {CONFIG['execute_delay']}): "))
            if new_execute_time <= 0:
                logging.critical("Error: Please enter a positive number (e.g., 6 or 7)\n") 
                print("Error: Please enter a positive number (e.g., 6 or 7)")
            CONFIG["execute_delay"] = new_execute_time
            print(f"Execute time updated to {new_execute_time} seconds.\n")
            logging.info(f"Execute time updated to {new_execute_time} seconds.\n")
            save_config()
            break
        except ValueError:
            logging.critical("Error: Please enter a valid number (e.g., 6 or 7)\n") 
            print("Error: Please enter a valid number (e.g., 6 or 7)")

def calculate_mouse_position(x_target, y_target, screen_width, screen_height):
    x_calculation = int(round(x_target * screen_width))
    y_calculation =  int(round(y_target * screen_height))
    full_coordinates = (x_calculation, y_calculation)
    return full_coordinates

def set_ascii_art():
    if CONFIG["ascii_art"] == True:
        print("Disabled ASCII art \n")
        logging.info("Disabled ASCII art \n")
        CONFIG["ascii_art"] = False
        save_config()
    else:
        CONFIG["ascii_art"] = True
        print("Enabled ASCII art")
        logging.info("Enabled ASCII art \n")
        save_config()
    sleep_ks(1.5)

try:
    with open("log.log", "r") as f:
        log_contents = (f.read())
        number_of_previous_runs = log_contents.count("Application started")
        run_count = number_of_previous_runs + 1
except FileNotFoundError:
    pass

# Logging
logging.basicConfig(filename="log.log", level=logging.INFO,
    format=f"[Run {run_count}]%(asctime)s:%(levelname)s:%(message)s")

# Checks to see if Python is running as administrator
def admin_check():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
    
if not admin_check():
    logging.critical("Error: Run this script as a administrator in order for it to work in Dark Souls 1 Remastered!\n")
    print("Error: Run this script as a administrator in order for it to work in Dark Souls 1 Remastered!\n")
    sys.exit()

# Movement key function
def movement(direction_key, duration):
    pydirectinput.keyDown(direction_key)
    sleep_ks(duration)
    pydirectinput.keyUp(direction_key)

# Sprint movement key function
def sprint_movement(direction_key, duration):
    pydirectinput.keyDown(direction_key)
    pydirectinput.keyDown(CONFIG["keybinds"]["sprint_dodge_key"])
    sleep_ks(duration)
    pydirectinput.keyUp(CONFIG["keybinds"]["sprint_dodge_key"])
    pydirectinput.keyUp(direction_key)

# Roll movement key function
def roll_movement(direction_key):
    pydirectinput.keyDown(direction_key)
    pydirectinput.keyDown(CONFIG["keybinds"]["sprint_dodge_key"])
    pydirectinput.keyUp(CONFIG["keybinds"]["sprint_dodge_key"])
    pydirectinput.keyUp(direction_key)

# Sprint jump movement key function
def sprint_jump_movement(direction_key, duration_until_jump, duration):
    pydirectinput.keyDown(direction_key)
    pydirectinput.keyDown(CONFIG["keybinds"]["sprint_dodge_key"])
    sleep_ks(duration_until_jump)
    pydirectinput.keyDown(CONFIG["keybinds"]["jump_key"])
    pydirectinput.keyUp(CONFIG["keybinds"]["jump_key"])
    sleep_ks(duration)
    pydirectinput.keyUp(CONFIG["keybinds"]["sprint_dodge_key"])     
    pydirectinput.keyUp(direction_key)

# Argument checker function
def argument_checker(words, word_count, command_name, valid_commands, command_count):
    number_of_arguments = word_count - 1

    if number_of_arguments != valid_commands[command_name]:
        if number_of_arguments > valid_commands[command_name]:
            print(f"The command {command_count}: {command_name} has too many arguments. Expected argument amount: {valid_commands[command_name]}")
            logging.error((f"The command {command_count}: {command_name} has too many arguments. Expected argument amount: {valid_commands[command_name]}"))
            return False
        elif number_of_arguments < valid_commands[command_name]:
            print(f"The command {command_count}: {command_name} does not have enough arguments. Expected argument amount: {valid_commands[command_name]}")
            logging.error((f"The command {command_count}: {command_name} does not have enough arguments. Expected argument amount: {valid_commands[command_name]}"))
            return False

    if number_of_arguments > 0:
        maximum_argument_value = CONFIG["maximum_argument_value"]
        negative_maximum_argument_value = -CONFIG["maximum_argument_value"]
        try:
            float(words[1])
            if command_name == "move_mouse":
                if not float(negative_maximum_argument_value) <= float(words[1]) <= float((CONFIG["maximum_argument_value"])):
                    print(f"Error: The argument {words[1]} for {command_count}: {command_name} must be between {negative_maximum_argument_value} and {maximum_argument_value}.")
                    logging.error(f"The argument {words[1]} for {command_count}: {command_name} must be between {negative_maximum_argument_value} and {maximum_argument_value}.")
                    return False
            elif command_name == "move_mouse_menu":
                if not float(0) <= float(words[1]) <= float(1):
                    print(f"Error: The argument {words[1]} for {command_count}: {command_name} must be a between 0 and 1.")
                    logging.error(f"The argument {words[1]} for {command_count}: {command_name} must be between 0 and 1.")
                    return False
            elif not float(0) <= float(words[1]) <= float((CONFIG["maximum_argument_value"])):
                print(f"Error: The argument {words[1]} for {command_count}: {command_name} must be a between 0 and {(CONFIG['maximum_argument_value'])}.")
                logging.error(f"The argument {words[1]} for {command_count}: {command_name} must be between 0 and {(CONFIG['maximum_argument_value'])}.")
                return False
        except ValueError:
            print(f"Error: The argument {words[1]} for {command_count}: {command_name} must be a number.")
            logging.error(f"The argument {words[1]} for {command_count}: {command_name} must be a number.")
            return False
        try:
            if number_of_arguments == 2:
                float(words[2])
                if command_name == "move_mouse":
                    if not float(negative_maximum_argument_value) <= float(words[2]) <= float((CONFIG["maximum_argument_value"])):
                        print(f"Error: The argument {words[1]} for {command_count}: {command_name} must be between {negative_maximum_argument_value} and {maximum_argument_value}.")
                        logging.error(f"The argument {words[1]} for {command_count}: {command_name} must be between {negative_maximum_argument_value} and {maximum_argument_value}.")
                        return False
                elif command_name == "move_mouse_menu":
                    if not float(0) <= float(words[2]) <= float(1):
                        print(f"Error: The argument {words[2]} for {command_name} must be a between 0 and 1.")
                        logging.error(f"The argument {words[2]} for {command_name} must be between 0 and 1.")
                        return False
                elif not float(0) <= float(words[2]) <= float((CONFIG["maximum_argument_value"])):
                    print(f"Error: The argument {words[2]} for {command_name} must be a between 0 and {(CONFIG['maximum_argument_value'])}.")
                    logging.error(f"The argument {words[2]} for {command_name} must be between 0 and {(CONFIG['maximum_argument_value'])}.")
                    return False
        except ValueError:
            print(f"Error: The argument {words[2]} for {command_name} must be a number.")
            logging.error(f"The argument {words[2]} for {command_name} must be a number.")
            return False
    return True

# Runback manager function
def runback_manager(user_input):
    # Variables
    console = Console()
    commands = []
    command_count = 0
    # Valid commands
    valid_commands = {
        "exit" : 0,
        "interact" : 0, 
        "camera_reset" : 0,
        "roll_forward": 0,
        "roll_right" : 0, 
        "roll_left" : 0,
        "roll_backwards" : 0,
        "left_click" : 0,
        "right_click" : 0,
        "wait" : 1,
        "forward" : 1,
        "backwards" : 1,
        "left" : 1,
        "right" : 1, 
        "sprint_forward" : 1,
        "sprint_backwards" : 1,
        "sprint_left" : 1,
        "sprint_right" : 1, 
        "sprint_jump_forward" : 2,
        "sprint_jump_backwards" : 2,
        "sprint_jump_left" : 2,
        "sprint_jump_right" : 2,
        "move_mouse_menu" : 2, 
        "move_mouse" : 2
    }
 
    # Dictionaries
    valid_movements = {
        "forward": CONFIG["keybinds"]["forward_key"],
        "backwards": CONFIG["keybinds"]["back_key"],
        "left": CONFIG["keybinds"]["left_key"],
        "right": CONFIG["keybinds"]["right_key"],
    }

    valid_sprint_movements = {
        "sprint_forward": CONFIG["keybinds"]["forward_key"],
        "sprint_backwards": CONFIG["keybinds"]["back_key"],
        "sprint_left": CONFIG["keybinds"]["left_key"],
        "sprint_right": CONFIG["keybinds"]["right_key"],
    }

    valid_roll_movements = {
        "roll_forward": CONFIG["keybinds"]["forward_key"],
        "roll_backwards": CONFIG["keybinds"]["back_key"],
        "roll_left": CONFIG["keybinds"]["left_key"],
        "roll_right": CONFIG["keybinds"]["right_key"],
    }

    valid_sprint_jump_movements = {
        "sprint_jump_forward": CONFIG["keybinds"]["forward_key"],
        "sprint_jump_backwards": CONFIG["keybinds"]["right_key"],
        "sprint_jump_left": CONFIG["keybinds"]["left_key"],
        "sprint_jump_right": CONFIG["keybinds"]["forward_key"],
    }
    scripts_folder = "scripts"
    file_path = os.path.join(scripts_folder, user_input)
    try:
        with open(file_path, "r") as f:
            logging.info(f"Application started")
            for line in f:
                line = line.strip()
                    
                # Skip empty lines and comments
                if line == "" or line.startswith("#"):
                    continue

                # Parses commands
                words = line.split()
                word_count = len(words)
                command_name = words[0]

                if command_name not in valid_commands:
                    print(f"Validation failed: '{command_name}' is not a valid command.")
                    logging.error(f"Validation failed: '{command_name}' is not a valid command.")
                    sleep_ks(1.5)
                    return
                
                # Checks arguments
                argument_result = argument_checker(words, word_count, command_name, valid_commands, command_count)

                if not argument_result:
                    sleep_ks(3)
                    return

                # Logging to log.log
                logging.info(f"Queued command: {line}")
                
                if word_count == 1:
                    console.print(f"Command #{command_count}", style="bold underline")
                    command_count = command_count+1
                    print(line)
                    print("\n")
                    commands.append(line)
                else:
                    console.print(f"Command #{command_count}", style="bold underline")
                    command_count = command_count+1    
                    print(words)
                    print("\n") 
                    commands.append(line)
                    
    except FileNotFoundError:
        print("Error: The file was deleted or moved!")
        logging.error(f"File not found: {file_path}")
        sleep_ks(2)
        return  
        

    print("\n")
    print(f"Executing commands in {CONFIG['execute_delay']} seconds:")
    for step in track(range(int(CONFIG['execute_delay'])), description="Running..."):
        sleep_ks(1)
    # Executing 
    # TIME TO ALT TAB BACK INTO DARK SOULS 1!
    run_number = 1
    # Safety block
    pydirectinput.keyUp("alt")
    pydirectinput.keyUp("tab")

    for command in track(commands, description="Executing script"):
        kill_switch()
        # Commands requiring no variables
        if command == "exit":
            pydirectinput.keyDown(CONFIG["keybinds"]["esc_key"]),
            pydirectinput.keyUp(CONFIG["keybinds"]["esc_key"])

        elif command == "interact":
            pydirectinput.keyDown(CONFIG["keybinds"]["interact_key"])
            pydirectinput.keyUp(CONFIG["keybinds"]["interact_key"])
        
        elif command == "camera_reset":
            pydirectinput.keyDown(CONFIG["keybinds"]["camera_lock_on_reset_key"])
            pydirectinput.keyUp(CONFIG["keybinds"]["camera_lock_on_reset_key"])

        elif command in valid_roll_movements:
            actual_command = valid_roll_movements[command]
            roll_movement(actual_command)

        elif command == "left_click":
            pydirectinput.click()

        elif command == "right_click":
            pydirectinput.rightClick()
        
        # Commands requiring one variable
        if " " in command:
            command_split_into_list = command.split()
            if len(command_split_into_list) == 2:
                    try:
                        actual_command = command_split_into_list[0]
                        time_set_for_command = command_split_into_list[1]     
                        time_set_for_command = float(time_set_for_command)
                    except ValueError:
                        error_message = (f"Invalid number format in command : '{command}'")
                        logging.error(error_message)
                        print(f"Error: '{error_message}'")
                        return

                    if actual_command == "wait":
                        timer = 0
                        while timer < time_set_for_command:
                            kill_switch()
                            sleep_ks(0.1)
                            timer = timer + 0.1
                
                    elif actual_command in valid_movements:
                        grab_movement_key = valid_movements[actual_command]
                        movement(grab_movement_key, time_set_for_command)

                    elif actual_command in valid_sprint_movements:
                        grab_movement_key = valid_sprint_movements[actual_command]
                        sprint_movement(grab_movement_key, time_set_for_command)
                
            # Commands requiring two variables
            elif len(command_split_into_list) ==  3:
                try:
                    actual_command = command_split_into_list[0]
                    time_set_for_command = command_split_into_list[1]
                    time_set_for_second_command = command_split_into_list[2]     
                    time_set_for_command = float(time_set_for_command)
                    time_set_for_second_command = float(time_set_for_second_command)
                except ValueError:
                        error_message = (f"Invalid number format in command : '{command}'")
                        logging.error(error_message)
                        print(f"Error: '{error_message}'")
                        return

                if actual_command in valid_sprint_jump_movements:
                    grab_movement_key = valid_sprint_jump_movements[actual_command]
                    sprint_jump_movement(grab_movement_key, time_set_for_command, time_set_for_second_command)
                
                elif actual_command == "move_mouse":
                    x_distance = int(time_set_for_command) 
                    y_distance = int(time_set_for_second_command)
                    pydirectinput.move(x_distance, y_distance, relative=True, duration=0.1)

                elif actual_command =="move_mouse_menu":
                    screen_width, screen_height = pydirectinput.size()
                    x_target = float(time_set_for_command)
                    y_target = float(time_set_for_second_command)
                    final_coordinates = calculate_mouse_position(x_target, y_target, screen_width, screen_height)
                    pydirectinput.moveTo(final_coordinates[0], final_coordinates[1], duration=0.1)

    # Releasing inputs
    pydirectinput.keyUp(CONFIG["keybinds"]["sprint_dodge_key"])
    pydirectinput.keyUp(CONFIG["keybinds"]["forward_key"])
    pydirectinput.keyUp(CONFIG["keybinds"]["left_key"])
    pydirectinput.keyUp(CONFIG["keybinds"]["right_key"])
    pydirectinput.keyUp(CONFIG["keybinds"]["back_key"])
    pydirectinput.keyUp(CONFIG["keybinds"]["esc_key"])
    pydirectinput.keyUp(CONFIG["keybinds"]["interact_key"])
    pydirectinput.keyUp(CONFIG["keybinds"]["camera_lock_on_reset_key"])
    pydirectinput.keyUp(CONFIG["keybinds"]["jump_key"])
    pydirectinput.mouseUp()
        
    sleep_ks(1.5)

# Main menu function
def menu_function():
    # ASCII art variable
    praise_the_sun = ("""
▒█▀▀█ █▀▀█ █▀▀█ ░▀░ █▀▀ █▀▀ 　 
▒█▄▄█ █▄▄▀ █▄▄█ ▀█▀ ▀▀█ █▀▀ 　 
▒█░░░ ▀░▀▀ ▀░░▀ ▀▀▀ ▀▀▀ ▀▀▀ 　 
▀▀█▀▀ █░░█ █▀▀ 　 
░▒█░░ █▀▀█ █▀▀ 　 
░▒█░░ ▀░░▀ ▀▀▀ 　 
▒█▀▀▀█ █░░█ █▀▀▄ 
░▀▀▀▄▄ █░░█ █░░█ 
▒█▄▄▄█ ░▀▀▀ ▀░░▀
""")
    console = Console()

    # Finds the files within the folder
    if not os.path.exists("scripts"):
        os.makedirs("scripts")
    files = os.listdir("scripts")
    runback_choices = []
    
    for f in files:
        if f.endswith(".txt"):
            runback_choices.append(Choice(title=f, value=f))

    settings_choices = [
        Separator("‎"),
        Separator("--------------------Settings--------------------"),
        Choice(title="Change keybinds", shortcut_key="z", value="change_keybinds"),
        Choice(title="Set execute time", shortcut_key="x", value="adjust_time_till_execute"),
        Choice(title="Disable ASCII art / Enable ASCII art", shortcut_key="c", value="ascii_art"),
        Choice(title="Exit the program", shortcut_key="v", value="exit")
        
    ]

    options_and_settings = runback_choices + settings_choices

    try:
        while True:
            # Screen wiper
            os.system("cls" if os.name == "nt" else "clear")

            # Prints ASCII art
            if CONFIG["ascii_art"] == True:
                print(praise_the_sun,"\n")

            console.print("Dark Souls 1 Remastered - Runback Automator\n", style="bold underline")
            
            # Menu
            user_input = questionary.select(
                "Select the runback you wish to choose",
                choices=options_and_settings,
                use_shortcuts = True
            ).ask()  

            # Settings
            if user_input == "ascii_art":
                set_ascii_art()
                
            elif user_input == "exit":
                print("Resting at bonfire... Exiting \n")
                sys.exit()

            elif user_input == "change_keybinds":
                user_input_for_keybind_menu = questionary.select(
                "Select the key you wish to edit",
                choices=[
                    Choice(title = "Forward key", value = "forward_key"),
                    Choice(title = "Left key", value = "left_key"),
                    Choice(title = "Back key", value = "back_key"),
                    Choice(title = "Right key", value = "right_key"),
                    Choice(title = "Sprint / Dodge key", value = "sprint_dodge_key"),
                    Choice(title = "Jump key", value = "jump_key"),
                    Choice(title = "Interact key", value = "interact_key"),
                    Choice(title = "Camera lock-on / reset key", value = "camera_lock_on_reset_key"),
                    Choice(title = "Kill switch key", value = "kill_switch_key")
                ],
                use_shortcuts = True
                ).ask()  
                rebind_keybinds(user_input_for_keybind_menu)

            elif user_input == "adjust_time_till_execute":
                change_execute_time()
                
            elif user_input == None:
                raise KeyboardInterrupt
            
            else:
                # Chooses an option
                runback_manager(user_input)

    # Ctrl + C checker
    except KeyboardInterrupt:
        kill_switch()
        logging.warning("Kill switch activated. Exiting\n")
        print("Kill switch activated. Exiting\n")
        sys.exit()

if __name__ == "__main__":
    if not user_consent(dpi_awareness_failed, dpi_error):
        print("User declined consent. Exiting.")
        logging.info("User declined consent. Exiting.")
        sys.exit()

    # Calling menu function
    menu_function()