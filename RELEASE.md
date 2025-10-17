# Release Guide for Miniflux Exporter

This guide explains how to prepare and publish a new release of Miniflux Exporter.

## Table of Contents

- [Pre-Release Checklist](#pre-release-checklist)
- [Version Management](#version-management)
- [Creating a Release](#creating-a-release)
- [Publishing to PyPI](#publishing-to-pypi)
- [Publishing Docker Images](#publishing-docker-images)
- [Post-Release Tasks](#post-release-tasks)

---

## Pre-Release Checklist

Before creating a new release, ensure the following:

### 1. Code Quality

- [ ] All tests pass locally
- [ ] All CI/CD checks pass
- [ ] Code coverage is acceptable (>80%)
- [ ] No known critical bugs
- [ ] All linting checks pass

```bash
# Run all checks locally
pytest tests/ -v --cov=miniflux_exporter
black --check miniflux_exporter/
flake8 miniflux_exporter/
pylint miniflux_exporter/
mypy miniflux_exporter/
```

### 2. Documentation

- [ ] README.md is up to date
- [ ] README_CN.md is up to date
- [ ] CHANGELOG.md is updated with release notes
- [ ] All new features are documented
- [ ] Configuration examples are current
- [ ] API documentation is complete

### 3. Dependencies

- [ ] All dependencies are up to date
- [ ] No security vulnerabilities in dependencies
- [ ] requirements.txt is accurate
- [ ] setup.py dependencies match requirements.txt

```bash
# Check for outdated packages
pip list --outdated

# Check for security vulnerabilities
pip install safety
safety check
```

### 4. Version Numbers

- [ ] Version updated in `miniflux_exporter/__init__.py`
- [ ] Version updated in `setup.py`
- [ ] Version follows semantic versioning

---

## Version Management

### Semantic Versioning

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality (backwards-compatible)
- **PATCH** version for backwards-compatible bug fixes

**Examples:**
- `1.0.0` → `1.0.1` (bug fix)
- `1.0.1` → `1.1.0` (new feature)
- `1.1.0` → `2.0.0` (breaking change)

### Updating Version Numbers

Update version in the following files:

1. **`miniflux_exporter/__init__.py`**
   ```python
   __version__ = "1.1.0"
   ```

2. **`setup.py`**
   ```python
   setup(
       name='miniflux-exporter',
       version='1.1.0',
       ...
   )
   ```

3. **`docker/Dockerfile`** (LABEL)
   ```dockerfile
   LABEL version="1.1.0"
   ```

---

## Creating a Release

### 1. Update CHANGELOG.md

Add a new section for the release:

```markdown
## [1.1.0] - 2024-01-15

### Added
- New feature X
- Support for Y

### Changed
- Improved Z performance
- Updated dependency A to version B

### Fixed
- Bug #123: Description
- Issue with error handling

### Deprecated
- Feature X will be removed in v2.0.0

### Security
- Fixed vulnerability CVE-XXXX-XXXX
```

### 2. Commit Version Changes

```bash
# Stage changes
git add miniflux_exporter/__init__.py setup.py CHANGELOG.md

# Commit with conventional commit message
git commit -m "chore(release): prepare version 1.1.0"

# Push to main branch
git push origin main
```

### 3. Create Git Tag

```bash
# Create annotated tag
git tag -a v1.1.0 -m "Release version 1.1.0"

# Push tag to remote
git push origin v1.1.0
```

### 4. GitHub Release

The GitHub release will be created automatically by the `release.yml` workflow when you push a tag. Alternatively, create it manually:

1. Go to: https://github.com/bullishlee/miniflux-exporter/releases
2. Click "Draft a new release"
3. Choose the tag `v1.1.0`
4. Release title: `Release v1.1.0`
5. Description: Copy content from CHANGELOG.md
6. Upload any additional assets (optional)
7. Click "Publish release"

---

## Publishing to PyPI

### Prerequisites

1. **Create PyPI account**: https://pypi.org/account/register/
2. **Create API token**: https://pypi.org/manage/account/token/
3. **Add token to GitHub Secrets**: `PYPI_API_TOKEN`

### Manual Publishing (if needed)

```bash
# Install build tools
pip install build twine

# Build distribution packages
python -m build

# Check the distribution
twine check dist/*

# Upload to TestPyPI (optional, for testing)
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

### Automatic Publishing

Publishing to PyPI is automatic when you push a tag:
1. Push a tag starting with `v` (e.g., `v1.1.0`)
2. GitHub Actions will build and publish automatically
3. Check the workflow: Actions → Release

---

## Publishing Docker Images

### Prerequisites

1. **Docker Hub account**: https://hub.docker.com/
2. **Add credentials to GitHub Secrets**:
   - `DOCKERHUB_USERNAME`
   - `DOCKERHUB_TOKEN`

### Manual Building

```bash
# Build for local platform
cd docker
docker build -t miniflux-exporter:1.1.0 .

# Build for multiple platforms
docker buildx create --use
docker buildx build \
  --platform linux/amd64,linux/arm64,linux/arm/v7 \
  -t bullishlee/miniflux-exporter:1.1.0 \
  -t bullishlee/miniflux-exporter:latest \
  --push \
  .
```

### Automatic Publishing

Docker images are built and pushed automatically:
1. Push a tag starting with `v` (e.g., `v1.1.0`)
2. GitHub Actions will build multi-platform images
3. Images are pushed to:
   - Docker Hub: `bullishlee/miniflux-exporter:1.1.0`
   - GHCR: `ghcr.io/bullishlee/miniflux-exporter:1.1.0`

---

## Post-Release Tasks

### 1. Verify Release

- [ ] Check PyPI page: https://pypi.org/project/miniflux-exporter/
- [ ] Test installation: `pip install miniflux-exporter==1.1.0`
- [ ] Test Docker image: `docker pull bullishlee/miniflux-exporter:1.1.0`
- [ ] Verify GitHub release page
- [ ] Check that all assets are uploaded

### 2. Test Installation

```bash
# Create clean virtual environment
python -m venv test-env
source test-env/bin/activate

# Install from PyPI
pip install miniflux-exporter==1.1.0

# Verify installation
miniflux-export --version
miniflux-export --help

# Clean up
deactivate
rm -rf test-env
```

### 3. Update Documentation

- [ ] Update any documentation that references version numbers
- [ ] Update examples if API changed
- [ ] Create migration guide if there are breaking changes

### 4. Announce Release

Consider announcing the release:
- [ ] GitHub Discussions
- [ ] Twitter/Social media
- [ ] Reddit (r/selfhosted, r/Python, etc.)
- [ ] Miniflux community
- [ ] Personal blog/website

**Announcement Template:**

```markdown
🎉 Miniflux Exporter v1.1.0 Released!

New features:
- Feature X
- Feature Y

Improvements:
- Better performance
- Enhanced error handling

Get it now:
pip install miniflux-exporter==1.1.0

Full changelog: https://github.com/bullishlee/miniflux-exporter/releases/tag/v1.1.0
```

### 5. Monitor for Issues

After release:
- Monitor GitHub issues for bug reports
- Watch PyPI download statistics
- Check Docker Hub pull statistics
- Respond to community feedback

---

## Hotfix Releases

For urgent bug fixes:

1. Create a hotfix branch from the release tag:
   ```bash
   git checkout -b hotfix/1.1.1 v1.1.0
   ```

2. Make the fix and commit:
   ```bash
   git commit -m "fix: urgent bug fix"
   ```

3. Update version to `1.1.1`

4. Merge back to main:
   ```bash
   git checkout main
   git merge hotfix/1.1.1
   ```

5. Tag and release as normal:
   ```bash
   git tag -a v1.1.1 -m "Hotfix release 1.1.1"
   git push origin v1.1.1
   ```

---

## Rollback Procedure

If a release has critical issues:

### PyPI Rollback
```bash
# You cannot delete a version, but you can yank it
# This prevents new installations but allows existing ones
pip install twine
twine yank miniflux-exporter 1.1.0
```

### Docker Rollback
```bash
# Remove the 'latest' tag and point it to previous version
docker pull bullishlee/miniflux-exporter:1.0.0
docker tag bullishlee/miniflux-exporter:1.0.0 bullishlee/miniflux-exporter:latest
docker push bullishlee/miniflux-exporter:latest
```

### GitHub Release
1. Edit the release on GitHub
2. Mark it as "Pre-release" to warn users
3. Add a warning to the description
4. Create a new hotfix release

---

## Troubleshooting

### Build Fails

```bash
# Clean build artifacts
rm -rf build dist *.egg-info

# Rebuild
python -m build
```

### Upload to PyPI Fails

```bash
# Check credentials
twine check dist/*

# Use --verbose for more information
twine upload --verbose dist/*
```

### Docker Build Fails

```bash
# Check Dockerfile syntax
docker build --no-cache -t test .

# Build with verbose output
docker build --progress=plain -t test .
```

---

## Release Checklist Summary

**Before Release:**
- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version numbers updated
- [ ] Dependencies checked

**Creating Release:**
- [ ] Commit version changes
- [ ] Create and push git tag
- [ ] GitHub release created

**After Release:**
- [ ] Verify PyPI package
- [ ] Verify Docker image
- [ ] Test installation
- [ ] Announce release
- [ ] Monitor for issues

---

## Contact

For questions about the release process, contact the maintainers or open a discussion on GitHub.

**Happy Releasing! 🚀**