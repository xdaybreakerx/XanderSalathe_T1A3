# import required functions for application
import colored
import d20
import os
import json
import math


def dragon_hello():
    print(
        r"""
        
        ,     \    /      ,        
       / \    )\__/(     / \       
      /   \  (_\  /_)   /   \      
 ____/_____\__\@  @/___/_____\____ 
|             |\../|              |
|              \VV/               |
|         ----hello----           |
|_________________________________|
 |    /\ /      \\       \ /\    | 
 |  /   V        ))       V   \  | 
 |/     `       //        '     \| 
 `              V                '
        """
    )


def dragon_goodbye():
    print(
        r"""
        
        ,     \    /      ,        
       / \    )\__/(     / \       
      /   \  (_\  /_)   /   \      
 ____/_____\__\@  @/___/_____\____ 
|             |\../|              |
|              \VV/               |
|        ----goodbye----          |
|_________________________________|
 |    /\ /      \\       \ /\    | 
 |  /   V        ))       V   \  | 
 |/     `       //        '     \| 
 `              V                '
        """
    )


def get_input(prompt, options):
    while True:
        user_input = input(prompt).lower()
        if user_input in options:
            return options[user_input]
        print("Invalid input. Please try again.\n")


def calculate_values(level):
    rage_bonus = 2 if level <= 8 else 3 if level <= 15 else 4
    attack_per_turn = 1 if level <= 4 else 2
    brutal_critical = (
        1
        if level >= 9 and level < 13
        else 2
        if level >= 13 and level < 17
        else 3
        if level >= 17
        else 0
    )
    pc_proficiency_bonus = math.ceil(1 + (level * 0.25))
    return rage_bonus, attack_per_turn, brutal_critical, pc_proficiency_bonus


def create_character_sheet():
    while True:
        pc_name = input("What is your characters name? \n")
        pc_level = int(
            get_input(f"What level is {pc_name}? \n", {str(i): i for i in range(1, 21)})
        )
        pc_strength_mod = int(
            get_input(
                f"What is {pc_name}s Strength modifier? \n",
                {str(i): i for i in range(-5, 6)},
            )
        )

        pc_weapon = get_input(
            "What weapon do you use? Choose: great(a)xe, great(s)word, or (m)aul:\n",
            {"a": "greataxe", "s": "greatsword", "m": "maul"},
        )

        (
            rage_bonus,
            attack_per_turn,
            brutal_critical,
            pc_proficiency_bonus,
        ) = calculate_values(pc_level)

        print(
            f"\nThanks for that {pc_name}. To confirm everything: \nYou are level {pc_level} with a strength modifier of {pc_strength_mod}.\n"
        )
        print(
            f"Based on your level, your rage bonus is {rage_bonus} and your proficiency bonus is {pc_proficiency_bonus}. \n"
        )
        print(
            f"Finally - like a true Barbarian you wield a {pc_weapon} to strike fear into the hearts of your enemies. \n"
        )

        char_info_check = get_input(
            "Is this all correct? (y/n) \n", {"y": True, "n": False}
        )
        if char_info_check:
            break

    char_sheet = {}
    char_sheet = {
        "level": pc_level,
        "proficiency": pc_proficiency_bonus,
        "strength_mod": pc_strength_mod,
        "rage_bonus": rage_bonus,
        "attack_per_turn": attack_per_turn,
        "brutal_critical": brutal_critical,
        "weapon": pc_weapon,
    }

    with open("char_sheet.json", "w") as json_file:
        # Write dictionary to file
        json.dump(char_sheet, json_file)


def combat_summary_file():
    # Relative path to the 'Combat_Summaries' folder in the root directory
    folder_path = "Combat_Summaries"
    os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist

    filename = "Combat_Summary_"

    i = 0
    while os.path.exists(os.path.join(folder_path, f"{filename}{i}.txt")):
        i += 1

    file_path = os.path.join(folder_path, f"{filename}{i}.txt")

    return file_path


