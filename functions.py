# import required functions for application
import colored
import d20
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


def roll_to_hit():
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

    print(f"\nYou swing your {pc_weapon} - {message}\n")
    return critical
