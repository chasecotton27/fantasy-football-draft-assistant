def _draft_by_name(team, repository, name):
    player = next(p for p in repository.fetch_all_players() if p.name == name)
    team.draft_player(player.player_id)


def test_draft_player_fills_direct_position_slot(team, repository):
    _draft_by_name(team, repository, 'Alpha QB')
    assert 'QB' not in team.required_roster_positions
    assert team.roster[-1].name == 'Alpha QB'


def test_draft_player_consumes_flex_when_position_full(team, repository):
    # Fill both RB slots first
    _draft_by_name(team, repository, 'Bravo RB')
    _draft_by_name(team, repository, 'Charlie RB')
    assert team.required_roster_positions.count('RB') == 0

    # A third RB should consume the Flex slot instead of Bench
    _draft_by_name(team, repository, 'Delta RB')
    assert 'Flex' not in team.required_roster_positions
    assert team.required_roster_positions.count('Bench') == 2


def test_draft_player_falls_back_to_bench(team, repository):
    _draft_by_name(team, repository, 'Bravo RB')
    _draft_by_name(team, repository, 'Charlie RB')
    _draft_by_name(team, repository, 'Delta RB')  # consumes Flex
    bench_before = team.required_roster_positions.count('Bench')

    _draft_by_name(team, repository, 'Lima RB')  # no RB/Flex slots left -> Bench
    assert team.required_roster_positions.count('Bench') == bench_before - 1


def test_draft_player_beyond_all_slots_does_not_crash(team, repository):
    # Fill every required slot for this small_draft roster (11 total slots),
    # then draft one more player beyond that — must not raise.
    draft_sequence = [
        'Alpha QB', 'Bravo RB', 'Charlie RB', 'Delta RB', 'Echo WR', 'Foxtrot WR',
        'Hotel TE', 'Golf WR', 'Juliet K', 'Kilo DST', 'India TE',
    ]
    for name in draft_sequence:
        _draft_by_name(team, repository, name)

    assert team.required_roster_positions == []

    # One more pick beyond every configured slot — this used to raise ValueError
    _draft_by_name(team, repository, 'Lima RB')
    assert team.required_roster_positions == []
    assert len(team.roster) == 12
