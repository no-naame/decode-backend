"""
Smart GitHub App Authentication Service

This service handles GitHub App authentication intelligently:
- App-level operations (no installation ID needed)
- Installation-level operations (with dynamic installation ID discovery)
- Webhook-driven authentication
"""

import jwt
import time
import requests
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta, timezone
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class SmartGitHubAuthService:
    """Smart GitHub App authentication service that handles both app-level and installation-level auth"""
    
    def __init__(self):
        self._jwt_token: Optional[str] = None
        self._jwt_expires_at: Optional[datetime] = None
        self._installation_tokens: Dict[str, Dict[str, Any]] = {}
    
    def _load_private_key(self) -> str:
        """Load the private key from environment variable"""
        if settings.GITHUB_PRIVATE_KEY:
            return settings.GITHUB_PRIVATE_KEY
        else:
            raise ValueError("GitHub private key must be provided via GITHUB_PRIVATE_KEY environment variable.")
    
    def _generate_jwt(self) -> str:
        """Generate a JWT token for GitHub App authentication"""
        if not settings.GITHUB_APP_ID:
            raise ValueError("GitHub App ID is not configured")
        
        private_key = self._load_private_key()
        
        now = int(time.time())
        payload = {
            'iat': now - 60,
            'exp': now + 600,
            'iss': settings.GITHUB_APP_ID
        }
        
        jwt_token = jwt.encode(payload, private_key, algorithm='RS256')
        
        self._jwt_token = jwt_token
        self._jwt_expires_at = datetime.now(timezone.utc) + timedelta(minutes=9)
        
        logger.info("Generated new JWT token for GitHub App")
        return jwt_token
    
    def get_jwt_token(self) -> str:
        """Get a valid JWT token for app-level operations"""
        if (self._jwt_token is None or 
            self._jwt_expires_at is None or 
            datetime.now(timezone.utc) >= self._jwt_expires_at):
            return self._generate_jwt()
        
        return self._jwt_token
    
    def get_app_level_headers(self) -> Dict[str, str]:
        """Get headers for app-level GitHub API requests (no installation needed)"""
        jwt_token = self.get_jwt_token()
        return {
            'Authorization': f'Bearer {jwt_token}',
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28'
        }
    
    def get_all_installations(self) -> List[Dict[str, Any]]:
        """Get all installations of the GitHub App (app-level operation)"""
        try:
            headers = self.get_app_level_headers()
            response = requests.get('https://api.github.com/app/installations', headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get installations: {e}")
            return []
    
    def get_installation_for_repo(self, owner: str, repo: str) -> Optional[Dict[str, Any]]:
        """Get installation ID for a specific repository (app-level operation)"""
        try:
            headers = self.get_app_level_headers()
            response = requests.get(f'https://api.github.com/repos/{owner}/{repo}/installation', headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get installation for {owner}/{repo}: {e}")
            return None
    
    def get_installation_for_org(self, org: str) -> Optional[Dict[str, Any]]:
        """Get installation ID for a specific organization (app-level operation)"""
        try:
            headers = self.get_app_level_headers()
            response = requests.get(f'https://api.github.com/orgs/{org}/installation', headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get installation for org {org}: {e}")
            return None
    
    def _get_installation_token(self, installation_id: str) -> str:
        """Get installation access token for a specific installation"""
        jwt_token = self.get_jwt_token()
        
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28'
        }
        
        url = f'https://api.github.com/app/installations/{installation_id}/access_tokens'
        
        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            
            token_data = response.json()
            installation_token = token_data['token']
            expires_at = token_data['expires_at']
            
            self._installation_tokens[installation_id] = {
                'token': installation_token,
                'expires_at': datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
            }
            
            logger.info(f"Generated new installation access token for installation {installation_id}")
            return installation_token
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get installation token for {installation_id}: {e}")
            raise
    
    def get_installation_token(self, installation_id: str) -> str:
        """Get a valid installation access token for a specific installation"""
        if installation_id in self._installation_tokens:
            cached_data = self._installation_tokens[installation_id]
            if datetime.now(timezone.utc) < cached_data['expires_at']:
                return cached_data['token']
        
        return self._get_installation_token(installation_id)
    
    def get_installation_headers(self, installation_id: str) -> Dict[str, str]:
        """Get headers for installation-level GitHub API requests"""
        token = self.get_installation_token(installation_id)
        return {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28'
        }
    
    def smart_authenticate(self, context: Dict[str, Any]) -> Dict[str, str]:
        """
        Smart authentication that determines the right authentication method based on context
        
        Context can contain:
        - installation_id: Use specific installation
        - owner/repo: Find installation for specific repo
        - org: Find installation for specific org
        - webhook_payload: Extract installation from webhook
        - username: For user-related queries
        - search_query: For search queries
        """
        # If installation_id is provided, use it
        if 'installation_id' in context:
            return self.get_installation_headers(context['installation_id'])
        
        # If webhook payload is provided, extract installation
        if 'webhook_payload' in context:
            installation_id = context['webhook_payload'].get('installation', {}).get('id')
            if installation_id:
                return self.get_installation_headers(str(installation_id))
        
        # If owner/repo is provided, find installation for that repo
        if 'owner' in context and 'repo' in context:
            installation = self.get_installation_for_repo(context['owner'], context['repo'])
            if installation:
                return self.get_installation_headers(str(installation['id']))
        
        # If org is provided, find installation for that org
        if 'org' in context:
            installation = self.get_installation_for_org(context['org'])
            if installation:
                return self.get_installation_headers(str(installation['id']))
            else:
                # If specific org installation not found, try using any available installation
                # This allows queries to work even if the app isn't installed on the specific org
                installations = self.get_all_installations()
                if installations and len(installations) > 0:
                    installation_id = str(installations[0]['id'])
                    return self.get_installation_headers(installation_id)
        
        # For user queries or search queries, try to use any available installation
        if 'username' in context or 'search_query' in context:
            installations = self.get_all_installations()
            if installations and len(installations) > 0:
                # Use the first available installation for user/search queries
                installation_id = str(installations[0]['id'])
                return self.get_installation_headers(installation_id)
        
        # Fallback to app-level authentication (may not work for all GraphQL queries)
        return self.get_app_level_headers()
    
    def test_app_auth(self) -> Dict[str, Any]:
        """Test app-level authentication"""
        try:
            headers = self.get_app_level_headers()
            response = requests.get('https://api.github.com/app', headers=headers)
            response.raise_for_status()
            
            return {
                'success': True,
                'app_info': response.json(),
                'message': 'App-level authentication successful'
            }
        except Exception as e:
            logger.error(f"App authentication test failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'App-level authentication failed'
            }


# Global instance
smart_github_auth_service = SmartGitHubAuthService()
