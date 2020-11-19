import random


class Battler:

    def __init__(self, battler_type, index, counters):
        self.battler_type = battler_type
        self.index = index
        self.chance_to_win = 50
        self.chance_to_win_counter = -1
        self.total_wins = 0
        self.total_matches = 0
        self.win_percentage = 0.0
        self.counters = counters

        if battler_type == "CONTENDER":
            self.chance_to_win = 65
        elif battler_type == "ALL-AROUND":
            self.chance_to_win = 55
        elif battler_type == "SPECIALIST":
            self.chance_to_win = 40
            self.counters.add("ALL-AROUND")
            self.counters.add("CONTENDER")

            self.chance_to_win_counter = 70
        elif battler_type == "UNDEFINED":
            return
        else:
            counter_contender_chance = random.randrange(0, 3)

            if counter_contender_chance == 0:
                print(self.battler_type, str(self.index), "counters CONTENDERs!!")
                self.counters.add("CONTENDER")
            self.chance_to_win_counter = 80

    def get_counters(self):
        return self.counters

    def load_stats(self, stats):
        self.battler_type = stats['type']
        self.index = int(stats['index'])
        self.chance_to_win = int(stats['ctw'])
        self.chance_to_win_counter = int(stats['ctwc'])
        self.total_wins = int(stats['wins'])
        self.total_matches = int(stats['matches'])
        self.counters = stats['counters']

    def get_win_percentage(self):
        self.win_percentage = (self.total_wins / self.total_matches) * 100
        return self.win_percentage

    def get_stats(self):
        stats = {"type": self.battler_type,
                 "index": self.index,
                 "ctw": self.chance_to_win,
                 "ctwc": self.chance_to_win_counter,
                 "wins": self.total_wins,
                 "matches": self.total_matches,
                 "counters": self.counters}
        return stats
