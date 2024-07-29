import itertools
import math

# List of possible colors
colors = ['white', 'yellow', 'red', 'black']


def number_of_combinations(dice_to_select):
    return math.comb(dice_to_select + len(colors) - 1, len(colors) - 1)


def generate_combinations(dice_to_select):
    return list(itertools.combinations_with_replacement(colors, dice_to_select))


if __name__ == "__main__":
    # Number of dice to select
    dice_number = 10
    print(f"Number of combinations for {dice_number} dice: {number_of_combinations(dice_number)}")