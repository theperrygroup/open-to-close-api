# Troubleshooting Guide

Common issues and solutions when using the Open To Close API client.

## Table of Contents

- [Authentication Issues](#authentication-issues)
- [Connection Problems](#connection-problems)
- [Data Validation Errors](#data-validation-errors)
- [Rate Limiting](#rate-limiting)
- [Common API Errors](#common-api-errors)
- [Performance Issues](#performance-issues)
- [Debugging Tips](#debugging-tips)

## Authentication Issues

### API Key Not Working

**Problem:** Getting `AuthenticationError` when making requests.

**Solutions:**

1. **Check API Key Format:**
   ```python
   # Ensure your API key is properly formatted
   client = OpenToCloseAPI(api_key="your_actual_api_key_here")
   ```

2. **Verify Environment Variable:**
   ```bash
   # Check if environment variable is set
   echo $OPEN_TO_CLOSE_API_KEY
   
   # Set it if missing
   export OPEN_TO_CLOSE_API_KEY="your_api_key_here"
   ```

3. **Check .env File:**
   ```env
   # Make sure .env file has correct format
   OPEN_TO_CLOSE_API_KEY=your_actual_api_key_here
   ```

4. **Verify API Key Status:**
   - Contact Open To Close support to verify your API key is active
   - Check if your account has the necessary permissions

### Permission Denied Errors

**Problem:** API key works but getting permission errors on specific endpoints.

**Solutions:**
- Verify your API key has the required scopes/permissions
- Contact support to check your account's access levels
- Some endpoints may require additional authentication

## Connection Problems

### Network Connectivity Issues

**Problem:** Getting `NetworkError` or connection timeouts.

**Solutions:**

1. **Check Internet Connection:**
   ```bash
   # Test basic connectivity
   ping api.opentoclose.com
   ```

2. **Firewall/Proxy Issues:**
   ```python
   # If behind corporate firewall, configure proxy
   import requests
   
   proxies = {
       'http': 'http://proxy.company.com:8080',
       'https': 'https://proxy.company.com:8080'
   }
   
   # You may need to modify the client to use proxies
   ```

3. **DNS Resolution:**
   ```bash
   # Test DNS resolution
   nslookup api.opentoclose.com
   ```

### SSL Certificate Issues

**Problem:** SSL verification errors.

**Solutions:**
```python
# Temporary workaround (not recommended for production)
import ssl
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Better solution: Update certificates
# pip install --upgrade certifi
```

## Data Validation Errors

### Invalid Field Formats

**Problem:** Getting `ValidationError` for seemingly correct data.

**Common Issues and Fixes:**

1. **Phone Number Format:**
   ```python
   # Wrong
   contact_data = {"phone": "555-123-4567"}
   
   # Correct
   contact_data = {"phone": "+15551234567"}
   ```

2. **Email Validation:**
   ```python
   # Ensure valid email format
   import re
   
   def validate_email(email):
       pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
       return re.match(pattern, email) is not None
   ```

3. **Date Formats:**
   ```python
   # Use ISO format for dates
   task_data = {
       "due_date": "2024-12-31",  # YYYY-MM-DD
       "created_at": "2024-01-15T10:30:00Z"  # ISO 8601
   }
   ```

4. **Required Fields:**
   ```python
   # Always include required fields
   contact_data = {
       "first_name": "John",    # Required
       "last_name": "Doe",      # Required
       "email": "john@example.com"  # Required
       # Optional fields can be omitted
   }
   ```

### Data Type Mismatches

**Problem:** Passing wrong data types.

**Solutions:**
```python
# Ensure correct types
property_data = {
    "bedrooms": 3,              # int, not "3"
    "bathrooms": 2.5,           # float for half baths
    "listing_price": 500000,    # int/float, not "$500,000"
    "square_feet": 2200,        # int, not "2,200"
    "active": True              # bool, not "true"
}
```

## Rate Limiting

### Rate Limit Exceeded

**Problem:** Getting `RateLimitError` when making many requests.

**Solutions:**

1. **Implement Retry Logic:**
   ```python
   import time
   from open_to_close_api import RateLimitError
   
   def api_call_with_retry(func, *args, max_retries=3, **kwargs):
       for attempt in range(max_retries):
           try:
               return func(*args, **kwargs)
           except RateLimitError as e:
               if attempt < max_retries - 1:
                   wait_time = 2 ** attempt  # Exponential backoff
                   print(f"Rate limited, waiting {wait_time} seconds...")
                   time.sleep(wait_time)
               else:
                   raise
   ```

2. **Add Delays Between Requests:**
   ```python
   import time
   
   for contact in contacts_to_create:
       client.contacts.create_contact(contact)
       time.sleep(0.1)  # 100ms delay between requests
   ```

3. **Batch Operations:**
   ```python
   # Process in smaller batches
   batch_size = 10
   for i in range(0, len(data), batch_size):
       batch = data[i:i + batch_size]
       process_batch(batch)
       time.sleep(1)  # Pause between batches
   ```

## Common API Errors

### 404 Not Found Errors

**Problem:** `NotFoundError` when trying to access resources.

**Common Causes:**
- Resource ID doesn't exist
- Resource was deleted
- Typo in resource ID

**Solutions:**
```python
def safe_retrieve(resource_type, resource_id):
    try:
        if resource_type == "contact":
            return client.contacts.retrieve_contact(resource_id)
        elif resource_type == "property":
            return client.properties.retrieve_property(resource_id)
    except NotFoundError:
        print(f"{resource_type} {resource_id} not found")
        return None
```

### 422 Validation Errors

**Problem:** Server returns validation errors for request data.

**Solutions:**
1. **Check Required Fields:**
   ```python
   # Get validation details from error
   try:
       client.contacts.create_contact(data)
   except ValidationError as e:
       print(f"Validation error: {e}")
       print(f"Error details: {e.response.json()}")
   ```

2. **Field Length Limits:**
   ```python
   # Ensure fields don't exceed maximum length
   contact_data = {
       "first_name": "John"[:50],  # Truncate if needed
       "notes": description[:1000]  # Limit notes length
   }
   ```

### 500 Server Errors

**Problem:** `ServerError` from API.

**Solutions:**
1. **Retry the Request:**
   ```python
   import time
   
   max_retries = 3
   for attempt in range(max_retries):
       try:
           result = client.contacts.list_contacts()
           break
       except ServerError:
           if attempt < max_retries - 1:
               time.sleep(2 ** attempt)
           else:
               raise
   ```

2. **Check API Status:**
   - Verify API service status
   - Contact support if errors persist

## Performance Issues

### Slow Response Times

**Problem:** API calls taking too long.

**Solutions:**

1. **Use Pagination:**
   ```python
   # Don't fetch all records at once
   params = {"limit": 50, "offset": 0}
   contacts = client.contacts.list_contacts(params=params)
   ```

2. **Filter Results:**
   ```python
   # Only fetch what you need
   params = {
       "created_after": "2024-01-01",
       "status": "active"
   }
   properties = client.properties.list_properties(params=params)
   ```

3. **Parallel Processing:**
   ```python
   import concurrent.futures
   
   def process_contact(contact_id):
       return client.contacts.retrieve_contact(contact_id)
   
   with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
       results = list(executor.map(process_contact, contact_ids))
   ```

### Memory Usage

**Problem:** High memory usage when processing large datasets.

**Solutions:**
```python
def process_large_dataset():
    offset = 0
    batch_size = 100
    
    while True:
        # Process in chunks
        params = {"limit": batch_size, "offset": offset}
        batch = client.contacts.list_contacts(params=params)
        
        if not batch:
            break
            
        # Process batch
        for contact in batch:
            process_contact(contact)
        
        offset += batch_size
        
        # Optional: garbage collection
        import gc
        gc.collect()
```

## Debugging Tips

### Enable Debug Logging

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('open_to_close_api')
logger.setLevel(logging.DEBUG)

# Your API calls will now show detailed information
client = OpenToCloseAPI()
```

### Inspect Request/Response Data

```python
def debug_api_call():
    try:
        response = client.contacts.list_contacts()
        print(f"Success: {len(response)} contacts retrieved")
    except Exception as e:
        print(f"Error: {e}")
        if hasattr(e, 'response'):
            print(f"Status Code: {e.response.status_code}")
            print(f"Response: {e.response.text}")
```

### Test with Minimal Data

```python
# Start with minimal data to isolate issues
minimal_contact = {
    "first_name": "Test",
    "last_name": "User",
    "email": "test@example.com"
}

try:
    contact = client.contacts.create_contact(minimal_contact)
    print("Basic contact creation works")
except Exception as e:
    print(f"Basic contact creation failed: {e}")
```

### Check API Response Format

```python
def inspect_response_format():
    try:
        contacts = client.contacts.list_contacts(params={"limit": 1})
        if contacts:
            print("Sample contact structure:")
            import json
            print(json.dumps(contacts[0], indent=2))
    except Exception as e:
        print(f"Error: {e}")
```

## Getting Help

If you continue to experience issues:

1. **Check this troubleshooting guide** for similar problems
2. **Review the [API documentation](../reference/api-reference.md)** for correct usage
3. **Check the [examples](examples.md)** for working code patterns
4. **Enable debug logging** to get more information
5. **Contact support** with:
   - Your code example
   - Complete error message
   - Debug logs
   - API client version

## Common Error Codes

| Code | Error Type | Description | Solution |
|------|------------|-------------|----------|
| 400 | Bad Request | Invalid request format | Check request syntax |
| 401 | Unauthorized | Invalid API key | Verify API key |
| 403 | Forbidden | Insufficient permissions | Contact support |
| 404 | Not Found | Resource doesn't exist | Check resource ID |
| 422 | Validation Error | Invalid data | Check field formats |
| 429 | Rate Limited | Too many requests | Implement retry logic |
| 500 | Server Error | API server issue | Retry or contact support |

## Version Compatibility

Make sure you're using compatible versions:

```bash
# Check your version
pip show open-to-close-api

# Update to latest version
pip install --upgrade open-to-close-api
```

Refer to the [changelog](../development/changelog.md) for version-specific information and breaking changes. 