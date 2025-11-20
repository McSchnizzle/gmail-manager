#!/usr/bin/env python3
"""
Gmail API Authentication Script
Run this locally on your machine to generate the token file
"""

import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.labels'
]

def authenticate():
    """Generate Gmail API token"""
    creds = None
    credentials_file = 'client_secret_861480904686-enbkcu25vtt61fb01r7c8q0bimohqc67.apps.googleusercontent.com.json'
    token_file = 'gmail_token.pickle'
    
    if not os.path.exists(credentials_file):
        print(f"Error: {credentials_file} not found!")
        print("Please place your OAuth client credentials file in the same directory.")
        return
    
    # Check for existing token
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    
    # Authenticate if needed
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token...")
            creds.refresh(Request())
        else:
            print("Starting authentication flow...")
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save token
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
        print(f"\n✓ Token saved to {token_file}")
        print("Upload this file to Claude to complete setup!")
    else:
        print("✓ Already authenticated!")
        print(f"Token file: {token_file}")

if __name__ == "__main__":
    authenticate()
