# Configuration

Advanced configuration options for the Open To Close API Python client. Learn how to customize client behavior, set up multiple environments, and optimize performance.

---

## 🔧 Client Configuration

### **Basic Configuration**

```python
from open_to_close import OpenToCloseAPI

# Basic configuration with environment variables
client = OpenToCloseAPI()

# Explicit configuration
client = OpenToCloseAPI(
    api_key="your_api_key_here",
    base_url="https://api.opentoclose.com/v1"
)
```

### **Advanced Configuration**

```python
# Custom configuration with all options
client = OpenToCloseAPI(
    api_key="your_api_key",
    base_url="https://api.opentoclose.com/v1",
    timeout=30,
    max_retries=3,
    retry_delay=1.0
)
```

---

## 🌍 Environment Management

### **Multiple Environments**

```python
import os

# Development environment
if os.getenv("ENVIRONMENT") == "development":
    client = OpenToCloseAPI(
        api_key=os.getenv("DEV_API_KEY"),
        base_url="https://dev-api.opentoclose.com/v1"
    )
# Production environment  
else:
    client = OpenToCloseAPI()
```

### **Configuration Class**

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class APIConfig:
    api_key: str
    base_url: str = "https://api.opentoclose.com/v1"
    timeout: int = 30
    
    @classmethod
    def from_environment(cls, env: str = "production"):
        """Load configuration from environment."""
        configs = {
            "development": {
                "api_key": os.getenv("DEV_API_KEY"),
                "base_url": "https://dev-api.opentoclose.com/v1"
            },
            "production": {
                "api_key": os.getenv("OPEN_TO_CLOSE_API_KEY"),
                "base_url": "https://api.opentoclose.com/v1"
            }
        }
        
        config = configs.get(env, configs["production"])
        return cls(**config)

# Usage
config = APIConfig.from_environment("development")
client = OpenToCloseAPI(api_key=config.api_key, base_url=config.base_url)
```

---

## ⚡ Performance Optimization

### **Connection Pooling**

```python
# Use session reuse for better performance
import requests

session = requests.Session()
session.mount('https://', requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=20))

# Note: Connection pooling is handled automatically by the client
client = OpenToCloseAPI()
```

### **Batch Operations**

```python
# Efficient batch processing
def process_properties_efficiently(client, property_ids):
    """Process multiple properties with rate limiting."""
    results = []
    
    for i, prop_id in enumerate(property_ids):
        if i > 0 and i % 10 == 0:
            time.sleep(1)  # Rate limiting
            
        try:
            prop = client.properties.retrieve_property(prop_id)
            results.append(prop)
        except Exception as e:
            print(f"Error processing property {prop_id}: {e}")
            
    return results
```

---

## 🔒 Security Configuration

### **API Key Security**

```python
# Secure API key handling
class SecureConfig:
    def __init__(self):
        self._api_key = None
        
    @property
    def api_key(self):
        if not self._api_key:
            self._api_key = self._load_api_key()
        return self._api_key
    
    def _load_api_key(self):
        # Load from secure storage or environment
        api_key = os.getenv("OPEN_TO_CLOSE_API_KEY")
        if not api_key:
            raise ValueError("API key not found")
        return api_key

config = SecureConfig()
client = OpenToCloseAPI(api_key=config.api_key)
```

---

## 📊 Logging Configuration

### **Enable Logging**

```python
import logging

# Configure logging for API client
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Enable debug logging for development
logging.getLogger('open_to_close').setLevel(logging.DEBUG)
```

---

## 🚀 Next Steps

- **[Try the API](../api/index.md)** - Start making API calls
- **[Error Handling](../guides/error-handling.md)** - Handle errors properly
- **[Best Practices](../guides/best-practices.md)** - Follow recommended patterns 