import re
from functools import reduce
from operator import add


def check_dice_format(formula: str):
    """Returns true if a string is a valid dice formula.

    If it returns false, it prints an error message.
    """
    valid = True
    dice = [dice.strip() for dice in formula.split("+")]
    for die in dice:
        try:
            num_dice, type_die = die.split("d")
        except ValueError as e:
            print(
                f"'{die}' is not a valid die format. It should be XdY where X and Y are integers."
            )
            valid = False
            continue
        try:
            int(num_dice)
        except ValueError as e:
            print(f"'{num_dice}' should be an integer.")
            valid = False
        try:
            type_die = int(type_die)
            if type_die not in [2, 4, 6, 8, 10, 12, 20, 100]:
                raise ValueError(f"The number {type_die} is not a standard die type.")
        except ValueError as e:
            print(f"'{type_die}' should be a kind of die.")
            valid = False

    return valid


def die_format_to_ints(die_format: str):
    """Given a string "XdY", returns a tuple (X, Y) with X and Y as integers."""
    num_dice, type_die = die_format.split("d")
    num_dice = int(num_dice)
    type_die = int(type_die)
    return num_dice, type_die


def die_mean(die_format: str):
    """Return the mean for a given die format "XdY"."""
    num_dice, type_die = die_format_to_ints(die_format)
    avg = ((type_die + 1) / 2) * num_dice
    return avg


def dice_sum_mean(dice_formula: str):
    """Return the mean for a given formula of sum of dice."""
    if not check_dice_format(dice_formula):
        return 0
    dice = [dice.strip() for dice in dice_formula.split("+")]
    return reduce(add, map(die_mean, dice))


def die_std(die_format: str):
    """Return the standard deviation for a given die format "XdY"."""
    num_dice, type_die = die_format_to_ints(die_format)
    return ((num_dice**2) * (type_die**2 - 1) / 12) ** 0.5


def dice_sum_std(dice_formula: str):
    """Return the standard deviation for a given formula of sum of dice."""
    if not check_dice_format(dice_formula):
        return 0
    dice = [dice.strip() for dice in dice_formula.split("+")]
    return reduce(add, map(die_std, dice))


def formula_to_mean_eval_str(str_formula: str):
    """Eval the mean of a given formula of dice."""
    eval_str = re.sub("\d+d\d+", lambda x: f"die_mean('{x.group(0)}')", str_formula)
    return eval_str


def formula_to_std_eval_str(str_formula: str):
    """Eval the standard deviation of a given formula of dice.

    IMPORTANT: this function doesn't return the right value if there are constants in the
    formula like "6d8 + 4", this will return the correct std plus 4.
    """
    eval_str = re.sub("\d+d\d+", lambda x: f"die_std('{x.group(0)}')", str_formula)
    return eval_str


def get_dice_formula_mean(dice_formula):
    """Main function to calculate the mean of a dice formula. It checks the format and
    return the mean.
    """
    # if not check_dice_format(dice_formula):
    #    return 0
    eval_str = formula_to_mean_eval_str(dice_formula)
    return eval(eval_str)


def get_dice_formula_std(dice_formula):
    """Main function to calculate the mean of a dice formula. It checks the format and
    return the mean.

    IMPORTANT: this function doesn't return the right value if there are constants in the
    formula like "6d8 + 4", this will return the correct std plus 4. This must be fixed.
    """
    # TODO: change the eval to remove constants. Right now we're summing or subtracting constants from the std
    if not check_dice_format(dice_formula):
        return 0
    eval_str = formula_to_std_eval_str(dice_formula)
    return eval(eval_str)
