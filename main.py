from functions import dragon_hello, create_character_sheet, update_character_sheet_menu, combat, dragon_goodbye

def main():
    try:
        dragon_hello()

        def create_menu():
            print("1. Enter 1 to add a character")
            print("2. Enter 2 to update a character")
            print("3. Enter 3 to enter combat")
            print("4. Enter 4 to exit\n")
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
                print("Invalid Input - Please input 1-4")

        print("Thank you for using the Barbarian Dice Roller! \ngood bye!")

        dragon_goodbye()
        
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt caught. Exiting the program.")
        dragon_goodbye()

main()