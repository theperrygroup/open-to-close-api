# Troubleshooting Guide

Comprehensive solutions for common issues when using the Open To Close API client with step-by-step debugging techniques.

!!! info "🔧 Quick Problem Solver"
    Having issues? Use our organized troubleshooting sections below to quickly identify and resolve common problems.

## 🎯 Common Issue Categories

<div class="grid cards" markdown>

-   :material-key:{ .lg .middle } **Authentication**

    ---

    API key issues, permission errors, and authentication failures

    [:octicons-arrow-right-24: Auth Solutions](#authentication-issues)

-   :material-wifi-off:{ .lg .middle } **Connection Problems**

    ---

    Network issues, SSL errors, and connectivity troubleshooting

    [:octicons-arrow-right-24: Network Solutions](#connection-problems)

-   :material-alert-circle:{ .lg .middle } **Validation Errors**

    ---

    Data format issues, field validation, and request problems

    [:octicons-arrow-right-24: Data Solutions](#data-validation-errors)

-   :material-speedometer:{ .lg .middle } **Rate Limiting**

    ---

    Request throttling, retry patterns, and performance optimization

    [:octicons-arrow-right-24: Rate Limit Solutions](#rate-limiting)

-   :material-bug:{ .lg .middle } **API Errors**

    ---

    Common HTTP errors, server issues, and error code explanations

    [:octicons-arrow-right-24: Error Solutions](#common-api-errors)

-   :material-chart-line:{ .lg .middle } **Performance**

    ---

    Slow responses, memory usage, and optimization techniques

    [:octicons-arrow-right-24: Performance Solutions](#performance-issues)

</div>

## 🔐 Authentication Issues

Resolve API key problems and authentication failures with these proven solutions.

!!! danger "🚨 Common Authentication Problems"

=== "API Key Not Working"
    **Problem:** Getting `AuthenticationError` when making requests.

    !!! example "🔑 Authentication Solutions"

    === "Check API Key Format"
        ```python
        from open_to_close import OpenToCloseAPI
        
        # ✅ Correct format
        client = OpenToCloseAPI(api_key="your_actual_api_key_here")
        
        # ❌ Common mistakes
        # - Extra spaces: " your_api_key "
        # - Missing quotes: your_api_key
        # - Wrong variable: api_key="some_other_value"
        ```

    === "Environment Variable Check"
        ```bash
        # Check if environment variable exists
        echo $OPEN_TO_CLOSE_API_KEY
        
        # If empty, set it
        export OPEN_TO_CLOSE_API_KEY="your_api_key_here"
        
        # For Windows PowerShell:
        $env:OPEN_TO_CLOSE_API_KEY="your_api_key_here"
        
        # For Windows Command Prompt:
        set OPEN_TO_CLOSE_API_KEY=your_api_key_here
        ```

    === ".env File Verification"
        ```env
        # ✅ Correct .env format
        OPEN_TO_CLOSE_API_KEY=your_actual_api_key_here
        
        # ❌ Common mistakes:
        # OPEN_TO_CLOSE_API_KEY="your_api_key"  # No quotes in .env
        # OPEN_TO_CLOSE_API_KEY = your_api_key  # No spaces around =
        # OPEN_TO_CLOSE_API_KEY:your_api_key    # Wrong separator
        ```

    === "Test Authentication"
        ```python
        from open_to_close import OpenToCloseAPI, AuthenticationError
        
        def test_authentication():
            """Test if API key is working."""
            try:
                client = OpenToCloseAPI()
                # Simple test call
                result = client.contacts.list_contacts(params={"limit": 1})
                print("✅ Authentication successful!")
                return True
            except AuthenticationError as e:
                print(f"❌ Authentication failed: {e}")
                print("🔍 Check your API key and try again")
                return False
            except Exception as e:
                print(f"⚠️ Other error: {e}")
                return False
        
        # Run the test
        test_authentication()
        ```

=== "Permission Denied"
    **Problem:** API key works but getting permission errors on specific endpoints.

    !!! warning "🔒 Permission Issues"
        Your API key may have limited scopes or your account may need additional permissions.

    **Solutions:**
    
    1. **Check Account Permissions**
       - Contact Open To Close support to verify endpoint access
       - Some endpoints require special permissions
       - Ensure your account is fully activated

    2. **Verify API Key Scopes**
       ```python
       # Test different endpoints to identify scope limits
       def test_permissions():
           client = OpenToCloseAPI()
           
           endpoints_to_test = [
               ("contacts", lambda: client.contacts.list_contacts(params={"limit": 1})),
               ("properties", lambda: client.properties.list_properties(params={"limit": 1})),
               ("agents", lambda: client.agents.list_agents(params={"limit": 1}))
           ]
           
           for name, func in endpoints_to_test:
               try:
                   func()
                   print(f"✅ {name}: Access granted")
               except Exception as e:
                   print(f"❌ {name}: {e}")
       ```

---

## 🌐 Connection Problems

Resolve network connectivity and SSL issues with these diagnostic steps.

!!! warning "⚠️ Network Troubleshooting"

=== "Basic Connectivity"
    **Problem:** Getting `NetworkError` or connection timeouts.

    !!! example "🔗 Connection Diagnostics"

    === "Test Network Access"
        ```bash
        # Test basic connectivity
        ping api.opentoclose.com
        
        # Test HTTPS access
        curl -I https://api.opentoclose.com
        
        # Check DNS resolution
        nslookup api.opentoclose.com
        ```

    === "Firewall/Proxy Config"
        ```python
        import requests
        from open_to_close import OpenToCloseAPI
        
        # If behind corporate firewall
        proxies = {
            'http': 'http://proxy.company.com:8080',
            'https': 'https://proxy.company.com:8080'
        }
        
        # Note: You may need to configure the client for proxy use
        # Contact support for proxy configuration guidance
        ```

    === "Timeout Configuration"
        ```python
        from open_to_close import OpenToCloseAPI
        
        # Increase timeout for slow connections
        client = OpenToCloseAPI(timeout=60)  # 60 second timeout
        
        # Test with extended timeout
        try:
            contacts = client.contacts.list_contacts()
            print("✅ Connection successful with extended timeout")
        except Exception as e:
            print(f"❌ Still failing: {e}")
        ```

=== "SSL Certificate Issues"
    **Problem:** SSL verification errors or certificate problems.

    !!! danger "🔒 SSL Problems"
        SSL issues often indicate certificate or security configuration problems.

    **Solutions:**

    === "Update Certificates"
        ```bash
        # Update certificate bundle
        pip install --upgrade certifi
        
        # Update requests library
        pip install --upgrade requests
        
        # Restart your application
        ```

    === "Certificate Verification"
        ```python
        import ssl
        import requests
        
        def test_ssl():
            """Test SSL connection to API."""
            try:
                response = requests.get('https://api.opentoclose.com', timeout=10)
                print(f"✅ SSL connection successful: {response.status_code}")
            except requests.exceptions.SSLError as e:
                print(f"❌ SSL Error: {e}")
                print("💡 Try updating certificates or contact your IT department")
            except Exception as e:
                print(f"⚠️ Other error: {e}")
        
        test_ssl()
        ```

    === "Temporary Workaround"
        ```python
        # ⚠️ ONLY for testing - NOT for production!
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # Better solution: Fix the underlying certificate issue
        print("🚨 SSL verification disabled - FIX CERTIFICATES FOR PRODUCTION!")
        ```

---

## 📝 Data Validation Errors

Fix common data format and validation issues with these field-specific solutions.

!!! example "✅ Data Format Solutions"

=== "Field Format Issues"
    **Problem:** Getting `ValidationError` for seemingly correct data.

    === "Phone Numbers"
        ```python
        # ❌ Wrong formats
        wrong_formats = [
            "555-123-4567",     # Dashes
            "(555) 123-4567",   # Parentheses  
            "555.123.4567",     # Dots
            "5551234567"        # No country code
        ]
        
        # ✅ Correct format
        contact_data = {
            "phone": "+15551234567"  # E.164 format with country code
        }
        
        def format_phone(phone_str):
            """Convert phone to correct format."""
            # Remove all non-digits
            digits = ''.join(filter(str.isdigit, phone_str))
            
            # Add country code if missing
            if len(digits) == 10:
                return f"+1{digits}"
            elif len(digits) == 11 and digits.startswith('1'):
                return f"+{digits}"
            else:
                raise ValueError(f"Invalid phone number: {phone_str}")
        
        # Example usage
        formatted = format_phone("(555) 123-4567")
        print(formatted)  # +15551234567
        ```

    === "Email Validation"
        ```python
        import re
        
        def validate_email(email):
            """Validate email format."""
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return re.match(pattern, email) is not None
        
        def clean_email(email):
            """Clean and validate email."""
            email = email.strip().lower()
            
            if validate_email(email):
                return email
            else:
                raise ValueError(f"Invalid email format: {email}")
        
        # ✅ Valid emails
        valid_emails = [
            "user@example.com",
            "first.last@company.co.uk",
            "user+tag@domain.org"
        ]
        
        # ❌ Invalid emails  
        invalid_emails = [
            "invalid-email",      # No @
            "@domain.com",        # No username
            "user@",              # No domain
            "user@domain"         # No TLD
        ]
        ```

    === "Date Formats"
        ```python
        from datetime import datetime
        
        def format_date(date_input):
            """Convert various date formats to ISO format."""
            if isinstance(date_input, str):
                # Try common formats
                formats = [
                    "%Y-%m-%d",           # 2024-01-15
                    "%m/%d/%Y",           # 01/15/2024
                    "%d/%m/%Y",           # 15/01/2024
                    "%Y-%m-%d %H:%M:%S",  # 2024-01-15 10:30:00
                ]
                
                for fmt in formats:
                    try:
                        dt = datetime.strptime(date_input, fmt)
                        return dt.strftime("%Y-%m-%d")
                    except ValueError:
                        continue
                
                raise ValueError(f"Unrecognized date format: {date_input}")
            
            return date_input
        
        # ✅ Correct date usage
        task_data = {
            "due_date": "2024-12-31",              # YYYY-MM-DD
            "created_at": "2024-01-15T10:30:00Z"   # ISO 8601
        }
        ```

=== "Data Type Mismatches"
    **Problem:** Passing wrong data types to API fields.

    ```python
    def clean_property_data(raw_data):
        """Clean and convert property data to correct types."""
        
        cleaned_data = {}
        
        # Numeric fields
        numeric_fields = ['bedrooms', 'bathrooms', 'listing_price', 'square_feet']
        for field in numeric_fields:
            if field in raw_data:
                value = raw_data[field]
                if isinstance(value, str):
                    # Remove commas and currency symbols
                    value = value.replace(',', '').replace('$', '').strip()
                    # Convert to appropriate type
                    if field == 'bathrooms':
                        cleaned_data[field] = float(value)  # Half baths allowed
                    else:
                        cleaned_data[field] = int(value)
                else:
                    cleaned_data[field] = value
        
        # Boolean fields
        boolean_fields = ['active', 'featured']
        for field in boolean_fields:
            if field in raw_data:
                value = raw_data[field]
                if isinstance(value, str):
                    cleaned_data[field] = value.lower() in ['true', '1', 'yes', 'on']
                else:
                    cleaned_data[field] = bool(value)
        
        # String fields (copy as-is)
        string_fields = ['address', 'city', 'state', 'zip_code', 'description']
        for field in string_fields:
            if field in raw_data:
                cleaned_data[field] = str(raw_data[field]).strip()
        
        return cleaned_data
    
    # Example usage
    raw_property = {
        "bedrooms": "3",           # String number
        "bathrooms": "2.5",        # String float
        "listing_price": "$500,000", # Formatted currency
        "active": "true"           # String boolean
    }
    
    clean_property = clean_property_data(raw_property)
    print(clean_property)
    # {'bedrooms': 3, 'bathrooms': 2.5, 'listing_price': 500000, 'active': True}
    ```

---

## ⏱️ Rate Limiting

Handle API rate limits effectively with retry patterns and optimization techniques.

!!! warning "🚦 Rate Limit Management"

=== "Retry Patterns"
    **Problem:** Getting `RateLimitError` when making multiple requests.

    !!! example "🔄 Retry Strategies"

    === "Exponential Backoff"
        ```python
        import time
        import random
        from open_to_close import RateLimitError, NetworkError
        
        def api_call_with_retry(func, *args, max_retries=3, **kwargs):
            """Execute API call with exponential backoff retry."""
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                    
                except RateLimitError as e:
                    if attempt < max_retries - 1:
                        # Exponential backoff with jitter
                        wait_time = (2 ** attempt) + random.uniform(0, 1)
                        print(f"⏱️ Rate limited, waiting {wait_time:.1f} seconds...")
                        time.sleep(wait_time)
                        continue
                    print("❌ Max retries exceeded for rate limiting")
                    raise
                    
                except NetworkError as e:
                    if attempt < max_retries - 1:
                        wait_time = 1 + random.uniform(0, 1)
                        print(f"🌐 Network error, retrying in {wait_time:.1f} seconds...")
                        time.sleep(wait_time)
                        continue
                    raise
        
        # Usage example
        def safe_create_contact(contact_data):
            return api_call_with_retry(client.contacts.create_contact, contact_data)
        ```

    === "Batch Processing"
        ```python
        import time
        
        def process_in_batches(items, process_func, batch_size=10, delay=1.0):
            """Process items in batches to avoid rate limits."""
            
            results = []
            failed_items = []
            
            for i in range(0, len(items), batch_size):
                batch = items[i:i + batch_size]
                batch_results = []
                
                print(f"📦 Processing batch {i//batch_size + 1} ({len(batch)} items)")
                
                for item in batch:
                    try:
                        result = process_func(item)
                        batch_results.append(result)
                        print(f"  ✅ Processed item {len(results) + len(batch_results)}")
                    except Exception as e:
                        print(f"  ❌ Failed item: {e}")
                        failed_items.append({"item": item, "error": str(e)})
                
                results.extend(batch_results)
                
                # Delay between batches
                if i + batch_size < len(items):
                    print(f"⏸️ Waiting {delay} seconds before next batch...")
                    time.sleep(delay)
            
            print(f"\n📊 Batch processing complete:")
            print(f"  ✅ Successful: {len(results)}")
            print(f"  ❌ Failed: {len(failed_items)}")
            
            return results, failed_items
        
        # Example usage
        contacts_to_create = [
            {"first_name": "John", "last_name": "Doe", "email": "john@example.com"},
            {"first_name": "Jane", "last_name": "Smith", "email": "jane@example.com"},
            # ... more contacts
        ]
        
        def create_contact_safe(contact_data):
            return client.contacts.create_contact(contact_data)
        
        results, failures = process_in_batches(
            contacts_to_create, 
            create_contact_safe, 
            batch_size=5, 
            delay=2.0
        )
        ```

=== "Request Optimization"
    **Problem:** Making too many requests that could be optimized.

    === "Smart Filtering"
        ```python
        def optimized_property_search(criteria):
            """Use filtering to reduce API calls."""
            
            # ✅ Good: Filter on server side
            params = {
                "city": criteria.get("city"),
                "min_price": criteria.get("min_price"),
                "max_price": criteria.get("max_price"),
                "bedrooms__gte": criteria.get("min_bedrooms"),
                "status": "active",
                "limit": 100  # Get more results per call
            }
            
            # Remove None values
            params = {k: v for k, v in params.items() if v is not None}
            
            try:
                properties = client.properties.list_properties(params=params)
                print(f"🔍 Found {len(properties)} properties with server-side filtering")
                return properties
            except Exception as e:
                print(f"❌ Search failed: {e}")
                return []
        
        # ❌ Bad: Multiple API calls for filtering
        def inefficient_search():
            all_properties = client.properties.list_properties()  # Gets everything
            filtered = [p for p in all_properties if p['city'] == 'San Francisco']  # Filters client-side
            return filtered
        ```

    === "Pagination Strategy"
        ```python
        def efficient_pagination(resource_type, max_items=None):
            """Efficiently paginate through large datasets."""
            
            all_items = []
            limit = 100  # Maximum per request
            offset = 0
            
            while True:
                params = {"limit": limit, "offset": offset}
                
                try:
                    if resource_type == "contacts":
                        batch = client.contacts.list_contacts(params=params)
                    elif resource_type == "properties":
                        batch = client.properties.list_properties(params=params)
                    else:
                        raise ValueError(f"Unknown resource type: {resource_type}")
                    
                    if not batch:
                        break
                    
                    all_items.extend(batch)
                    print(f"📄 Loaded {len(batch)} items (Total: {len(all_items)})")
                    
                    # Check if we've hit our limit
                    if max_items and len(all_items) >= max_items:
                        all_items = all_items[:max_items]
                        break
                    
                    # Check if we got fewer than requested (last page)
                    if len(batch) < limit:
                        break
                    
                    offset += limit
                    
                    # Small delay to be nice to the API
                    time.sleep(0.1)
                    
                except Exception as e:
                    print(f"❌ Error during pagination: {e}")
                    break
            
            print(f"✅ Pagination complete: {len(all_items)} total items")
            return all_items
        ```

---

## 📋 What's Next?

Found a solution? Continue building with these resources:

<div class="grid cards" markdown>

-   :material-rocket:{ .lg .middle } **Quick Start**

    ---

    Get back to building with our 5-minute tutorial

    [:octicons-arrow-right-24: Quick Start Guide](../getting-started/quickstart.md)

-   :material-code-tags:{ .lg .middle } **Examples**

    ---

    Working code examples for common scenarios

    [:octicons-arrow-right-24: View Examples](examples.md)

-   :material-api:{ .lg .middle } **API Reference**

    ---

    Complete technical documentation for all methods

    [:octicons-arrow-right-24: API Documentation](../reference/api-reference.md)

-   :material-help-circle:{ .lg .middle } **Get Support**

    ---

    Still need help? Contact our support team

    [:octicons-arrow-right-24: Contact Support](../development/contributing.md)

</div>

!!! success "🎯 Troubleshooting Complete!"
    You now have comprehensive solutions for:
    
    - ✅ Authentication and permission issues
    - ✅ Network connectivity problems
    - ✅ Data validation and format errors
    - ✅ Rate limiting and optimization
    - ✅ Performance and memory issues
    
    **Still having problems?** Enable debug logging and contact support with detailed error information.

## 📊 Quick Reference Tables

### Common HTTP Error Codes

| Code | Error Type | Description | Solution |
|------|------------|-------------|----------|
| 400 | Bad Request | Invalid request format | Check request syntax and data |
| 401 | Unauthorized | Invalid API key | Verify API key configuration |
| 403 | Forbidden | Insufficient permissions | Contact support for access |
| 404 | Not Found | Resource doesn't exist | Check resource ID |
| 422 | Validation Error | Invalid data format | Fix field formats and types |
| 429 | Rate Limited | Too many requests | Implement retry with backoff |
| 500 | Server Error | API server issue | Retry or contact support |

### Debug Checklist

!!! note "🔍 Pre-Support Checklist"
    Before contacting support, verify:
    
    - [ ] API key is correct and active
    - [ ] Network connectivity is working  
    - [ ] Data formats match API requirements
    - [ ] Using latest client version
    - [ ] Debug logging is enabled
    - [ ] Error messages are complete
    
    **Still stuck?** Include all the above information when contacting support. 