import numpy as np
import pandas as pd
import pickle
from datetime import datetime

from combo_generator import generate_combinations
from dice import play_many_hands_with_fixed_dice_type
from make_probabilities import generate_pdf_and_ccdf


if __name__ == '__main__':
    """
    Run through many different possible combinations of dice, reroll amonts
    Save the data from the resulting simulations to pickle files
    """
    results = []
    max_dice = 1
    max_rerolls = 0
    hands_played_per_combo = int(1e6)

    for dice_count in np.arange(1, max_dice + 1):
        combinations = generate_combinations(dice_count)
        print(f'** Number of combinations for {dice_count} dice: {len(combinations)}')
        for current_reroll in np.arange(0, max_rerolls + 1):
            print(f'* Rerolls set to {current_reroll}')
            for dice_combination in combinations:
                df = play_many_hands_with_fixed_dice_type(dice_combination, current_reroll, hands_played_per_combo)

                expected_value = df['value'].mean()
                miss_rate = df['missed'].mean()

                print(f'Combination {dice_combination} - Expected value: {expected_value} - Miss rate: {miss_rate}')
                results.append({
                    'combination': dice_combination,
                    'expected_value': expected_value,
                    'miss_rate': miss_rate,
                    'rerolls': current_reroll,
                    'result_df': generate_pdf_and_ccdf(df['value'])
                })

    # print current time
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # pickle the results
    filename = f"results_maxDice{max_dice}-maxRerolls{max_rerolls}.pkl"
    with open(filename, 'wb') as f:
        pickle.dump(results, f, protocol=pickle.HIGHEST_PROTOCOL)
        print(f"Results saved to {filename}")