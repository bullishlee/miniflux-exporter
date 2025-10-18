# Troubleshooting GitHub Actions

This guide helps you diagnose and fix common GitHub Actions issues.

## 🔍 How to Check GitHub Actions Status

### View Workflow Runs

1. Go to your repository: https://github.com/bullishlee/miniflux-exporter
2. Click on the **"Actions"** tab
3. You'll see a list of recent workflow runs
4. Click on any run to see details

### Understanding Workflow Status

- ✅ **Green checkmark** = All checks passed
- ❌ **Red X** = One or more checks failed
- 🟡 **Yellow circle** = Workflow is running
- ⚪ **Gray circle** = Workflow is queued

### View Detailed Logs

1. Click on a workflow run
2. Click on a job (e.g., "Test on Python 3.12")
3. Expand individual steps to see logs
4. Look for error messages in red

---

## 🐛 Common Issues and Solutions

### Issue 1: Test Failures - `test_sanitize_filename`

**Error Message:**
```
AssertionError: assert 'hello_world' == 'hello_world_'
```

**Cause:**
GitHub Actions might be running an old version of the code due to caching.

**Solution:**
1. **Verify local code is correct:**
   ```bash
   cd miniflux-exporter
   cat tests/test_basic.py | grep "hello<world>"
   ```
   
   Should show:
   ```python
   assert sanitize_filename('hello<world>') == 'hello_world'
   ```

2. **Check remote repository:**
   ```bash
   git fetch origin
   git show origin/main:tests/test_basic.py | grep "hello<world>"
   ```

3. **Force new workflow run:**
   ```bash
   git commit --allow-empty -m "ci: trigger new workflow"
   git push
   ```

4. **Wait for the new run to start** (usually takes 10-30 seconds)

5. **Check the Actions tab** to verify it's using the latest commit

**Expected Result:**
After the fix in commit `16806ca`, this test should pass.

---

### Issue 2: CLI Command Not Found

**Error Message:**
```
miniflux-export: command not found
Error: Process completed with exit code 127
```

**Cause:**
The console script is not in the PATH in the CI environment.

**Solution:**
Already fixed in commits `aa725ef` and `96389a2`. The workflow now uses:
```bash
python -m miniflux_exporter --version
```

If you see this error, verify your workflow file has been updated:
```bash
git show origin/main:.github/workflows/test.yml | grep "python -m miniflux_exporter"
```

---

### Issue 3: Black Formatting Failures

**Error Message:**
```
would reformat /path/to/file.py
Oh no! 💥 💔 💥
5 files would be reformatted
```

**Cause:**
Code is not formatted according to Black standards.

**Solution:**
```bash
# Format all files
black miniflux_exporter/

# Verify formatting
black --check miniflux_exporter/

# Commit and push
git add miniflux_exporter/
git commit -m "style: format code with black"
git push
```

---

### Issue 4: isort Import Sorting Issues

**Error Message:**
```
ERROR: Imports are incorrectly sorted and/or formatted
```

**Cause:**
Imports are not sorted, or isort/Black configurations conflict.

**Solution:**
```bash
# Sort imports
isort miniflux_exporter/

# Verify
isort --check-only miniflux_exporter/

# Commit and push
git add miniflux_exporter/
git commit -m "style: sort imports with isort"
git push
```

**Note:** Make sure `pyproject.toml` has:
```toml
[tool.isort]
profile = "black"
```

---

### Issue 5: Workflow Using Old Code

**Symptoms:**
- Tests fail with errors that were already fixed
- Workflow shows correct commit but runs old code
- Local tests pass but GitHub Actions fails

**Possible Causes:**
1. GitHub Actions cache
2. Multiple concurrent workflow runs
3. Viewing an old workflow run

**Solution:**

1. **Check which commit is running:**
   - In GitHub Actions, look at the commit SHA in the workflow run
   - Compare it with your latest commit: `git log --oneline -1`

2. **Cancel old workflow runs:**
   - Go to Actions tab
   - Click on running workflows
   - Click "Cancel workflow"

3. **Clear GitHub Actions cache:**
   - Add this to your workflow (already included):
   ```yaml
   - name: Clear cache
     run: |
       rm -rf ~/.cache/pip
   ```

4. **Trigger a fresh workflow:**
   ```bash
   # Make a trivial change
   git commit --allow-empty -m "ci: trigger fresh workflow"
   git push
   ```

5. **Wait and refresh:**
   - GitHub Actions can take 10-60 seconds to start
   - Refresh the Actions page to see new runs

---

### Issue 6: Coverage Upload Fails

**Error Message:**
```
Error uploading to Codecov
```

