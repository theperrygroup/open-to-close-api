# Rate Limits

This guide covers the rate limiting policies, quotas, and best practices for the Open To Close API. Understanding rate limits is crucial for building robust applications that can handle high-volume operations efficiently.

## Overview

The Open To Close API implements rate limiting to ensure fair usage and maintain service quality for all users. Rate limits are applied at multiple levels:

- **Per-API Key**: Limits based on your API key
- **Per-Endpoint**: Different limits for different endpoints
- **Per-IP Address**: Additional limits based on source IP
- **Burst vs Sustained**: Different limits for short bursts vs sustained usage

---

## Rate Limit Tiers

### Standard Tier

Default limits for all API keys:

| Metric | Limit | Window |
|--------|-------|--------|
| Requests per minute | 1,000 | 60 seconds |
| Requests per hour | 10,000 | 3,600 seconds |
| Requests per day | 100,000 | 86,400 seconds |
| Concurrent requests | 10 | N/A |

### Premium Tier

Enhanced limits for premium accounts:

| Metric | Limit | Window |
|--------|-------|--------|
| Requests per minute | 5,000 | 60 seconds |
| Requests per hour | 50,000 | 3,600 seconds |
| Requests per day | 500,000 | 86,400 seconds |
| Concurrent requests | 25 | N/A |

### Enterprise Tier

Custom limits for enterprise customers:

| Metric | Limit | Window |
|--------|-------|--------|
| Requests per minute | Custom | 60 seconds |
| Requests per hour | Custom | 3,600 seconds |
| Requests per day | Custom | 86,400 seconds |
| Concurrent requests | Custom | N/A |

---

## Endpoint-Specific Limits

Different endpoints have different rate limits based on their resource intensity:

### Read Operations (GET)

| Endpoint Category | Requests/Minute | Requests/Hour |
|-------------------|-----------------|---------------|
| List endpoints | 500 | 5,000 |
| Individual resource | 1,000 | 10,000 |
| Search endpoints | 200 | 2,000 |
| Reports/Analytics | 100 | 1,000 |

### Write Operations (POST, PUT, DELETE)

| Endpoint Category | Requests/Minute | Requests/Hour |
|-------------------|-----------------|---------------|
| Create operations | 200 | 2,000 |
| Update operations | 300 | 3,000 |
| Delete operations | 100 | 1,000 |
| Bulk operations | 50 | 500 |

### Special Endpoints

| Endpoint | Requests/Minute | Requests/Hour | Notes |
|----------|-----------------|---------------|-------|
| File uploads | 20 | 200 | Large file operations |
| Email sending | 100 | 1,000 | Email delivery limits |
| Webhook registration | 10 | 100 | Configuration changes |
| Authentication | 60 | 600 | Login/token refresh |

---

## Rate Limit Headers

The API returns rate limit information in response headers:

### Standard Headers

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
X-RateLimit-Window: 60
```

### Header Descriptions

| Header | Description | Example |
|--------|-------------|---------|
| `X-RateLimit-Limit` | Maximum requests allowed in window | `1000` |
| `X-RateLimit-Remaining` | Requests remaining in current window | `999` |
| `X-RateLimit-Reset` | Unix timestamp when window resets | `1640995200` |
| `X-RateLimit-Window` | Window duration in seconds | `60` |
| `X-RateLimit-Retry-After` | Seconds to wait before retrying (when limited) | `30` |

### Multiple Window Headers

For endpoints with multiple rate limit windows:

```http
X-RateLimit-Limit-Minute: 1000
X-RateLimit-Remaining-Minute: 999
X-RateLimit-Reset-Minute: 1640995200

X-RateLimit-Limit-Hour: 10000
X-RateLimit-Remaining-Hour: 9999
X-RateLimit-Reset-Hour: 1640998800

X-RateLimit-Limit-Day: 100000
X-RateLimit-Remaining-Day: 99999
X-RateLimit-Reset-Day: 1641081600
```

---

## Rate Limit Responses

### HTTP 429 - Too Many Requests

When rate limits are exceeded, the API returns a 429 status code:

```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1640995260
X-RateLimit-Retry-After: 60

