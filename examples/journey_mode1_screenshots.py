"""
VLOEX SDK Example: Journey Mode 1 - Provide Screenshots
Use this when you already have screenshots or custom automation
"""
import asyncio
import base64
from pathlib import Path
from vloex import Vloex

async def main():
    # Initialize VLOEX SDK
    vloex = Vloex('vs_live_...')  # Replace with your API key

    # Load screenshots from files
    screenshot1_path = Path('screenshot1.png')
    screenshot2_path = Path('screenshot2.png')

    # Convert to base64
    screenshot1_b64 = base64.b64encode(screenshot1_path.read_bytes()).decode('utf-8')
    screenshot2_b64 = base64.b64encode(screenshot2_path.read_bytes()).decode('utf-8')

    # Generate video from screenshots
    result = vloex.videos.from_journey(
        screenshots=[screenshot1_b64, screenshot2_b64],
        product_context='My Product Demo - Key Features',
        step_duration=15,
        avatar_position='bottom-right',
        tone='professional'
    )

    print(f"Video generated successfully!")
    print(f"Video URL: {result['video_url']}")
    print(f"Duration: {result['duration_seconds']}s")
    print(f"Cost: ${result['cost']:.2f}")

if __name__ == '__main__':
    asyncio.run(main())
