import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from backend.repository import PlayerRepository
from backend.processing import Draft, Team


# (rank, name, team, position) — enough players across positions for roster-filling tests
SAMPLE_PLAYERS = [
    (1, 'Alpha QB', 'AAA', 'QB1'),
    (2, 'Bravo RB', 'BBB', 'RB1'),
    (3, 'Charlie RB', 'CCC', 'RB2'),
    (4, 'Delta RB', 'DDD', 'RB3'),
    (5, 'Echo WR', 'EEE', 'WR1'),
    (6, 'Foxtrot WR', 'FFF', 'WR2'),
    (7, 'Golf WR', 'GGG', 'WR3'),
    (8, 'Hotel TE', 'HHH', 'TE1'),
    (9, 'India TE', 'III', 'TE2'),
    (10, 'Juliet K', 'JJJ', 'K1'),
    (11, 'Kilo DST', 'KKK', 'DST'),
    (12, 'Lima RB', 'LLL', 'RB4'),
]


@pytest.fixture
def repository():
    repo = PlayerRepository()
    for rank, name, team, position in SAMPLE_PLAYERS:
        repo.add_player(rank, name, team, bye=5, position=position, adp_espn=float(rank),
                         adp_yahoo=float(rank), adp_cbs=float(rank), adp_sleeper=float(rank),
                         adp_nfl=float(rank), adp_rtsports=float(rank), adp_fantrax=float(rank),
                         avg_adp=float(rank))
    return repo


@pytest.fixture
def small_draft():
    position_count = {'QB': 1, 'RB': 2, 'WR': 2, 'TE': 1, 'Flex': 1, 'K': 1, 'DST': 1, 'Bench': 2}
    return Draft('Full PPR', position_count, 'Snake', num_teams=2)


@pytest.fixture
def team(repository, small_draft):
    return Team('Team One', 1, repository, small_draft)
