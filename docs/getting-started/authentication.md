# Authentication

Configure authentication for the Open To Close API Python client. This guide covers API key setup, security best practices, and multiple configuration methods.

---

## 🔑 API Key Setup

The Open To Close API uses API key authentication. You'll need a valid API key to make requests.

!!! note "Getting Your API Key"
    📋 Contact your Open To Close administrator or account representative to obtain your API key. Each organization has unique API credentials.

### **API Key Format**

Your API key will look something like this:
```
MWI2TnluVjdxRVZPdm00eUREblRNQT09OmlPT2M0UlRKY2cyVEZmeUdqTk9PVVRrclJLZXdoancxOmE4ODZjMmVmNTI3MGQyNGM0YWY5N2Y1ZWZjOWQ5M2Q2OWVmMTgyMzZhMmY3YTEwZTI3MDk0ZWM1YmI4MTk4MTg=
```

---

## 🛡️ Security Best Practices

!!! warning "Security Considerations"
    ⚠️ **Never log sensitive credentials in error messages. Always sanitize authentication errors before logging.**
    
    - Never commit API keys to version control
    - Use environment variables for production deployments
    - Rotate API keys regularly
    - Monitor API key usage for unusual activity

### **What NOT to do**

```python
# ❌ DON'T: Hard-code API keys
client = OpenToCloseAPI(api_key="MWI2TnluVjdxRVZPdm00eUREYmx...")

# ❌ DON'T: Include in configuration files committed to git
config = {
    "api_key": "MWI2TnluVjdxRVZPdm00eUREYmx...",
    "base_url": "https://api.opentoclose.com/v1"
}

# ❌ DON'T: Log API keys
print(f"Using API key: {api_key}")
```

### **What TO do**

```python
# ✅ DO: Use environment variables
client = OpenToCloseAPI()  # Automatically reads from environment

# ✅ DO: Load from secure configuration
import os
api_key = os.getenv("OPEN_TO_CLOSE_API_KEY")
if not api_key:
    raise ValueError("API key not found in environment")

# ✅ DO: Sanitize error logging
try:
    client = OpenToCloseAPI()
except AuthenticationError:
    logger.error("Authentication failed - check API key configuration")
```

---

## 🔧 Configuration Methods

### **Method 1: Environment Variables (Recommended)**

The most secure and flexible approach for production environments:

=== ":material-bash: Linux/macOS"

    ```bash
    # Set environment variable for current session
    export OPEN_TO_CLOSE_API_KEY="your_api_key_here"
    
    # Add to shell profile for persistence (.bashrc, .zshrc, etc.)
    echo 'export OPEN_TO_CLOSE_API_KEY="your_api_key_here"' >> ~/.bashrc
    source ~/.bashrc
    ```

=== ":material-microsoft-windows: Windows"

    ```cmd
    # Command Prompt
    set OPEN_TO_CLOSE_API_KEY=your_api_key_here
    
    # PowerShell
    $env:OPEN_TO_CLOSE_API_KEY="your_api_key_here"
    
    # Permanent (System Properties > Environment Variables)
    # Add OPEN_TO_CLOSE_API_KEY to user or system environment variables
    ```

=== ":material-docker: Docker"

    ```dockerfile
    # In Dockerfile
    ENV OPEN_TO_CLOSE_API_KEY=""
    
    # Or in docker-compose.yml
    environment:
      - OPEN_TO_CLOSE_API_KEY=${OPEN_TO_CLOSE_API_KEY}
    ```

Then use the client without explicit configuration:

```python
from open_to_close import OpenToCloseAPI

# Automatically uses OPEN_TO_CLOSE_API_KEY environment variable
client = OpenToCloseAPI()
```

### **Method 2: .env Files**

For development environments, use a `.env` file:

**Create `.env` file:**
```bash
# .env file (add to .gitignore!)
OPEN_TO_CLOSE_API_KEY=your_api_key_here
OPEN_TO_CLOSE_BASE_URL=https://api.opentoclose.com/v1
```

**Load in your application:**
```python
from dotenv import load_dotenv
from open_to_close import OpenToCloseAPI

# Load environment variables from .env file
load_dotenv()

# Client automatically uses loaded environment variables
client = OpenToCloseAPI()
```

!!! warning "Don't Commit .env Files"
    Add `.env` to your `.gitignore` file to prevent accidentally committing secrets:
    ```gitignore
    # .gitignore
    .env
    .env.local
    .env.production
    ```

### **Method 3: Direct Configuration**

For testing or when environment variables aren't practical:

```python
from open_to_close import OpenToCloseAPI

# Pass API key directly (not recommended for production)
client = OpenToCloseAPI(
    api_key="your_api_key_here",
    base_url="https://api.opentoclose.com/v1"  # Optional
)
```

---

## ✅ Verify Authentication

Test your authentication setup to ensure it's working correctly:

### **Basic Authentication Test**

```python
from open_to_close import OpenToCloseAPI
from open_to_close.exceptions import AuthenticationError

def test_authentication():
    """Test API authentication setup."""
    try:
        client = OpenToCloseAPI()
        
        # Make a simple API call to verify authentication
        result = client.agents.list_agents(params={"limit": 1})
        
        print("✅ Authentication successful!")
        print(f"API is working - found {len(result)} agents")
        return True
        
    except AuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

# Run the test
if __name__ == "__main__":
    test_authentication()
```

### **Environment Variable Check**

