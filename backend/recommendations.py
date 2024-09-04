import copy

class Simulation:
    def __init__(self, my_teams, my_playerboard, draft_order):
        self.my_teams = my_teams
        self.my_playerboard = my_playerboard
        self.my_draft_order = draft_order

    def find_best_available_position_players(self, available_players, drafting_team):
        teams = copy.deepcopy(self.my_teams)
        top_available_players = available_players[0:20]
        top_target_players = []
        checked_positions = []

        required_positions = []
        
        for team in teams:
            if team.team_name == drafting_team:
                required_positions = team.required_roster_positions
                for player in top_available_players:
                    for position in required_positions:
                        if position in player[5] and player not in top_target_players and position not in checked_positions:
                            top_target_players.append(player)
                            checked_positions.append(position)
                if not top_target_players:
                    top_target_players.append(top_available_players[0])
                break
        
        player_position_added = []
        recommended_players = []

        for player in top_target_players:
            player_position = ''.join([char for char in player[5] if char.isalpha()])
            if player_position not in player_position_added:
                recommended_players.append(player)
                player_position_added.append(player_position)

        return recommended_players, required_positions

    def recommend_player(self, available_players, drafting_team):
        best_available_position_players = self.find_best_available_position_players(available_players, drafting_team)
        recommended_players = best_available_position_players[0]
        required_positions = best_available_position_players[1]

        position_priority = {
            'QB': required_positions.count('QB'),
            'RB': required_positions.count('RB'),
            'WR': required_positions.count('WR'),
            'TE': required_positions.count('TE'),
            'Flex': required_positions.count('Flex'),
            'K': required_positions.count('K'),
            'DST': required_positions.count('DST')
        }

        # Sort positions by need
        sorted_positions = sorted(position_priority.items(), key=lambda x: x[1], reverse=True)
        
        target_players = []
        for position, _ in sorted_positions:
            for player in recommended_players:
                if position in player[5]:
                    target_players.append(player)

        rank = 100000
        for player in target_players:
            if player[1] < rank:
                target_player = player
                rank = player[1]

        return target_player

    def determine_picks_to_sim(self, rounds_to_sim):
        drafting_team = self.my_draft_order[0]
        occurence_count = 0
        picks_to_sim = 0

        for picks, team in enumerate(self.my_draft_order):
            if team == drafting_team:
                occurence_count += 1
                if occurence_count == rounds_to_sim + 1:
                    picks_to_sim = picks
                    break

        return picks_to_sim

    def predict_available_players(self):
        picks_to_sim_one_round = self.determine_picks_to_sim(1)
        picks_to_sim_two_rounds = self.determine_picks_to_sim(2)

        available_players_one_round = copy.deepcopy(self.my_playerboard.players)
        available_players_two_rounds = copy.deepcopy(self.my_playerboard.players)
        draft_order_one_round = copy.deepcopy(self.my_draft_order)
        draft_order_two_rounds = copy.deepcopy(self.my_draft_order)
        teams = copy.deepcopy(self.my_teams)

        for _ in range(picks_to_sim_one_round):
            for team in teams:
                if team.team_name == draft_order_one_round[0]:
                    recommended_player = self.recommend_player(available_players_one_round, draft_order_one_round[0])
                    if recommended_player:
                        available_players_one_round.remove(recommended_player)
                    del draft_order_one_round[0]
                    break
        
        for _ in range(picks_to_sim_two_rounds):
            for team in teams:
                if team.team_name == draft_order_two_rounds[0]:
                    recommended_player = self.recommend_player(available_players_two_rounds, draft_order_two_rounds[0])
                    if recommended_player:
                        available_players_two_rounds.remove(recommended_player)
                    del draft_order_two_rounds[0]
                    break

        return available_players_one_round, available_players_two_rounds

    def recommend_future_players(self):
        available_players = self.predict_available_players()
        available_players_one_round = available_players[0][0:5]
        available_players_two_rounds = available_players[1][0:5]

        return available_players_one_round, available_players_two_rounds
