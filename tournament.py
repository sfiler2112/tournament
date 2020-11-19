from classes.battler import Battler
from classes.analyzer import TournamentAnalyzer
import random

# testBattler1 = Battler("ALL-AROUND", 0)
# testBattler2 = Battler("REGULAR-1", 1, 3)
# testBattler3 = Battler("REGULAR-2", 2, 1)
# testBattler4 = Battler("REGULAR-3", 3, 2)
# testBattler5 = Battler("CONTENDER", 4)


def generate_battler_groups():
    generating = True
    battler_index = 0
    battlers = []
    battler_groups = []
    while generating:
        battlers.append(Battler("ALL-AROUND", battler_index, {""}))
        battlers.append(Battler("REGULAR-1", battler_index+1, {"REGULAR-3"}))
        battlers.append(Battler("REGULAR-2", battler_index+2, {"REGULAR-1"}))
        battlers.append(Battler("REGULAR-3", battler_index+3, {"REGULAR-2"}))
        battlers.append(Battler("CONTENDER", battler_index+4, {""}))
        battlers.append(Battler("SPECIALIST", battler_index+5, {""}))
        battler_index += 6

        battler_groups.append(battlers.copy())
        battlers.clear()

        if battler_index >= 96:
            generating = False

    return battler_groups


def match_is_won(random_winner, battler):
    if random_winner < battler.chance_to_win:
        return True
    else:
        return False


# Determines a winner between two battlers.  Returns the index of the victor. Returns -1 if no victor is determined
def fight_match(battler_a, battler_b):
    random_winner = random.randrange(0, 100)
    battler_a.total_matches += 1
    battler_b.total_matches += 1

    # Battler A counters Battler B
    if battler_b.battler_type in battler_a.get_counters():

        print(battler_a.battler_type, "COUNTERS", battler_b.battler_type)
        if random_winner < battler_a.chance_to_win_counter:
            battler_a.total_wins += 1
            return battler_a.index
        else:
            battler_b.total_wins += 1
            return battler_b.index

    # Battler B counters Battler A
    elif battler_a.battler_type in battler_b.get_counters():
        print(battler_b.battler_type, "COUNTERS", battler_a.battler_type)
        if random_winner < battler_b.chance_to_win_counter:
            battler_b.total_wins += 1
            return battler_b.index
        else:
            battler_a.total_wins += 1
            return battler_a.index

    # Neither battler counters the other
    else:
        basic_win_chance = 50
        if battler_a.chance_to_win > battler_b.chance_to_win:
            chance_spread = battler_b.chance_to_win - battler_a.chance_to_win
            if random_winner < chance_spread + basic_win_chance:
                battler_a.total_wins += 1
                return battler_a.index
            else:
                battler_b.total_wins += 1
                return battler_b.index
        elif battler_a.chance_to_win < battler_b.chance_to_win:
            chance_spread = battler_b.chance_to_win - battler_a.chance_to_win
            if random_winner < chance_spread + basic_win_chance:
                battler_b.total_wins += 1
                return battler_b.index
            else:
                battler_a.total_wins += 1
                return battler_a.index
        else:

            if random_winner < basic_win_chance:
                battler_a.total_wins += 1
                return battler_a.index
            else:
                battler_b.total_wins += 1
                return battler_b.index

    return -1


def run_single_elimination(se_battlers):
    battler_counter = len(se_battlers)
    match_counter = 0

    round_banner = "\nTOURNAMENT ELIMINATION ROUND!"
    if len(se_battlers) <= 8:
        if len(se_battlers) <= 4:
            if len(se_battlers) <= 2:
                round_banner = "\nTOURNAMENT FINALS!"
            else:
                round_banner = "\nTOURNAMENT SEMIFINALS!"
        else:
            round_banner = "\nTOURNAMENT QUARTERFINALS!"

    battler_dict = {}

    for battler in se_battlers:
        battler_dict[battler.index] = battler
    if battler_counter > 1:
        print(round_banner)
        match_counter = battler_counter / 2
        winners_group = []
        fighting_matches = True
        while fighting_matches:
            battler_a = se_battlers.pop(1)
            battler_b = se_battlers.pop(0)
            winning_battler = battler_dict[fight_match(battler_a, battler_b)]
            winners_group.append(winning_battler)
            print("Match between", battler_a.battler_type, "and", battler_b.battler_type + "! Winner is",
                  winning_battler.battler_type, str(winning_battler.index))
            match_counter -= 1
            if match_counter == 0:
                fighting_matches = False
        return run_single_elimination(winners_group)
    elif battler_counter == 1:
        # This is the final winner of the whole single elimination tournament
        return se_battlers[0]


