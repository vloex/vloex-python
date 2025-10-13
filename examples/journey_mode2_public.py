"""
VLOEX SDK Example: Journey Mode 2 - URL with Guided Navigation (Public Site)
Use this to automate screenshot capture for public documentation sites
Vision AI analyzes each page automatically - no descriptions needed!
"""
from vloex import Vloex

def main():
    # Initialize VLOEX SDK
    vloex = Vloex('vs_live_...')  # Replace with your API key

    # Generate video from public URL - just specify which pages!
    result = vloex.videos.from_journey(
        product_url='https://api.vloex.com/docs',
        pages=[
            '/',
            '#tag/videos/POST/v1/generate',
            '#tag/videos/GET/v1/jobs/{job_id}/status'
        ],
        product_context='VLOEX API Documentation',
        step_duration=15,
        avatar_position='bottom-right',
        tone='professional'
    )

    if result['success']:
        print(f"Video generated successfully!")
        print(f"Video URL: {result['video_url']}")
        print(f"Duration: {result['duration_seconds']}s")
        print(f"File size: {result['file_size_mb']:.2f} MB")
        print(f"Cost: ${result['cost']:.2f}")
        print(f"Steps: {result['steps_count']}")
    else:
        print(f"Video generation failed: {result['error']}")

if __name__ == '__main__':
    main()
