import os
import requests
from dotenv import load_dotenv

from .models import Token


load_dotenv()


class LinkedInPoster:
    def __init__(self):
        """
        Initialize with your LinkedIn app credentials
        
        Args:
            client_id (str): Your LinkedIn app client ID
            client_secret (str): Your LinkedIn app client secret
            refresh_token (str, optional): Existing refresh token if available
            access_token (str, optional): Existing access token if available
        """
        token = Token.objects.first()
        self.client_id = os.getenv('LINKEDIN_CLIENT_ID')
        self.client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
        self.refresh_token = token.refresh_token
        self.access_token = token.access_token
    
    def post_text(self, text):
        """
        Automatically post text to LinkedIn company page
        Handles token refresh if needed
        
        Args:
            text (str): The text content to post
            
        Returns:
            dict: API response from LinkedIn
        """
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'X-Restli-Protocol-Version': '2.0.0',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "author": "urn:li:company:107318690", # "urn:li:person:7_FNgzDEmw"
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
        
        return response.json()