def run_round_robin(rr_battlers):
    battler_dict = {}
    for battler in rr_battlers:
        battler_dict[battler.index] = battler
    i = 0
    print("\nROUND ROBIN TOURNAMENT!")
    for battler in rr_battlers:
        battler_index = i
        while battler_index < (len(rr_battlers)-1):
            battler_index += 1
            winner_index = fight_match(battler, rr_battlers[battler_index])
            print("Match between", battler.battler_type, "and", rr_battlers[battler_index].battler_type
                  + "! Winner is", battler_dict[winner_index].battler_type, str(winner_index))
        i += 1

    winners = []
    print("\nBATTLER RESULTS:")
    for battler in rr_battlers:
        print(battler.battler_type, str(battler.index), "results:", str(battler.total_wins) + ",",
              str(battler.get_win_percentage()))
        if len(winners) == 0:
            winners.append(battler)
        elif winners[0].total_wins < battler.total_wins:
            winners.clear()
            winners.append(battler)
        elif winners[0].total_wins == battler.total_wins:
            winners.append(battler)

    print("\nWINNER:")
    for winner in winners:
        print(winner.battler_type, str(winner.index))

    if len(winners) > 1:
        print("\nAdditional round robin between winners:")
        return run_round_robin(winners)
    else:
        print("returning winner for round robin group:", winners[0].battler_type, str(winners[0].index))
        return winners[0]

    # while running:
    #     i = 0
    #     for battler in tournamentBattlers:
    #         battler_index = i
    #         while battler_index < 3:
    #             battler_index += 1
    #             winner_index = fight_match(battler, tournamentBattlers[battler_index])
    #             print("Match between", battler.battler_type, "and", tournamentBattlers[battler_index].battler_type
    #                   + "! Winner is", tournamentBattlers[winner_index].battler_type, str(winner_index))
    #         i += 1
    #
    #     running = False


def begin_tournament():
    tournament_battlers = generate_battler_groups()
    winning_battlers = []
    winning_battler_indices = []

    print("Number of groups:", str(len(tournament_battlers)))
    for battler_group in tournament_battlers:
        winner = run_round_robin(battler_group)
        print("listing winner:", winner.battler_type, str(winner.index))
        winning_battler_indices.append(winner.index)
        winning_battlers.append(winner)
    print("\nWinner's Tourney Participants:")
    for battler in winning_battlers:
        print(battler.battler_type, str(battler.index) + ":", str(battler.total_wins) + ",",
              str(battler.win_percentage))
    champion_battler = run_single_elimination(winning_battlers)
    champion_battler_index = champion_battler.index

    tournament_results_dictionary = {"battlers": tournament_battlers, "winners": winning_battler_indices, "champion":
                                     champion_battler_index}

    print("")
    print("The GRAND CHAMPION IS FOUND!", champion_battler.battler_type, str(champion_battler.index))
    print("~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~")
    return tournament_results_dictionary


def display_tournament_results(tournament_results):
    undefined_count = 0
    for group in tournament_results['battlers']:
        for battler in group:
            print(battler.battler_type, str(battler.index))
            print("    wins:", str(battler.total_wins))
            print(" matches:", str(battler.total_matches))
            print("counters:", battler.counters)
            if battler.battler_type == "UNDEFINED":
                undefined_count += 1

    print("\nNumber of undefined battlers:", str(undefined_count))

    print("\nWinners:")
    for winner in tournament_results['winners']:
        print("   ", str(winner))

    print("\nChampion:")
    print("   ", str(tournament_results['champion']))


