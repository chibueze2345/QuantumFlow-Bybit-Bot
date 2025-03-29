"""
QuantumFlow Elite Bybit Bot - Storage Handler
Last Updated: 2025-03-29 18:13:19 UTC
Author: chibueze2345
Version: 2.1.0
"""

import os
import json
import base64
import requests
from datetime import datetime, timezone

class BotStorage:
    def __init__(self):
        self.repo = "chibueze2345/QuantumFlow-Bybit-Bot"
        self.branch = "data"
        self.token = os.environ.get('GITHUB_TOKEN')
        self.last_updated = '2025-03-29 18:13:19'

    def save_data(self, data, filename):
        url = f"https://api.github.com/repos/{self.repo}/contents/data/{filename}"
        
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        content = base64.b64encode(json.dumps(data).encode()).decode()
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                sha = response.json()['sha']
            else:
                sha = None
                
            commit_data = {
                "message": f"Update {filename} - {datetime.now(timezone.utc)}",
                "content": content,
                "branch": self.branch
            }
            
            if sha:
                commit_data["sha"] = sha
                
            response = requests.put(url, headers=headers, json=commit_data)
            return response.status_code in [200, 201]
            
        except Exception as e:
            print(f"Storage error: {str(e)}")
            return False

    def load_data(self, filename):
        url = f"https://api.github.com/repos/{self.repo}/contents/data/{filename}"
        
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                content = response.json()['content']
                decoded = base64.b64decode(content).decode()
                return json.loads(decoded)
        except Exception as e:
            print(f"Load error: {str(e)}")
            
        return None