**Cause:**
Usually a temporary Codecov service issue, or missing token.

**Solution:**
This is configured to not fail the CI (`fail_ci_if_error: false`), so it won't block your build.

To fix permanently:
1. Sign up at https://codecov.io
2. Add your repository
3. Get the upload token
4. Add it as a secret: `Settings → Secrets → CODECOV_TOKEN`

---

## 🔄 Workflow Files

### Current Workflows

1. **`test.yml`** - Main testing workflow
   - Runs on: Push to main/develop, Pull requests
   - Tests: Multiple OS (Ubuntu, macOS, Windows)
   - Python versions: 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12

2. **`release.yml`** - Release and publish
   - Runs on: Git tags (v*.*.*)
   - Builds: Python package, Docker images
   - Publishes: PyPI, Docker Hub, GitHub Releases

3. **`docker.yml`** - Docker image builds
   - Runs on: Push to main, Pull requests
   - Platforms: amd64, arm64, arm/v7

### Verify Workflow Content

```bash
# View test workflow
cat .github/workflows/test.yml

# View specific section
grep -A 5 "Test CLI commands" .github/workflows/test.yml
```

---

## 📋 Verification Checklist

Before assuming there's a problem:

- [ ] Check if you're looking at the latest workflow run
- [ ] Verify the commit SHA matches your latest push
- [ ] Check if old runs are still in progress
- [ ] Wait 1-2 minutes for new runs to appear
- [ ] Refresh the GitHub Actions page
- [ ] Check both "All workflows" and individual workflow tabs

---

## 🚀 Quick Commands

### Run All Quality Checks Locally

```bash
# This should match what GitHub Actions runs
black miniflux_exporter/
isort miniflux_exporter/
flake8 miniflux_exporter --count --select=E9,F63,F7,F82
pytest tests/ -v --cov=miniflux_exporter
```

### Check Remote Status

```bash
# Fetch latest from GitHub
git fetch origin

# Compare with remote
git log origin/main --oneline -5

# Check specific file on remote
git show origin/main:tests/test_basic.py | grep -n "hello<world>"
```

### Force Workflow Re-run

```bash
# Method 1: Empty commit
git commit --allow-empty -m "ci: re-run checks"
git push

# Method 2: Update timestamp file
date > .github/workflows/.timestamp
git add .github/workflows/.timestamp
git commit -m "ci: refresh timestamp"
git push
```

---

## 📊 Expected Results

After all fixes (as of commit `7bb6d41`):

```
✅ Lint with flake8        → 0 errors
✅ Check formatting        → All files formatted
✅ Type check with mypy    → Passed (warnings allowed)
✅ Run tests              → 14/14 passed
✅ Upload coverage        → 18% baseline
✅ Test CLI commands      → python -m miniflux_exporter works
✅ Check imports          → Sorted correctly
```

---

## 🆘 Still Having Issues?

### Check These Files

1. **Test file:** `tests/test_basic.py` line 60 should be:
   ```python
   assert sanitize_filename('hello<world>') == 'hello_world'
   ```

2. **Workflow file:** `.github/workflows/test.yml` should use:
   ```yaml
   python -m miniflux_exporter --version
   ```

3. **Config file:** `pyproject.toml` should exist with Black/isort config

### Get the Commit History

```bash
# Show commits that fixed tests
git log --oneline --all | grep -i "test\|fix"

# Key commits:
# 16806ca - test: fix sanitize_filename test assertion
# aa725ef - ci: fix CLI command testing to use python -m method
# cdec479 - build: add pyproject.toml
```

### Manual Verification

```bash
# Clone fresh and test
cd /tmp
git clone https://github.com/bullishlee/miniflux-exporter.git test-repo
cd test-repo
pip install -e .
pytest tests/ -v
```

---

## 📝 Notes

- **GitHub Actions cache:** Can take a few minutes to update
- **Multiple runs:** Cancel old runs if they're blocking new ones
- **Commit SHA:** Always verify you're looking at the right commit
- **Local vs CI:** Both should pass the same tests

---

## 📞 Need Help?

If you've tried everything above and still have issues:

1. **Document the problem:**
   - Which workflow is failing?
   - What's the commit SHA?
   - What's the exact error message?
   - Screenshot of the failure

2. **Check commit history:**
   ```bash
   git log --oneline -20
   ```

3. **Compare with working commit:**
   - Find a commit that worked
   - Use `git diff` to see what changed

4. **Open an issue:**
   - Include all the above information
   - Link to the failing workflow run

---

**Last Updated:** 2024-12-19  
**All issues should be resolved as of commit:** `7bb6d41`
