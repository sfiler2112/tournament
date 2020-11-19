from classes.battler import Battler


class TournamentAnalyzer:

    def __init__(self, tournament_data):
        self.tournament_data = tournament_data
        print(len(self.tournament_data["battlers"]))

        self.battler_tuple = ()
        for group in self.tournament_data['battlers']:
            for battler in group:
                self.battler_tuple = self.battler_tuple + (battler,)

        self.winners_dict = {}
        # for winner_index in self.tournament_data['winners']:
        #     self.winners_dict[winner_index] = self.battler_dict[winner_index]

        # self.champion_battler = self.battler_dict[tournament_data['champion']]

    def get_battler(self, index):
        return self.battler_tuple[index]

    def analyze_winners(self):
        winners_info = {}
        average_win_percentage = 0

        for index in self.tournament_data['winners']:
            current_winner = self.battler_tuple[index]
            if current_winner.battler_type in winners_info:
                winners_info[current_winner.battler_type] += 1
            else:
                winners_info[current_winner.battler_type] = 1
            average_win_percentage += current_winner.get_win_percentage()
        average_win_percentage = average_win_percentage / len(self.tournament_data['winners'])
        winners_info['awp'] = average_win_percentage

        return winners_info

