# Contributing to Miniflux Exporter

Thank you for your interest in contributing to Miniflux Exporter! We welcome contributions from everyone.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

### Our Standards

- **Be respectful**: Treat everyone with respect and kindness
- **Be collaborative**: Work together and help each other
- **Be inclusive**: Welcome and support people of all backgrounds
- **Be constructive**: Provide helpful feedback and criticism

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** (code snippets, configuration files, etc.)
- **Describe the behavior you observed** and what you expected
- **Include screenshots** if applicable
- **Include your environment details**:
  - OS and version
  - Python version
  - Miniflux Exporter version
  - Miniflux version

**Bug Report Template:**

```markdown
**Description:**
A clear and concise description of the bug.

**Steps to Reproduce:**
1. Go to '...'
2. Run command '...'
3. See error

**Expected Behavior:**
What you expected to happen.

**Actual Behavior:**
What actually happened.

**Environment:**
- OS: [e.g., Ubuntu 22.04]
- Python: [e.g., 3.11]
- Miniflux Exporter: [e.g., 1.0.0]
- Miniflux: [e.g., 2.0.49]

**Additional Context:**
Add any other context about the problem here.
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested enhancement
- **Explain why this enhancement would be useful**
- **Provide examples** of how the feature would be used
- **List any alternatives** you've considered

**Enhancement Request Template:**

```markdown
**Feature Description:**
A clear description of the feature you'd like to see.

**Use Case:**
Explain how this feature would be used and who would benefit.

**Proposed Solution:**
Describe how you envision the feature working.

**Alternatives Considered:**
Any alternative solutions or features you've considered.

**Additional Context:**
Any other context, screenshots, or examples.
```

### Pull Requests

We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`
2. Make your changes
3. Add tests if applicable
4. Ensure tests pass
5. Update documentation if needed
6. Submit a pull request

## Development Setup

### Prerequisites

- Python 3.6 or higher
- Git
- pip and virtualenv

### Setup Steps

1. **Fork and clone the repository**

   ```bash
   git clone https://github.com/YOUR_USERNAME/miniflux-exporter.git
   cd miniflux-exporter
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Install in editable mode**

   ```bash
   pip install -e .
   ```

5. **Verify installation**

   ```bash
   miniflux-export --version
   ```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=miniflux_exporter

# Run specific test file
pytest tests/test_exporter.py

# Run with verbose output
pytest -v
```

### Code Quality Checks

```bash
# Format code with black
black miniflux_exporter/

# Sort imports
isort miniflux_exporter/

# Lint with flake8
flake8 miniflux_exporter/

# Type check with mypy
mypy miniflux_exporter/

# Lint with pylint
pylint miniflux_exporter/
```

### Running the Development Version

```bash
# Run with test configuration
miniflux-export --config examples/config.example.yaml --test

# Run with command-line arguments
miniflux-export --url https://demo.miniflux.app --api-key YOUR_KEY --test
```

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with some modifications:

- **Line length**: Maximum 127 characters
- **Imports**: Organized with `isort`
- **Formatting**: Automated with `black`
- **Type hints**: Use where appropriate
- **Docstrings**: Use Google style docstrings

### Code Style Example

```python
def export_articles(
    url: str,
    api_key: str,
    output_dir: str = "articles"
) -> Dict[str, Any]:
    """
    Export articles from Miniflux to Markdown.

    Args:
        url: Miniflux instance URL.
        api_key: API authentication key.
        output_dir: Directory to save exported articles.

    Returns:
        Dictionary containing export statistics.

    Raises:
        ValueError: If URL or API key is invalid.
        ConnectionError: If unable to connect to Miniflux.
    """
    # Implementation here
    pass
```

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- **Format**: `<type>(<scope>): <subject>`
- **Types**:
  - `feat`: New feature
  - `fix`: Bug fix
  - `docs`: Documentation changes
  - `style`: Code style changes (formatting, etc.)
  - `refactor`: Code refactoring
  - `test`: Adding or updating tests
  - `chore`: Maintenance tasks

**Examples:**

```
feat(exporter): add support for custom filename templates
fix(cli): handle connection timeout errors gracefully
docs(readme): update installation instructions
test(exporter): add tests for metadata generation
```

### Documentation

- **Code comments**: Explain "why", not "what"
- **Docstrings**: Use for all public functions, classes, and modules
- **README**: Keep up-to-date with features and usage
- **CHANGELOG**: Document all notable changes

## Submitting Changes

### Pull Request Process

1. **Create a branch**

   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-number-description
   ```

2. **Make your changes**
   - Write clean, readable code
   - Add tests for new features
   - Update documentation
   - Follow coding standards

3. **Commit your changes**

   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

4. **Push to your fork**

   ```bash
   git push origin feature/your-feature-name
   ```

5. **Open a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template

### Pull Request Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to break)
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added new tests for this change
- [ ] Updated existing tests

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added/updated
- [ ] All tests pass
```

### Review Process

- Maintainers will review your PR within a few days
- Address any requested changes
- Once approved, your PR will be merged
- Your contribution will be credited in the changelog

## Project Structure

```
miniflux-exporter/
├── miniflux_exporter/       # Main package
│   ├── __init__.py          # Package initialization
│   ├── cli.py               # Command-line interface
│   ├── exporter.py          # Core export logic
│   ├── config.py            # Configuration management
│   └── utils.py             # Utility functions
├── tests/                   # Test suite
├── docs/                    # Documentation
├── examples/                # Usage examples
├── docker/                  # Docker files
└── .github/                 # GitHub workflows
```

## Testing Guidelines

### Writing Tests

- **Unit tests**: Test individual functions
- **Integration tests**: Test component interactions
- **End-to-end tests**: Test complete workflows

**Test Example:**

```python
import pytest
from miniflux_exporter import MinifluxExporter, Config

def test_config_validation():
    """Test configuration validation."""
    config = Config({
        'miniflux_url': 'https://example.com',
        'api_key': 'test_key'
    })
    assert config.validate() is True

def test_invalid_url():
    """Test invalid URL handling."""
    config = Config({'miniflux_url': 'invalid'})
    with pytest.raises(ValueError):
        config.validate()
```

### Test Coverage

- Aim for >80% code coverage
- Write tests for edge cases
- Test error handling

## Documentation Guidelines

### Docstring Format

Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Short description of function.

    Longer description if needed, explaining the purpose
    and behavior of the function.

    Args:
        param1: Description of param1.
        param2: Description of param2.

    Returns:
        Description of return value.

    Raises:
        ValueError: When validation fails.
        ConnectionError: When connection fails.

    Example:
        >>> result = function_name("test", 42)
        >>> print(result)
        True
    """
    pass
```

## Getting Help

- **Documentation**: Check the [README](README.md) and [docs](docs/)
- **Issues**: Search existing [issues](https://github.com/bullishlee/miniflux-exporter/issues)
- **Discussions**: Join [discussions](https://github.com/bullishlee/miniflux-exporter/discussions)

## Recognition

Contributors will be recognized in:

- `CONTRIBUTORS.md` file
- Release notes
- GitHub contributors page

Thank you for contributing to Miniflux Exporter! 🎉