"""
VLOEX SDK Client
Minimal, Stripe-style API
"""

from typing import Dict, Optional
import requests
from .exceptions import VloexError


DEFAULT_BASE_URL = 'https://api.vloex.com'


class VideoResource:
    """Videos resource - core primitive"""

    def __init__(self, client: 'Vloex'):
        self._client = client

    def create(self, script: str, **options) -> Dict:
        """
        Create a video from text

        Args:
            script: The text script for your video
            **options: Optional settings (avatar, voice, background - coming soon)

        Returns:
            dict: Video object with id and status

        Example:
            video = vloex.videos.create(
                script='Version 2.0 is live!'
            )
        """
        return self._client._request('POST', '/v1/generate', {
            'input': script,
            'options': options
        })

    def retrieve(self, id: str) -> Dict:
        """
        Get video status and URL

        Args:
            id: Video job ID

        Returns:
            dict: Video object with current status

        Example:
            status = vloex.videos.retrieve('job_abc123')
            print(status['url'])
        """
        return self._client._request('GET', f'/v1/jobs/{id}/status')


class Vloex:
    """VLOEX SDK Client"""

    def __init__(self, api_key: str, base_url: str = DEFAULT_BASE_URL):
        """
        Initialize VLOEX SDK

        Args:
            api_key: Your VLOEX API key (get one at https://vloex.com/api-keys)
            base_url: Optional custom base URL
        """
        if not api_key:
            raise ValueError('VLOEX API key required. Get one at https://vloex.com/api-keys')

        self.api_key = api_key
        self.base_url = base_url
        self.videos = VideoResource(self)

    def _request(self, method: str, path: str, body: Optional[Dict] = None) -> Dict:
        """Internal: Make HTTP request"""
        url = f'{self.base_url}{path}'

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }

        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=body
        )

        try:
            data = response.json()
        except ValueError:
            data = {}

        if not response.ok:
            error_message = data.get('detail') or data.get('message') or 'API request failed'
            raise VloexError(error_message, response.status_code)

        # Transform API response to SDK format
        if '/generate' in path:
            return {
                'id': data.get('job_id') or data.get('id'),
                'status': data.get('status'),
                'url': data.get('url'),
                'error': data.get('error')
            }

        if '/status' in path:
            return {
                'id': data.get('id'),
                'status': data.get('status'),
                'url': data.get('video_url') or data.get('url'),
                'error': data.get('error_message') or data.get('error')
            }

        return data