def roll_to_hit(file_path):
    # load data from JSON
    with open("char_sheet.json", "r") as f:
        character_sheet = json.load(f)

    critical = False
    pc_strength_mod = character_sheet["strength_mod"]
    pc_proficiency_bonus = character_sheet["proficiency"]
    pc_weapon = character_sheet["weapon"]

    while True:
        roll_modifier = input(
            "Do you have (a)dvantage, (d)isadvantage or is it a (n)ormal roll?\n"
        ).lower()

        if roll_modifier.startswith("a"):
            roll_value = "2d20kh1"  # roll 2x d20, keep highest 1
            break
        elif roll_modifier.startswith("d"):
            roll_value = "2d20kl1"  # roll 2x d20, keep lowest 1
            break
        elif roll_modifier.startswith("n"):
            roll_value = "1d20"  # roll 1x d20
            break
        elif roll_modifier.startswith("t"):
            roll_value = (
                "20"  # rolls 20 - t for testing, will be removed in final version
            )
            break
        else:
            print(
                "Invalid input. Please enter (a)dvantage, (d)isadvantage, or is it a (n)ormal roll?"
            )

    roll_natural = d20.roll(roll_value)
    roll_total = roll_natural.total + pc_strength_mod + pc_proficiency_bonus

    if roll_natural.total == 20:
        critical = True
        message = "*** A natural twenty! ***\n"
    elif roll_natural.total == 1:
        message = "*** A nautral one! ***"
        # critical = False
    else:
        message = f"You roll a {roll_total} to hit! Confirm you hit enemy AC."
        # critical = False

    console_and_text_output(file_path, f"\nYou swing your {pc_weapon} - {message}\n")
    return critical


def console_and_text_output(file_path, *args, **kwargs):
    print(*args, **kwargs)  # Print to console
    with open(file_path, "a") as file:
        print(*args, **kwargs, file=file)  # Print to file
    # Code from Markus Dutschke
    # https://stackoverflow.com/questions/11325019/how-to-output-to-the-console-and-file


def combat_round(file_path):
    try:
        with open("char_sheet.json") as f:
            character_sheet = json.load(f)
        # assign variables based on json file
        pc_strength_mod = character_sheet["strength_mod"]
        pc_weapon = character_sheet["weapon"]
        pc_rage_bonus = character_sheet["rage_bonus"]
        attack_per_turn = character_sheet["attack_per_turn"]
        brutal_critical_no = str(character_sheet["brutal_critical"])

        # maths for weapon damage types
        greataxe = "1d12  + " + str(pc_strength_mod)
        greatsword = "2d6 + " + str(pc_strength_mod)
        maul = greatsword

        rage_greataxe = greataxe + str(pc_rage_bonus)
        rage_greatsword = greatsword + str(pc_rage_bonus)
        rage_maul = rage_greatsword

        critical_greataxe = greataxe + " + 1d12 + " + brutal_critical_no + "d12"
        critical_greatsword = greatsword + " + 2d6 + " + brutal_critical_no + "d6"
        critical_maul = critical_greatsword

        rage_critical_greataxe = critical_greataxe + str(pc_rage_bonus)
        rage_critical_greatsword = critical_greatsword + str(pc_rage_bonus)
        rage_critical_maul = rage_critical_greatsword

        # initialise variables for Rage tracking, and round tracking
        rage_status = False
        rage_counter = 0
        round_number = 1
        result = 0

        while True:
            console_and_text_output(file_path, f"\nRound {round_number} of Combat\n")
            for attack in range(1, attack_per_turn + 1):
                console_and_text_output(file_path, f"Attack {attack}:\n")
                critical = roll_to_hit(file_path)

                if pc_weapon == "greataxe":
                    result = d20.roll(greataxe)
                    if critical:
                        result = d20.roll(critical_greataxe)
                    if rage_status:
                        result = d20.roll(rage_greataxe)
                        if critical:
                            result = d20.roll(rage_critical_greataxe)
                    console_and_text_output(
                        file_path, f"You deal {result} slashing damage!\n"
                    )

                elif pc_weapon == "greatsword":
                    result = d20.roll(greatsword)
                    if critical:
                        result = d20.roll(critical_greatsword)
                    if rage_status:
                        result = d20.roll(rage_greatsword)
                        if critical:
                            result = d20.roll(rage_critical_greatsword)
                    console_and_text_output(
                        file_path, f"You deal {result} slashing damage!\n"
                    )

                elif pc_weapon == "maul":
                    result = d20.roll(maul)
                    if critical:
                        result = d20.roll(critical_maul)
                    if rage_status:
                        result = d20.roll(rage_maul)
                        if critical:
                            result = d20.roll(rage_critical_maul)
                    console_and_text_output(
                        file_path, f"You deal {result} bludgeoning damage!\n"
                    )

            # Ask the user if they want to continue to the next round
            continue_combat = input("Continue to next round? (yes/no): \n").lower()
            if continue_combat != "yes":
                console_and_text_output(file_path, "\nCombat ended.")
                break
            round_number += 1
    except FileNotFoundError:
        print(
            "We can't find your character sheet file. Please make sure you've created a character before starting combat!"
        )
        return
    except KeyError:
        print(
            "We're missing some information in your character sheet. Can you please create it again?"
        )
        return
    except json.JSONDecodeError as e:
        print("Invalid JSON syntax:", e)


