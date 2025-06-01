# Getting Started

Get up and running with the Open To Close API Python client in just a few minutes. This section covers everything you need to start making API calls successfully.

---

## 🚀 Quick Navigation

<div class="grid cards" markdown>

-   :material-download:{ .lg .middle } **Installation**

    ---

    Install the Python client library and verify your setup

    [:octicons-arrow-right-24: Install Now](installation.md)

-   :material-key-variant:{ .lg .middle } **Authentication**

    ---

    Configure your API key and environment setup

    [:octicons-arrow-right-24: Setup Auth](authentication.md)

-   :material-rocket-launch:{ .lg .middle } **Quick Start**

    ---

    Make your first API call in under 5 minutes

    [:octicons-arrow-right-24: Start Tutorial](quickstart.md)

-   :material-cog:{ .lg .middle } **Configuration**

    ---

    Advanced client configuration and environment options

    [:octicons-arrow-right-24: Configure Client](configuration.md)

</div>

---

## 📋 Prerequisites

Before getting started, ensure you have:

!!! note "System Requirements"
    📋 **Python Version**: Python 3.8 or higher
    
    **Package Manager**: pip (included with Python)
    
    **API Access**: Valid Open To Close API key

!!! info "Development Environment"
    While not required, we recommend using:
    
    - Virtual environment (`venv` or `conda`)
    - Code editor with Python support (VS Code, PyCharm, etc.)
    - Git for version control

---

## ⚡ Quick Setup Path

For experienced developers who want to get started immediately:

=== ":material-terminal: Terminal Setup"

    ```bash
    # Create virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    
    # Install the client
    pip install open-to-close
    
    # Set your API key
    export OPEN_TO_CLOSE_API_KEY="your_api_key_here"
    ```

=== ":material-code-tags: First API Call"

    ```python
    from open_to_close import OpenToCloseAPI
    
    # Initialize client (automatically uses environment variable)
    client = OpenToCloseAPI()
    
    # Make your first API call
    properties = client.properties.list_properties()
    print(f"Found {len(properties)} properties")
    ```

=== ":material-check-circle: Verification"

    ```python
    # Test your setup
    try:
        # Simple test call
        result = client.agents.list_agents(params={"limit": 1})
        print("✅ Setup successful!")
        print(f"API is working, found agents: {len(result)}")
    except Exception as e:
        print(f"❌ Setup issue: {e}")
    ```

---

## 🎯 Learning Path

### **Beginner Path** 
New to the Open To Close API or Python API clients:

1. **[Installation](installation.md)** - Set up your environment step by step
2. **[Authentication](authentication.md)** - Learn about API keys and security
3. **[Quick Start](quickstart.md)** - Guided tutorial with explanations
4. **[Configuration](configuration.md)** - Understand all available options

### **Experienced Path**
Familiar with API clients and Python development:

1. **[Quick Start](quickstart.md)** - Jump straight to making API calls
2. **[Configuration](configuration.md)** - Customize for your needs
3. **[API Reference](../api/index.md)** - Explore all available methods

---

## 🔧 Common Setup Scenarios

### **Development Environment**
```python
# Development setup with verbose logging
import logging
from open_to_close import OpenToCloseAPI

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Initialize with explicit configuration
client = OpenToCloseAPI(
    api_key="your_development_key",
    base_url="https://api.opentoclose.com/v1"  # Production URL
)
```

### **Production Environment**
```python
# Production setup with environment variables
import os
from open_to_close import OpenToCloseAPI

# Verify environment is properly configured
if not os.getenv("OPEN_TO_CLOSE_API_KEY"):
    raise EnvironmentError("API key not found in environment")

# Initialize for production
client = OpenToCloseAPI()  # Uses environment variables
```

### **Testing Environment**
```python
# Testing setup with mock responses
from open_to_close import OpenToCloseAPI
import responses

# Mock API responses for testing
@responses.activate
def test_api_client():
    responses.add(
        responses.GET,
        "https://api.opentoclose.com/v1/properties",
        json={"results": []},
        status=200
    )
    
    client = OpenToCloseAPI(api_key="test_key")
    properties = client.properties.list_properties()
    assert properties == []
```

---

## 🆘 Troubleshooting

### **Common Issues**

!!! warning "Authentication Errors"
    If you're getting authentication errors:
    
    - Verify your API key is correct
    - Check that the environment variable is set properly
    - Ensure there are no extra spaces or characters
    - Try regenerating your API key

!!! warning "Import Errors"
    If the import fails:
    
    - Verify the package is installed: `pip list | grep open-to-close`
    - Check you're using the correct virtual environment
    - Try reinstalling: `pip install --upgrade open-to-close`

!!! warning "Connection Issues"
    If you can't connect to the API:
    
    - Check your internet connection
    - Verify the base URL is correct
    - Check if there are any firewall restrictions

### **Getting Help**

- **[Error Handling Guide](../guides/error-handling.md)** - Comprehensive error handling patterns
- **[Best Practices](../guides/best-practices.md)** - Recommended usage patterns
- **[GitHub Issues](https://github.com/theperrygroup/open-to-close/issues)** - Report bugs or request features

---

## 🚀 Next Steps

Once you've completed the setup:

1. **[Explore the API Reference](../api/index.md)** - See all available methods
2. **[Check out Examples](../guides/examples.md)** - Real-world usage patterns
3. **[Learn Best Practices](../guides/best-practices.md)** - Optimize your implementation 