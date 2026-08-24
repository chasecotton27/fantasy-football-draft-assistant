import math

FLEX_ELIGIBLE_GROUPS = {'RB', 'WR', 'TE'}

# Which concrete position groups can fill each required roster slot. Bench maps to
# no groups since it has no scarcity of its own -- any player fills it.
CONCRETE_GROUPS_BY_SLOT = {
    'QB': {'QB'},
    'RB': {'RB'},
    'WR': {'WR'},
    'TE': {'TE'},
    'K': {'K'},
    'DST': {'DST'},
    'Flex': FLEX_ELIGIBLE_GROUPS,
    'Bench': set(),
}


# Whether a player is eligible to fill a given required roster slot. 'Flex' accepts
# RB/WR/TE and 'Bench' accepts anyone; every other slot must match the player's
# position group exactly.
def slot_matches_player(slot, player):
    if slot == 'Flex':
        return player.position_group in FLEX_ELIGIBLE_GROUPS
    if slot == 'Bench':
        return True
    return player.position_group == slot


# The set of concrete position groups (QB/RB/WR/TE/K/DST) that could fill at least
# one of the given required slots.
def needed_position_groups(required_positions):
    groups = set()
    for slot in required_positions:
        groups |= CONCRETE_GROUPS_BY_SLOT.get(slot, set())
    return groups


def best_at_position(players, position_group):
    candidates = [p for p in players if p.position_group == position_group]
    return min(candidates, key=lambda p: p.rank) if candidates else None


class Simulation:
    def __init__(self, my_teams, my_playerboard, draft_order):
        self.my_teams = my_teams
        self.my_playerboard = my_playerboard
        self.my_draft_order = draft_order

    def _find_team(self, team_name):
        for team in self.my_teams:
            if team.team_name == team_name:
                return team
        return None

    def find_best_available_position_players(self, available_players, drafting_team):
        top_available_players = available_players[:20]
        top_target_players = []
        checked_positions = []

        required_positions = []
        team = self._find_team(drafting_team)
        if team is not None:
            required_positions = team.required_roster_positions
            for player in top_available_players:
                for position in required_positions:
                    if slot_matches_player(position, player) and player not in top_target_players and position not in checked_positions:
                        top_target_players.append(player)
                        checked_positions.append(position)
            if not top_target_players and top_available_players:
                top_target_players.append(top_available_players[0])

        player_position_added = set()
        recommended_players = []
        for player in top_target_players:
            if player.position_group not in player_position_added:
                recommended_players.append(player)
                player_position_added.add(player.position_group)

        return recommended_players, required_positions

    # Simple, cheap "best rank among currently needed positions" pick. Used to model
    # opponents' picks during forward simulation and as the fallback when there's no
    # named position left to weigh (e.g. only Bench is open) -- deliberately not
    # cliff-aware, since cliff-awareness needs its own forward simulation and using
    # it here would make every simulated pick recursively simulate the whole draft.
    def recommend_player(self, available_players, drafting_team):
        recommended_players, _ = self.find_best_available_position_players(available_players, drafting_team)
        if not recommended_players:
            return None
        return min(recommended_players, key=lambda p: p.rank)

    def determine_picks_to_sim(self, rounds_to_sim):
        drafting_team = self.my_draft_order[0]
        occurence_count = 0
        for picks, team in enumerate(self.my_draft_order):
            if team == drafting_team:
                occurence_count += 1
                if occurence_count == rounds_to_sim + 1:
                    return picks
        return len(self.my_draft_order)

    # Fake-draft forward through picks_to_sim picks (using the simple, cheap
    # recommend_player for every team) and return what's left of available_players.
    def _simulate_forward(self, available_players, picks_to_sim):
        simulated_pool = list(available_players)
        simulated_order = list(self.my_draft_order)
        for _ in range(picks_to_sim):
            drafting_team = simulated_order[0]
            recommended_player = self.recommend_player(simulated_pool, drafting_team)
            if recommended_player:
                simulated_pool.remove(recommended_player)
            del simulated_order[0]
        return simulated_pool

    def predict_available_players(self):
        picks_to_sim_one_round = self.determine_picks_to_sim(1)
        picks_to_sim_two_rounds = self.determine_picks_to_sim(2)

        available_players_one_round = self._simulate_forward(self.my_playerboard.players, picks_to_sim_one_round)
        available_players_two_rounds = self._simulate_forward(self.my_playerboard.players, picks_to_sim_two_rounds)

        return available_players_one_round, available_players_two_rounds

    def recommend_future_players(self):
        available_players_one_round, available_players_two_rounds = self.predict_available_players()
        return available_players_one_round[:5], available_players_two_rounds[:5]

    # The real recommendation: for each position currently needed, compare the best
    # player available right now against the best player projected to still be on
    # the board at this team's next turn. Recommend the best-now player at whichever
    # position stands to lose the most value by waiting (the steepest cliff), even
    # if another needed position's best-now player is ranked slightly better overall.
    def recommend_player_avoiding_cliffs(self, available_players, drafting_team):
        team = self._find_team(drafting_team)
        required_positions = team.required_roster_positions if team is not None else []
        groups = needed_position_groups(required_positions)
        if not groups:
            # Only Bench (or nothing) is open -- no positional scarcity to weigh.
            return self.recommend_player(available_players, drafting_team)

        picks_to_next_turn = self.determine_picks_to_sim(1)
        projected_pool = self._simulate_forward(available_players, picks_to_next_turn)

        candidates = []
        for group in groups:
            best_now = best_at_position(available_players, group)
            if best_now is None:
                continue
            best_next = best_at_position(projected_pool, group)
            drop_off = (best_next.rank - best_now.rank) if best_next else math.inf
            candidates.append((drop_off, best_now))

        if not candidates:
            return self.recommend_player(available_players, drafting_team)

        # Highest drop-off wins; ties broken by the better (lower) rank.
        _, best_choice = max(candidates, key=lambda item: (item[0], -item[1].rank))
        return best_choice
