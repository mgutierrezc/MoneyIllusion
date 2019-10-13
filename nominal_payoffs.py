import math

"""
Nominal Payoffs: This .py contains a function that can be used to
obtain the payoffs for FT2001 and PW2014

The purpose of this is to create a dynamically programmed nominal payoff table instead of hardcoding the values   
"""


def set_nominal_payoffs(others_avg_price, selling_price, role, mode):
    # Defining constants

    a = 0.5
    b = 0.6
    c = 27
    d = 1
    e = 0.05
    f = 20
    v = 40
    money = [42, 14]
    shock_period = 0
    eq_prices = dict(x=9, y=27)
    nominal_payoff = None

    # Los valores siguientes son los que ve un x e y en los demas
    eq_avg_prices_others = dict(x=21, y=15)

    delta = (others_avg_price - eq_avg_prices_others[role]) / money[shock_period]
    epsilon = selling_price / money[shock_period] - eq_prices[role] / money[
        shock_period]
    numer = v * ((1 + a * delta ** 2) / (1 + b * delta ** 2))
    denom = (1 + c * (epsilon - d * delta + e * math.atan(f * delta)))
    real_payoff = numer / denom

    if mode == 'FT':
        nominal_payoff = real_payoff * others_avg_price

    elif mode == 'PW':
        nominal_payoff = round((real_payoff + others_avg_price) * others_avg_price)

    else:
        print('Input a valid mode')

    return nominal_payoff


def nominal_payoff_table_values(player_role, game_mode):
    """
    This function generates the values for the table that should be presented to the player during the game
    in the SettingPrice template (For that reason, it should be executed before arriving to that page)
    """

    # We are going to initialize our table with a column that contains only the selling prices
    nominal_payoffs = {'Selling Price': []}
    for price in range(0, 31):
        nominal_payoffs['Selling Price'].append(price)

    # For the table, we are going to need a list with all the column names
    col_names = ['Selling Price']

    # 31 is used because range ignores the last element
    for others_avg_price in range(1, 31):

        # We are creating a column (an entry in the dict) per value of others_avg_price
        nominal_payoffs['col.{}'.format(others_avg_price)] = []

        col_names.append('col.{}'.format(others_avg_price))

        # To make the code more understandable, we are going to reference the the current column with the following var
        current_column = nominal_payoffs['col.{}'.format(others_avg_price)]

        for selling_price in range(1, 31):
            current_column.append(set_nominal_payoffs(others_avg_price, selling_price, player_role, game_mode))

    rows = zip(*nominal_payoffs[colname] for colname in col_names)
    nominal_payoffs_table = dict(rows=rows, col_names=col_names)

    return nominal_payoffs_table


nominal_payoff_table_values('x','FT')