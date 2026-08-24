from backend.processing import Draft, Team, generate_draft_order


def _make_teams(repository, draft, num_teams):
    return [Team(f'Team {i + 1}', i + 1, repository, draft) for i in range(num_teams)]


def test_generate_draft_order_standard(repository):
    draft = Draft('Standard', {'QB': 1, 'RB': 1}, 'Standard', num_teams=3)
    teams = _make_teams(repository, draft, 3)

    order = generate_draft_order(teams, draft)

    assert order == ['Team 1', 'Team 2', 'Team 3', 'Team 1', 'Team 2', 'Team 3']


def test_generate_draft_order_snake(repository):
    draft = Draft('Standard', {'QB': 1, 'RB': 1}, 'Snake', num_teams=3)
    teams = _make_teams(repository, draft, 3)

    order = generate_draft_order(teams, draft)

    assert order == ['Team 1', 'Team 2', 'Team 3', 'Team 3', 'Team 2', 'Team 1']


def test_generate_draft_order_length_matches_rounds(repository):
    position_count = {'QB': 1, 'RB': 2, 'WR': 2, 'Bench': 3}
    draft = Draft('Standard', position_count, 'Snake', num_teams=4)
    teams = _make_teams(repository, draft, 4)

    order = generate_draft_order(teams, draft)

    total_rounds = sum(position_count.values())
    assert len(order) == total_rounds * draft.num_teams
