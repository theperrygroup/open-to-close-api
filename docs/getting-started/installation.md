# Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Install from PyPI

```bash
pip install open-to-close
```

## Install from Source

For development or to get the latest features:

```bash
git clone https://github.com/theperrygroup/open-to-close.git
cd open-to-close
pip install -e .
```

## Development Installation

To contribute to the project:

```bash
# Clone the repository
git clone https://github.com/theperrygroup/open-to-close.git
cd open-to-close

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt
pip install -e .
```

## Verify Installation

```python
import open_to_close
print(open_to_close.__version__)
```

## Environment Setup

### API Key Configuration

Set your Open To Close API key as an environment variable:

**Linux/macOS:**
```bash
export OPEN_TO_CLOSE_API_KEY="your_api_key_here"
```

**Windows:**
```cmd
set OPEN_TO_CLOSE_API_KEY=your_api_key_here
```

### Using .env File

Create a `.env` file in your project root:

```env
OPEN_TO_CLOSE_API_KEY=your_actual_api_key_here
```

The client will automatically load this when you initialize it:

```python
from open_to_close import OpenToCloseAPI

# Automatically loads from environment or .env file
client = OpenToCloseAPI()
```

## Next Steps

- [Quick Start Guide](quickstart.md) - Get started with basic usage
- [API Reference](../reference/api-reference.md) - Explore all available methods
- [Examples](../guides/examples.md) - See comprehensive usage examples 