# Logic for processing ADP data

import requests
import json
from collections import defaultdict

class ADPProcessor:
    def __init__(self):
        self.sources = {
            'yahoo_sports': self.fetch_yahoo_sports_data,
            'espn': self.fetch_espn_data,
            'nfl': self.fetch_nfl_data,
            'cbs': self.fetch_cbs_data,
            'fanduel': self.fetch_fanduel_data,
            'draftkings': self.fetch_draftkings_data
        }
        self.adp_data = defaultdict(list)  # Stores ADP data aggregated from all sources
    
    def fetch_yahoo_sports_data(self):
        # Example API request for Source 1
        url = 'https://api.source1.com/adp'
        headers = {
            'Authorization': 'Bearer YOUR_TOKEN',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            self.process_adp_data(data, 'yahoo_sports')
        else:
            print(f"Failed to fetch data from Yahoo Sports: {response.status_code}")

    def fetch_espn_data(self):
        # Example API request for Source 2
        url = 'https://api.source2.com/adp'
        headers = {
            'Authorization': 'Bearer YOUR_TOKEN',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            self.process_adp_data(data, 'espn')
        else:
            print(f"Failed to fetch data from ESPN: {response.status_code}")

    def fetch_nfl_data(self):
        # Example API request for Source 3
        url = 'https://api.source2.com/adp'
        headers = {
            'Authorization': 'Bearer YOUR_TOKEN',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            self.process_adp_data(data, 'nfl')
        else:
            print(f"Failed to fetch data from NFL: {response.status_code}")

    def fetch_cbs_data(self):
        # Example API request for Source 4
        url = 'https://api.source2.com/adp'
        headers = {
            'Authorization': 'Bearer YOUR_TOKEN',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            self.process_adp_data(data, 'cbs')
        else:
            print(f"Failed to fetch data from CBS: {response.status_code}")

    def fetch_fanduel_data(self):
        # Example API request for Source 5
        url = 'https://api.source2.com/adp'
        headers = {
            'Authorization': 'Bearer YOUR_TOKEN',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            self.process_adp_data(data, 'fanduel')
        else:
            print(f"Failed to fetch data from FanDuel: {response.status_code}")

    def fetch_draftkings_data(self):
        # Example API request for Source 6
        url = 'https://api.source2.com/adp'
        headers = {
            'Authorization': 'Bearer YOUR_TOKEN',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            self.process_adp_data(data, 'draftkings')
        else:
            print(f"Failed to fetch data from DraftKings: {response.status_code}")

    def process_adp_data(self, data, source):
        """
        Processes the JSON data returned by the API.
        Aggregates the ADP data by player and stores it in self.adp_data.
        """
        for player in data['players']:
            player_name = player['name']
            adp = player['adp']
            self.adp_data[player_name].append((source, adp))
    
    def calculate_average_adp(self):
        """
        Calculates the average ADP across all sources for each player.
        """
        average_adp = {}
        for player, adps in self.adp_data.items():
            total_adp = sum(adp for source, adp in adps)
            average_adp[player] = total_adp / len(adps)
        
        return average_adp
    
    def fetch_and_aggregate_adp(self):
        """
        Fetches ADP data from all sources and aggregates it.
        """
        for source_name, fetch_method in self.sources.items():
            print(f"Fetching ADP data from {source_name}...")
            fetch_method()
        
        return self.calculate_average_adp()

if __name__ == "__main__":
    processor = ADPProcessor()
    aggregated_adp = processor.fetch_and_aggregate_adp()
    
    # Print or save the aggregated ADP data
    print(json.dumps(aggregated_adp, indent=4))
