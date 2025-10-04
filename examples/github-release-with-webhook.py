"""
Generate Videos from GitHub Releases with Webhooks
==================================================

This example shows how to use webhooks for async video generation,
eliminating the need for polling.

Benefits of Webhooks:
--------------------
- ✅ No polling required - get notified when video is ready
- ✅ Reduced API calls - save on rate limits
- ✅ Better architecture - event-driven, not polling-based
- ✅ Faster response - instant notification vs 5-second polling

Use Cases:
----------
- CI/CD pipelines that continue other tasks while video generates
- Serverless functions with limited execution time
- High-volume video generation workloads
- Applications that need real-time notifications

Requirements:
-------------
pip install vloex requests flask

Get your API key from: https://vloex.com/dashboard/api-keys
"""

import os
import requests
from vloex import Vloex, VloexError

# ============================================================================
# Part 1: Video Generation with Webhook
# ============================================================================

def generate_release_video_with_webhook(api_key, repo_owner, repo_name, webhook_url, webhook_secret=None):
    """
    Generate a video from GitHub release with webhook notification.

    Args:
        api_key (str): Your VLOEX API key
        repo_owner (str): GitHub repo owner (e.g., 'vercel')
        repo_name (str): GitHub repo name (e.g., 'next.js')
        webhook_url (str): Your webhook endpoint URL
        webhook_secret (str, optional): Secret for HMAC signature verification

    Returns:
        dict: Video job details
    """
    # Fetch latest release
    release_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest'
    response = requests.get(release_url)
    response.raise_for_status()
    release = response.json()

    # Extract release information
    version = release.get('tag_name', 'Unknown')
    name = release.get('name', version)
    body = release.get('body', 'No release notes available.')

    # Format script for video
    script = f"""
    Hey everyone! {name} is here!

    We're excited to announce {version} with some amazing updates.

    {body[:500]}...

    Check out the full release notes on GitHub to learn more.
    Update now to get these improvements!
    """

    # Initialize VLOEX client
    vloex = Vloex(api_key)

    # Create video with webhook (no need to wait!)
    video = vloex.videos.create(
        script=script,
        webhook_url=webhook_url,
        webhook_secret=webhook_secret  # Optional: for signature verification
    )

    print(f"✅ Video job created: {video.id}")
    print(f"📤 Webhook will be called at: {webhook_url}")
    print(f"🎬 You can continue with other tasks - webhook will notify you when ready!")

    return video


# ============================================================================
# Part 2: Webhook Receiver (Flask Example)
# ============================================================================

from flask import Flask, request, jsonify
import hmac
import hashlib
import time

app = Flask(__name__)

# Store your webhook secret (same as used in generate_video call)
WEBHOOK_SECRET = os.getenv('VLOEX_WEBHOOK_SECRET', 'my_secret_key_123')


def verify_webhook_signature(payload_json, signature, timestamp, secret):
    """
    Verify HMAC signature from VLOEX webhook.

    This prevents unauthorized webhook calls and replay attacks.
    """
    # Check timestamp is not too old (prevent replay attacks)
    if abs(time.time() - int(timestamp)) > 300:  # 5 minutes tolerance
        return False

    # Reconstruct the signed message
    message = f"{timestamp}.{payload_json}"

    # Calculate expected signature
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    # Compare signatures (constant-time comparison prevents timing attacks)
    provided_signature = signature.split('=')[1] if '=' in signature else signature
    return hmac.compare_digest(expected_signature, provided_signature)


@app.route('/api/vloex-webhook', methods=['POST'])
def handle_vloex_webhook():
    """
    Handle incoming VLOEX webhooks.

    This endpoint receives notifications when videos are completed.
    """
    # Get headers
    signature = request.headers.get('X-VLOEX-Signature', '')
    timestamp = request.headers.get('X-VLOEX-Timestamp', '')

    # Get raw payload for signature verification
    payload_json = request.get_data(as_text=True)

    # Verify signature (if secret was provided)
    if WEBHOOK_SECRET and signature:
        if not verify_webhook_signature(payload_json, signature, timestamp, WEBHOOK_SECRET):
            print("❌ Invalid webhook signature!")
            return jsonify({"error": "Invalid signature"}), 401

    # Parse payload
    payload = request.get_json()

    # Handle different webhook events
    event = payload.get('event')
    job_id = payload.get('job_id')

    if event == 'video.completed':
        video_url = payload.get('video_url')
        print(f"✅ Video {job_id} completed!")
        print(f"📹 Video URL: {video_url}")

        # TODO: Process the completed video
        # - Upload to CDN
        # - Send email notification
        # - Update database
        # - Trigger next step in pipeline

    elif event == 'video.failed':
        error = payload.get('error')
        print(f"❌ Video {job_id} failed!")
        print(f"🔴 Error: {error}")

        # TODO: Handle failure
        # - Retry with different options
        # - Send error notification
        # - Log to error tracking

    # Always return 200 to acknowledge receipt
    # (Prevents VLOEX from retrying)
    return jsonify({"status": "received"}), 200


# ============================================================================
# Part 3: Express.js Webhook Receiver (Alternative)
# ============================================================================

