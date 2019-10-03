from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import math


class Introduction(Page):
    pass


class SettingPrice(Page):
    form_model = 'player'
    form_fields = ['selling_price', 'expected_price', 'confidence']

    def before_next_page(self):
        con = Constants
        players = self.group.get_players()
        player = self.player
        group = self.group
        for p in players:
            self.group.sum_prices += p.selling_price

        # todo: Actualizar avg price al modelo de PW, porque ahora está en versión FT
        if self.round_number <= con.shock_round:
            group.shock_period = 0
        elif self.round_number > con.shock_round:
            group.shock_period = 1

        player.others_avg_price = (group.sum_prices - player.selling_price)/\
                                       (con.players_per_group-1)

        # Definiendo func de pagos reales FT2001
        delta = (player.others_avg_price/con.money[group.shock_period] - con.eq_avg_prices_others[player.role()]/con.money[group.shock_period])
        epsilon = player.selling_price/con.money[group.shock_period] - con.eq_prices[player.role()]/con.money[group.shock_period]
        player.payoff = con.V*((1+con.a*delta^2)/(1+con.b*delta^2))/\
                        (1+con.c*(epsilon-con.d*delta+con.e*math.atan(con.f*delta)))


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        pass


class Results(Page):
    def vars_for_template(self):
        # Aux variables
        player = self.player
        players = self.group.get_players()

        # Vars for the template
        price = player.selling_price
        actual_avg_price_others = player.others_avg_price
        income = self.player.payoff
        total_income = 0 # Initializing the total_income value

        for p in players:
            total_income += self.p.payoff

        return dict(price=price, actual_avg=actual_avg_price_others, income=income)


page_sequence = [Introduction, ResultsWaitPage, Results]
