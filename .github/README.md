# GitHub Actions Workflows

This directory contains GitHub Actions workflows for automated CI/CD processes for the Open To Close API project.

## Workflows

### 1. CI (`ci.yml`)
**Trigger**: Push to `main`/`develop` branches, PRs to `main`/`develop`

**Features**:
- Tests on Python 3.8-3.12
- Code formatting with Black
- Import sorting with isort
- Linting with flake8
- Type checking with mypy
- Testing with pytest (100% coverage required)
- Security vulnerability scanning with safety
- Package building and validation

### 2. Documentation (`docs.yml`)
**Trigger**: Push to `main`/`master` affecting docs/, PRs, manual trigger

**Features**:
- Builds MkDocs documentation
- Deploys to GitHub Pages on main branch pushes
- Adds helpful PR comments for documentation changes
- Runs tests to ensure code examples work

### 3. Release (`release.yml`)
**Trigger**: Version tags (e.g., `v1.0.0`)

**Features**:
- Validates version consistency across files
- Runs full test suite
- Builds and publishes to PyPI
- Creates GitHub releases with auto-generated changelogs
- Uploads build artifacts

### 4. Netlify Deployment (`deploy-netlify.yml`) - Optional
**Trigger**: Push to `main` affecting docs/, manual trigger

**Features**:
- Alternative to GitHub Pages
- Deploys documentation to Netlify
- Requires `NETLIFY_AUTH_TOKEN` and `NETLIFY_SITE_ID` secrets

## Required Secrets

Configure these in your GitHub repository settings (`Settings > Secrets and variables > Actions`):

### Required for all workflows:
- `OPEN_TO_CLOSE_API_KEY`: Your Open To Close API key for testing

### Required for releases:
- `PYPI_API_TOKEN`: PyPI API token for package publishing

### Optional (for Netlify):
- `NETLIFY_AUTH_TOKEN`: Netlify authentication token
- `NETLIFY_SITE_ID`: Your Netlify site ID

## Environment Setup

The release workflow uses a `release` environment for additional protection. Configure this in:
`Settings > Environments > New environment > release`

You can add protection rules like:
- Required reviewers
- Wait timer
- Deployment branches (restrict to main/master)

## Usage

### Running CI
CI runs automatically on pushes and PRs. Ensure your code:
- Passes all tests
- Is formatted with Black
- Has correct import order (isort)
- Passes type checking (mypy)
- Has 100% test coverage

### Deploying Documentation
Documentation deploys automatically when docs/ files change on main branch.
To preview locally: `mkdocs serve`

### Creating Releases
1. Update version in `pyproject.toml` and `open_to_close_api/__init__.py`
2. Commit changes
3. Create and push a version tag: `git tag v1.0.1 && git push origin v1.0.1`
4. The release workflow will automatically:
   - Test the package
   - Build and publish to PyPI
   - Create a GitHub release

## Maintenance

- Update Python versions in the matrix as needed
- Keep GitHub Actions versions current
- Monitor security advisories for dependencies
- Review and update coverage requirements as project grows 