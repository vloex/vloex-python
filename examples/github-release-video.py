"""
Generate Videos from GitHub Release Notes
==========================================

This example demonstrates how to automatically create announcement videos
for GitHub releases using the VLOEX Python SDK.

Use Case:
---------
Perfect for:
- Open source project maintainers announcing new releases
- Developer relations teams creating release highlight videos
- Product teams sharing feature updates
- CI/CD pipelines with automated video generation

What This Example Does:
-----------------------
1. Fetches the latest release from any GitHub repository
2. Extracts key information (version, changes, highlights)
3. Formats a professional video script
4. Generates a video using VLOEX
5. Polls for completion and returns the video URL

Requirements:
-------------
pip install vloex requests

Get your API key from: https://vloex.com/dashboard/api-keys
"""

import os
import sys
import time
import json
import requests
from vloex import Vloex, VloexError


def fetch_latest_release(repo_owner, repo_name):
    """
    Fetch the latest release from a GitHub repository.

    Args:
        repo_owner (str): GitHub username or organization (e.g., 'vercel')
        repo_name (str): Repository name (e.g., 'next.js')

    Returns:
        dict: Release data from GitHub API
    """
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest'

    print(f'🔍 Fetching latest release from {repo_owner}/{repo_name}...')

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f'GitHub API error: {response.status_code}')

    return response.json()


def extract_release_highlights(release_body, max_items=5):
    """
    Extract key changes from release notes.

    Args:
        release_body (str): Raw release notes from GitHub
        max_items (int): Maximum number of changes to include

    Returns:
        list: List of change descriptions
    """
    # Extract bullet points (lines starting with '- ')
    changes = [
        line[2:].strip()  # Remove '- ' prefix
        for line in release_body.split('\n')
        if line.strip().startswith('- ')
    ]

    return changes[:max_items]


def create_release_script(version, changes, repo_name):
    """
    Format a professional script for the release video.

    Args:
        version (str): Release version (e.g., 'v15.5.4')
        changes (list): List of key changes
        repo_name (str): Repository name

    Returns:
        str: Formatted video script
    """
    script = f"{repo_name} {version} has been released!\n\n"

    if changes:
        script += "This release includes important updates:\n\n"
        script += "\n".join(changes)
        script += "\n\n"

    script += "Check out the full release notes on GitHub!"

    return script.strip()


def generate_release_video(api_key, repo_owner, repo_name):
    """
    Complete workflow: Fetch release → Generate video → Return URL

    Args:
        api_key (str): Your VLOEX API key
        repo_owner (str): GitHub repository owner
        repo_name (str): GitHub repository name

    Returns:
        dict: Video metadata including URL and status
    """
    # Step 1: Initialize VLOEX SDK
    vloex = Vloex(api_key)

    # Step 2: Fetch latest release from GitHub
    release = fetch_latest_release(repo_owner, repo_name)

    version = release['tag_name']
    published_date = release['published_at'][:10]

    print(f'📦 Found: {version}')
    print(f'📝 Published: {published_date}')

    # Step 3: Extract and format key changes
    changes = extract_release_highlights(release['body'])
    script = create_release_script(version, changes, repo_name)

    print('\n📄 Video Script:')
    print('─' * 60)
    print(script)
    print('─' * 60)

    # Step 4: Create video job
    print('\n🎬 Creating video with VLOEX...')

    try:
        video = vloex.videos.create(script=script)

        print(f'✅ Video job created: {video["id"]}')
        print(f'📊 Initial status: {video["status"]}')

        # Step 5: Poll for completion
        print('\n⏳ Waiting for video generation...')

        max_attempts = 60  # 5 minutes max (60 * 5 seconds)
        attempt = 0

        while attempt < max_attempts:
            time.sleep(5)
            status = vloex.videos.retrieve(video['id'])
            attempt += 1

            # Show progress
            print(f'   Attempt {attempt}/{max_attempts} - Status: {status["status"]}', end='\r')

            if status['status'] == 'completed':
                print('\n\n🎉 Video generation complete!')
                print(f'🎥 Video URL: {status["url"]}')
                print(f'\n📊 Full Response:')
                print(json.dumps(status, indent=2))
                return status

            if status['status'] == 'failed':
                print('\n\n❌ Video generation failed')
                print(f'Error: {status.get("error", "Unknown error")}')
                return status

        # Timeout
        print('\n\n⏰ Timeout: Video generation took longer than expected')
        print('   Check the video status later using:')
        print(f'   vloex.videos.retrieve("{video["id"]}")')
        return status

    except VloexError as error:
        print(f'\n❌ VLOEX API Error: {error.message}')
        if error.status_code:
            print(f'   HTTP Status: {error.status_code}')
        raise


def main():
    """
    Example usage with different repositories
    """
    # Get API key from environment variable (recommended for security)
    api_key = os.environ.get('VLOEX_API_KEY')

    if not api_key:
        print('⚠️  VLOEX_API_KEY environment variable not set')
        print('   Set it with: export VLOEX_API_KEY=vs_live_your_key_here')
        print('   Or get your key from: https://vloex.com/dashboard/api-keys')
        sys.exit(1)

    print('🚀 GitHub Release Video Generator')
    print('=' * 60)

    # Example 1: Next.js Release
    print('\n📦 Example: Next.js Latest Release\n')
    try:
        result = generate_release_video(
            api_key=api_key,
            repo_owner='vercel',
            repo_name='next.js'
        )

        if result['status'] == 'completed':
            print('\n✅ Success! Video is ready to share.')

    except Exception as e:
        print(f'\n❌ Error: {e}')
        import traceback
        traceback.print_exc()

    print('\n' + '=' * 60)
    print('\n💡 Try other repositories:')
    print('   - facebook/react')
    print('   - microsoft/vscode')
    print('   - vuejs/vue')
    print('   - angular/angular')
    print('\n📚 Documentation: https://docs.vloex.com')


if __name__ == '__main__':
    main()
