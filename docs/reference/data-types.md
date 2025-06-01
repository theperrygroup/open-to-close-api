# Data Types

This reference guide documents the data types, field formats, and validation rules used throughout the Open To Close API. Understanding these data types is essential for proper API integration and data handling.

## Overview

The Open To Close API uses consistent data types across all endpoints. This guide covers:

- **Primitive Types**: Basic data types (strings, numbers, booleans)
- **Date and Time Formats**: Timestamp and date handling
- **Enumerated Values**: Predefined value sets for specific fields
- **Complex Objects**: Structured data types for resources
- **Validation Rules**: Field constraints and requirements

---

## Primitive Data Types

### String Types

| Type | Description | Example | Max Length |
|------|-------------|---------|------------|
| `string` | Standard text field | `"123 Main Street"` | 255 chars |
| `text` | Long text field | `"Detailed property description..."` | 65,535 chars |
| `email` | Email address | `"user@example.com"` | 255 chars |
| `phone` | Phone number | `"(555) 123-4567"` | 20 chars |
| `url` | Web URL | `"https://example.com/photo.jpg"` | 2048 chars |
| `uuid` | Unique identifier | `"550e8400-e29b-41d4-a716-446655440000"` | 36 chars |

**String Validation Rules:**
- All strings are UTF-8 encoded
- Leading and trailing whitespace is automatically trimmed
- Empty strings are treated as `null` unless explicitly allowed
- HTML tags are escaped for security

### Numeric Types

| Type | Description | Range | Example |
|------|-------------|-------|---------|
| `integer` | Whole numbers | -2,147,483,648 to 2,147,483,647 | `123` |
| `bigint` | Large integers | -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807 | `1234567890` |
| `decimal` | Decimal numbers | Up to 10 digits, 2 decimal places | `850000.00` |
| `float` | Floating point | IEEE 754 double precision | `1234.5678` |
| `percentage` | Percentage value | 0.00 to 100.00 | `5.25` |

**Numeric Validation Rules:**
- Negative values are allowed unless specified otherwise
- Currency values use decimal type with 2 decimal places
- Percentages are stored as decimal values (5.25% = 5.25)

### Boolean Type

| Type | Description | Values | Example |
|------|-------------|--------|---------|
| `boolean` | True/false value | `true`, `false` | `true` |

**Boolean Validation Rules:**
- Accepts `true`/`false`, `1`/`0`, `"true"`/`"false"` (case-insensitive)
- `null` values are treated as `false` unless explicitly nullable

---

## Date and Time Types

### Date Formats

All dates and times in the API use ISO 8601 format:

| Type | Format | Example | Description |
|------|--------|---------|-------------|
| `date` | `YYYY-MM-DD` | `"2024-01-15"` | Date only |
| `datetime` | `YYYY-MM-DDTHH:MM:SSZ` | `"2024-01-15T10:30:00Z"` | UTC datetime |
| `datetime_local` | `YYYY-MM-DDTHH:MM:SS±HH:MM` | `"2024-01-15T10:30:00-08:00"` | Local datetime with timezone |
| `timestamp` | Unix timestamp | `1705312200` | Seconds since epoch |

**Date/Time Validation Rules:**
- All datetime values are stored in UTC
- Local times are converted to UTC using provided timezone
- Date-only fields ignore time components
- Future dates are allowed unless specified otherwise
- Invalid dates (e.g., February 30) are rejected

### Common Date Fields

```python
# Example date/time fields in API responses
{
    "created_at": "2024-01-15T10:30:00Z",      # When record was created
    "updated_at": "2024-01-15T14:20:00Z",      # When record was last modified
    "listing_date": "2024-01-15",              # Date property was listed
    "closing_date": "2024-02-15",              # Expected/actual closing date
    "due_date": "2024-01-20",                  # Task due date
    "expires_at": "2024-12-31T23:59:59Z"       # When something expires
}
```

---

## Enumerated Values

### Property Status

| Value | Description | Workflow Stage |
|-------|-------------|----------------|
| `draft` | Property being prepared | Initial |
| `active` | Available for sale/rent | Marketing |
| `pending` | Offer accepted, pending conditions | Under Contract |
| `under_contract` | Contract signed, pending closing | Under Contract |
| `sold` | Sale completed | Closed |
| `rented` | Property rented | Closed |
| `withdrawn` | Removed from market | Inactive |
| `expired` | Listing expired | Inactive |
| `cancelled` | Listing cancelled | Inactive |

### Property Types

| Value | Description | Category |
|-------|-------------|----------|
| `single_family` | Single-family home | Residential |
| `condo` | Condominium | Residential |
| `townhouse` | Townhouse | Residential |
| `multi_family` | Multi-family home | Residential |
| `apartment` | Apartment unit | Residential |
| `mobile_home` | Mobile/manufactured home | Residential |
| `land` | Vacant land | Land |
| `commercial` | Commercial property | Commercial |
| `industrial` | Industrial property | Commercial |
| `retail` | Retail space | Commercial |
| `office` | Office space | Commercial |
| `warehouse` | Warehouse | Commercial |

