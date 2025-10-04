# VLOEX Python SDK

Official Python SDK for VLOEX - Turn text into professional videos with AI.

[![PyPI version](https://badge.fury.io/py/vloex.svg)](https://pypi.org/project/vloex/)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📦 Installation

```bash
pip install vloex
```

**Requirements:** Python 3.7 or higher

---

## 🚀 Quick Start (5 minutes)

### Step 1: Get Your API Key

1. Sign up at [vloex.com](https://vloex.com)
2. Go to **Dashboard** → **API Keys**
3. Click **Create New Key**
4. Copy your key (starts with `vs_live_...`)

### Step 2: Set Your API Key

**Option A: Environment Variable (Recommended)**
```bash
export VLOEX_API_KEY='vs_live_your_key_here'
```

**Option B: In Code**
```python
from vloex import Vloex

vloex = Vloex('vs_live_your_key_here')
```

### Step 3: Generate Your First Video

```python
from vloex import Vloex

# Initialize client
vloex = Vloex('vs_live_your_key_here')

# Create a video
video = vloex.videos.create(
    script="Hello! This is my first AI-generated video using VLOEX."
)

print(f"✅ Video job created: {video['id']}")
print(f"📊 Status: {video['status']}")
```

### Step 4: Wait for Video to Complete

```python
import time

# Poll for completion (simple approach)
while True:
    status = vloex.videos.retrieve(video['id'])

    if status['status'] == 'completed':
        print(f"🎉 Video ready!")
        print(f"📹 URL: {status['url']}")
        break

    if status['status'] == 'failed':
        print(f"❌ Failed: {status.get('error')}")
        break

    print(f"⏳ Status: {status['status']}... waiting 5 seconds")
    time.sleep(5)
```

**That's it!** You just created your first AI video. 🎉

---

## 📚 Complete Guide for Beginners

### Understanding Video Generation

1. **You send text** (the script for your video)
2. **VLOEX processes it** (creates video with AI avatar, voice, visuals)
3. **You get back a video URL** (ready to share/download)

**Important:** Video generation takes 2-5 minutes. You have two options:

#### Option 1: Polling (Simple but not ideal)
```python
# Keep checking "is it done yet?" every 5 seconds
while video['status'] != 'completed':
    time.sleep(5)
    video = vloex.videos.retrieve(video['id'])
```

❌ **Problem:** Wastes API calls, blocks your code

#### Option 2: Webhooks (Recommended ✅)
```python
# Get notified when video is ready - no polling needed!
video = vloex.videos.create(
    script="Hello world",
    webhook_url="https://your-app.com/webhook"  # We'll call this when done
)
# Your code continues immediately!
```

✅ **Better:** Event-driven, no wasted API calls, non-blocking

---

## 🎯 Step-by-Step Examples

### Example 1: Basic Video (For Testing)

**Goal:** Create a simple video to test your API key

```python
from vloex import Vloex
import os

# Step 1: Get API key from environment
api_key = os.getenv('VLOEX_API_KEY')

# Step 2: Initialize client
vloex = Vloex(api_key)

# Step 3: Create video
video = vloex.videos.create(
    script="Testing VLOEX API. This is my first video!"
)

print(f"Job ID: {video['id']}")
print(f"Status: {video['status']}")
```

**What you'll get:**
- `job_id`: Unique ID like `"abc-123-def-456"`
- `status`: Initially `"pending"` or `"processing"`

---

### Example 2: Wait for Video with Polling

**Goal:** Generate video and wait until it's ready

```python
from vloex import Vloex
import time

vloex = Vloex('vs_live_your_key_here')

# Create video
video = vloex.videos.create(
    script="This video demonstrates polling. We'll check every 5 seconds until it's done."
)

print(f"🎬 Creating video: {video['id']}")
print("⏳ Waiting for completion...\n")

# Poll every 5 seconds
max_wait = 300  # 5 minutes
start_time = time.time()

while time.time() - start_time < max_wait:
    # Get current status
    status = vloex.videos.retrieve(video['id'])

    print(f"Status: {status['status']}")

    if status['status'] == 'completed':
        print(f"\n✅ SUCCESS!")
        print(f"📹 Video URL: {status['url']}")
        print(f"⏱️  Took {int(time.time() - start_time)} seconds")
        break

    if status['status'] == 'failed':
        print(f"\n❌ FAILED: {status.get('error', 'Unknown error')}")
        break

    # Wait before checking again
    time.sleep(5)
else:
    print("\n⏱️ Timeout: Video took too long")
```

---

### Example 3: Webhooks (Best Practice)

**Goal:** Get notified when video is ready without polling

**Step 1: Create a webhook receiver (Flask)**

```python
# webhook_receiver.py
from flask import Flask, request, jsonify
import hmac
import hashlib

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """Receive VLOEX webhook when video completes"""

    # Get the payload
    payload = request.get_json()

    # Handle different events
    if payload['event'] == 'video.completed':
        print(f"✅ Video {payload['job_id']} completed!")
        print(f"📹 URL: {payload['video_url']}")

        # TODO: Your code here
        # - Save to database
        # - Send email notification
        # - Upload to CDN
        # - etc.

    elif payload['event'] == 'video.failed':
        print(f"❌ Video {payload['job_id']} failed!")
        print(f"Error: {payload['error']}")

    # Always return 200 OK
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(port=5000)
```

**Step 2: Generate video with webhook**

```python
# generate_with_webhook.py
from vloex import Vloex

vloex = Vloex('vs_live_your_key_here')

# Create video with webhook
video = vloex.videos.create(
    script="This video uses webhooks. No polling needed!",
    webhook_url="https://your-app.com/webhook"  # Your Flask endpoint
)

print(f"✅ Video job created: {video['id']}")
print(f"📤 Webhook will be called when ready!")
print(f"🚀 Your code can continue immediately...")

# Your code continues - no need to wait!
# Webhook will notify you when done
```

**Step 3: Test locally with ngrok**

```bash
# Terminal 1: Start Flask webhook receiver
python webhook_receiver.py

# Terminal 2: Start ngrok tunnel
ngrok http 5000

# Terminal 3: Use ngrok URL in your code
python generate_with_webhook.py
```

**Full example:** See [examples/github-release-with-webhook.py](./examples/github-release-with-webhook.py)

---

### Example 4: Real-World - GitHub Release Videos

**Goal:** Automatically create videos for GitHub releases

```python
from vloex import Vloex
import requests

# Step 1: Fetch latest GitHub release
release_url = 'https://api.github.com/repos/vercel/next.js/releases/latest'
release = requests.get(release_url).json()

# Step 2: Extract information
version = release['tag_name']  # e.g., "v15.5.4"
changes = release['body'][:500]  # First 500 chars

# Step 3: Create video script
script = f"""
Hey everyone! {version} is here!

We're excited to announce Next.js {version} with some amazing updates.

{changes}

Check out the full release notes on GitHub to learn more.
Update now to get these improvements!
"""

# Step 4: Generate video
vloex = Vloex('vs_live_your_key_here')

video = vloex.videos.create(script=script)

print(f"✅ Release video created: {video['id']}")
```

**Full example:** See [examples/github-release-video.py](./examples/github-release-video.py)

---

## 📖 API Reference

### Initialize Client

```python
from vloex import Vloex

# From environment variable
vloex = Vloex()  # Reads VLOEX_API_KEY automatically

# Or pass directly
vloex = Vloex('vs_live_your_key_here')

# With custom options
vloex = Vloex(
    api_key='vs_live_...',
    base_url='https://api.vloex.com',  # Custom API endpoint
    timeout=30  # Request timeout in seconds
)
```

---

### Create Video

```python
video = vloex.videos.create(
    script="Your video script here",

    # Optional: Customize avatar, voice, background
    options={
        'avatar': 'lily',              # Professional female (default)
        'voice': 'excited',            # Enthusiastic tone (default)
        'background': 'modern_office'  # Clean workspace (default)
    },

    # Optional: Webhook for async notification
    webhook_url="https://your-app.com/webhook",
    webhook_secret="your_secret_key"  # For HMAC verification
)
```

**Available Customization:**

| Option | Values | Description |
|--------|--------|-------------|
| `avatar` | `lily` (default), `anna`, `tyler` | AI presenter |
| `voice` | `excited` (default), `friendly`, `professional` | Voice tone |
| `background` | `modern_office` (default), `conference_room`, `tech_office` | Background scene |

**Returns:**
```python
{
    'id': 'abc-123-def-456',       # Job ID
    'status': 'pending',            # Current status
    'created_at': '2025-01-04...',  # Timestamp
    'estimated_completion': '...'   # When it should be done
}
```

---

### Get Video Status

```python
video = vloex.videos.retrieve('abc-123-def-456')
```

**Returns:**
```python
{
    'id': 'abc-123-def-456',
    'status': 'completed',  # pending | processing | completed | failed
    'url': 'https://...',   # Video URL (when completed)
    'thumbnail_url': '...', # Preview image
    'duration': 12.5,       # Video length in seconds
    'error': None,          # Error message (if failed)
    'created_at': '...',
    'updated_at': '...'
}
```

---

## 🔐 Webhooks (Advanced)

### Why Use Webhooks?

**Polling (Old Way):**
```python
# ❌ Bad: Wastes API calls, blocks code
while video['status'] != 'completed':
    time.sleep(5)
    video = vloex.videos.retrieve(video['id'])  # API call every 5s
```

**Webhooks (Modern Way):**
```python
# ✅ Good: Event-driven, no wasted calls, non-blocking
video = vloex.videos.create(
    script="...",
    webhook_url="https://your-app.com/webhook"
)
# Your code continues immediately!
# Webhook notifies you when done
```

### Webhook Payload

When video completes, VLOEX sends:

```http
POST https://your-app.com/webhook
Content-Type: application/json

{
  "event": "video.completed",
  "job_id": "abc-123",
  "status": "completed",
  "video_url": "https://api.vloex.com/videos/abc-123.mp4",
  "error": null,
  "timestamp": "2025-01-04T12:00:00Z"
}
```

### Webhook Security (HMAC Verification)

```python
from flask import Flask, request
import hmac
import hashlib
import time

app = Flask(__name__)
WEBHOOK_SECRET = 'your_secret_key'

@app.route('/webhook', methods=['POST'])
def webhook():
    # Get signature from headers
    signature = request.headers.get('X-VLOEX-Signature', '')
    timestamp = request.headers.get('X-VLOEX-Timestamp', '')

    # Get raw payload
    payload_json = request.get_data(as_text=True)

    # Verify signature
    if not verify_signature(payload_json, signature, timestamp, WEBHOOK_SECRET):
        return 'Invalid signature', 401

    # Process webhook
    payload = request.get_json()
    print(f"Video {payload['job_id']} completed!")

    return 'OK', 200

def verify_signature(payload, signature, timestamp, secret):
    # Check timestamp (prevent replay attacks)
    if abs(time.time() - int(timestamp)) > 300:  # 5 min tolerance
        return False

    # Calculate expected signature
    message = f"{timestamp}.{payload}"
    expected = hmac.new(
        secret.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()

    # Compare (constant-time to prevent timing attacks)
    provided = signature.split('=')[1] if '=' in signature else signature
    return hmac.compare_digest(expected, provided)
```

**Full webhook guide:** [Backend WEBHOOKS.md](https://github.com/vloex/vloex-video/blob/main/backend/WEBHOOKS.md)

---

## ⚠️ Error Handling

```python
from vloex import Vloex, VloexError

vloex = Vloex('vs_live_...')

try:
    video = vloex.videos.create(script="Hello world")

except VloexError as e:
    # Handle specific errors
    if e.status_code == 401:
        print("❌ Invalid API key")
        print("Get your key from: https://vloex.com/dashboard")

    elif e.status_code == 429:
        print("❌ Rate limit exceeded")
        print("Wait a moment and try again")

    elif e.status_code == 402:
        print("❌ Quota exceeded")
        print("Upgrade your plan or wait for reset")

    else:
        print(f"❌ Error: {e.message}")
        print(f"Status: {e.status_code}")
```

**Common Error Codes:**

| Code | Error | Solution |
|------|-------|----------|
| 401 | Invalid API key | Check your key at vloex.com/dashboard |
| 429 | Rate limit exceeded | Wait 1 minute or upgrade plan |
| 402 | Quota exceeded | Upgrade plan or wait for monthly reset |
| 400 | Bad request | Check your script/parameters |
| 500 | Server error | Retry in a few seconds |

---

## 📁 Real-World Examples

See the [`examples/`](./examples) directory for production-ready code:

### 1. [GitHub Release Videos](./examples/github-release-video.py)
Automatically create announcement videos from GitHub releases.

**Perfect for:**
- Open source project maintainers
- DevRel teams
- Product announcements
- CI/CD pipelines

**What it does:**
1. Fetches latest release from GitHub API
2. Extracts version and changes
3. Generates professional video
4. Returns shareable URL

### 2. [GitHub Releases with Webhooks](./examples/github-release-with-webhook.py) 🆕
Same as above but using webhooks (event-driven).

**Includes:**
- Complete Flask webhook receiver
- HMAC signature verification
- Production best practices
- ngrok local testing setup

---

## 🛠️ Advanced Configuration

### Custom API Endpoint

```python
vloex = Vloex(
    api_key='vs_live_...',
    base_url='https://custom-api.vloex.com'
)
```

### Request Timeout

```python
vloex = Vloex(
    api_key='vs_live_...',
    timeout=60  # 60 seconds (default: 30)
)
```

### Debug Mode

```python
import logging

logging.basicConfig(level=logging.DEBUG)

vloex = Vloex('vs_live_...')
# Will print all API requests/responses
```

---

## 🚀 Best Practices

### 1. Use Environment Variables for API Keys
```python
# ✅ Good
import os
vloex = Vloex(os.getenv('VLOEX_API_KEY'))

# ❌ Bad (hardcoded key)
vloex = Vloex('vs_live_abc123')  # Don't commit this!
```

### 2. Use Webhooks in Production
```python
# ✅ Good: Event-driven
video = vloex.videos.create(
    script="...",
    webhook_url="https://your-app.com/webhook"
)

# ❌ Bad: Polling wastes API calls
while video['status'] != 'completed':
    time.sleep(5)
    video = vloex.videos.retrieve(video['id'])
```

### 3. Handle Errors Gracefully
```python
# ✅ Good
try:
    video = vloex.videos.create(script="...")
except VloexError as e:
    logger.error(f"Video failed: {e}")
    return fallback_video_url
```

### 4. Set Reasonable Timeouts
```python
# ✅ Good: Set timeout based on your use case
vloex = Vloex(api_key='...', timeout=60)
```

---

## 📚 Resources

- **Documentation:** https://api.vloex.com/docs
- **Python SDK:** https://github.com/vloex/vloex-python
- **Node.js SDK:** https://github.com/vloex/vloex-node
- **Webhook Guide:** [WEBHOOKS.md](https://github.com/vloex/vloex-video/blob/main/backend/WEBHOOKS.md)
- **Examples:** [examples/](./examples)
- **PyPI Package:** https://pypi.org/project/vloex/

---

## 🆘 Support

- **Email:** support@vloex.com
- **GitHub Issues:** https://github.com/vloex/vloex-python/issues
- **Documentation:** https://docs.vloex.com

---

## 📝 Changelog

### v0.1.1 (2025-01-04)
- ✨ Added webhook support for async notifications
- 📝 Comprehensive documentation with step-by-step guides
- 🔒 HMAC signature verification for webhooks
- 📚 Real-world examples (GitHub releases)

### v0.1.0 (2025-01-03)
- 🎉 Initial release
- ✅ Video generation with polling
- ✅ Error handling
- ✅ Type hints

---

## 📄 License

MIT License - see [LICENSE](./LICENSE) for details

---

**Made with ❤️ by the VLOEX team**
