# Publishing vloex to PyPI

PyPI now requires API tokens instead of username/password authentication.

## Step 1: Create PyPI Account (if not already done)

1. Go to: https://pypi.org/account/register/
2. Username: `satsvloex`
3. Email: `sats@vloex.com`
4. Password: `SecureUsa@9099`
5. Verify your email address

## Step 2: Create API Token

1. Login to PyPI: https://pypi.org/account/login/
2. Go to Account Settings: https://pypi.org/manage/account/
3. Scroll to "API tokens" section
4. Click "Add API token"
5. Token name: `vloex-sdk-publish`
6. Scope: "Entire account" (for first-time publish)
7. Click "Add token"
8. **IMPORTANT:** Copy the token immediately (starts with `pypi-...`)
   - You'll only see it once!
   - Save it somewhere safe

## Step 3: Publish to PyPI

### Option A: Using token directly in command

```bash
cd /Users/vegullasatyaveerendra/Desktop/vloex/sdks/python

twine upload dist/* --username __token__ --password pypi-YOUR_TOKEN_HERE
```

Replace `pypi-YOUR_TOKEN_HERE` with the actual token.

### Option B: Create .pypirc file (recommended for repeated use)

Create file `~/.pypirc`:

```ini
[pypi]
username = __token__
password = pypi-YOUR_TOKEN_HERE
```

Then just run:
```bash
twine upload dist/*
```

## Step 4: Verify Publication

After successful upload, you should see:
```
Uploading vloex-0.1.0-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 10.6/10.6 kB
Uploading vloex-0.1.0.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 7.4/7.4 kB

View at:
https://pypi.org/project/vloex/0.1.0/
```

## Step 5: Test Installation

```bash
# Create test environment
python3 -m venv /tmp/test-vloex
source /tmp/test-vloex/bin/activate

# Install from PyPI
pip install vloex

# Test it works
python -c "from vloex import Vloex; print('✅ VLOEX SDK installed successfully!')"
```

## Quick Reference

### Get Token
1. https://pypi.org/manage/account/
2. Scroll to "API tokens"
3. Add token → Copy it

### Publish Command
```bash
twine upload dist/* --username __token__ --password pypi-YOUR_TOKEN_HERE
```

### After Publishing
- Package URL: https://pypi.org/project/vloex/
- Install: `pip install vloex`
- Usage: `from vloex import Vloex`

---

## Troubleshooting

### "Invalid or non-existent authentication"
- Make sure token starts with `pypi-`
- Username must be exactly `__token__` (with underscores)
- Copy token with no extra spaces

### "File already exists"
- Cannot re-upload same version
- Increment version in setup.py
- Rebuild: `python3 setup.py sdist bdist_wheel`

### "Project name already exists"
- Package `vloex` is already taken by someone else
- Change name in setup.py to `vloex-sdk` or `vloex-video`

---

## After Successful Publish

Update documentation:
- README.md: Add installation badge
- Website: Add "pip install vloex" to docs
- Tweet: "VLOEX Python SDK is now on PyPI! 🐍"

Track downloads:
- https://pypistats.org/packages/vloex
