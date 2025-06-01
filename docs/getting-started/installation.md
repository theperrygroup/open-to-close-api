# Installation

Install the Open To Close API Python client and set up your development environment. This guide covers multiple installation methods and verification steps.

---

## 🎯 Installation Methods

### **Standard Installation (Recommended)**

Install the latest stable version from PyPI using pip:

```bash
pip install open-to-close
```

### **Development Installation**

For development work or to get the latest features:

```bash
# Install from GitHub
pip install git+https://github.com/theperrygroup/open-to-close.git

# Or clone and install in development mode
git clone https://github.com/theperrygroup/open-to-close.git
cd open-to-close
pip install -e .
```

### **Specific Version Installation**

To install a specific version:

```bash
# Install specific version
pip install open-to-close==2.0.7

# Install with version constraints
pip install "open-to-close>=2.0.0,<3.0.0"
```

---

## 🐍 Python Version Requirements

!!! note "Supported Python Versions"
    📋 The client supports **Python 3.8** and higher:
    
    - Python 3.8 ✅
    - Python 3.9 ✅  
    - Python 3.10 ✅
    - Python 3.11 ✅
    - Python 3.12 ✅

### **Check Your Python Version**

```bash
# Check Python version
python --version

# Or more detailed version info
python -c "import sys; print(sys.version)"
```

If you need to upgrade Python, visit [python.org](https://www.python.org/downloads/) for installation instructions.

---

## 🔧 Virtual Environment Setup

We strongly recommend using a virtual environment to avoid dependency conflicts:

=== ":material-folder: Using venv (Built-in)"

    ```bash
    # Create virtual environment
    python -m venv open-to-close-env
    
    # Activate on macOS/Linux
    source open-to-close-env/bin/activate
    
    # Activate on Windows
    open-to-close-env\Scripts\activate
    
    # Install the client
    pip install open-to-close
    ```

=== ":material-snake: Using conda"

    ```bash
    # Create conda environment
    conda create -n open-to-close-env python=3.11
    
    # Activate environment
    conda activate open-to-close-env
    
    # Install the client
    pip install open-to-close
    ```

=== ":material-application: Using pyenv"

    ```bash
    # Install Python version if needed
    pyenv install 3.11.0
    pyenv local 3.11.0
    
    # Create virtual environment
    python -m venv venv
    source venv/bin/activate
    
    # Install the client
    pip install open-to-close
    ```

---

## 📦 Dependencies

The client has minimal dependencies that are automatically installed:

### **Required Dependencies**

| Package | Version | Purpose |
|---------|---------|---------|
| `requests` | >=2.25.0 | HTTP client for API calls |
| `python-dotenv` | >=0.19.0 | Environment variable loading |

### **Development Dependencies**

If you're contributing to the project, install development dependencies:

```bash
# Install with development dependencies
pip install "open-to-close[dev]"

# Or install from source with dev dependencies
git clone https://github.com/theperrygroup/open-to-close.git
cd open-to-close
pip install -e ".[dev]"
```

---

## ✅ Verify Installation

After installation, verify everything is working correctly:

### **Basic Import Test**

```python
# Test basic import
try:
    from open_to_close import OpenToCloseAPI
    print("✅ Import successful!")
except ImportError as e:
    print(f"❌ Import failed: {e}")
```

### **Version Check**

```python
# Check installed version
import open_to_close
print(f"Open To Close API Client version: {open_to_close.__version__}")
```

### **Dependencies Check**

```python
# Verify all dependencies are available
try:
    import requests
    import dotenv
    print("✅ All dependencies available")
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
```

### **Command Line Verification**

```bash
# Check installed packages
pip list | grep open-to-close

# Show package information
pip show open-to-close
```

---

## 🔄 Updating the Client

Keep your client up to date with the latest features and bug fixes:

### **Standard Update**

```bash
# Update to latest version
pip install --upgrade open-to-close
```

### **Update with Version Constraints**

```bash
# Update within major version
pip install --upgrade "open-to-close>=2.0.0,<3.0.0"

# Update to specific version
pip install --upgrade open-to-close==2.0.7
```

### **Check for Updates**

```bash
# Check if updates are available
pip list --outdated | grep open-to-close

# Show current and available versions
pip install open-to-close==
```

---

## 🆘 Troubleshooting Installation

### **Common Issues**

!!! warning "Permission Errors"
    If you get permission errors during installation:
    
    ```bash
    # Use --user flag to install for current user only
    pip install --user open-to-close
    
    # Or ensure you're in a virtual environment
    python -m venv venv && source venv/bin/activate
    pip install open-to-close
    ```

!!! warning "SSL Certificate Errors"
    If you encounter SSL certificate issues:
    
    ```bash
    # Upgrade pip and certificates
    pip install --upgrade pip
    pip install --upgrade certifi
    
    # Install with trusted hosts (temporary workaround)
    pip install --trusted-host pypi.org --trusted-host pypi.python.org open-to-close
    ```

!!! warning "Network/Proxy Issues"
    If you're behind a corporate firewall:
    
    ```bash
    # Install with proxy settings
    pip install --proxy http://proxy.company.com:8080 open-to-close
    
    # Or configure pip permanently
    pip config set global.proxy http://proxy.company.com:8080
    ```

### **Environment Issues**

!!! info "Virtual Environment Not Working"
    If virtual environment activation fails:
    
    ```bash
    # Recreate virtual environment
    rm -rf venv
    python -m venv venv
    
    # Use full path to activate (macOS/Linux)
    source ./venv/bin/activate
    
    # Use full path to activate (Windows)
    ./venv/Scripts/activate
    ```

!!! info "Import Path Issues"
    If imports fail after installation:
    
    ```python
    # Check Python path
    import sys
    print(sys.path)
    
    # Check where package is installed
    import open_to_close
    print(open_to_close.__file__)
    ```

### **Getting Help**

If you continue to have issues:

- **[GitHub Issues](https://github.com/theperrygroup/open-to-close/issues)** - Report installation problems
- **[Python Packaging Guide](https://packaging.python.org/)** - General pip and packaging help
- **[Virtual Environment Guide](https://docs.python.org/3/tutorial/venv.html)** - Official venv documentation

---

## 🚀 Next Steps

Now that you have the client installed:

1. **[Set up authentication](authentication.md)** - Configure your API key
2. **[Try the quick start](quickstart.md)** - Make your first API call
3. **[Explore configuration options](configuration.md)** - Customize the client

---

## 📋 Installation Checklist

- [ ] Python 3.8+ installed and verified
- [ ] Virtual environment created and activated  
- [ ] `open-to-close` package installed via pip
- [ ] Import test successful
- [ ] Dependencies verified
- [ ] Ready to configure authentication

Once all items are checked, proceed to **[Authentication Setup](authentication.md)**. 