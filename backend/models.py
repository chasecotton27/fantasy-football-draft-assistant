from dataclasses import dataclass


def parse_position_group(position):
    return ''.join(char for char in (position or '') if char.isalpha())


@dataclass(frozen=True, eq=False)
class Player:
    player_id: int
    rank: int
    name: str
    team: str
    bye: int
    position: str
    position_group: str
    adp_espn: float
    adp_yahoo: float
    adp_cbs: float
    adp_sleeper: float
    adp_nfl: float
    adp_rtsports: float
    adp_fantrax: float
    avg_adp: float

    def __eq__(self, other):
        return isinstance(other, Player) and self.player_id == other.player_id

    def __hash__(self):
        return hash(self.player_id)
