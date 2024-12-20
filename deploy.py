import os
import base64
import requests
from pathlib import Path
from typing import List, Dict

class GitHubDeployer:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.api_url = 'https://api.github.com'

    def create_repository(self, name: str, description: str) -> Dict:
        """Create a new GitHub repository"""
        data = {
            'name': name,
            'description': description,
            'private': False,
            'auto_init': False
        }
        response = requests.post(
            f'{self.api_url}/user/repos',
            headers=self.headers,
            json=data
        )
        response.raise_for_status()
        return response.json()

    def is_binary_file(self, file_path: str) -> bool:
        """Check if a file is binary based on its extension"""
        binary_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.ico', '.pdf', '.zip', '.tar', '.gz'}
        return Path(file_path).suffix.lower() in binary_extensions

    def upload_file(self, repo: str, file_path: str, content: bytes, message: str) -> None:
        """Upload a file to the repository"""
        url = f'{self.api_url}/repos/{repo}/contents/{file_path}'
        data = {
            'message': message,
            'content': base64.b64encode(content).decode()
        }
        response = requests.put(url, headers=self.headers, json=data)
        response.raise_for_status()

    def deploy(self, repo_name: str, description: str) -> str:
        """Deploy the current project to GitHub"""
        try:
            # Create repository
            repo = self.create_repository(repo_name, description)
            full_repo_name = repo['full_name']
            
            # Files to ignore
            ignore_patterns = [
                '__pycache__', '*.pyc', '.env', '.git', '.gitignore',
                '*.log', '.DS_Store', '.idea/', '.vscode/'
            ]
            
            # Upload files
            root_path = Path('.')
            for file_path in root_path.rglob('*'):
                # Skip directories and ignored files
                if file_path.is_dir() or any(str(file_path).startswith(p.rstrip('/')) for p in ignore_patterns):
                    continue
                
                try:
                    relative_path = str(file_path.relative_to(root_path))
                    if self.is_binary_file(str(file_path)):
                        with open(file_path, 'rb') as f:
                            content = f.read()
                    else:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read().encode('utf-8')
                    
                    self.upload_file(
                        full_repo_name,
                        relative_path,
                        content,
                        f'Add {relative_path}'
                    )
                    print(f'Uploaded: {relative_path}')
                except Exception as e:
                    print(f'Error uploading {file_path}: {str(e)}')
                    continue
            
            return f'https://github.com/{full_repo_name}'
        except Exception as e:
            print(f'Deployment failed: {str(e)}')
            raise

if __name__ == '__main__':
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        print('Error: GITHUB_TOKEN environment variable is not set')
        exit(1)

    deployer = GitHubDeployer(token)
    # Generate a unique repository name using timestamp
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    repo_name = f'logo-creator-{timestamp}'
    
    repo_url = deployer.deploy(
        repo_name,
        'Logo Creator with DALL-E 3 and SVG'
    )
    print(f'Successfully deployed to: {repo_url}')
