import os
import requests
from urllib.parse import urlencode, quote
from dotenv import load_dotenv

from linkedin.models import OAUTH


load_dotenv()


class LinkedInPoster:
    def __init__(self):
        """
        Initialize with your LinkedIn app credentials
        
        Args:
            client_id (str): Your LinkedIn app client ID
            client_secret (str): Your LinkedIn app client secret
            redirect_uri (str): Your authorized redirect URI
            person_urn (str): Your personal URN (format: "urn:li:organization:123456")
            refresh_token (str, optional): Existing refresh token if available
        """
        self.client_id = os.getenv('LINKEDIN_CLIENT_ID')
        self.client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
        self.redirect_uri = "https://relocate.works/linkedin/callback/"
        self.person_urn = "urn:li:person:1265428294"
        self.refresh_token = None
        self.access_token = None
        
    def get_auth_url(self):
        """Generate the LinkedIn authorization URL"""
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': 'w_member_social',
            'state': 'linkedin_auth'
        }
        return f"https://www.linkedin.com/oauth/v2/authorization?{urlencode(params, quote_via=quote)}"
    
    def fetch_tokens(self):
        """
        Exchange authorization code for access and refresh tokens
        
        Args:
            authorization_code (str): The code received after user authorization
        """
        code = OAUTH.objects.first().code
        token_url = "https://www.linkedin.com/oauth/v2/accessToken"
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        
        response = requests.post(token_url, data=data)
        if response.status_code == 200:
            tokens = response.json()
            self.access_token = tokens['access_token']
            self.refresh_token = tokens['refresh_token']
            return True
        return False
    
    def refresh_access_token(self):
        """
        Refresh expired access token using refresh token
        """
        if not self.refresh_token:
            raise Exception("No refresh token available")
            
        token_url = "https://www.linkedin.com/oauth/v2/accessToken"
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        
        response = requests.post(token_url, data=data)
        if response.status_code == 200:
            tokens = response.json()
            self.access_token = tokens['access_token']
            return True
        return False
    
    def post_text(self, text):
        """
        Automatically post text to LinkedIn company page
        Handles token refresh if needed
        
        Args:
            text (str): The text content to post
            
        Returns:
            dict: API response from LinkedIn
        """
        if not self.access_token:
            self.fetch_tokens()
            
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'X-Restli-Protocol-Version': '2.0.0',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "author": self.person_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        response = requests.post(
            "https://api.linkedin.com/v2/ugcPosts",
            json=payload,
            headers=headers
        )
        
        # If token expired, refresh and try again
        if response.status_code == 401:
            if self.refresh_access_token():
                headers['Authorization'] = f'Bearer {self.access_token}'
                response = requests.post(
                    "https://api.linkedin.com/v2/ugcPosts",
                    json=payload,
                    headers=headers
                )
        
        return response.json()