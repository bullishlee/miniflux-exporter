# Pre-Commit Checklist

Use this checklist before committing code to ensure all quality checks pass.

## Quick Commands

Run all checks at once:
```bash
black miniflux_exporter/ && \
isort miniflux_exporter/ && \
flake8 miniflux_exporter --count --select=E9,F63,F7,F82 && \
pytest tests/ -v
```

## Individual Checks

### 1. Format Code with Black ✨
```bash
# Format code
black miniflux_exporter/

# Check formatting (don't modify)
black --check miniflux_exporter/
```

### 2. Sort Imports with isort 📦
```bash
# Sort imports
isort miniflux_exporter/

# Check imports (don't modify)
isort --check-only miniflux_exporter/
```

### 3. Check Syntax with flake8 🔍
```bash
# Critical errors only (E9, F63, F7, F82)
flake8 miniflux_exporter --count --select=E9,F63,F7,F82 --show-source --statistics

# All warnings (optional)
flake8 miniflux_exporter --count --max-complexity=10 --max-line-length=127 --statistics
```

### 4. Run Tests with pytest 🧪
```bash
# Run all tests with coverage
pytest tests/ -v --cov=miniflux_exporter --cov-report=term-missing

# Quick test run
pytest tests/ -v

# Run specific test
pytest tests/test_basic.py::test_version -v
```

### 5. Type Check with mypy (Optional) 🔤
```bash
mypy miniflux_exporter --ignore-missing-imports
```

### 6. Security Check with bandit (Optional) 🔒
```bash
bandit -r miniflux_exporter -ll
```

## Pre-Commit Workflow

1. **Make your changes** to the code

2. **Format and organize**:
   ```bash
   black miniflux_exporter/
   isort miniflux_exporter/
   ```

3. **Run tests**:
   ```bash
   pytest tests/ -v
   ```

4. **Check for errors**:
   ```bash
   flake8 miniflux_exporter --count --select=E9,F63,F7,F82
   ```

5. **Stage and commit**:
   ```bash
   git add .
   git commit -m "your message"
   ```

6. **Push**:
   ```bash
   git push
   ```

## CI/CD Pipeline

GitHub Actions will automatically run these checks on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

The pipeline includes:
- ✅ Code formatting (Black)
- ✅ Import sorting (isort)
- ✅ Linting (flake8, pylint)
- ✅ Type checking (mypy)
- ✅ Tests (pytest)
- ✅ Coverage reporting (Codecov)
- ✅ Security scanning (bandit)

## Installation

Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

Or install individually:
```bash
pip install black isort flake8 pylint mypy pytest pytest-cov bandit
```

## Configuration

All tool configurations are in `pyproject.toml`:
- Black: Line length 88, Python 3.6+
- isort: Profile "black" for compatibility
- pytest: Coverage reporting enabled
- mypy: Ignore missing imports

## Troubleshooting

### Black and isort conflict
If Black and isort produce conflicting results:
1. Run `isort` first
2. Then run `black`
3. Black's formatting takes precedence

### Tests fail locally but pass in CI
- Check Python version (3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12)
- Ensure all dependencies are installed
- Check for environment-specific issues

### Flake8 errors
Common errors and fixes:
- `E9`: Syntax errors - fix the Python syntax
- `F63`: Invalid print statement - use `print()` function
- `F7`: Import but unused - remove unused imports
- `F82`: Undefined name - define the variable/function

## Best Practices

1. **Always format before committing**: `black miniflux_exporter/`
2. **Keep imports organized**: `isort miniflux_exporter/`
3. **Write tests for new features**: Coverage goal is 80%+
4. **Run tests locally**: Don't rely solely on CI
5. **Fix errors immediately**: Don't let them accumulate
6. **Use meaningful commit messages**: Follow conventional commits

## Conventional Commit Messages

Format: `<type>(<scope>): <subject>`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `ci`: CI/CD changes
- `perf`: Performance improvements

Examples:
```bash
git commit -m "feat(exporter): add support for filtering by date"
git commit -m "fix(config): handle missing API key gracefully"
git commit -m "docs: update installation instructions"
git commit -m "style: format code with black"
git commit -m "test: add tests for sanitize_filename"
```

## Quick Reference

| Tool | Purpose | Command |
|------|---------|---------|
| black | Code formatting | `black miniflux_exporter/` |
| isort | Import sorting | `isort miniflux_exporter/` |
| flake8 | Linting | `flake8 miniflux_exporter` |
| pylint | Advanced linting | `pylint miniflux_exporter` |
| mypy | Type checking | `mypy miniflux_exporter` |
| pytest | Testing | `pytest tests/ -v` |
| bandit | Security | `bandit -r miniflux_exporter` |

---

**Remember**: Code quality is everyone's responsibility! 🚀