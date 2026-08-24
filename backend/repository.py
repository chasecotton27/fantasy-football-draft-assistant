from backend.models import Player, parse_position_group


class PlayerRepository:
    def __init__(self):
        self._players = {}
        self._next_id = 1

    def add_player(self, rank, name, team, bye, position, adp_espn, adp_yahoo, adp_cbs,
                    adp_sleeper, adp_nfl, adp_rtsports, adp_fantrax, avg_adp):
        player = Player(
            player_id=self._next_id,
            rank=rank,
            name=name,
            team=team,
            bye=bye,
            position=position,
            position_group=parse_position_group(position),
            adp_espn=adp_espn,
            adp_yahoo=adp_yahoo,
            adp_cbs=adp_cbs,
            adp_sleeper=adp_sleeper,
            adp_nfl=adp_nfl,
            adp_rtsports=adp_rtsports,
            adp_fantrax=adp_fantrax,
            avg_adp=avg_adp,
        )
        self._players[player.player_id] = player
        self._next_id += 1
        return player

    # Re-insert a previously removed player (used by undo) without assigning a new id
    def restore(self, player):
        self._players[player.player_id] = player

    def remove_player(self, player_id):
        self._players.pop(player_id, None)

    def fetch_player(self, player_id):
        return self._players.get(player_id)

    def fetch_all_players(self):
        return sorted(self._players.values(), key=lambda p: p.player_id)

    def fetch_by_position(self, position_group):
        return [p for p in self.fetch_all_players() if p.position_group == position_group]

    def find_player(self, name, team, position):
        for player in self.fetch_all_players():
            if player.name == name and player.team == team and player.position == position:
                return player
        return None