```python
import os

def check_environment():
    """Check if environment variables are properly set."""
    api_key = os.getenv("OPEN_TO_CLOSE_API_KEY")
    
    if not api_key:
        print("❌ OPEN_TO_CLOSE_API_KEY environment variable not found")
        return False
    
    if len(api_key) < 50:  # Basic length check
        print("⚠️ API key seems too short - check for truncation")
        return False
    
    print("✅ Environment variable properly set")
    print(f"API key length: {len(api_key)} characters")
    return True

check_environment()
```

---

## 🔧 Advanced Configuration

### **Multiple Environments**

Manage different API keys for different environments:

```python
import os
from open_to_close import OpenToCloseAPI

def get_client(environment="production"):
    """Get configured client for specific environment."""
    env_configs = {
        "development": {
            "api_key": os.getenv("DEV_OPEN_TO_CLOSE_API_KEY"),
            "base_url": "https://dev-api.opentoclose.com/v1"
        },
        "staging": {
            "api_key": os.getenv("STAGING_OPEN_TO_CLOSE_API_KEY"),
            "base_url": "https://staging-api.opentoclose.com/v1"
        },
        "production": {
            "api_key": os.getenv("OPEN_TO_CLOSE_API_KEY"),
            "base_url": "https://api.opentoclose.com/v1"
        }
    }
    
    config = env_configs.get(environment)
    if not config:
        raise ValueError(f"Unknown environment: {environment}")
    
    return OpenToCloseAPI(**config)

# Usage
dev_client = get_client("development")
prod_client = get_client("production")
```

### **Configuration Class**

Create a configuration class for complex setups:

```python
import os
from dataclasses import dataclass
from typing import Optional
from open_to_close import OpenToCloseAPI

@dataclass
class APIConfig:
    """Configuration for Open To Close API client."""
    api_key: str
    base_url: str = "https://api.opentoclose.com/v1"
    timeout: int = 30
    retry_attempts: int = 3
    
    @classmethod
    def from_environment(cls) -> "APIConfig":
        """Create configuration from environment variables."""
        api_key = os.getenv("OPEN_TO_CLOSE_API_KEY")
        if not api_key:
            raise ValueError("OPEN_TO_CLOSE_API_KEY environment variable required")
        
        return cls(
            api_key=api_key,
            base_url=os.getenv("OPEN_TO_CLOSE_BASE_URL", cls.base_url),
            timeout=int(os.getenv("API_TIMEOUT", cls.timeout)),
            retry_attempts=int(os.getenv("API_RETRY_ATTEMPTS", cls.retry_attempts))
        )

# Usage
config = APIConfig.from_environment()
client = OpenToCloseAPI(api_key=config.api_key, base_url=config.base_url)
```

---

## 🆘 Troubleshooting Authentication

### **Common Authentication Errors**

!!! warning "Invalid API Key"
    **Error**: `AuthenticationError: Invalid API key`
    
    **Solutions**:
    - Verify the API key is correctly copied (no extra spaces/characters)
    - Check that the environment variable is properly set
    - Ensure the API key hasn't expired or been revoked
    - Contact your administrator to verify API key status

!!! warning "Environment Variable Not Found"
    **Error**: `AuthenticationError: API key not provided`
    
    **Solutions**:
    - Check environment variable name: `OPEN_TO_CLOSE_API_KEY`
    - Verify the variable is exported: `echo $OPEN_TO_CLOSE_API_KEY`
    - Restart your terminal/IDE after setting the variable
    - Check if using a virtual environment that needs reactivation

!!! warning "Permission Denied"
    **Error**: `AuthenticationError: Permission denied`
    
    **Solutions**:
    - Verify your API key has the necessary permissions
    - Check if your account has access to the specific endpoints
    - Contact your administrator about API access levels

### **Debug Authentication Issues**

```python
import os
from open_to_close import OpenToCloseAPI

def debug_authentication():
    """Debug authentication configuration."""
    print("🔍 Authentication Debug Information")
    print("-" * 40)
    
    # Check environment variable
    api_key = os.getenv("OPEN_TO_CLOSE_API_KEY")
    if api_key:
        print(f"✅ API key found (length: {len(api_key)})")
        print(f"📝 First 10 chars: {api_key[:10]}...")
        print(f"📝 Last 10 chars: ...{api_key[-10:]}")
    else:
        print("❌ API key environment variable not found")
    
    # Test client initialization
    try:
        client = OpenToCloseAPI()
        print("✅ Client initialization successful")
    except Exception as e:
        print(f"❌ Client initialization failed: {e}")
    
    # Test simple API call
    try:
        result = client.agents.list_agents(params={"limit": 1})
        print("✅ API call successful")
    except Exception as e:
        print(f"❌ API call failed: {e}")

debug_authentication()
```

---

## 🚀 Next Steps

Once authentication is configured:

1. **[Try the quick start guide](quickstart.md)** - Make your first authenticated API calls
2. **[Try the quick start guide](quickstart.md)** - Make your first API calls
3. **[Explore API documentation](../api/index.md)** - Learn about available operations

---

## 📋 Authentication Checklist

- [ ] API key obtained from Open To Close administrator
- [ ] Environment variable `OPEN_TO_CLOSE_API_KEY` set
- [ ] API key not committed to version control
- [ ] Authentication test successful
- [ ] Error handling implemented
- [ ] Ready to make API calls

Once all items are checked, proceed to **[Quick Start Guide](quickstart.md)**. 