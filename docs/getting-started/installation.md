# Installation Guide

Get the Open To Close API Python client installed and configured in your environment quickly and easily.

!!! note "📋 Prerequisites"
    Before installing, ensure you have the following requirements:
    
    - **Python 3.8 or higher** - Check with `python --version`
    - **pip package manager** - Usually included with Python

## 🚀 Quick Installation

=== "From PyPI (Recommended)"
    Install the latest stable version from the Python Package Index:

    ```bash
    pip install open-to-close
    ```

    !!! success "✅ That's it!"
        You're ready to use the client. Jump to [verification](#verify-installation) to confirm everything works.

=== "From Source"
    For development or to get the latest features:

    ```bash
    git clone https://github.com/theperrygroup/open-to-close.git
    cd open-to-close
    pip install -e .
    ```

    !!! tip "💡 Development Mode"
        The `-e` flag installs in "editable" mode, so changes to the source code are immediately available.

=== "Using pipx"
    Install in an isolated environment using pipx:

    ```bash
    pipx install open-to-close
    ```

    !!! info "📝 About pipx"
        pipx installs packages in isolated environments, preventing dependency conflicts.

## 🔧 Development Installation

For contributors or advanced users who want to modify the source code:

!!! warning "⚠️ Development Setup"
    This section is for developers who plan to contribute to the project or need the absolute latest features.

=== "Complete Setup"
    ```bash
    # Clone the repository
    git clone https://github.com/theperrygroup/open-to-close.git
    cd open-to-close

    # Create virtual environment
    python -m venv .venv
    
    # Activate virtual environment
    source .venv/bin/activate  # Linux/macOS
    # .venv\Scripts\activate   # Windows

    # Install development dependencies
    pip install -r requirements-dev.txt
    pip install -e .
    ```

=== "Platform-Specific"
    === "Linux/macOS"
        ```bash
        python -m venv .venv
        source .venv/bin/activate
        pip install -r requirements-dev.txt
        pip install -e .
        ```

    === "Windows"
        ```cmd
        python -m venv .venv
        .venv\Scripts\activate
        pip install -r requirements-dev.txt
        pip install -e .
        ```

=== "Using Make"
    ```bash
    # If Makefile is available
    make install-dev
    make test
    ```

## ✅ Verify Installation

Confirm the installation was successful:

!!! example "🧪 Quick Test"
    ```python
    import open_to_close
    print(f"Successfully installed version: {open_to_close.__version__}")
    ```

    Expected output: `Successfully installed version: x.x.x`

## 🔑 Environment Setup

### API Key Configuration

!!! warning "🔐 API Key Required"
    You'll need a valid Open To Close API key to use the client. Contact your administrator or check your account settings.

=== "Environment Variable"
    **Linux/macOS:**
    ```bash
    export OPEN_TO_CLOSE_API_KEY="your_api_key_here"
    ```

    **Windows Command Prompt:**
    ```cmd
    set OPEN_TO_CLOSE_API_KEY=your_api_key_here
    ```

    **Windows PowerShell:**
    ```powershell
    $env:OPEN_TO_CLOSE_API_KEY="your_api_key_here"
    ```

=== ".env File"
    Create a `.env` file in your project root:

    ```env
    OPEN_TO_CLOSE_API_KEY=your_actual_api_key_here
    ```

    !!! tip "💡 Best Practice"
        Using a `.env` file is recommended for development. Add `.env` to your `.gitignore` to keep your API key secure.

=== "Direct Configuration"
    You can also provide the API key directly in your code:

    ```python
    from open_to_close import OpenToCloseAPI

    client = OpenToCloseAPI(api_key="your_api_key_here")
    ```

    !!! warning "⚠️ Security Note"
        Only use direct configuration for testing. Never commit API keys to version control.

### Verification Test

Test your API key configuration:

```python
from open_to_close import OpenToCloseAPI, AuthenticationError

try:
    client = OpenToCloseAPI()
    # Test with a simple API call
    result = client.contacts.list_contacts(top=1)
    print("✅ API key is valid and working!")
except AuthenticationError:
    print("❌ Invalid API key. Please check your configuration.")
except Exception as e:
    print(f"⚠️ Connection issue: {e}")
```

## 🚫 Troubleshooting

!!! note "📋 Common Issues"

=== "Installation Issues"
    **Permission Error:**
    ```bash
    # Use --user flag to install for current user only
    pip install --user open-to-close
    ```

    **Python Version Error:**
    ```bash
    # Check your Python version
    python --version
    
    # Use specific Python version if needed
    python3.8 -m pip install open-to-close
    ```

=== "Import Issues"
    **ModuleNotFoundError:**
    ```python
    # Ensure you're in the correct environment
    import sys
    print(sys.path)
    
    # Reinstall if necessary
    pip uninstall open-to-close
    pip install open-to-close
    ```

=== "API Key Issues"
    **Authentication Failed:**
    
    1. ✅ Check API key format (no extra spaces)
    2. ✅ Verify environment variable name
    3. ✅ Confirm API key is active
    4. ✅ Test with a simple API call

## 📋 What's Next?

Choose your next step:

<div class="grid cards" markdown>

-   :material-flash:{ .lg .middle } **Quick Start**

    ---

    Jump right in with a 5-minute tutorial

    [:octicons-arrow-right-24: Quick Start Guide](quickstart.md)

-   :material-code-tags:{ .lg .middle } **Examples**

    ---

    See comprehensive usage examples

    [:octicons-arrow-right-24: View Examples](../guides/examples.md)

-   :material-api:{ .lg .middle } **API Reference**

    ---

    Explore complete API documentation

    [:octicons-arrow-right-24: API Docs](../reference/api-reference.md)

-   :material-wrench:{ .lg .middle } **Need Help?**

    ---

    Check troubleshooting guide

    [:octicons-arrow-right-24: Get Help](../guides/troubleshooting.md)

</div> 