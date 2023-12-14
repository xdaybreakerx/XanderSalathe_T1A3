import pytest
import json
import functions
from unittest.mock import patch, mock_open


#  test, test, is pytest on?
def test_basic():
    assert "" == ""


def test_dragon_hello():
    assert functions.dragon_hello != ""


def test_dragon_goodbye():
    assert functions.dragon_goodbye != ""

# run test with -s flag
def test_char_sheet_json():
    with patch("functions.get_input") as mock_input:
        mock_input.side_effect = ["10", "3", "greatsword", "y"]
        # level, strength_mod, weapon, charInfoCheck

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
    
def test_file_not_found_handling(capsys):
    with patch('functions.open', mock_open()) as mock_file:
        mock_file.side_effect = FileNotFoundError
        functions.combat()
        captured = capsys.readouterr()
        assert "can't find your character sheet file" in captured.out