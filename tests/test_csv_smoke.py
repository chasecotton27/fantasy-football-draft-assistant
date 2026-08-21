import pytest

from backend.repository import PlayerRepository
from backend.processing import CSVFile, SCORING_FORMAT_CSV_PATHS


@pytest.mark.parametrize("csv_path", SCORING_FORMAT_CSV_PATHS.values())
def test_real_adp_csv_loads_without_error(csv_path):
    repo = PlayerRepository()
    CSVFile(csv_path, repo)

    players = repo.fetch_all_players()
    assert len(players) > 0
    assert all(p.name for p in players)
