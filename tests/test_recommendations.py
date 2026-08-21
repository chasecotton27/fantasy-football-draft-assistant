from backend.processing import Draft, Team, PlayerBoard
from backend.repository import PlayerRepository
from backend.recommendations import Simulation


def test_recommend_player_picks_best_rank_among_needed_positions(repository, small_draft):
    # recommend_player is the simple, cheap heuristic used to model opponents and as
    # the Bench-only fallback -- not cliff-aware. It should just take the single
    # best-ranked player among any currently needed position, regardless of how many
    # open slots each position has. Alpha QB (rank 1) outranks everyone else overall
    # and QB is a currently needed position, so it wins.
    team_one = Team('Team One', 1, repository, small_draft)
    team_two = Team('Team Two', 2, repository, small_draft)

    board = PlayerBoard(repository)
    sim = Simulation([team_one, team_two], board, ['Team One', 'Team Two'])

    recommended = sim.recommend_player(board.players, 'Team One')

    assert recommended is not None
    assert recommended.name == 'Alpha QB'


def test_recommend_player_fills_flex_with_eligible_position_player(repository, small_draft):
    # Every named slot is already filled; only Flex remains open.
    team_one = Team('Team One', 1, repository, small_draft)
    team_one.required_roster_positions = ['Flex']
    team_two = Team('Team Two', 2, repository, small_draft)

    board = PlayerBoard(repository)
    sim = Simulation([team_one, team_two], board, ['Team One', 'Team Two'])

    recommended = sim.recommend_player(board.players, 'Team One')

    # Flex accepts RB/WR/TE; the best-ranked eligible player is Bravo RB (rank 2).
    assert recommended is not None
    assert recommended.name == 'Bravo RB'


def test_recommend_player_falls_back_to_best_available_for_bench_only(repository, small_draft):
    # Only Bench remains open — no named position or Flex need left.
    team_one = Team('Team One', 1, repository, small_draft)
    team_one.required_roster_positions = ['Bench']
    team_two = Team('Team Two', 2, repository, small_draft)

    board = PlayerBoard(repository)
    sim = Simulation([team_one, team_two], board, ['Team One', 'Team Two'])

    recommended = sim.recommend_player(board.players, 'Team One')

    # Bench accepts anyone; the algorithm should still recommend someone rather than None.
    assert recommended is not None


def test_recommend_player_avoiding_cliffs_prefers_position_about_to_dry_up():
    # WR Top is the single best player on the board, with RB Top close behind. But
    # after this pick, the only other RB left (RB Second) is far worse (rank 30),
    # while WR stays deep (next best WR is rank 3). Waiting on the RB costs far more
    # than waiting on the WR, so RB Top should be recommended despite ranking worse.
    repo = PlayerRepository()

    def add(rank, name, position):
        return repo.add_player(rank, name, team='ZZZ', bye=5, position=position,
                                adp_espn=float(rank), adp_yahoo=float(rank), adp_cbs=float(rank),
                                adp_sleeper=float(rank), adp_nfl=float(rank), adp_rtsports=float(rank),
                                adp_fantrax=float(rank), avg_adp=float(rank))

    add(1, 'WR Top', 'WR1')
    add(2, 'RB Top', 'RB1')
    add(3, 'WR Second', 'WR2')
    add(5, 'WR Third', 'WR3')
    add(6, 'WR Fourth', 'WR4')
    add(30, 'RB Second', 'RB2')

    draft = Draft('Full PPR', {'RB': 1, 'WR': 1}, 'Standard', num_teams=2)
    team_one = Team('Team One', 1, repo, draft)
    team_one.required_roster_positions = ['RB', 'WR']
    team_two = Team('Team Two', 2, repo, draft)
    team_two.required_roster_positions = ['RB']  # drives the RB run that creates the cliff

    board = PlayerBoard(repo)
    draft_order = ['Team One', 'Team Two', 'Team One', 'Team Two']
    sim = Simulation([team_one, team_two], board, draft_order)

    recommended = sim.recommend_player_avoiding_cliffs(board.players, 'Team One')

    assert recommended is not None
    assert recommended.name == 'RB Top'


def test_recommend_player_avoiding_cliffs_falls_back_when_only_bench_needed(repository, small_draft):
    team_one = Team('Team One', 1, repository, small_draft)
    team_one.required_roster_positions = ['Bench']
    team_two = Team('Team Two', 2, repository, small_draft)

    board = PlayerBoard(repository)
    sim = Simulation([team_one, team_two], board, ['Team One', 'Team Two'])

    recommended = sim.recommend_player_avoiding_cliffs(board.players, 'Team One')

    assert recommended is not None


def test_determine_picks_to_sim_counts_occurrences():
    sim = Simulation(my_teams=[], my_playerboard=None,
                      draft_order=['Team A', 'Team B', 'Team A', 'Team B', 'Team A'])

    assert sim.determine_picks_to_sim(1) == 2
    assert sim.determine_picks_to_sim(2) == 4


def test_predict_available_players_does_not_mutate_real_teams(repository, small_draft):
    team_one = Team('Team One', 1, repository, small_draft)
    team_two = Team('Team Two', 2, repository, small_draft)
    board = PlayerBoard(repository)
    draft_order = ['Team One', 'Team Two'] * 6

    required_before = list(team_one.required_roster_positions)
    roster_before = list(team_one.roster)

    sim = Simulation([team_one, team_two], board, draft_order)
    sim.recommend_future_players()

    assert team_one.required_roster_positions == required_before
    assert team_one.roster == roster_before