{
    "error": {
        "code": "RATE_LIMIT_EXCEEDED",
        "message": "Rate limit exceeded",
        "details": {
            "limit": 1000,
            "window": "1 minute",
            "retry_after": 60
        }
    },
    "meta": {
        "timestamp": "2024-01-15T10:30:00Z"
    }
}
```

### Error Response Fields

| Field | Description | Type |
|-------|-------------|------|
| `code` | Error code identifier | string |
| `message` | Human-readable error message | string |
| `details.limit` | Rate limit that was exceeded | integer |
| `details.window` | Time window description | string |
| `details.retry_after` | Seconds to wait before retry | integer |

---

## Handling Rate Limits

### Python Implementation

```python
import time
import requests
from datetime import datetime, timedelta

class RateLimitHandler:
    """Handle rate limits with exponential backoff and retry logic"""
    
    def __init__(self, max_retries=3, base_delay=1):
        self.max_retries = max_retries
        self.base_delay = base_delay
    
    def make_request(self, method, url, **kwargs):
        """Make API request with rate limit handling"""
        for attempt in range(self.max_retries + 1):
            try:
                response = requests.request(method, url, **kwargs)
                
                # Check rate limit headers
                self._log_rate_limit_status(response.headers)
                
                if response.status_code == 429:
                    if attempt < self.max_retries:
                        delay = self._calculate_delay(response.headers, attempt)
                        print(f"Rate limited. Waiting {delay} seconds before retry {attempt + 1}")
                        time.sleep(delay)
                        continue
                    else:
                        raise Exception("Max retries exceeded for rate limit")
                
                response.raise_for_status()
                return response
                
            except requests.exceptions.RequestException as e:
                if attempt < self.max_retries:
                    delay = self.base_delay * (2 ** attempt)  # Exponential backoff
                    print(f"Request failed. Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    raise e
    
    def _calculate_delay(self, headers, attempt):
        """Calculate delay based on rate limit headers"""
        # Use Retry-After header if available
        retry_after = headers.get('X-RateLimit-Retry-After')
        if retry_after:
            return int(retry_after)
        
        # Use reset time if available
        reset_time = headers.get('X-RateLimit-Reset')
        if reset_time:
            reset_timestamp = int(reset_time)
            current_timestamp = int(time.time())
            delay = max(0, reset_timestamp - current_timestamp)
            return delay
        
        # Fallback to exponential backoff
        return self.base_delay * (2 ** attempt)
    
    def _log_rate_limit_status(self, headers):
        """Log current rate limit status"""
        limit = headers.get('X-RateLimit-Limit')
        remaining = headers.get('X-RateLimit-Remaining')
        reset = headers.get('X-RateLimit-Reset')
        
        if limit and remaining:
            print(f"Rate limit: {remaining}/{limit} remaining")
            
            if reset:
                reset_time = datetime.fromtimestamp(int(reset))
                print(f"Resets at: {reset_time}")

# Usage with Open To Close client
from open_to_close import OpenToCloseAPI

class RateLimitedOTCClient:
    """OTC client with built-in rate limit handling"""
    
    def __init__(self, api_key=None):
        self.client = OpenToCloseAPI(api_key=api_key)
        self.rate_handler = RateLimitHandler()
        self._track_usage()
    
    def _track_usage(self):
        """Track API usage for rate limit awareness"""
        self.usage = {
            'minute': {'count': 0, 'reset': time.time() + 60},
            'hour': {'count': 0, 'reset': time.time() + 3600},
            'day': {'count': 0, 'reset': time.time() + 86400}
        }
    
    def _update_usage(self):
        """Update usage counters"""
        current_time = time.time()
        
        for window in self.usage:
            if current_time >= self.usage[window]['reset']:
                # Reset counter
                self.usage[window]['count'] = 0
                if window == 'minute':
                    self.usage[window]['reset'] = current_time + 60
                elif window == 'hour':
                    self.usage[window]['reset'] = current_time + 3600
                elif window == 'day':
                    self.usage[window]['reset'] = current_time + 86400
            
            self.usage[window]['count'] += 1
    
    def _check_preemptive_limit(self, limits):
        """Check if we're approaching rate limits"""
        for window, limit in limits.items():
            if self.usage[window]['count'] >= limit * 0.9:  # 90% threshold
                reset_time = self.usage[window]['reset']
                delay = max(0, reset_time - time.time())
                print(f"Approaching {window} rate limit. Waiting {delay:.1f} seconds")
                time.sleep(delay)
                self._track_usage()  # Reset counters
    
    def list_properties(self, params=None):
        """List properties with rate limit handling"""
        # Check preemptive limits (adjust based on your tier)
        self._check_preemptive_limit({
            'minute': 500,  # Standard tier limit for list endpoints
            'hour': 5000
        })
        
        self._update_usage()
        return self.client.properties.list_properties(params)

# Usage
rate_limited_client = RateLimitedOTCClient()
properties = rate_limited_client.list_properties()
```

### JavaScript Implementation

```javascript
class RateLimitHandler {
    constructor(maxRetries = 3, baseDelay = 1000) {
        this.maxRetries = maxRetries;
        this.baseDelay = baseDelay;
    }

    async makeRequest(url, options = {}) {
        for (let attempt = 0; attempt <= this.maxRetries; attempt++) {
            try {
                const response = await fetch(url, options);
                
                // Log rate limit status
                this.logRateLimitStatus(response.headers);
                
                if (response.status === 429) {
                    if (attempt < this.maxRetries) {
                        const delay = this.calculateDelay(response.headers, attempt);
                        console.log(`Rate limited. Waiting ${delay}ms before retry ${attempt + 1}`);
                        await this.sleep(delay);
                        continue;
                    } else {
                        throw new Error('Max retries exceeded for rate limit');
                    }
                }
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                
                return response;
                
            } catch (error) {
                if (attempt < this.maxRetries && error.name !== 'TypeError') {
                    const delay = this.baseDelay * Math.pow(2, attempt);
                    console.log(`Request failed. Retrying in ${delay}ms...`);
                    await this.sleep(delay);
                } else {
                    throw error;
                }
            }
        }
    }

    calculateDelay(headers, attempt) {
        // Use Retry-After header if available
        const retryAfter = headers.get('X-RateLimit-Retry-After');
        if (retryAfter) {
            return parseInt(retryAfter) * 1000; // Convert to milliseconds
        }
        
        // Use reset time if available
        const resetTime = headers.get('X-RateLimit-Reset');
        if (resetTime) {
            const resetTimestamp = parseInt(resetTime) * 1000;
            const currentTimestamp = Date.now();
            const delay = Math.max(0, resetTimestamp - currentTimestamp);
            return delay;
        }
        
        // Fallback to exponential backoff
        return this.baseDelay * Math.pow(2, attempt);
    }

    logRateLimitStatus(headers) {
        const limit = headers.get('X-RateLimit-Limit');
        const remaining = headers.get('X-RateLimit-Remaining');
        const reset = headers.get('X-RateLimit-Reset');
        
        if (limit && remaining) {
            console.log(`Rate limit: ${remaining}/${limit} remaining`);
            
            if (reset) {
                const resetTime = new Date(parseInt(reset) * 1000);
                console.log(`Resets at: ${resetTime.toISOString()}`);
            }
        }
    }

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Usage
const rateLimitHandler = new RateLimitHandler();

async function makeAPICall(endpoint, options = {}) {
    const url = `https://api.opentoclose.com${endpoint}`;
    const response = await rateLimitHandler.makeRequest(url, {
        headers: {
            'Authorization': `Bearer ${API_KEY}`,
            'Content-Type': 'application/json',
            ...options.headers
        },
        ...options
    });
    
    return response.json();
}
```

---

## Best Practices

### 1. Monitor Rate Limit Headers

Always check rate limit headers in responses:

```python
def monitor_rate_limits(response):
    """Monitor and log rate limit status"""
    headers = response.headers
    
    limit = int(headers.get('X-RateLimit-Limit', 0))
    remaining = int(headers.get('X-RateLimit-Remaining', 0))
    reset = int(headers.get('X-RateLimit-Reset', 0))
    
    # Calculate usage percentage
    usage_percent = ((limit - remaining) / limit) * 100 if limit > 0 else 0
    
    # Log warning if approaching limit
    if usage_percent > 80:
        reset_time = datetime.fromtimestamp(reset)
        print(f"WARNING: {usage_percent:.1f}% of rate limit used. Resets at {reset_time}")
    
    return {
        'limit': limit,
        'remaining': remaining,
        'reset': reset,
        'usage_percent': usage_percent
    }
```

### 2. Implement Exponential Backoff

Use exponential backoff for retries:

```python
import random

def exponential_backoff(attempt, base_delay=1, max_delay=60, jitter=True):
    """Calculate delay with exponential backoff and optional jitter"""
    delay = min(base_delay * (2 ** attempt), max_delay)
    
    if jitter:
        # Add random jitter to prevent thundering herd
        delay = delay * (0.5 + random.random() * 0.5)
    
    return delay
```

### 3. Batch Operations

Combine multiple operations into single requests when possible:

```python
# Instead of multiple individual requests
for property_id in property_ids:
    client.properties.retrieve_property(property_id)

# Use batch operations or list with filtering
properties = client.properties.list_properties(
    params={'ids': ','.join(map(str, property_ids))}
)
```

### 4. Cache Frequently Accessed Data

Implement caching to reduce API calls:

```python
import time
from functools import wraps

def cache_with_ttl(ttl_seconds=300):
    """Cache decorator with TTL"""
    cache = {}
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key
            key = f"{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"
            
            # Check cache
            if key in cache:
                result, timestamp = cache[key]
                if time.time() - timestamp < ttl_seconds:
                    return result
            
            # Call function and cache result
            result = func(*args, **kwargs)
            cache[key] = (result, time.time())
            
            return result
        return wrapper
    return decorator

# Usage
@cache_with_ttl(ttl_seconds=600)  # Cache for 10 minutes
def get_property(property_id):
    return client.properties.retrieve_property(property_id)
```

### 5. Use Webhooks for Real-time Updates

Instead of polling, use webhooks for real-time updates:

```python
# Instead of polling for changes
while True:
    properties = client.properties.list_properties(
        params={'updated_since': last_check}
    )
    # Process changes
    time.sleep(60)  # Check every minute

# Use webhooks to receive updates
@app.route('/webhook/property-update', methods=['POST'])
def handle_property_update():
    data = request.json
    # Process update immediately
    return {'status': 'received'}
```

---

## Rate Limit Monitoring

### Dashboard Metrics

Track these metrics in your monitoring dashboard:

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| Requests per minute | Current request rate | > 80% of limit |
| Rate limit violations | 429 responses received | > 0 |
| Average response time | API response latency | > 2 seconds |
| Error rate | Non-2xx responses | > 5% |
| Queue depth | Pending requests | > 100 |

### Alerting Rules

Set up alerts for rate limit issues:

```python
def check_rate_limit_health():
    """Check rate limit health and send alerts"""
    metrics = get_rate_limit_metrics()
    
    alerts = []
    
    # Check usage percentage
    if metrics['usage_percent'] > 90:
        alerts.append({
            'level': 'critical',
            'message': f"Rate limit usage at {metrics['usage_percent']:.1f}%"
        })
    elif metrics['usage_percent'] > 80:
        alerts.append({
            'level': 'warning',
            'message': f"Rate limit usage at {metrics['usage_percent']:.1f}%"
        })
    
    # Check error rate
    if metrics['error_rate'] > 10:
        alerts.append({
            'level': 'critical',
            'message': f"High error rate: {metrics['error_rate']:.1f}%"
        })
    
    # Send alerts
    for alert in alerts:
        send_alert(alert)
```

---

## Upgrading Rate Limits

### When to Upgrade

Consider upgrading your rate limit tier when:

- Consistently hitting rate limits during normal operations
- Need for higher burst capacity
- Running batch processing jobs
- Supporting multiple concurrent users
- Building real-time applications

### How to Request Upgrades

1. **Contact Support**: Reach out to Open To Close support
2. **Provide Usage Data**: Share your current usage patterns
3. **Explain Use Case**: Describe your application requirements
4. **Business Justification**: Explain the business need for higher limits

### Custom Enterprise Limits

Enterprise customers can request custom rate limits based on:

- **Volume Requirements**: Expected request volume
- **Peak Usage Patterns**: Burst requirements
- **Geographic Distribution**: Multi-region deployments
- **SLA Requirements**: Uptime and performance needs

---

## Related Resources

- [Error Handling Guide](../guides/error-handling.md) - Handle rate limit errors
- [Best Practices](../guides/best-practices.md) - General API best practices
- [Integration Patterns](../guides/integration-patterns.md) - Efficient integration strategies
- [API Reference](../api/index.md) - Complete API documentation