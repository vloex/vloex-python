# VLOEX Python SDK Examples

Production-ready examples showing real-world use cases for the VLOEX Python SDK.

## 📦 Available Examples

### [github-release-video.py](./github-release-video.py)
**Automatically generate announcement videos from GitHub releases**

Perfect for:
- Open source project maintainers
- Developer relations teams
- Product teams sharing feature updates
- CI/CD pipelines

**What it does:**
1. Fetches the latest release from any GitHub repository
2. Extracts key changes and highlights
3. Formats a professional video script
4. Generates and polls for video completion
5. Returns the final video URL

### [github-release-with-webhook.py](./github-release-with-webhook.py) 🆕
**GitHub release videos with webhooks (async notifications)**

**Why webhooks?**
- ✅ No polling required - get instant notifications when video is ready
- ✅ Reduced API calls - save on rate limits
- ✅ Better architecture - event-driven, not polling-based
- ✅ Perfect for long-running tasks and serverless environments

**What it includes:**
1. Video generation with webhook URL
2. Complete Flask webhook receiver with signature verification
3. HMAC security implementation
4. Production best practices
5. ngrok setup for local testing

**Run it:**
```bash
# Set your API key
export VLOEX_API_KEY=vs_live_your_key_here

# Install dependencies
pip install vloex requests

# Run the example
python github-release-video.py
```

**Customize it:**
```python
# Try different repositories
generate_release_video(api_key, 'facebook', 'react')
generate_release_video(api_key, 'microsoft', 'vscode')
generate_release_video(api_key, 'vuejs', 'vue')
```

## 🔑 Getting Your API Key

1. Sign up at [vloex.com](https://vloex.com)
2. Go to Dashboard → API Keys
3. Create a new key or copy your existing key
4. Set it as an environment variable: `export VLOEX_API_KEY=vs_live_...`

## 🚀 More Examples Coming Soon

- **CI/CD Pipeline Notifications** - Send video updates when builds complete
- **Product Launch Announcements** - Auto-generate launch videos from product data
- **Customer Onboarding** - Create personalized welcome videos
- **Social Media Automation** - Generate content for Twitter, LinkedIn, etc.

## 📚 Documentation

- [Python SDK Documentation](../README.md)
- [VLOEX API Docs](https://api.vloex.com/docs)
- [Get Support](https://github.com/vloex/vloex-python/issues)

## 💡 Contributing Examples

Have a great use case? We'd love to add it!

1. Fork the repository
2. Create your example file
3. Add comprehensive comments and documentation
4. Submit a pull request

Make sure your example:
- Solves a real-world problem
- Includes detailed comments
- Handles errors gracefully
- Uses environment variables for API keys
- Follows Python best practices