# The following method assumes the contents of the text file being opened are properly formatted as a save file for this
# program. Each battler's information should be stored as the string output for a dict object.  The save file should
# also include the indices of the winner's tournament battlers and the index of the champion battler.
def load_tournament():
    file_name = input("\nEnter the name of an existing save file: ")
    tournament_results_dictionary = {"battlers": [], "winners": [], "champion": -1}
    try:
        file = open(file_name + ".txt", "r")
        reading_winners = False
        reading_champion = False
        group_size = 6
        battler_count = 0
        battler_group = []
        for line in file:
            if reading_winners:
                if reading_champion:
                    tournament_results_dictionary['champion'] = int(line)
                else:
                    if "CHAMPION" in line:
                        reading_champion = True
                    else:
                        tournament_results_dictionary['winners'].append(int(line))
            else:
                if "WINNERS" in line:
                    reading_winners = True
                else:
                    battler_count += 1
                    battler_stats_string = line
                    battler_stats_list = battler_stats_string.split()
                    stat_focus = ""
                    loaded_battler = Battler("UNDEFINED", -1, [""])
                    battler_stat_dict = loaded_battler.get_stats()

                    print(battler_stats_list)
                    for stat_slice in battler_stats_list:
                        stat_slice = stat_slice.strip('{}:\'\", ')
                        if stat_focus == "":
                            stat_focus = stat_slice
                        elif stat_focus != 'counters':
                            # TO DO: set the values of a battler object according to the stats and values provided.
                            print(stat_focus, stat_slice)
                            battler_stat_dict[stat_focus] = stat_slice
                            stat_focus = ""
                        else:
                            print(stat_focus, stat_slice)
                            battler_stat_dict[stat_focus].append(stat_slice)
                    loaded_battler.load_stats(battler_stat_dict)
                    battler_group.append(loaded_battler)
                    print(loaded_battler.counters)
                    if battler_count == 6:
                        tournament_results_dictionary["battlers"].append(battler_group.copy())
                        battler_group.clear()
                        battler_count = 0

        return tournament_results_dictionary

    except FileNotFoundError:
        print("file not found, ya dink!")


# The following method saves the data of each battler in the overall tournament.  This data is stored as the string
# output for a dictionary object containing all the important battler information.  One battler will be stored on each
# line.  If a line says "WINNERS\n N" where N is an integer, the next N lines will be the indices of those who
# participated in the winner's tournament.  If a line says "CHAMPION", the next line will be the index of the overall
# tournament champion.
def save_tournament(tournament_results):
    file_name = input("\nEnter a name for the save file: ")

    file = open(file_name + ".txt", "w")

    for group in tournament_results['battlers']:
        for battler in group:
            file.write(str(battler.get_stats())+"\n")

    file.write("WINNERS\n" + str(len(tournament_results['winners'])) + "\n")
    for winner_index in tournament_results['winners']:
        file.write(str(winner_index) + "\n")

    file.write("CHAMPION\n")
    file.write(str(tournament_results['champion']))

    file.close()


def analyze_tournament(tournament_results):
    t_analyzer = TournamentAnalyzer(tournament_results)
    winners_info = t_analyzer.analyze_winners()

    for key in winners_info.keys():
        print(key, ":", str(winners_info[key]))


def request_initial_input():
    user_input = input("\nEnter 1 to begin a new tournament or 2 to load save file data. To quit, enter any other "
                       "input: ")
    if user_input == str(1):
        tournament_results = begin_tournament()
    elif user_input == str(2):
        tournament_results = load_tournament()
        display_tournament_results(tournament_results)
    else:
        return

    request_input_to_save(tournament_results)


def request_input_to_save(tournament_results):
    user_input = input("\nEnter 1 to change the tournament, 2 to save the current tournament data, 3 to "
                       "analyze current tournament data.  To quit, enter any other input: ")

    if user_input == str(1):
        request_initial_input()
    elif user_input == str(2):
        save_tournament(tournament_results)
        request_input_to_save(tournament_results)
    elif user_input == str(3):
        analyze_tournament(tournament_results)
        request_input_to_save(tournament_results)
    return


def init():
    request_initial_input()


init()
# running = True
# while running:
#     user_choice = request_initial_input()
#     if user_choice == str(1):
#         tournament_results = begin_tournament()
#         user_choice = request_input_to_save()
#         if user_choice != str(1):
#             load_tournament()
#             print("Good-bye!")
#             running = False
#     else:
#         print("Good-bye!")
#         running = False
