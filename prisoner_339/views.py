from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduction(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1

    timeout_seconds = 100


class Decision(Page):
    form_model = models.Player
    form_fields = ['decision']


class ResultsWaitPage(WaitPage):
    body_text = 'Waiting for the other participant to choose.'

    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_payoff()


class Results(Page):
    def vars_for_template(self):
        self.player.set_payoff()

        return {
            'my_decision': self.player.decision.lower(),
            'other_player_decision': self.player.other_player().decision.lower(),
            'same_choice': self.player.decision == self.player.other_player().decision
        }


class EnterName(Page):
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    form_model = models.Player
    form_fields = ['participant_name']


class WaitForName(WaitPage):
    body_text = 'Waiting for the response of the other participant'

    wait_for_all_groups = True


class FinalResults(Page):
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):
        total_payoff = sum([p.payoff for p in self.player.in_all_rounds()])

        return {
            'selfname': self.player.participant_name,
            'othername': self.player.other_player().participant_name,
            'total_payoff': total_payoff,
            'player_in_all_rounds': self.player.in_all_rounds()
        }


page_sequence = [
    Introduction,
    Decision,
    ResultsWaitPage,
    Results,
    EnterName,
    WaitForName,
    FinalResults
]
