import csv

from backend.repository import PlayerRepository
from backend.processing import CSVFile


def test_fetch_all_players_sorted_by_player_id(repository):
    ids = [p.player_id for p in repository.fetch_all_players()]
    assert ids == sorted(ids)


def test_fetch_by_position_exact_match(repository):
    rbs = repository.fetch_by_position('RB')
    assert {p.name for p in rbs} == {'Bravo RB', 'Charlie RB', 'Delta RB', 'Lima RB'}


def test_find_player_exact_match(repository):
    player = repository.find_player('Echo WR', 'EEE', 'WR1')
    assert player is not None
    assert player.name == 'Echo WR'


def test_find_player_no_match_returns_none(repository):
    assert repository.find_player('Nobody', 'ZZZ', 'QB1') is None


def test_remove_then_restore_preserves_order(repository):
    before = [p.player_id for p in repository.fetch_all_players()]
    target = repository.fetch_player(before[5])

    repository.remove_player(target.player_id)
    assert target.player_id not in [p.player_id for p in repository.fetch_all_players()]

    repository.restore(target)
    after = [p.player_id for p in repository.fetch_all_players()]
    assert after == before


def test_position_group_handles_missing_position():
    repo = PlayerRepository()
    player = repo.add_player(rank=1, name='No Position', team='ZZZ', bye=5, position=None,
                              adp_espn=1.0, adp_yahoo=1.0, adp_cbs=1.0, adp_sleeper=1.0,
                              adp_nfl=1.0, adp_rtsports=1.0, adp_fantrax=1.0, avg_adp=1.0)
    assert player.position_group == ''


def test_csv_file_skips_malformed_rows(tmp_path):
    csv_path = tmp_path / 'players.csv'
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Rank', 'Player', 'Team', 'Bye', 'POS', 'ESPN', 'Yahoo', 'CBS',
                          'Sleeper', 'NFL', 'RTSports', 'Fantrax', 'AVG'])
        writer.writerow(['1', 'Good Player', 'AAA', '5', 'QB1', '1', '1', '1', '1', '1', '1', '1', '1'])
        # Missing rank -> should be skipped
        writer.writerow(['', 'No Rank Player', 'BBB', '6', 'RB1', '2', '2', '2', '2', '2', '2', '2', '2'])
        # Missing/empty POS -> should still be loaded, with an empty position_group
        writer.writerow(['3', 'No Position Player', 'CCC', '7', '', '3', '3', '3', '3', '3', '3', '3', '3'])

    repo = PlayerRepository()
    CSVFile(str(csv_path), repo)

    players = repo.fetch_all_players()
    assert [p.name for p in players] == ['Good Player', 'No Position Player']
    assert players[1].position_group == ''
