# Guides & Examples

Practical guides, best practices, and real-world examples for building applications with the Open To Close API Python client. Learn patterns and techniques for common use cases.

---

## 🚀 Quick Navigation

<div class="grid cards" markdown>

-   :material-api:{ .lg .middle } **API Reference**

    ---

    Complete documentation of all available API methods and endpoints

    [:octicons-arrow-right-24: API Documentation](../api/index.md)

-   :material-home:{ .lg .middle } **Properties API**

    ---

    Detailed property management operations and examples

    [:octicons-arrow-right-24: Properties Guide](../api/properties.md)

-   :material-rocket-launch:{ .lg .middle } **Quick Start**

    ---

    Get started quickly with guided tutorials and examples

    [:octicons-arrow-right-24: Quick Start Guide](../getting-started/quickstart.md)

-   :material-account-tie:{ .lg .middle } **Getting Started**

    ---

    Complete setup guide from installation to first API calls

    [:octicons-arrow-right-24: Setup Guide](../getting-started/index.md)

</div>

---

## 📋 What You'll Learn

### **Error Handling Mastery**
Learn to build resilient applications that gracefully handle API errors, network issues, and unexpected conditions:

- Exception types and when they occur
- Retry strategies and circuit breakers
- Logging and monitoring best practices
- Graceful degradation patterns

### **Production-Ready Code**
Discover patterns and practices for building maintainable, scalable applications:

- Authentication and security best practices
- Performance optimization techniques
- Testing strategies and mocking
- Configuration management

### **Real-World Applications**
Explore complete examples that demonstrate practical usage:

- Property management dashboards
- Automated workflow systems
- Data synchronization pipelines
- Integration with CRM systems

### **Integration Strategies**
Learn how to integrate the Open To Close API with existing systems:

- Webhook handling and event processing
- Batch operations and bulk updates
- Database synchronization patterns
- External service integration

---

## 🎯 Choose Your Path

=== ":material-account-tie: Real Estate Professional"

    **Building internal tools and workflows:**
    
    1. **[Quick Start Tutorial](../getting-started/quickstart.md)** - Get familiar with the API
    2. **[Properties API](../api/properties.md)** - Core property workflows
    3. **[Authentication Setup](../getting-started/authentication.md)** - Secure API access
    4. **[API Reference](../api/index.md)** - Explore all available operations

=== ":material-code-braces: Developer"

    **Building applications and integrations:**
    
    1. **[API Reference](../api/index.md)** - Understand all available methods
    2. **[Properties API](../api/properties.md)** - Property management operations
    3. **[Installation Guide](../getting-started/installation.md)** - Setup and configuration
    4. **[Authentication](../getting-started/authentication.md)** - Security implementation

=== ":material-chart-line: Data Analyst"

    **Working with property and transaction data:**
    
    1. **[Properties API](../api/properties.md)** - Extract and analyze property data
    2. **[Quick Start](../getting-started/quickstart.md)** - Get started with data extraction
    3. **[API Reference](../api/index.md)** - Explore data endpoints

---

## 🔧 Common Use Cases

### **Property Management Workflows**
```python
# Complete property onboarding workflow
def onboard_new_listing(property_data, seller_info):
    """End-to-end property listing creation."""
    client = OpenToCloseAPI()
    
    # Create property
    property = client.properties.create_property(property_data)
    
    # Add seller contact
    seller = client.contacts.create_contact(seller_info)
    client.property_contacts.create_property_contact(
        property['id'], 
        {"contact_id": seller['id'], "role": "Seller"}
    )
    
    # Create initial tasks
    tasks = create_listing_tasks(property['id'])
    
    return property, seller, tasks
```

### **Data Synchronization**
```python
# Sync properties with external CRM
def sync_properties_to_crm():
    """Synchronize property data with external CRM system."""
    client = OpenToCloseAPI()
    
    # Get updated properties
    properties = client.properties.list_properties(params={
        "modified_since": get_last_sync_time(),
        "status": "Active"
    })
    
    # Process each property
    for prop in properties:
        sync_property_to_crm(prop)
        update_sync_timestamp(prop['id'])
```