### Contact Types

| Value | Description | Role |
|-------|-------------|------|
| `buyer` | Property buyer | Client |
| `seller` | Property seller | Client |
| `tenant` | Property renter | Client |
| `landlord` | Property owner/lessor | Client |
| `agent` | Real estate agent | Professional |
| `broker` | Real estate broker | Professional |
| `attorney` | Legal counsel | Professional |
| `inspector` | Property inspector | Professional |
| `appraiser` | Property appraiser | Professional |
| `lender` | Mortgage lender | Professional |
| `title_company` | Title company | Professional |
| `vendor` | Service provider | Professional |

### Task Status

| Value | Description | State |
|-------|-------------|-------|
| `pending` | Not started | Open |
| `in_progress` | Currently being worked on | Open |
| `completed` | Successfully finished | Closed |
| `cancelled` | Cancelled/no longer needed | Closed |
| `on_hold` | Temporarily paused | Open |
| `overdue` | Past due date | Open |

### Priority Levels

| Value | Description | Urgency |
|-------|-------------|---------|
| `low` | Low priority | 1 |
| `medium` | Normal priority | 2 |
| `high` | High priority | 3 |
| `urgent` | Critical/urgent | 4 |

---

## Complex Data Types

### Address Object

```python
{
    "address": "123 Main Street",           # string, required
    "address_2": "Unit 4B",                # string, optional
    "city": "San Francisco",               # string, required
    "state": "CA",                         # string, 2 chars, required
    "zip_code": "94102",                   # string, 5-10 chars, required
    "country": "US",                       # string, 2 chars, default "US"
    "latitude": 37.7749,                   # float, optional
    "longitude": -122.4194,                # float, optional
    "formatted_address": "123 Main Street, Unit 4B, San Francisco, CA 94102"  # string, computed
}
```

### Money Object

```python
{
    "amount": 850000.00,                   # decimal, required
    "currency": "USD",                     # string, 3 chars, default "USD"
    "formatted": "$850,000.00"             # string, computed
}
```

### Contact Information Object

```python
{
    "email": "john@example.com",           # email, optional
    "phone": "(555) 123-4567",             # phone, optional
    "mobile": "(555) 987-6543",            # phone, optional
    "fax": "(555) 123-4568",               # phone, optional
    "website": "https://example.com",      # url, optional
    "preferred_contact": "email"           # enum: email, phone, mobile
}
```

### Dimensions Object

```python
{
    "length": 25.5,                        # float, feet
    "width": 12.0,                         # float, feet
    "height": 9.0,                         # float, feet
    "area": 306.0,                         # float, square feet (computed)
    "unit": "feet"                         # string, measurement unit
}
```

---

## Property-Specific Data Types

### Property Details Object

```python
{
    "bedrooms": 3,                         # integer, 0-20
    "bathrooms": 2.5,                      # float, 0-20, increments of 0.5
    "half_baths": 1,                       # integer, 0-10
    "square_feet": 1800,                   # integer, living area
    "lot_size": 0.25,                      # float, acres
    "year_built": 1995,                    # integer, 1800-current year
    "stories": 2,                          # integer, 1-10
    "garage_spaces": 2,                    # integer, 0-20
    "parking_spaces": 4,                   # integer, 0-50
    "pool": true,                          # boolean
    "fireplace": true,                     # boolean
    "basement": false,                     # boolean
    "attic": true                          # boolean
}
```

### Financial Information Object

```python
{
    "listing_price": 850000.00,           # decimal, current asking price
    "original_price": 875000.00,          # decimal, initial listing price
    "sale_price": 825000.00,              # decimal, final sale price
    "price_per_sqft": 472.22,             # decimal, computed
    "hoa_fee": 250.00,                    # decimal, monthly HOA fee
    "property_taxes": 8500.00,            # decimal, annual taxes
    "insurance": 1200.00,                 # decimal, annual insurance
    "utilities": 150.00,                  # decimal, monthly utilities
    "maintenance": 200.00                 # decimal, monthly maintenance
}
```

---

## Validation Rules and Constraints

### Field Validation

| Field Type | Validation Rules | Error Messages |
|------------|------------------|----------------|
| Email | Valid email format, RFC 5322 compliant | "Invalid email format" |
| Phone | Digits, spaces, parentheses, hyphens allowed | "Invalid phone number format" |
| URL | Valid HTTP/HTTPS URL | "Invalid URL format" |
| ZIP Code | 5 digits or 5+4 format (US) | "Invalid ZIP code format" |
| State | Valid US state abbreviation | "Invalid state code" |
| Price | Positive number, max 2 decimal places | "Price must be positive" |
| Date | Valid ISO 8601 date | "Invalid date format" |

### Business Logic Validation

```python
# Property validation rules
{
    "bedrooms": {
        "min": 0,
        "max": 20,
        "message": "Bedrooms must be between 0 and 20"
    },
    "bathrooms": {
        "min": 0,
        "max": 20,
        "increment": 0.5,
        "message": "Bathrooms must be between 0 and 20 in 0.5 increments"
    },
    "year_built": {
        "min": 1800,
        "max": "current_year + 5",
        "message": "Year built must be between 1800 and 5 years in the future"
    },
    "listing_price": {
        "min": 1000,
        "max": 100000000,
        "message": "Listing price must be between $1,000 and $100,000,000"
    }
}
```

