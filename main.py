from colored import fg, attr
from functions import (
    dragon_hello,
    create_character_sheet,
    update_character_sheet_menu,
    combat,
    dragon_goodbye,
)


def main():
    try:
        print(f"{fg('light_goldenrod_2b')}")
        dragon_hello()

        print(f"{attr('reset')}")

        def create_menu():
            print(f"1. Enter 1 to {fg('orange_1')}add a character{attr('reset')}")
            print(f"2. Enter 2 to {fg('orange_red_1')}update a character{attr('reset')}")
            print(f"3. Enter 3 to {fg('red_1')}enter combat{attr('reset')}")
            print(f"4. Enter 4 to {fg('medium_turquoise')}exit{attr('reset')}\n")
            choice = input("Enter your selection: ")
            return choice

        users_choice = ""

        while users_choice != "4":
            users_choice = create_menu()
            if users_choice == "1":
                create_character_sheet()
            elif users_choice == "2":
                update_character_sheet_menu()
            elif users_choice == "3":
                combat()
            elif users_choice == "4":
                continue
            else:
                print("Invalid Input - Please input 1-4\n")

        print(f"Thank you for using the Barbarian Dice Roller! \ngood bye!{fg('light_red')}")

        dragon_goodbye()

    except KeyboardInterrupt:
        print(f"\nKeyboardInterrupt caught. Exiting the program.{fg('light_red')}")
        dragon_goodbye()


main()
