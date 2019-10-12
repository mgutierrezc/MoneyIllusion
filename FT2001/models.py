from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import math

author = 'Marco Gutierrez'

doc = """
Fehr and Tyran 2001 Nominal Treatment Design
"""


class Constants(BaseConstants):
    name_in_url = 'FT2001'
    players_per_group = 4
    num_rounds = 30
    # Pre and Post Shock values of the money
    money = [42, 14]
    # Shock Round
    shock_round = 15
    # Instructions
    instructions_template = 'FT2001/Instructions.html'
    calculator_template = 'FT2001/Calculator.html'
    table_template = 'FT2001/ResultsTable.html'

    # todo: Crear un config.py que tenga los valores de equilibrio para FT2001 y LP2014, y hacer que las constantes
    #  cambien para todo el juego de acuerdo a eso (con un custom session config parameter)
    # Valores de equilibrio en FT2001
    eq_prices = dict(x=9, y=27)
    # Los valores siguientes son los que ven x e y en los demas
    eq_avg_prices_others = dict(x=21, y=15)

    # Constantes de func de pagos FT2001
    a = 0.5
    b = 0.6
    c = 27
    d = 1
    e = 0.05
    f = 20
    V = 40

    confidence_choices = [
                 [1, 'Desconfío totalmente que mis expectativas sean correctas'],
                 [2, 'Desconfío mucho que mis expectativas sean correctas'],
                 [3, 'Desconfío un poco que mis expectativas sean correctas'],
                 [4, 'Confío un poco que mis expectativas sean correctas'],
                 [5, 'Confío mucho que mis expectativas sean correctas'],
                 [6, 'Confío totalmente que mis expectativas sean correctas']
                 ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    sum_prices = models.FloatField(min=0, initial=0)
    shock_period = models.IntegerField()
    total_payoff = models.CurrencyField(min=0, initial=0)

    def set_payoffs(self):
        players = self.get_players()
        con = Constants
        for player in players:

            player.others_avg_price = (self.sum_prices - player.selling_price) /(con.players_per_group - 1)
            # Definiendo func de pagos reales FT2001
            player.delta = (player.others_avg_price - con.eq_avg_prices_others[player.role()]) / con.money[self.shock_period]
            player.epsilon = player.selling_price / con.money[self.shock_period] - con.eq_prices[player.role()] / con.money[
                self.shock_period]

            player.numer = con.V * ((1 + con.a * player.delta ** 2) / (1 + con.b * player.delta ** 2))
            player.denom = (1 + con.c * ((player.epsilon - con.d * player.delta + con.e * math.atan(con.f * player.delta))**2))
            player.payoff = c(player.numer /player.denom)

        for player in players:
            self.total_payoff += player.payoff


class Player(BasePlayer):
    selling_price = models.FloatField(min=0, max=30, label='Tu precio de venta')
    others_avg_price = models.FloatField(min=0, max=30, label='Precio promedio de los demás')
    expected_price = models.FloatField(min=0, max=30, label='¿Cuál crees que sea el precio promedio de los demás?')
    delta = models.FloatField()
    epsilon = models.FloatField()
    numer = models.FloatField()
    denom = models.FloatField()
    confidence = models.IntegerField(
        choices=Constants.confidence_choices,
        label='¿Qué tanto confías en que el precio promedio que esperas que tengan los demás sea correcto?',
        widget=widgets.RadioSelect)

    def role(self):
        if (self.id_in_group == 1) or (self.id_in_group == 2):
            return 'x'
        elif (self.id_in_group == 3) or (self.id_in_group == 4):
            return 'y'

