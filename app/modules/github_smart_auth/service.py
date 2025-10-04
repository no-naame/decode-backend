"""
GitHub Smart Authentication Service

Service layer for GitHub smart authentication operations.
"""

import requests
from typing import List, Dict, Any, Optional
import logging

from app.shared.smart_github_auth import smart_github_auth_service

logger = logging.getLogger(__name__)


class GitHubSmartAuthService:
    """Service for GitHub smart authentication operations"""
    
    def __init__(self):
        self.auth_service = smart_github_auth_service
    
    def get_app_info(self) -> Dict[str, Any]:
        """Get GitHub App information (app-level operation)"""
        return self.auth_service.test_app_auth()
    
    def get_all_installations(self) -> Dict[str, Any]:
        """Get all installations of the GitHub App (app-level operation)"""
        try:
            installations = self.auth_service.get_all_installations()
            return {
                "success": True,
                "count": len(installations),
                "installations": installations
            }
        except Exception as e:
            logger.error(f"Failed to get installations: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to get installations"
            }
    
    def get_repositories(
        self, 
        organization: Optional[str] = None, 
        installation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get repositories - automatically determines the right installation"""
        try:
            # Build context for smart authentication
            context = {}
            if installation_id:
                context['installation_id'] = installation_id
            elif organization:
                context['org'] = organization
            
            # Get authentication headers
            headers = self.auth_service.smart_authenticate(context)
            
            # Use the headers to make GitHub API call
            if 'token' in headers.get('Authorization', ''):
                # Installation-level call
                response = requests.get('https://api.github.com/installation/repositories', headers=headers)
            else:
                # App-level call - get all installations and their repos
                installations = self.auth_service.get_all_installations()
                all_repos = []
                
                for installation in installations:
                    inst_id = installation['id']
                    inst_headers = self.auth_service.get_installation_headers(str(inst_id))
                    inst_response = requests.get('https://api.github.com/installation/repositories', headers=inst_headers)
                    if inst_response.status_code == 200:
                        repos = inst_response.json().get('repositories', [])
                        for repo in repos:
                            repo['installation_id'] = inst_id
                        all_repos.extend(repos)
                
                return {
                    "success": True,
                    "count": len(all_repos),
                    "repositories": all_repos
                }
            
            response.raise_for_status()
            repos = response.json().get('repositories', [])
            
            return {
                "success": True,
                "count": len(repos),
                "repositories": repos
            }
        except Exception as e:
            logger.error(f"Failed to get repositories: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to get repositories"
            }
    
    def get_repository(self, owner: str, repo: str, installation_id: Optional[str] = None) -> Dict[str, Any]:
        """Get repository details - automatically finds the right installation"""
        try:
            # Build context for smart authentication
            context = {
                'owner': owner,
                'repo': repo
            }
            if installation_id:
                context['installation_id'] = installation_id
            
            # Get authentication headers
            headers = self.auth_service.smart_authenticate(context)
            
            # Make GitHub API call
            response = requests.get(f'https://api.github.com/repos/{owner}/{repo}', headers=headers)
            response.raise_for_status()
            
            repository = response.json()
            
            return {
                "success": True,
                "repository": repository
            }
        except Exception as e:
            logger.error(f"Failed to get repository {owner}/{repo}: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to get repository {owner}/{repo}"
            }
    
    def get_repository_contents(
        self, 
        owner: str, 
        repo: str, 
        path: str = "", 
        installation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get repository contents - automatically finds the right installation"""
        try:
            # Build context for smart authentication
            context = {
                'owner': owner,
                'repo': repo
            }
            if installation_id:
                context['installation_id'] = installation_id
            
            # Get authentication headers
            headers = self.auth_service.smart_authenticate(context)
            
            # Make GitHub API call
            response = requests.get(f'https://api.github.com/repos/{owner}/{repo}/contents/{path}', headers=headers)
            response.raise_for_status()
            
            contents = response.json()
            
            return {
                "success": True,
                "path": path,
                "contents": contents
            }
        except Exception as e:
            logger.error(f"Failed to get repository contents {owner}/{repo}/{path}: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to get repository contents {owner}/{repo}/{path}"
            }
    
    def get_file_content(
        self, 
        owner: str, 
        repo: str, 
        file_path: str, 
        installation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get file content - automatically finds the right installation"""
        try:
            # Build context for smart authentication
            context = {
                'owner': owner,
                'repo': repo
            }
            if installation_id:
                context['installation_id'] = installation_id
            
            # Get authentication headers
            headers = self.auth_service.smart_authenticate(context)
            
            # Make GitHub API call
            response = requests.get(f'https://api.github.com/repos/{owner}/{repo}/contents/{file_path}', headers=headers)
            response.raise_for_status()
            
            file_content = response.json()
            
            return {
                "success": True,
                "file": file_content
            }
        except Exception as e:
            logger.error(f"Failed to get file content {owner}/{repo}/{file_path}: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to get file content {owner}/{repo}/{file_path}"
            }
    
    def get_branches(
        self, 
        owner: str, 
        repo: str, 
        installation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get repository branches - automatically finds the right installation"""
        try:
            # Build context for smart authentication
            context = {
                'owner': owner,
                'repo': repo
            }
            if installation_id:
                context['installation_id'] = installation_id
            
            # Get authentication headers
            headers = self.auth_service.smart_authenticate(context)
            
            # Make GitHub API call
            response = requests.get(f'https://api.github.com/repos/{owner}/{repo}/branches', headers=headers)
            response.raise_for_status()
            
            branches = response.json()
            
            return {
                "success": True,
                "branches": branches
            }
        except Exception as e:
            logger.error(f"Failed to get branches {owner}/{repo}: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to get branches {owner}/{repo}"
            }
    
    def get_commits(
        self, 
        owner: str, 
        repo: str, 
        branch: str = "main", 
        limit: int = 10, 
        installation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get repository commits - automatically finds the right installation"""
        try:
            # Build context for smart authentication
            context = {
                'owner': owner,
                'repo': repo
            }
            if installation_id:
                context['installation_id'] = installation_id
            
            # Get authentication headers
            headers = self.auth_service.smart_authenticate(context)
            
            # Make GitHub API call
            response = requests.get(f'https://api.github.com/repos/{owner}/{repo}/commits?sha={branch}&per_page={limit}', headers=headers)
            response.raise_for_status()
            
            commits = response.json()
            
            return {
                "success": True,
                "branch": branch,
                "commits": commits
            }
        except Exception as e:
            logger.error(f"Failed to get commits {owner}/{repo}: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to get commits {owner}/{repo}"
            }
    
    def get_issues(
        self, 
        owner: str, 
        repo: str, 
        state: str = "open", 
        limit: int = 10, 
        installation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get repository issues - automatically finds the right installation"""
        try:
            # Build context for smart authentication
            context = {
                'owner': owner,
                'repo': repo
            }
            if installation_id:
                context['installation_id'] = installation_id
            
            # Get authentication headers
            headers = self.auth_service.smart_authenticate(context)
            
            # Make GitHub API call
            response = requests.get(f'https://api.github.com/repos/{owner}/{repo}/issues?state={state}&per_page={limit}', headers=headers)
            response.raise_for_status()
            
            issues = response.json()
            
            return {
                "success": True,
                "state": state,
                "issues": issues
            }
        except Exception as e:
            logger.error(f"Failed to get issues {owner}/{repo}: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to get issues {owner}/{repo}"
            }
    
    def create_issue(
        self, 
        owner: str, 
        repo: str, 
        title: str, 
        body: str, 
        labels: Optional[List[str]] = None, 
        installation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create issue in repository - automatically finds the right installation"""
        try:
            # Build context for smart authentication
            context = {
                'owner': owner,
                'repo': repo
            }
            if installation_id:
                context['installation_id'] = installation_id
            
            # Get authentication headers
            headers = self.auth_service.smart_authenticate(context)
            
            # Prepare issue data
            issue_data = {
                'title': title,
                'body': body
            }
            if labels:
                issue_data['labels'] = labels
            
            # Make GitHub API call
            response = requests.post(f'https://api.github.com/repos/{owner}/{repo}/issues', 
                                  headers=headers, json=issue_data)
            response.raise_for_status()
            
            issue = response.json()
            
            return {
                "success": True,
                "issue": issue
            }
        except Exception as e:
            logger.error(f"Failed to create issue {owner}/{repo}: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to create issue {owner}/{repo}"
            }
    
    def process_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle GitHub webhooks - automatically extracts installation ID from webhook payload"""
        try:
            # Extract installation ID from webhook payload
            installation_id = payload.get('installation', {}).get('id')
            
            if not installation_id:
                return {
                    "success": False,
                    "message": "No installation ID in webhook payload"
                }
            
            # Build context for smart authentication
            context = {
                'webhook_payload': payload
            }
            
            # Get authentication headers
            headers = self.auth_service.smart_authenticate(context)
            
            # Process webhook based on event type
            event_type = payload.get('action', 'unknown')
            
            return {
                "success": True,
                "event_type": event_type,
                "installation_id": installation_id,
                "message": f"Webhook processed for installation {installation_id}"
            }
        except Exception as e:
            logger.error(f"Failed to process webhook: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to process webhook"
            }


# Global instance
github_smart_auth_service = GitHubSmartAuthService()
