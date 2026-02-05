# Dark Souls 1 Remastered - Runback Automator

This is a personal student scripting project made in Python. It is used to automate runbacks in Dark Souls 1 Remastered by parsing scripts written in `.txt` files through input injection. This project was made to practice implementing best practices for a Python tool.

## Features
**Global Kill Switch:** A function is set to monitor the key press of a kill switch (Default: `HOME` key) that when activated, terminates the script and releases all inputs for safety.

**DPI-Aware Coordinate Mapping:** Uses `ctypes` to bypass Windows scaling to ensure absolute mouse movements when moving the cursor within the menu regardless of monitor resolution.

**Logging** Keep track of your runs and provides error logging.

**Informed Consent Gate:** The tool verifies system safety and administrator privileges before inputs are injected.

**Input Sanitization:** Scripts are parsed before execution to validate proper syntax.

## Motivation

I thought of making this tool when doing the Bed of Chaos and Seathe the Scaleless runback over and over on my second playthrough, and thought "Wonder if I could automate this...". 

## Use case
I recommend using this tool only after you finished the game and experienced the pain and suffering of taking 2 minutes to get back to the boss. Ironically, taking the time to map a route takes longer than just playing normally due to trial and error, so it is more so a tool for repeat playthroughs if you want to automate a runback and enjoy the challenge of scripting through trial and error.

## Disclaimer
Dark Souls 1's enemies do NOT have set behaviour. One time they might move out of your way, the next time they might lunge and kill you. Treat it like a self driving car, where you still need to have your hand on the wheel to takeover if things go awry. Due to this nature, it is recommended for longer runbacks that are less dangerous, like Bed of Chaos or Seathe the Scaleless. More dangerous runbacks with more enemies are less consistent due to RNG.

Also to be safe, use only in offline mode.

## Consistency
1. Your starting point and mouse position should be consistent when starting the script. I personally always scripted my runbacks from the state your character is in after respawning at the bonfire, that way when they died and reset, you just needed to run the script and not move your mouse or press any keys.

2. Your in-game sensitivity should be consistent as this affects the way the `move_mouse` command travels.

3. In game configuration options such as "Camera auto wall recovery" and the UI scale can affect your script in certain situations. Make sure you write your configuration for these settings in the top of the `.txt` file.

4. It is good practice to make a comment on the top of the `.txt` about your in-game sensitivity, your current roll speed (light, medium, heavy), your starting state, and your endurance stat as not meeting the requirements could make the script not work for differing builds and settings.

Ex:
```text
# REQ: Fast Roll
# REQ: 30 Endurance
# REQ: Starting point: after respawning at Firelink Shrine
# REQ: Camera auto wall recovery: ON
# REQ: UI Scale: 1.00x
```

## Video
[![Dark Souls Automator Demo](https://img.youtube.com/vi/XiqiFbVAEI0/0.jpg)](https://www.youtube.com/watch?v=XiqiFbVAEI0)

## Installation
1.  Clone the repository.
2.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Map a route with proper syntax in a `.txt` file within the `scripts/` folder.
2. Run the python file:
    ```bash
    python route_parser.py
    ```
3. Select your route within the menu and tab back into Dark Souls 1.
4. Watch your script run, and be ready to hit the kill switch key in case the enemy RNG is not on your side.

## Command list
**exit:** Presses the `esc` key. No arguments required.

**left_click:** Clicks mouse 1 down. No arguments required.

**right_click:** Clicks mouse 2 down. No arguments required.

**interact:** Presses the interact key, the default is `e`. No arguments required.

**camera_reset:** Presses the camera lock on / camera reset key, the defaults are `q`. No arguments required.

**roll_forward:** Presses the forward key and the sprint / dodge key, the defaults are `w` and `space` respectively. No arguments required.

**roll_left:** Presses the left key and the sprint / dodge key, the defaults are `a` and `space` respectively. No arguments required.

**roll_backwards:** Presses the back key and the sprint / dodge key, the defaults are `s` and `space` respectively. No arguments required.

**roll_right:** Presses the right key and the sprint / dodge key, the defaults are `d` and `space` respectively. No arguments required.

**wait:** Initiates a wait period where no inputs are executed. Requires one argument that amounts to how much time will be waited before executing the next command. Example usage: wait 3

**forward:** Presses the forward key, the default is `w`. Requires one argument that amounts to how much time the `w` key will be held. Example usage: forward 3

**left:** Presses the left key, the default is `a`. Requires one argument that amounts to how much time the `a` key will be held. Example usage: left 3

**backwards:** Presses the back key, the default is `s`. Requires one argument that amounts to how much time the `s` key will be held. Example usage: backwards 3

**right:** Presses the right key, the default is `d`. Requires one argument that amounts to how much time the `d` key will be held. Example usage: right 3 

**sprint_forward:** Presses the forward key and the sprint / dodge key, the defaults are `w` and `space` respectively. Requires one argument that amounts to how much time the `w` key and the `space` key will be held. Example usage: sprint_forward 3

**sprint_left:** Presses the left key and the sprint / dodge key, the defaults are `a` and `space` respectively. Requires one argument that amounts to how much time the `a` key and the `space` key will be held. Example usage: sprint_left 3

**sprint_backwards:** Presses the back key and the sprint / dodge key, the defaults are `s` and `space` respectively. Requires one argument that amounts to how much time the `s` key and the `space` key will be held. Example usage: sprint_backwards 3

**sprint_right:** Presses the right key and the sprint / dodge key, the defaults are `d` and `space` respectively. Requires one argument that amounts to how much time the `d` key and the `space` key will be held. Example usage: sprint_right 3

**sprint_jump_forward:** Presses the forward key and the sprint / dodge key, and then presses the jump key (Defaults: `w`, `space`, `c`). Requires two arguments: the first is how long to sprint before the jump, and the second is how long to continue sprinting after the jump. Example usage: sprint_jump_forward 3 8 (Sprints for 3 seconds, jumps, then keeps sprinting for another 8 seconds).

**sprint_jump_left:** Presses the left key and the sprint / dodge key, and then presses the jump key (Defaults: `a`, `space`, `c`). Requires two arguments: the first is how long to sprint before the jump, and the second is how long to continue sprinting after the jump. Example usage: sprint_jump_left 3 8

**sprint_jump_backwards:** Presses the back key and the sprint / dodge key, and then presses the jump key (Defaults: `s`, `space`, `c`). Requires two arguments: the first is how long to sprint before the jump, and the second is how long to continue sprinting after the jump. Example usage: sprint_jump_backwards 3 8

**sprint_jump_right:** Presses the right key and the sprint / dodge key, and then presses the jump key (Defaults: `d`, `space`, `c`). Requires two arguments: the first is how long to sprint before the jump, and the second is how long to continue sprinting after the jump. Example usage: sprint_jump_right 3 8

**move_mouse_menu:** Moves the cursor within the menu. Requires two arguments, the first being the x coordinate and the second being the y coordinate. Arguments must be between 0 and 1. Example usage: move_mouse_menu 0.3 0.2

**move_mouse:** Moves the cursor in game. Requires two arguments, the first being the x coordinate and the second being the y coordinate. Arguments must be between the negative `maximum_argument_value` and the positive `maximum_argument_value`, the default being 100000. Example usage: move_mouse 500 500

## Configuration
A `CONFIG.json` file is created on the first run. Within the menu or by editing the file directly you can change:
**Keybinds:**  Remap controls to match your in-game settings.
**Execute Delay:** Modify the start time (Default: 7)
**ASCII Art:** Toggle the ASCII art on/off.