import pytest
import json
import functions
from unittest.mock import patch, mock_open


#  test, test, is pytest on?
def test_basic():
    assert "" == ""

# as this function is not critical to app functionality this is a simple test to ensure that it does not return an empty string.
def test_dragon_hello():
    assert functions.dragon_hello != ""

# as this function is not critical to app functionality this is a simple test to ensure that it does not return an empty string.
def test_dragon_goodbye():
    assert functions.dragon_goodbye != ""

# The following three functions test the create_character_sheet() function with different value sets to ensure it calculates correctly across level 1-20
# The order of questions asked are: "character name", "character level", "character strength modifier", "weapon choice", "confirm input (y)"
# Each test case is designed to validate user input against expected values that are manually calculated.

def test_create_char_sheet_json_low():
    with patch("builtins.input", side_effect=["character_name", "1", "-1", "m", "y"]):
        functions.create_character_sheet()

    with open("char_sheet.json", "r") as file:
        data = json.load(file)

    expected_data = {
        "level": 1,
        "proficiency": 2,
        "strength_mod": -1,
        "rage_bonus": 2,
        "attack_per_turn": 1,
        "brutal_critical": 0,
        "weapon": "maul",
    }

    assert data == expected_data

def test_create_char_sheet_json_med():
    with patch("builtins.input", side_effect=["character_name", "10", "3", "s", "y"]):
        functions.create_character_sheet()

    with open("char_sheet.json", "r") as file:
        data = json.load(file)

    expected_data = {
        "level": 10,
        "proficiency": 4,
        "strength_mod": 3,
        "rage_bonus": 3,
        "attack_per_turn": 2,
        "brutal_critical": 1,
        "weapon": "greatsword",
    }

    assert data == expected_data

def test_create_char_sheet_json_high():
    with patch("builtins.input", side_effect=["character_name", "20", "5", "a", "y"]):
        functions.create_character_sheet()

    with open("char_sheet.json", "r") as file:
        data = json.load(file)

    expected_data = {
        "level": 20,
        "proficiency": 6,
        "strength_mod": 5,
        "rage_bonus": 4,
        "attack_per_turn": 2,
        "brutal_critical": 3,
        "weapon": "greataxe",
    }

    assert data == expected_data

# The following test confirms that if the combat() function is called without a character sheet file created that the FileNotFoundError is captured correctly and provided to the user.
# If the character sheet cannot be found, the program should call the check_character_sheet_exists() functions which outputs a message to the console. 
# This test confirms that the phrase "can't find your character sheet file" is contained within the console output. 
def test_file_not_found_combat_handling(capsys):
    with patch("functions.open", mock_open()) as mock_file:
        mock_file.side_effect = FileNotFoundError
        functions.combat()
        captured = capsys.readouterr()
        assert "can't find your character sheet file" in captured.out

# The following test confirms that if the combat() function is called with the character sheet present it completes the first round of combat successfully.
def test_file_found_combat():
    # set values for character sheet
    mock_file_data = {
        "level": 20,
        "proficiency": 6,
        "strength_mod": 5,
        "rage_bonus": 4,
        "attack_per_turn": 2,
        "brutal_critical": 3,
        "weapon": "greataxe",
    }
    # convert to JSON file
    mock_json_data = json.dumps(mock_file_data)
    
    with patch("builtins.open", mock_open(read_data=mock_json_data)):
        with patch('builtins.input', side_effect=["n", "a", "n", "a", "n"]):
            # this input string is for "(n)o rage", "(a)dvantage roll", (n)o rage", "(a)dvantage roll", "do (n)ot continue to next round"
            functions.combat()

# This test confirms that if called the combat() function will persist for multiple rounds until the user elects to end combat by pressing 'n' when prompted.
def test_combat_multiple_rounds():
    mock_file_data = {
        "level": 20,
        "proficiency": 6,
        "strength_mod": 5,
        "rage_bonus": 4,
        "attack_per_turn": 2,
        "brutal_critical": 3,
        "weapon": "greataxe",
    }
    # convert to JSON file
    mock_json_data = json.dumps(mock_file_data)
    
    with patch("builtins.open", mock_open(read_data=mock_json_data)):
        with patch('builtins.input', side_effect=["y", # yes to rage
                                                  "a", "a", "y", # continue to next round
                                                  "a", "a", "n"]): # end combat at this point
            functions.combat()

# The following two tests confirm that the Rage Counter mechanic works correctly.
# If the character is less than level 15, rage should drop after 10 rounds of combat. When this occurs a message is printed to the console. 
# If the character is greater than level 15, rage persists until end of combat.

# The hardest part of making these tests was counting the inputs for 10+ rounds of combat 눈_눈

def test_combat_rage_tracker_less_than_l15(capsys):
    mock_file_data = {
        "level": 10,
        "proficiency": 4,
        "strength_mod": 3,
        "rage_bonus": 3,
        "attack_per_turn": 2,
        "brutal_critical": 1,
        "weapon": "greatsword",
    }
    # convert to JSON file
    mock_json_data = json.dumps(mock_file_data)
    
    user_inputs = [
    "y",  # Enter rage at the start
    "a", "d", "y",  # Rounds 1-10: Attack with advantage, then disadvantage, continue to next round
    "a", "d", "y",
    "a", "d", "y",
    "a", "d", "y",
    "a", "d", "y",
    "a", "d", "y",
    "a", "d", "y",
    "a", "d", "y",
    "a", "d", "y",
    "a", "d", "y",
    "y",  # Re-enter rage in round 11
    "a", "d", "n"   # Round 11: Attack with advantage and disadvantage, then choose to end combat
]

    with patch("builtins.open", mock_open(read_data=mock_json_data)):
        with patch('builtins.input', side_effect=user_inputs):
            functions.combat()
            # as the character is < level 15, and has been in combat more than 10 rounds while raging the expected outcome is for the following message to have been outputted in the console.
            captured = capsys.readouterr()
            assert "You have been in a state of rage for 10 turns - as such you have now dropped Rage" in captured.out

def test_combat_rage_tracker_greater_than_l15(capsys):
    mock_file_data = {
        "level": 20,
        "proficiency": 6,
        "strength_mod": 5,
        "rage_bonus": 4,
        "attack_per_turn": 2,
        "brutal_critical": 3,
        "weapon": "greataxe",
    }
    # convert to JSON file
    mock_json_data = json.dumps(mock_file_data)
    
    user_inputs = [
    "y",  # Enter rage at the start
    "a", "d", "y",  # Rounds 1-10: Attack with advantage, then disadvantage, continue to next round
    "a", "d", "y",
    "a", "d", "y",
    "a", "d", "y",
    "a", "d", "y",
    "a", "d", "y",
    "a", "d", "y",
    "a", "d", "y",
    "a", "d", "y",
    "a", "d", "y",
    "a", "d", "n"   # Round 11: Attack with advantage and disadvantage, then choose to end combat
]

    with patch("builtins.open", mock_open(read_data=mock_json_data)):
        with patch('builtins.input', side_effect=user_inputs):
            functions.combat()
            # as the character is > level 15, and has been in combat more than 10 rounds while raging the expected outcome is for the following message to not have been outputted in the console as the character can continue to rage indefinitely. 
            captured = capsys.readouterr()
            assert "You have been in a state of rage for 10 turns - as such you have now dropped Rage" not in captured.out