"""
// Node.js / Express.js example
const express = require('express');
const crypto = require('crypto');

const app = express();
app.use(express.json());

const WEBHOOK_SECRET = process.env.VLOEX_WEBHOOK_SECRET || 'my_secret_key_123';

function verifyWebhookSignature(payloadJson, signature, timestamp, secret) {
  // Check timestamp
  if (Math.abs(Date.now() / 1000 - parseInt(timestamp)) > 300) {
    return false;
  }

  // Calculate expected signature
  const message = `${timestamp}.${payloadJson}`;
  const expectedSignature = crypto
    .createHmac('sha256', secret)
    .update(message)
    .digest('hex');

  // Compare signatures
  const providedSignature = signature.split('=')[1] || signature;
  return crypto.timingSafeEqual(
    Buffer.from(expectedSignature),
    Buffer.from(providedSignature)
  );
}

app.post('/api/vloex-webhook', (req, res) => {
  const signature = req.headers['x-vloex-signature'] || '';
  const timestamp = req.headers['x-vloex-timestamp'] || '';
  const payloadJson = JSON.stringify(req.body);

  // Verify signature
  if (WEBHOOK_SECRET && signature) {
    if (!verifyWebhookSignature(payloadJson, signature, timestamp, WEBHOOK_SECRET)) {
      console.error('❌ Invalid webhook signature!');
      return res.status(401).json({ error: 'Invalid signature' });
    }
  }

  // Handle webhook
  const { event, job_id, video_url, error } = req.body;

  if (event === 'video.completed') {
    console.log(`✅ Video ${job_id} completed!`);
    console.log(`📹 Video URL: ${video_url}`);
    // TODO: Process completed video
  } else if (event === 'video.failed') {
    console.log(`❌ Video ${job_id} failed!`);
    console.log(`🔴 Error: ${error}`);
    // TODO: Handle failure
  }

  res.status(200).json({ status: 'received' });
});

app.listen(3000, () => {
  console.log('📡 Webhook receiver listening on port 3000');
});
"""


# ============================================================================
# Part 4: Usage Examples
# ============================================================================

def example_basic_webhook():
    """Basic webhook usage - start video generation and move on"""
    api_key = os.getenv('VLOEX_API_KEY')
    webhook_url = "https://your-app.com/api/vloex-webhook"

    video = generate_release_video_with_webhook(
        api_key=api_key,
        repo_owner='vercel',
        repo_name='next.js',
        webhook_url=webhook_url
    )

    # Video is generating in background
    # Your webhook will be called when ready
    # Continue with other tasks...
    print("🚀 Video generation started, continuing with other tasks...")


def example_webhook_with_signature():
    """Webhook with HMAC signature for security"""
    api_key = os.getenv('VLOEX_API_KEY')
    webhook_url = "https://your-app.com/api/vloex-webhook"
    webhook_secret = "my_secret_key_123"  # Store this securely!

    video = generate_release_video_with_webhook(
        api_key=api_key,
        repo_owner='vercel',
        repo_name='next.js',
        webhook_url=webhook_url,
        webhook_secret=webhook_secret  # Enables HMAC signature
    )

    print("✅ Video generation started with webhook signature verification")


def example_ngrok_local_testing():
    """Test webhooks locally using ngrok"""
    # 1. Start your Flask webhook receiver:
    #    python github-release-with-webhook.py

    # 2. In another terminal, start ngrok:
    #    ngrok http 5000

    # 3. Use the ngrok HTTPS URL as your webhook_url:
    api_key = os.getenv('VLOEX_API_KEY')
    ngrok_url = "https://abc123.ngrok.io/api/vloex-webhook"  # Replace with your ngrok URL

    video = generate_release_video_with_webhook(
        api_key=api_key,
        repo_owner='vercel',
        repo_name='next.js',
        webhook_url=ngrok_url
    )

    print("🔗 Webhook will be delivered to ngrok tunnel")
    print("   Check ngrok dashboard to see incoming webhook: http://localhost:4040")


# ============================================================================
# Part 5: Production Best Practices
# ============================================================================

"""
Production Checklist:
--------------------

1. ✅ Verify webhook signatures (use webhook_secret)
2. ✅ Return 200 OK quickly (process async)
3. ✅ Handle duplicate deliveries (use job_id for idempotency)
4. ✅ Validate timestamp (prevent replay attacks)
5. ✅ Use HTTPS webhook URLs (required in production)
6. ✅ Implement retry logic on your side (if webhook processing fails)
7. ✅ Log all webhook events for debugging
8. ✅ Monitor webhook delivery success rate

Example Production Setup:
-------------------------

1. Use a message queue (Redis, RabbitMQ) to process webhooks async
2. Store webhook events in database for audit trail
3. Implement idempotency using job_id
4. Set up monitoring/alerting for failed webhooks
5. Use webhook signatures in production
6. Have a fallback to polling if webhooks fail
"""


if __name__ == '__main__':
    # Run Flask webhook receiver
    print("🚀 Starting VLOEX webhook receiver...")
    print("📡 Webhook endpoint: http://localhost:5000/api/vloex-webhook")
    print("\nTo test:")
    print("1. Start ngrok: ngrok http 5000")
    print("2. Run: python github-release-with-webhook.py")
    print("3. Use ngrok URL as webhook_url\n")

    app.run(host='0.0.0.0', port=5000, debug=True)
