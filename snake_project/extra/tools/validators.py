# Validators for all player's inputs 
import os


def validate_main_menu_selection() -> int:
    while True:
        try:
            player_input = int(input('~ '))
        except ValueError:
            print("Please, сhoose something from menu[1-7]")
            continue

        if player_input < 1 or player_input > 7:
            print("Please, сhoose something from menu[1-7]")
            continue
        else:
            os.system('cls')
            return player_input


def validate_choice_in_field_size() -> int:
    while True:
        try:
            player_input = int(input('~ '))
        except ValueError:
            print("Please, select one of the available field sizes[1-4]")
            continue
        if player_input < 1 or player_input > 4:
            print("Please, select one of the available field sizes[1-4]")
            continue
        else:
            os.system('cls')
            return player_input


def validate_choice_in_snake_length(custom=0) -> int:
    if custom == 0:
        while True:
            try:
                player_input = int(input('~ '))
            except ValueError:
                print("Please, select one variant[1-5]")
                continue

            if player_input < 1 or player_input > 5:
                print("Please, select one variant[1-5]")
                continue
            else:
                os.system('cls')
                return player_input
    else:
        while True:
            print('MIN length = 3')
            try:
                player_input = int(input('~ '))

            except ValueError:
                print("Please, set custom length [MUST BE NUMBER]")
                continue

            if player_input < 3:
                print("The entered snake length doesn't meet the requirements")
                print('Try again!')
                continue
            else:
                os.system('cls')
                return player_input


def validate_choice_in_snake_and_walls() -> int:
    while True:
        try:
            player_input = int(input('~ '))
        except ValueError:
            print('Please, choose one variant[1 or 2]')
            continue

        if player_input < 1 or player_input > 2:
            print('Please, choose one variant[1 or 2]')
            continue
        else:
            os.system('cls')
            return player_input


def validate_choice_in_color_of_snake(second_player=0) -> int:
    if second_player == 0:
        while True:
            try:
                player_input = int(input('~ '))
            except ValueError:
                print("Please, сhoose one color for the 1-st player[1-7]")
                continue

            if player_input < 1 or player_input > 7:
                print("Please, сhoose one color for the 1-st player[1-7]")
                continue
            else:
                os.system('cls')
                return player_input
    else:
        while True:
            try:
                player_input = int(input('~ '))
            except ValueError:
                print("Please, сhoose one color for the 2-nd player[1-6]")
                continue

            if player_input < 1 or player_input > 6:
                print("Please, сhoose one color for the 2-nd player[1-6]")
                continue
            else:
                os.system('cls')
                return player_input


def validate_player_input_in_speed() -> int:
    while True:
        try:
            player_input = int(input('~ '))
        except ValueError:
            print("Please, select one variant[1-3]")
            continue

        if player_input < 1 or player_input > 3:
            print("Please, select one variant[1-3]")
            continue
        else:
            os.system('cls')
            return player_input


def validate_player_input_in_game_time() -> int:
    while True:
        try:
            player_input = int(input('~ '))
        except ValueError:
            print("Please, set game time [MUST BE NUMBER]")
            continue

        if player_input < 100:
            print('MIN TIME IS 100!')
            continue
        else:
            os.system('cls')
            return player_input


def validate_after_the_game_input() -> int:
    while True:
        try:
            player_input = int(input('~ '))
        except ValueError:
            print("Please, select one variant[1-4]")
            continue

        if player_input < 1 or player_input > 4:
            print("Please, select one variant[1-4]")
            continue
        else:
            os.system('cls')
            return player_input
