import random
from typing import List
import pandas as pd

from make_probabilities import generate_pdf_and_ccdf

DIE_COLORS = {
    "regular": [1, 2, 3, 4, 5, 6],  # just for testing
    "white": [0, 0, 1, 1, 2, 2],
    "yellow": [0, 0, 1, 2, 3, 3],
    "red": [0, 0, 2, 3, 3, 4],
    "black": [0, 0, 3, 3, 4, 5],
}

REROLL_STRATEGIES = [
    'blanks',
]

CRITICAL_NUMBER_OF_BLANKS = 2


class Side:
    def __init__(self, value: int, is_blank: bool = False, is_crit: bool = False):
        self.value = value
        self.is_blank = is_blank
        self.is_crit = is_crit

    def __str__(self):
        return f"Side{self.value}{'-' if self.is_blank else ''}{'*' if self.is_crit else ''}"

    __repr__ = __str__


class Die:
    def __init__(self, color: str, has_blanks: bool = True, has_crits: bool = True):
        if color not in DIE_COLORS:
            raise ValueError(f"Invalid die type: {color}")

        self.color = color
        self.sides: List[Side] = []
        self.side_up = None
        self.blank_side_up = None
        self.crit_side_up = None

        is_blank_map = [True, True, False, False, False, False] if has_blanks else [False] * 6
        is_crit_map = [False, False, False, False, False, True] if has_crits else [False] * 6

        for i, value in enumerate(DIE_COLORS[color]):
            self.sides.append(Side(value, is_blank_map[i], is_crit_map[i]))

        self.roll()

    def __str__(self):
        return f"{self.color} die with {self.side_up} up"

    __repr__ = __str__

    def roll(self):
        self.side_up = random.choice(self.sides)
        self.blank_side_up = self.side_up.is_blank
        self.crit_side_up = self.side_up.is_crit

    def copy(self, has_blanks: bool = True, has_crits: bool = True):
        return Die(self.color, has_blanks, has_crits)


class Hand:
    def __init__(self, dice: List[Die], rerolls: int = 0, reroll_strategy: str = 'blanks'):
        if reroll_strategy not in REROLL_STRATEGIES:
            raise ValueError(f"Invalid reroll strategy: {reroll_strategy}")

        self.dice = dice
        self.rerolls = rerolls
        self.reroll_strategy = reroll_strategy

        # perform reroll strategy, e.g. reroll blanks if there are more than the critical number (i.e. 2)
        self.reroll()
        # resolve crits
        self.resolve_crits()

    def __str__(self):
        return f"Hand({[str(die) for die in self.dice]}, rerolls={self.rerolls})"

    __repr__ = __str__

    def __iter__(self):
        return iter(self.dice)

    def sum(self) -> int:
        if self.miss():
            return 0
        return sum(die.side_up.value for die in self.dice)

    def miss(self) -> bool:
        # A hand is a miss if there are 2 or more blanks
        return sum(die.blank_side_up for die in self.dice) >= CRITICAL_NUMBER_OF_BLANKS

    def miss_count(self) -> int:
        return sum(die.blank_side_up for die in self.dice)

    def reroll_blank_die(self):
        blank_die = next((die for die in self.dice if die.blank_side_up), None)
        if blank_die:
            blank_die.roll()

    def reroll(self):
        if self.reroll_strategy == 'blanks':
            if not self.miss():
                return
            while self.rerolls > 0:
                self.reroll_blank_die()
                self.rerolls -= 1
                if not self.miss():
                    break
        else:
            raise NotImplementedError(f"Reroll strategy '{self.reroll_strategy}' not implemented")

    def add_new_die_to_hand(self, die: Die):
        self.dice.append(die)

    def copy_and_add_new_die_to_hand(self, die: Die, has_blanks: bool = True, has_crits: bool = True):
        new_die = die.copy(has_blanks, has_crits)
        self.add_new_die_to_hand(new_die)
        return new_die

    def resolve_crits(self):
        crit_dice = [die for die in self.dice if die.crit_side_up]
        for die in crit_dice:
            new_die = self.copy_and_add_new_die_to_hand(die, has_blanks=False, has_crits=True)
            while new_die.crit_side_up:
                new_die = self.copy_and_add_new_die_to_hand(new_die, has_blanks=False, has_crits=True)


def play_many_hands_with_fixed_dice_type(
        dice_colors: tuple,
        rerolls: int = 0,
        hands_to_play: int = 100,
        has_blanks: bool = True,
        has_crits: bool = True
):
    data = []
    for _ in range(hands_to_play):
        dice = [Die(color, has_blanks=has_blanks, has_crits=has_crits) for color in dice_colors]
        hand = Hand(dice, rerolls=rerolls)
        data.append({
            'value': hand.sum(),
            'missed': hand.miss()
        })

    return pd.DataFrame(data)


if __name__ == '__main__':
    # Simulate a single, "regular", die
    regular_die = Die('regular', has_blanks=False, has_crits=False)
    print(f'one roll of a regular die: {regular_die}, side up has value: {regular_die.side_up.value}')

    # Simulate a single, "hand" of oathsworn dice
    dice_colors = ['white', 'red', 'black']
    dice = [Die(color, has_blanks=True, has_crits=True) for color in dice_colors]
    hand = Hand(dice, rerolls=0)
    print(f'current hand: {hand}')

    # Simulate many "dice hands" with the same set of dice
    df = play_many_hands_with_fixed_dice_type(
        tuple(dice_colors),
        rerolls=0,
        hands_to_play=100000
    )
    expected_value = df['value'].mean()
    miss_rate = df['missed'].mean()
    print(f'played 100,000 hands with fixed dice type: {dice_colors}')
    print(f'expected value: {expected_value}')
    print(f'miss rate: {miss_rate}')

    # check things by running a simulation with "regular" dice
    dice_colors = ['regular', 'regular']
    df = play_many_hands_with_fixed_dice_type(
        tuple(dice_colors),
        rerolls=0,
        hands_to_play=100000,
        has_blanks=False,
        has_crits=False
    )
    expected_value = df['value'].mean()
    miss_rate = df['missed'].mean()
    print(f'played 100,000 hands with fixed dice type: {dice_colors}')
    print(f'expected value (better be close to 7.0): {expected_value}')
    print(f'miss rate (by definition will be 0.0): {miss_rate}')
