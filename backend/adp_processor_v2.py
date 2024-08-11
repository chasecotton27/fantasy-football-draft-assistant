# adp_processor.py

import os
import time
import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient, TokenExpiredError

# Yahoo OAuth2 credentials (you will get these from the Yahoo Developer portal)
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
REDIRECT_URI = 'your_redirect_uri'
TOKEN_URL = 'https://api.login.yahoo.com/oauth2/get_token'
AUTHORIZATION_BASE_URL = 'https://api.login.yahoo.com/oauth2/request_auth'
REFRESH_URL = TOKEN_URL
SCOPE = ['fspt-r']

# Path to store tokens locally
TOKEN_FILE = 'yahoo_token.json'

def save_token(token):
    with open(TOKEN_FILE, 'w') as f:
        json.dump(token, f)

def load_token():
    try:
        with open(TOKEN_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def get_yahoo_oauth_session():
    # Try to load the token from the file
    token = load_token()

    client = BackendApplicationClient(client_id=CLIENT_ID)
    oauth = OAuth2Session(client=client, scope=SCOPE, redirect_uri=REDIRECT_URI, token=token)

    # If no token is found or the token has expired, start the OAuth process
    if not token or oauth.token['expires_at'] < time.time():
        # If we have a refresh token, refresh it
        if token and 'refresh_token' in token:
            try:
                token = oauth.refresh_token(TOKEN_URL, refresh_token=token['refresh_token'], client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
                save_token(token)
            except TokenExpiredError:
                print("Refresh token expired. Need to reauthorize.")
                token = None

        # If we don't have a valid token, start a new OAuth flow
        if not token:
            oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
            authorization_url, state = oauth.authorization_url(AUTHORIZATION_BASE_URL)
            print(f'Please go to this URL and authorize access: {authorization_url}')
            redirect_response = input('Paste the full redirect URL here: ')
            token = oauth.fetch_token(TOKEN_URL, authorization_response=redirect_response, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
            save_token(token)

    return oauth

def fetch_yahoo_adp_data():
    oauth = get_yahoo_oauth_session()
    
    url = "https://fantasysports.yahooapis.com/fantasy/v2/game/nfl/players;out=avg_draft_position"
    
    try:
        response = oauth.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Yahoo ADP data: {e}")
        return None
    
    return response.json()

# Example usage
if __name__ == "__main__":
    adp_data = fetch_yahoo_adp_data()
    if adp_data:
        print(adp_data)
