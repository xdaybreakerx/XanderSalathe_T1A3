# Barbarian Dice Roller for D&D 5e

## Introduction
The Barbarian Dice Roller is a Python3 terminal application specially designed for Dungeons & Dragons 5e players who play the Barbarian subclass. This tool simplifies the process of rolling dice in combat, such as attacking, damage calculation, and rage tracking - allowing you to spend more time doing normal barbarian things like drinking and picking up large rocks.

## System/Hardware Requirements
- No specific hardware requirements.
- Operating System: Compatible with any OS that can run Python 3 (e.g., Windows, macOS, Linux).

- The setup scripts require Bash support. If you are in a Windows environment this is not supported natively. However, you can use either the [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/install) for Windows 10+ or other third party Bash emulators to provide this support. 
 
## Dependencies
The application requires the following Python libraries:
- `d20`: A Python library for rolling dice and resolving complex dice expressions. You can find more information on this library [here.](https://github.com/avrae/d20)
- `coloured`: A Python library for adding color to terminal text.  You can find more information on this library [here.](https://dslackw.gitlab.io/colored/)

All dependencies are automatically installed during the setup process.

## Installation Instructions
To install the Barbarian Dice Roller, follow these steps:

1. **Download the Application**: 
   Download the ZIP file of the application from the GitHub provided green ```Code``` dropdown menu, and selecting download ZIP. It is found at the upper right corner of this page.

2. **Extract the Files**: 
   Extract the contents of the ZIP file to a desired directory.

3. **Run Setup Script**:
   Open your terminal and navigate to the application's directory. Run the setup script by executing:
   ```bash
   bash setup.sh
   ```

4. **Launch the Application**:
Once the setup is complete, start the application by running:
    ```bash
    bash run.sh
    ```

5. **Usage**:

    Once the program is launched, use the parent menu to create, or update an existing character sheet. Once a valid character sheet is created, you can then enter combat. 

    - If a question asks for inputs based on a prompt with (), then the input will be the letter within the brackets. 
    - Eg, if given the option to select: great(s)word, great(a)xe, or (m)aul - the expected input is either 's', 'a', or 'm' respectively. 

    During the combat loop you can:
    - Enter Rage
    - Attack with disadvantage, advantage, or as a straight roll
    - Based on your character sheet all relevant modifiers will be calculated (eg, proficiency, strength bonus, weapon choice, etc)
    - In the event of a critical hit (die roll = 20) the damage will be calculated based on your character sheet (eg, brutal critical, extra damage dice based on weapon, etc)


## License
Distributed under the terms of the MIT License

### Thank you for using the Barbarian Dice Roller for D&D 5e!