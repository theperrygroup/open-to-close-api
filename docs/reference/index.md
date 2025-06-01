# Reference Documentation

Complete reference materials for the Open To Close API Python client. This section provides detailed technical specifications, data formats, and system information.

---

## 📚 Available References

<div class="grid cards" markdown>

-   :material-alert-circle:{ .lg .middle } **Exception Reference**

    ---

    Complete documentation of all exception types and error handling patterns

    [:octicons-arrow-right-24: Exception Reference](exceptions.md)

-   :material-database:{ .lg .middle } **Data Types**

    ---

    Type definitions, enums, and data structure specifications

    [:octicons-arrow-right-24: Data Types Reference](data-types.md)

-   :material-speedometer:{ .lg .middle } **Rate Limits**

    ---

    API rate limiting policies, quotas, and best practices

    [:octicons-arrow-right-24: Rate Limits](rate-limits.md)

-   :material-history:{ .lg .middle } **Changelog**

    ---

    Version history, breaking changes, and migration guides

    [:octicons-arrow-right-24: Changelog](changelog.md)

</div>

---

## 🚀 Quick Reference

### **Common Data Types**

```python
from typing import Dict, List, Optional, Any

# Property data structure
PropertyData = Dict[str, Any]

# Contact data structure  
ContactData = Dict[str, Any]

# Standard API response
APIResponse = Dict[str, Any]
```

### **Exception Hierarchy**

```python
OpenToCloseAPIError (Base)
├── AuthenticationError
├── ValidationError
├── NotFoundError
├── RateLimitError
├── ServerError
└── NetworkError
```

### **Rate Limits**

| Resource | Requests per Minute | Burst Limit |
|----------|--------------------:|------------:|
| Properties | 1000 | 100 |
| Contacts | 1000 | 100 |
| Agents | 500 | 50 |
| General | 2000 | 200 |

---

## 🔍 How to Use This Section

**For Developers:**
- Use **[Exception Reference](exceptions.md)** to implement proper error handling
- Refer to **[Data Types](data-types.md)** for request/response structures
- Check **[Rate Limits](rate-limits.md)** when designing bulk operations

**For System Administrators:**
- Monitor **[Rate Limits](rate-limits.md)** for capacity planning
- Track **[Changelog](changelog.md)** for system updates

**For API Consumers:**
- Follow **[Exception Reference](exceptions.md)** for robust applications
- Use **[Data Types](data-types.md)** for validation and testing

---

## 📋 Reference Standards

All reference documentation follows these standards:

- **Complete coverage** of all API features
- **Executable examples** where applicable  
- **Version compatibility** information
- **Migration guidance** for breaking changes
- **Performance considerations** and recommendations

---

## 🚀 Next Steps

1. **[Start with Exceptions](exceptions.md)** - Essential for error handling
2. **[Review Data Types](data-types.md)** - Understand API structures
3. **[Check Rate Limits](rate-limits.md)** - Plan your implementation
4. **[Read Changelog](changelog.md)** - Stay updated on changes

---

*Reference documentation provides the technical foundation for building robust applications with the Open To Close API.* 