### Cross-Field Validation

```python
# Examples of cross-field validation rules
{
    "sale_price_vs_listing": {
        "rule": "sale_price <= listing_price * 1.5",
        "message": "Sale price cannot exceed 150% of listing price"
    },
    "closing_date_vs_listing": {
        "rule": "closing_date >= listing_date",
        "message": "Closing date must be after listing date"
    },
    "bathrooms_vs_bedrooms": {
        "rule": "bathrooms <= bedrooms * 2",
        "message": "Bathrooms cannot exceed twice the number of bedrooms"
    }
}
```

---

## API Response Formats

### Standard Response Structure

```python
# Successful response
{
    "data": {
        # Resource data here
    },
    "meta": {
        "timestamp": "2024-01-15T10:30:00Z",
        "version": "2.0.7"
    }
}

# List response with pagination
{
    "data": [
        # Array of resources
    ],
    "meta": {
        "pagination": {
            "page": 1,
            "per_page": 25,
            "total": 150,
            "total_pages": 6
        },
        "timestamp": "2024-01-15T10:30:00Z",
        "version": "2.0.7"
    }
}

# Error response
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Validation failed",
        "details": {
            "field": "email",
            "message": "Invalid email format"
        }
    },
    "meta": {
        "timestamp": "2024-01-15T10:30:00Z",
        "version": "2.0.7"
    }
}
```

### Null and Empty Values

| Scenario | Representation | Example |
|----------|----------------|---------|
| Field not provided | Omitted from response | `{}` |
| Field explicitly null | `null` value | `{"field": null}` |
| Empty string | Empty string | `{"field": ""}` |
| Empty array | Empty array | `{"field": []}` |
| Empty object | Empty object | `{"field": {}}` |

---

## Type Conversion Examples

### Python Type Mapping

```python
# API to Python type conversion
api_to_python = {
    "string": str,
    "integer": int,
    "decimal": float,  # or Decimal for precision
    "boolean": bool,
    "date": datetime.date,
    "datetime": datetime.datetime,
    "array": list,
    "object": dict
}

# Example conversion function
from datetime import datetime, date
from decimal import Decimal

def convert_api_types(data):
    """Convert API response data to appropriate Python types"""
    if isinstance(data, dict):
        converted = {}
        for key, value in data.items():
            if key.endswith('_at') and isinstance(value, str):
                # Convert datetime strings
                converted[key] = datetime.fromisoformat(value.replace('Z', '+00:00'))
            elif key.endswith('_date') and isinstance(value, str):
                # Convert date strings
                converted[key] = date.fromisoformat(value)
            elif key in ['listing_price', 'sale_price'] and isinstance(value, (int, float)):
                # Convert money fields to Decimal for precision
                converted[key] = Decimal(str(value))
            else:
                converted[key] = convert_api_types(value)
        return converted
    elif isinstance(data, list):
        return [convert_api_types(item) for item in data]
    else:
        return data
```

### JavaScript Type Mapping

```javascript
// API to JavaScript type conversion
const convertApiTypes = (data) => {
    if (Array.isArray(data)) {
        return data.map(convertApiTypes);
    } else if (data !== null && typeof data === 'object') {
        const converted = {};
        for (const [key, value] of Object.entries(data)) {
            if (key.endsWith('_at') && typeof value === 'string') {
                // Convert datetime strings to Date objects
                converted[key] = new Date(value);
            } else if (key.endsWith('_date') && typeof value === 'string') {
                // Convert date strings to Date objects
                converted[key] = new Date(value + 'T00:00:00Z');
            } else if (['listing_price', 'sale_price'].includes(key) && typeof value === 'number') {
                // Keep money fields as numbers but could use a Money library
                converted[key] = value;
            } else {
                converted[key] = convertApiTypes(value);
            }
        }
        return converted;
    }
    return data;
};
```

---

## Best Practices

### Data Handling

1. **Always validate input data** before sending to the API
2. **Use appropriate data types** for your programming language
3. **Handle null values gracefully** in your application logic
4. **Convert dates/times to local timezone** for display purposes
5. **Use decimal types for currency** to avoid floating-point precision issues

### Error Handling

1. **Check field-level validation errors** in API responses
2. **Implement client-side validation** that matches API rules
3. **Provide user-friendly error messages** based on API error codes
4. **Log detailed error information** for debugging purposes

### Performance

1. **Request only needed fields** using field selection parameters
2. **Use appropriate data types** to minimize payload size
3. **Cache frequently accessed data** with appropriate TTL
4. **Batch operations** when possible to reduce API calls

---

## Related Resources

- [API Reference](../api/index.md) - Complete API endpoint documentation
- [Error Handling Guide](../guides/error-handling.md) - Comprehensive error handling
- [Examples](../guides/examples.md) - Practical usage examples
- [Best Practices](../guides/best-practices.md) - Development best practices