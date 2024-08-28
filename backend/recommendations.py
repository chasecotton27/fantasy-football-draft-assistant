import copy

class Simulation:
    def __init__(self, my_teams, my_playerboard, draft_order):
        self.my_teams = my_teams
        self.my_playerboard = my_playerboard
        self.draft_order = draft_order

    def recommend_player(self):
        teams = copy.deepcopy(self.my_teams)
        drafting_team = self.draft_order[0]
        available_players = copy.deepcopy(self.my_playerboard.players)
        recommended_player = None
        player_recommended = False

        for team in teams:
            if team.team_name == drafting_team:
                target_positions = team.determine_target_positions()
                for player in available_players:
                    for position in target_positions:
                        if position in player[5]:
                            recommended_player = player
                            player_recommended = True
                            break
                    if player_recommended:
                        break
                if player_recommended:
                    break

        return recommended_player

    def determine_picks_to_sim(self, rounds_to_sim):
        drafting_team = self.draft_order[0]
        occurence_count = 0
        picks_to_sim = 0

        for picks, team in enumerate(self.draft_order):
            if team == drafting_team:
                occurence_count += 1
                if occurence_count == rounds_to_sim + 1:
                    picks_to_sim = picks
                    break

        return picks_to_sim

    def predict_available_players(self, picks_to_sim):
        available_players = copy.deepcopy(self.my_playerboard.players)
        draft_order = copy.deepcopy(self.draft_order)
        teams = copy.deepcopy(self.my_teams)

        for _ in range(picks_to_sim):
            pick_simulated = False
            for team_name in draft_order:
                for team in teams:
                    if team_name == team.team_name:
                        target_positions = team.determine_target_positions()
                        for player in available_players:
                            for position in target_positions:
                                if position in player[5]:
                                    available_players.remove(player)
                                    pick_simulated = True
                                    break
                            if pick_simulated:
                                break
                        if pick_simulated:
                            break
                if pick_simulated:
                    break

        return available_players

    def recommend_future_players(self, available_players):
        teams = copy.deepcopy(self.my_teams)
        drafting_team = self.draft_order[0]
        recommended_players = []
        players_recommended = 0
        
        for team in teams:
            if team.team_name == drafting_team:
                target_positions = team.determine_target_positions()
                for player in available_players:
                    for position in target_positions:
                        if position in player[5]:
                            recommended_players.append(player)
                            players_recommended += 1
                            break
                    if players_recommended == 5:
                        break
                if players_recommended == 5:
                    break

        return recommended_players
