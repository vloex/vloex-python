"""
VLOEX SDK Example: Journey Mode 1 - Screenshots with Descriptions
Use this when you already have screenshots and know what each one shows
(Fastest method - no Vision AI needed!)
"""
from vloex import Vloex
import base64

def main():
    # Initialize VLOEX SDK
    vloex = Vloex('vs_live_...')  # Replace with your API key

    # Load your screenshots (from Figma, design tools, or manual captures)
    screenshot1_path = "path/to/login.png"
    screenshot2_path = "path/to/dashboard.png"

    # Read and encode screenshots
    with open(screenshot1_path, 'rb') as f:
        screenshot1_b64 = base64.b64encode(f.read()).decode('utf-8')

    with open(screenshot2_path, 'rb') as f:
        screenshot2_b64 = base64.b64encode(f.read()).decode('utf-8')

    # Generate video with YOUR descriptions (fast and cheap!)
    result = vloex.videos.from_journey(
        screenshots=[screenshot1_b64, screenshot2_b64],
        descriptions=[
            "Welcome to the login page. Enter your credentials to access the dashboard.",
            "The main dashboard shows all your metrics and recent activity at a glance."
        ],
        product_context='MyApp Product Demo',
        step_duration=10,
        avatar_position='bottom-right',
        tone='professional'
    )

    if result['success']:
        print(f"Video generated successfully!")
        print(f"Video URL: {result['video_url']}")
        print(f"Duration: {result['duration_seconds']}s")
        print(f"File size: {result['file_size_mb']:.2f} MB")
        print(f"Steps: {result['steps_count']}")
    else:
        print(f"Video generation failed: {result['error']}")

if __name__ == '__main__':
    main()