### **Automated Reporting**
```python
# Generate daily activity report
def daily_activity_report():
    """Generate comprehensive daily activity report."""
    client = OpenToCloseAPI()
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Gather activity data
    new_properties = get_properties_created_today(client, today)
    updated_properties = get_properties_updated_today(client, today)
    completed_tasks = get_tasks_completed_today(client, today)
    
    # Generate report
    return generate_report(new_properties, updated_properties, completed_tasks)
```

---

## 🛡️ Security & Performance

### **Security Best Practices**
- **API Key Management**: Never hardcode credentials
- **Input Validation**: Sanitize all user inputs
- **Error Logging**: Avoid logging sensitive information
- **Rate Limiting**: Respect API limits and implement backoff

### **Performance Optimization**
- **Efficient Queries**: Use filtering and pagination
- **Batch Operations**: Group related API calls
- **Caching Strategies**: Cache frequently accessed data
- **Async Processing**: Handle long-running operations properly

---

## 🧪 Testing & Development

### **Testing Strategies**
```python
# Example test setup with mocking
import responses
from open_to_close import OpenToCloseAPI

@responses.activate
def test_property_creation():
    # Mock API response
    responses.add(
        responses.POST,
        "https://api.opentoclose.com/v1/properties",
        json={"id": 123, "address": "123 Test St"},
        status=201
    )
    
    client = OpenToCloseAPI(api_key="test_key")
    property = client.properties.create_property({
        "address": "123 Test St"
    })
    
    assert property["id"] == 123
```

### **Development Environment Setup**
```python
# Configuration for different environments
class Config:
    def __init__(self, environment="production"):
        self.environment = environment
        self.api_key = self._get_api_key()
        self.base_url = self._get_base_url()
    
    def _get_api_key(self):
        env_var = f"{self.environment.upper()}_OPEN_TO_CLOSE_API_KEY"
        return os.getenv(env_var)
    
    def _get_base_url(self):
        urls = {
            "development": "https://dev-api.opentoclose.com/v1",
            "staging": "https://staging-api.opentoclose.com/v1",
            "production": "https://api.opentoclose.com/v1"
        }
        return urls[self.environment]
```

---

## 📊 Monitoring & Observability

### **API Usage Monitoring**
```python
import logging
from datetime import datetime

class APIMonitor:
    """Monitor API usage and performance."""
    
    def __init__(self, client):
        self.client = client
        self.logger = logging.getLogger(__name__)
    
    def track_request(self, method, endpoint, duration, status_code):
        """Track API request metrics."""
        self.logger.info(f"{method} {endpoint} - {status_code} ({duration}ms)")
        
        # Send to monitoring system
        send_metric("api.request", {
            "method": method,
            "endpoint": endpoint,
            "duration": duration,
            "status": status_code,
            "timestamp": datetime.now()
        })
```

### **Health Checks**
```python
def health_check():
    """Verify API connectivity and authentication."""
    try:
        client = OpenToCloseAPI()
        # Simple test call
        client.agents.list_agents(params={"limit": 1})
        return {"status": "healthy", "timestamp": datetime.now()}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e), "timestamp": datetime.now()}
```

---

## 📚 Related Documentation

!!! tip "Additional Resources"

    - **[API Reference](../api/index.md)** - Complete method documentation
    - **[Getting Started](../getting-started/index.md)** - Installation and setup
    - **[Properties API](../api/properties.md)** - Property management operations

---

## 🚀 Quick Start

Ready to dive in? Here's your learning path:

1. **[Getting Started](../getting-started/index.md)** - Setup and configuration
2. **[Quick Start Tutorial](../getting-started/quickstart.md)** - Make your first API calls
3. **[Properties API](../api/properties.md)** - Learn property management
4. **[API Reference](../api/index.md)** - Explore all available operations

---

*Build better applications with proven patterns and best practices from the Open To Close API community.* 