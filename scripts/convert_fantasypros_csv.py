import csv
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ADP_DIR = PROJECT_ROOT / 'adp-data'

# FantasyPros' export merges "Name   TEAM (Bye)" into one "Player (Bye)" column.
# Team is 2-4 uppercase letters; team defenses use the literal "DST" in that slot
# (e.g. "Houston Texans DST   (8)"), matching this app's existing DST convention.
# Deep/unrostered players sometimes have neither team nor bye at all.
PLAYER_BYE_PATTERN = re.compile(r'^(?P<name>.+?)\s+(?P<team>[A-Z]{2,4})\s+\((?P<bye>\d+)\)$')

OUTPUT_FIELDS = ['Rank', 'Player', 'Team', 'Bye', 'POS', 'ESPN', 'Yahoo', 'CBS',
                  'Sleeper', 'NFL', 'RTSports', 'Fantrax', 'AVG']

# The app's live data files. Re-run this script any time a fresh raw FantasyPros
# export gets dropped in at one of these same paths.
TARGET_FILES = ['adp_standard.csv', 'adp_half_ppr.csv', 'adp_full_ppr.csv']


def parse_player_bye(raw):
    match = PLAYER_BYE_PATTERN.match(raw.strip())
    if match:
        return match.group('name'), match.group('team'), match.group('bye')
    return raw.strip(), '', ''


# Converts a file in place if it's in FantasyPros' raw "Player (Bye)" format.
# Leaves it untouched (returns False) if it's already in the app's format, so
# this is safe to re-run against a mix of fresh and already-converted files.
def convert_in_place(path):
    with open(path, newline='', encoding='utf-8') as source_file:
        reader = csv.DictReader(source_file)
        fieldnames = reader.fieldnames or []
        if 'Player (Bye)' not in fieldnames:
            return False

        rows = []
        for row in reader:
            name, team, bye = parse_player_bye(row['Player (Bye)'])
            rows.append({
                'Rank': row.get('Rank', ''),
                'Player': name,
                'Team': team,
                'Bye': bye,
                'POS': row.get('POS', ''),
                'ESPN': row.get('ESPN', ''),
                'Yahoo': row.get('Yahoo', ''),
                'CBS': row.get('CBS', ''),
                'Sleeper': row.get('Sleeper', ''),
                'NFL': row.get('NFL', ''),
                'RTSports': row.get('RTSports', ''),
                'Fantrax': row.get('Fantrax', ''),
                'AVG': row.get('AVG', ''),
            })

    with open(path, 'w', newline='', encoding='utf-8') as target_file:
        writer = csv.DictWriter(target_file, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return True


def main():
    for name in TARGET_FILES:
        path = ADP_DIR / name
        if not path.exists():
            print(f'Skipping missing file: {path}')
            continue
        if convert_in_place(path):
            print(f'Converted in place: {path.name}')
        else:
            print(f'Already in app format, left untouched: {path.name}')


if __name__ == '__main__':
    main()
