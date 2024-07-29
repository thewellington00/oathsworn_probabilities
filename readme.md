# README

Congrats! This is the readme and you are reading it. Means I didn’t write this all in vain, sweet! 

Long story short – I played a game with a unique dice rolling dynamic called "Oathsworn Into The Deepwood." I wanted to figure out the best strategy for selecting dice and ultimately decided to simulate many different dice rolls, and build a spreadsheet, to come up with an answer.

Let’s go!

## Oathsworn dice dynamic

Ok, so here’s the quick run down on playing with dice in Oathsworn:

1. Basics
    1. You can roll as many white dice as you like but if you get 2 or more blanks, your attack misses and you do no damage. There are 2 blank sides on every die in the game.
    2. Otherwise, if you don’t miss, you add up the values of all the dice and that’s your damage done.
2. Critical Hits
    1. Each die has one side that is a “critical hit”. For each die with a critical side up, you get to roll another die of the same color and add its value to the total damage. If you get another critical, you keep on rolling baby. Blanks drawn during this “critical hit run” do not cause, or contribute to, a miss.
3. Different Color Dice
    1. There are white, yellow, red, and black dice. You can roll as many white dice as you like and depending on how many might cubes you have (what i also call “power ups”, my term not theirs), you can upgrade your white dice to the higher colors.
    2. Higher colors deal more damage (i.e. have higher numbers on them) but have the same probability of hitting a critical (i.e. 1 critical hit side) and missing (i.e. 2 blank sides) as white dice.
    3. The progression of dice, from worst to best, is white, yellow, red, and black. If you have 3 power ups, you can upgrade one die from white to black, or 2 whites to yellow and red, and so on.
4. Reroll Tokens
    1. After rolling dice, you can spend Reroll Tokens to reroll one die for each token used. The new result replaces the original die rolled.
    2. You can reroll a die that has already been rerolled if you have additional Reroll Tokens.

Basically, all this means you want to select the dice set that has the lowest likelihood of missing (i.e. getting two or more blanks) and highest probability of getting a large number. And that’s all going to depend on two key things:

- How many might cubes (aka power ups) do you have?
    - i.e. How many times can you upgrade your white dice? If you have 3 upgrades, you can do an unlimited number of white dice plus 3 yellows, or one black, or one yellow and one red, etc.
- How many Reroll Tokens do you have?
    - i.e. How many times can you reroll a die after your first roll? In the simulation, we’re assuming that you’d only use a reroll token if you missed on a roll (e.g. had 2+ blanks) and wanted to not miss.

## Running Over a Billion Simulations

To run the simulation we considered all possible combinations of 1, 2, 3, 4, 5, and 6 dice across all possible color combinations. And for each one of those combinations, we considered scenarios with 0 through 5 Rerolls. That made for 1,254 combinations in total and each combination was simulated 1 million times. Which means we simulated 1.254 billion “attacks.”

Of course, these are simulated results and not analytical results so there is a margin error to the results. Likely that margin of error goes up as more dice are simulated. 

To view the results in the google sheet click here.

## To Run a Simulation Yourself

To generate your own simulation, clone the repo and run:

```python
pip install -r requirements.txt
```

As an example, let’s say we had a dice set of 1x white, 1x yellow and 2x red dice and we had 2 Reroll Tokens. In order to simulate that 10 times, we would run the following:

```python
dice = ('white', 'yellow', 'red', 'red')
play_many_hands_with_fixed_dice_type(dice_colors=dice, rerolls=2, 10) 
```
