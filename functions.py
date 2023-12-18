# import required functions for application
from colored import fg, attr
import d20
import os
import json
import math


def dragon_hello():
    print(
        rf"""
        
        ,     \    /      ,        
       / \    )\__/(     / \       
      /   \  (_\  /_)   /   \      
 ____/_____\__\@  @/___/_____\____ 
|             |\../|              |
|              \VV/               |
|         {attr('reset')}----hello----{fg('light_goldenrod_2b')}           |
|_________________________________|
 |    /\ /      \\       \ /\    | 
 |  /   V        ))       V   \  | 
 |/     `       //        '     \| 
 `              V                '
        """
    )


def dragon_goodbye():
    print(
        rf"""
        
        ,     \    /      ,        
       / \    )\__/(     / \       
      /   \  (_\  /_)   /   \      
 ____/_____\__\@  @/___/_____\____ 
|             |\../|              |
|              \VV/               |
|        {attr('reset')}----goodbye----{fg('light_red')}          |
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
        pc_name = input(f"What is your {fg('deep_sky_blue_3a')}characters name?{attr('reset')} \n")
        pc_level = int(
            get_input(
                f"What {fg('spring_green_3a')}level{attr('reset')} is {pc_name}? \n", 
                {str(i): i for i in range(1, 21)}
            )
        )
        pc_strength_mod = int(
            get_input(
                f"What is {pc_name}s {fg('light_sea_green')}Strength modifier?{attr('reset')} \n",
                {str(i): i for i in range(-5, 6)},
            )
        )

        pc_weapon = get_input(
            f"What weapon do you use? Choose: {fg('medium_spring_green')}great(a)xe, great(s)word, or (m)aul:{attr('reset')}\n",
            {"a": "greataxe", "s": "greatsword", "m": "maul"},
        )

        (
            rage_bonus,
            attack_per_turn,
            brutal_critical,
            pc_proficiency_bonus,
        ) = calculate_values(pc_level)

        print(
            f"\nThanks for that {fg('deep_sky_blue_3a')}{pc_name}{attr('reset')}. To confirm everything: \nYou are {fg('spring_green_3a')}level {pc_level}{attr('reset')} with a strength modifier of {fg('light_sea_green')}{pc_strength_mod}{attr('reset')}.\n"
        )
        print(
            f"Based on your level, your rage bonus is {fg('dark_turquoise')}{rage_bonus}{attr('reset')} and your proficiency bonus is {fg('steel_blue_3')}{pc_proficiency_bonus}.{attr('reset')} \n"
        )
        print(
            f"Finally - like a true Barbarian you wield a {fg('medium_spring_green')}{pc_weapon}{attr('reset')} to strike fear into the hearts of your enemies. \n"
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
    folder_path = "combat_summaries"
    os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist

    filename = "combat_summary_"

    i = 0
    while os.path.exists(os.path.join(folder_path, f"{filename}{i}.txt")):
        i += 1

    file_path = os.path.join(folder_path, f"{filename}{i}.txt")

    return file_path


def roll_to_hit(file_path):
    loaded_character = load_character_sheet()

    critical = False

    while True:
        roll_modifier = input(
            f"Do you have {fg('green')}(a)dvantage{attr('reset')}, {fg('red')}(d)isadvantage{attr('reset')} or is it a {fg('blue')}(n)ormal roll?{attr('reset')}\n"
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
            roll_value = "20"  # roll 2x d20, keep highest 1
            break
        else:
            print(
                "Invalid input. Please enter (a)dvantage, (d)isadvantage, or is it a (n)ormal roll?\n"
            )

    roll_natural = d20.roll(roll_value)
    roll_total = (
        roll_natural.total
        + loaded_character["strength_mod"]
        + loaded_character["proficiency"]
    )

    if roll_natural.total == 20:
        critical = True
        message = "*** A natural twenty! ***\n"
    elif roll_natural.total == 1:
        message = "*** A nautral one! ***"
    else:
        message = f"You roll a {roll_total} to hit! Confirm you hit enemy AC."

    console_and_text_output(file_path, f"\nYou swing your {loaded_character['weapon']} - {message}\n")
    return critical


def console_and_text_output(file_path, *args, **kwargs):
    print(*args, **kwargs)  # Print to console
    with open(file_path, "a") as file:
        print(*args, **kwargs, file=file)  # Print to file
    # Code from Markus Dutschke
    # https://stackoverflow.com/questions/11325019/how-to-output-to-the-console-and-file


def combat_round(file_path):
    try:
        loaded_character = load_character_sheet()

        if not check_character_sheet_exists():
            return False

        # maths for weapon damage types
        greataxe = "1d12  + " + str(loaded_character["strength_mod"])
        greatsword = "2d6 + " + str(loaded_character["strength_mod"])
        maul = greatsword

        rage_greataxe = greataxe + " + " + (str(loaded_character["rage_bonus"]))
        rage_greatsword = greatsword + " + " + (str(loaded_character["rage_bonus"]))
        rage_maul = rage_greatsword

        critical_greataxe = (
            greataxe + " + 1d12 + " + (str(loaded_character["brutal_critical"])) + "d12"
        )
        critical_greatsword = (
            greatsword + " + 2d6 + " + (str(loaded_character["brutal_critical"])) + "d6"
        )
        critical_maul = critical_greatsword

        rage_critical_greataxe = (
            critical_greataxe + " + " + str(loaded_character["rage_bonus"])
        )
        rage_critical_greatsword = (
            critical_greatsword + " + " + str(loaded_character["rage_bonus"])
        )
        rage_critical_maul = rage_critical_greatsword

        # initialise variables for Rage tracking, and round tracking
        rage_status = False
        rage_counter = 1
        round_number = 1
        result = 0

        while True:
            console_and_text_output(file_path, f"\nRound {round_number} of Combat\n")
            for attack in range(1, loaded_character["attack_per_turn"] + 1):
                console_and_text_output(file_path, f"Attack {attack}:\n")
                if rage_status == False:
                    rage_choice = get_input(
                        f"Do you want to {fg('red')}enter rage before attacking?{attr('reset')} (y/n): ".lower(),
                        {"y": True, "n": False},
                    )
                if rage_choice == True:
                    rage_status = True

                critical = roll_to_hit(file_path)

                if loaded_character["weapon"] == "greataxe":
                    result = d20.roll(greataxe)
                    if critical:
                        result = d20.roll(critical_greataxe)
                    if rage_status:
                        result = d20.roll(rage_greataxe)
                        if critical:
                            result = d20.roll(rage_critical_greataxe)
                    console_and_text_output(
                        file_path,
                        f"You roll {result}\nDealing {result.total} slashing damage!\n",
                    )

                elif loaded_character["weapon"] == "greatsword":
                    result = d20.roll(greatsword)
                    if critical:
                        result = d20.roll(critical_greatsword)
                    if rage_status:
                        result = d20.roll(rage_greatsword)
                        if critical:
                            result = d20.roll(rage_critical_greatsword)
                    console_and_text_output(
                        file_path,
                        f"You roll {result}\nDealing {result.total} slashing damage!\n",
                    )

                elif loaded_character["weapon"] == "maul":
                    result = d20.roll(maul)
                    if critical:
                        result = d20.roll(critical_maul)
                    if rage_status:
                        result = d20.roll(rage_maul)
                        if critical:
                            result = d20.roll(rage_critical_maul)
                    console_and_text_output(
                        file_path,
                        f"You roll {result}\nDealing {result.total} bludgeoning damage!\n",
                    )

            # Ask the user if they want to continue to the next round
            continue_combat = get_input(
                "Continue to next round? (y/n): \n".lower(), {"y": True, "n": False}
            )
            if not continue_combat:
                console_and_text_output(file_path, "\nCombat ended.")
                break
            round_number += 1
            # Rage Status tracking
            if rage_status:
                rage_counter += 1
                console_and_text_output(file_path, f"\n{rage_counter} turn(s) Raging")
                if rage_counter > 10 and (loaded_character["level"] < 15):
                    rage_status = False
                    rage_counter = 1
                    print(
                        "You have been in a state of rage for 10 turns - as such you have now dropped Rage"
                    )

    except KeyError:
        print(
            "We're missing some information in your character sheet. Can you please create it again?"
        )
        return


def combat():
    file_path = combat_summary_file()
    combat_round(file_path)


def update_character_sheet_menu_selector():
    print(f"1. Enter 1 to {fg('plum_3')}update your level{attr('reset')}")
    print(f"2. Enter 2 to {fg('pink_3')}update your strength modifier{attr('reset')}")
    print(f"3. Enter 3 to {fg('purple_3')}update your weapon{attr('reset')}")
    print(f"4. Enter 4 to {fg('medium_turquoise')}exit{attr('reset')}\n")
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
