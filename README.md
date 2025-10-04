# VLOEX Python SDK

Video generation as a computing primitive.

## Installation

```bash
pip install vloex
```

## Usage

```python
from vloex import Vloex

vloex = Vloex('vs_live_...')

# Generate a video
video = vloex.videos.create(
    script='Version 2.0 is now live with dark mode and AI chat!'
)

print(video['id'])      # → "job_abc123"
print(video['status'])  # → "processing"

# Check status
updated = vloex.videos.retrieve(video['id'])
print(updated['status'])  # → "completed"
print(updated['url'])     # → "https://..."
```

## API

### `vloex.videos.create(script, **options)`

Create a video from text.

**Arguments:**
- `script` (str, required) - The text script for your video
- `**options` (optional):
  - `avatar` - Avatar to use (default: 'lily')
  - `voice` - Voice tone (default: 'excited')
  - `background` - Background setting (default: 'modern_office')
  - `webhook_url` - URL to call when complete

**Returns:** `dict` with `id` and `status`

### `vloex.videos.retrieve(id)`

Get video status and URL.

**Arguments:**
- `id` (str, required) - Video job ID

**Returns:** `dict` with current status

## Examples

### Basic video generation

```python
from vloex import Vloex

vloex = Vloex('vs_live_...')

video = vloex.videos.create(
    script='We just shipped a major update!'
)
```

### With options

```python
video = vloex.videos.create(
    script='Check out our new features',
    avatar='lily',
    voice='professional',
    background='modern_office'
)
```

### Wait for completion

```python
import time
from vloex import Vloex

vloex = Vloex('vs_live_...')

video = vloex.videos.create(script='Release notes for v2.0')

# Poll until complete
while True:
    status = vloex.videos.retrieve(video['id'])

    if status['status'] == 'completed':
        print(f"Video ready: {status['url']}")
        break

    if status['status'] == 'failed':
        print(f"Failed: {status['error']}")
        break

    time.sleep(5)  # Wait 5s
```

### Using webhooks

```python
video = vloex.videos.create(
    script='Product update',
    webhook_url='https://yourapp.com/webhooks/vloex'
)

# VLOEX will POST to your webhook when done
```

## Error Handling

```python
from vloex import Vloex, VloexError

vloex = Vloex('vs_live_...')

try:
    video = vloex.videos.create(script='Hello world')
except VloexError as e:
    if e.status_code == 401:
        print('Invalid API key')
    elif e.status_code == 429:
        print('Rate limit exceeded')
    else:
        print(f'Error: {e.message}')
```

## Type Hints

Full type hint support:

```python
from vloex import Vloex
from typing import Dict

vloex: Vloex = Vloex('vs_live_...')

video: Dict[str, str] = vloex.videos.create(
    script='New release',
    avatar='lily'
)
```

## Documentation

Full API documentation: https://docs.vloex.com

## Support

- GitHub: https://github.com/vloex/vloex-python
- Email: support@vloex.com
- Docs: https://docs.vloex.com

## License

MIT