def combat():
    file_path = combat_summary_file()
    combat_round(file_path)


def update_character_sheet_menu_selector():
    print("1. Enter 1 to update your level")
    print("2. Enter 2 to update your strength modifier")
    print("3. Enter 3 to update your weapon")
    print("4. Enter 4 to exit\n")
    update_choice = input("Enter your selection: ")
    return update_choice


def update_character_sheet_menu():
    choice = update_character_sheet_menu_selector
    while True:
        update_choice = update_character_sheet_menu_selector()
        if update_choice == "1":
            update_character_sheet_level()
        elif update_choice == "2":
            update_character_sheet_strength()
        elif update_choice == "3":
            update_character_sheet_weapon()
        elif update_choice == "4":
            break
        else:
            print("Invalid Input - Please input 1-4")


def update_character_sheet_level():
    loaded_character = load_character_sheet()

    if not check_character_sheet_exists():
        return False

    pc_level = int(
        get_input(
            f"What level is your new level? \n", {str(i): i for i in range(1, 21)}
        )
    )
    rage_bonus = 0
    attack_per_turn = 0
    brutal_critical = 0
    pc_proficiency_bonus = 0

    (
        rage_bonus,
        attack_per_turn,
        brutal_critical,
        pc_proficiency_bonus,
    ) = calculate_values(pc_level)

    loaded_character["level"] = pc_level
    loaded_character["rage_bonus"] = rage_bonus
    loaded_character["attack_per_turn"] = attack_per_turn
    loaded_character["brutal_critical"] = brutal_critical
    loaded_character["proficiency"] = pc_proficiency_bonus

    with open("char_sheet.json", "w") as json_file:
        # Write dictionary to file
        json.dump(loaded_character, json_file)
    return


def update_character_sheet_strength():
    loaded_character = load_character_sheet()

    if not check_character_sheet_exists():
        return False

    pc_strength_mod = int(
        get_input(
            f"What is your new Strength modifier? \n",
            {str(i): i for i in range(-5, 6)},
        )
    )

    loaded_character["strength_mod"] = pc_strength_mod
    with open("char_sheet.json", "w") as json_file:
        json.dump(loaded_character, json_file)


def update_character_sheet_weapon():
    loaded_character = load_character_sheet()

    if not check_character_sheet_exists():
        return False

    pc_weapon = get_input(
        "What weapon do you use? Choose: great(a)xe, great(s)word, or (m)aul:\n",
        {"a": "greataxe", "s": "greatsword", "m": "maul"},
    )

    loaded_character["weapon"] = pc_weapon
    with open("char_sheet.json", "w") as json_file:
        json.dump(loaded_character, json_file)


def load_character_sheet():
    try:
        with open("char_sheet.json") as f:
            character_sheet = json.load(f)

            loaded_character = {
                "level": character_sheet["level"],
                "proficiency": character_sheet["proficiency"],
                "strength_mod": character_sheet["strength_mod"],
                "rage_bonus": character_sheet["rage_bonus"],
                "attack_per_turn": character_sheet["attack_per_turn"],
                "brutal_critical": character_sheet["brutal_critical"],
                "weapon": character_sheet["weapon"],
            }

        return loaded_character
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def check_character_sheet_exists():
    try:
        with open("char_sheet.json", "r") as json_file:
            return True
    except FileNotFoundError:
        print(
            "We can't find your character sheet file. Please make sure you've created a character before proceeding."
        )
        return False
