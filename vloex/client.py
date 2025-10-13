"""
VLOEX SDK Client
Minimal, Stripe-style API
"""

from typing import Dict, Optional, List
import requests
from .exceptions import VloexError


DEFAULT_BASE_URL = 'https://api.vloex.com'


class VideoResource:
    """Videos resource - core primitive"""

    def __init__(self, client: 'Vloex'):
        self._client = client

    def create(self, script: str, webhook_url: str = None, webhook_secret: str = None, **options) -> Dict:
        """
        Create a video from text

        Args:
            script: The text script for your video
            webhook_url: Optional webhook URL to receive completion notification
            webhook_secret: Optional secret for webhook HMAC signature
            **options: Optional settings (avatar, voice, background - coming soon)

        Returns:
            dict: Video object with id and status

        Example:
            video = vloex.videos.create(
                script='Version 2.0 is live!',
                webhook_url='https://your-app.com/webhook'
            )
        """
        payload = {
            'input': script,
            'options': options
        }

        if webhook_url:
            payload['webhook_url'] = webhook_url

        if webhook_secret:
            payload['webhook_secret'] = webhook_secret

        return self._client._request('POST', '/v1/generate', payload)

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

    def from_journey(
        self,
        screenshots: Optional[List[str]] = None,
        descriptions: Optional[List[str]] = None,
        product_url: Optional[str] = None,
        pages: Optional[List[str]] = None,
        product_context: str = None,
        step_duration: int = 15,
        avatar_position: str = 'bottom-right',
        tone: str = 'professional',
        **options
    ) -> Dict:
        """
        Create product demo videos from screenshots or URLs

        Level 1 - Provide screenshots + descriptions:
            video = vloex.videos.from_journey(
                screenshots=['base64img1...', 'base64img2...'],
                descriptions=['Login page', 'Dashboard view'],
                product_context='My Product Demo'
            )

        Level 2 - Provide URL + pages:
            video = vloex.videos.from_journey(
                product_url='https://myapp.com',
                pages=['/', '/features', '/pricing'],
                product_context='MyApp Website Tour'
            )

        Args:
            screenshots: List of base64-encoded images (Level 1)
            descriptions: Descriptions for each screenshot (Level 1)
            product_url: Public URL to capture (Level 2)
            pages: List of page paths like ['/dashboard', '/pricing'] (Level 2)
            product_context: Description of what's being shown
            step_duration: Seconds per screenshot (default: 15)
            avatar_position: Avatar placement - 'bottom-right', 'bottom-left', 'top-right', 'top-left'
            tone: Narration style - 'professional', 'casual', 'technical'
            **options: Additional settings

        Returns:
            dict: Video generation result
        """
        if not product_context:
            raise ValueError('product_context is required')

        payload = {
            'product_context': product_context,
            'step_duration': step_duration,
            'avatar_position': avatar_position,
            'tone': tone,
            **options
        }

        # Level 1: Screenshots + descriptions
        if screenshots:
            payload['screenshots'] = screenshots
            if descriptions:
                payload['descriptions'] = descriptions

        # Level 2: URL + pages
        if product_url:
            payload['product_url'] = product_url
            if pages:
                payload['pages'] = pages

        return self._client._request('POST', '/v1/videos/from-journey', payload)


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

        if '/from-journey' in path:
            return {
                'success': data.get('success'),
                'video_path': data.get('video_path'),
                'video_url': data.get('video_url'),
                'duration_seconds': data.get('duration_seconds'),
                'file_size_mb': data.get('file_size_mb'),
                'cost': data.get('cost'),
                'steps_count': data.get('steps_count'),
                'error': data.get('error_message') or data.get('error')
            }

        return data
