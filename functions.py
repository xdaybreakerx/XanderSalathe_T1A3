# import required functions for application
import json
import csv
import d20
import colored
import math


def create_character_sheet():
    char_info = True
    while char_info:
        pc_name = input("What is your characters name? \n")
        pc_level = int(input(f"And what level is {pc_name}? \n"))
        pc_strength_mod = int(input(f"What is {pc_name}s Strength modifier? \n"))

        while True:
            pc_weapon = input(
                "What weapon do you use? Choose: great(a)xe, great(s)word, or (m)aul:\n"
            ).lower()
            if pc_weapon[0] == "a":
                pc_weapon = "greataxe"
                break
            elif pc_weapon[0] == "s":
                pc_weapon = "greatsword"
                break
            elif pc_weapon[0] == "m":
                pc_weapon = "maul"
                break
            else:
                print(
                    "I'm sorry - I dont understand! Try '(a)xe', '(s)word', or (m)aul \n"
                )

        rage_bonus = 0
        if pc_level <= 8:
            rage_bonus = 2
        elif pc_level <= 15:
            rage_bonus = 3
        else:
            rage_bonus = 4

        attack_per_turn = 0
        if pc_level <= 4:
            attack_per_turn = 1
        else:
            attack_per_turn = 2

        brutal_critical = 0
        if pc_level >= 9 and pc_level < 13:
            brutal_critical = 1
        elif pc_level >= 13 and pc_level < 17:
            brutal_critical = 2
        else:
            brutal_critical = 3

        pc_proficiency_bonus = math.ceil(1 + (pc_level * 0.25))

        print(f"\nThanks for that {pc_name}. To confirm everything: \nYou are level {pc_level} with a strength modifier of {pc_strength_mod}. \n")
        print(f"Based on your level, your rage bonus is {rage_bonus} and your proficiency bonus is {pc_proficiency_bonus}. \n")
        print(f"Finally - like a true Barbarian you wield a {pc_weapon} to strike fear into the hearts of your enemies. \n")

        char_info_check = input(str("Is this all correct? \n")).lower()
        if char_info_check[0] == "n":
            print("Okay, let's get that information again. One more time! Let's go. \n")
            char_info
        elif char_info_check[0] == "y":
            break
        else:
            print("I'm sorry - I dont understand! Try '(y)es' or '(n)o' \n")

    char_sheet = {}
    char_sheet = {
        "pc_name": pc_name,
        "level": pc_level,
        "proficiency": pc_proficiency_bonus,
        "strength_mod": pc_strength_mod,
        "rage_bonus": rage_bonus,
        "attack_per_turn": attack_per_turn,
        "brutal_critical": brutal_critical,
        "weapon": pc_weapon,
    }

    print(char_sheet) #this is used for troubleshooting and will be removed in final version

    # Write dictionary to file
    with open("char_sheet.json", "w") as json_file:
        json.dump(char_sheet, json_file)


create_character_sheet()
