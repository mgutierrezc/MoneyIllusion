from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    pass


class SettingPrice(Page):
    form_model = 'player'
    form_fields = ['selling_price', 'expected_price', 'confidence']

    def before_next_page(self):
        con = Constants
        group = self.group

        # todo: Actualizar avg price al modelo de PW, porque ahora está en versión FT
        if self.round_number <= con.shock_round:
            group.shock_period = 0
        elif self.round_number > con.shock_round:
            group.shock_period = 1


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        players = self.group.get_players()
        group = self.group
        for p in players:
            group.sum_prices += p.selling_price

        self.group.set_payoffs()


class Results(Page):
    def vars_for_template(self):
        # Aux variables
        player = self.player
        players = self.group.get_players()

        # Vars for the template
        price = player.selling_price
        actual_avg_price_others = player.others_avg_price
        income = self.player.payoff
        total_income = 0  # Initializing the total_income value

        for p in players:
            total_income += p.payoff

        return dict(price=price, actual_avg=actual_avg_price_others, income=income)


page_sequence = [Introduction, SettingPrice, ResultsWaitPage, Results]
