from functions import dragon_hello, create_character_sheet, combat, dragon_goodbye

dragon_hello()

def app_menu():
    print("1. Enter 1 to add a character")
    print("2. Enter 2 to update a character")
    print("3. Enter 3 to enter combat")
    print("4. Enter 4 to exit\n")
    choice = input("Enter your selection: ")
    return choice

users_choice = ""

while users_choice != "4":
    users_choice = app_menu()
    if users_choice == "1":
        create_character_sheet()
    elif users_choice == "2":
        pass
    elif users_choice == "3":
        combat()
    elif users_choice == "4":
        continue
    else:
        print("Invalid Input - Please input 1-4")

print("Thank you for using the Barbarian Dice Roller! \ngood bye!")

dragon_goodbye()