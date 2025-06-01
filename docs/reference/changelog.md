# Changelog

All notable changes to the Open To Close API Python client are documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Enhanced documentation with comprehensive examples and integration patterns
- New caching patterns and performance optimization guides
- Advanced error handling strategies and retry mechanisms

### Changed
- Improved documentation structure and navigation
- Enhanced code examples with real-world scenarios

---

## [2.0.7] - 2024-01-15

### Added
- Complete property sub-resource support (documents, emails, notes, tasks)
- Enhanced error handling with specific exception types
- Comprehensive test coverage for all endpoints
- Type hints for better IDE support and development experience
- Lazy loading for improved client initialization performance

### Changed
- Improved API response processing and error handling
- Enhanced documentation with detailed examples
- Better parameter validation and error messages

### Fixed
- Issue with property contact relationship creation
- Pagination handling for large result sets
- Date/time parsing for various timezone formats

---

## [2.0.6] - 2024-01-10

### Added
- Property contacts API support
- Enhanced filtering options for list endpoints
- Better support for custom fields and metadata

### Changed
- Improved client initialization with better configuration options
- Enhanced error messages with more context

### Fixed
- Authentication token refresh handling
- Memory leak in long-running applications

---

## [2.0.5] - 2024-01-05

### Added
- Teams and users management API support
- Tags API for property and contact organization
- Bulk operations support for improved performance

### Changed
- Optimized API request handling for better performance
- Improved logging and debugging capabilities

### Fixed
- Issue with special characters in search queries
- Timeout handling for long-running requests

---

## [2.0.4] - 2024-01-01

### Added
- Comprehensive contacts API support
- Advanced search and filtering capabilities
- Support for custom property types and statuses

### Changed
- Enhanced client configuration options
- Improved error handling and retry logic

### Fixed
- Issue with nested object serialization
- Rate limiting edge cases

---

## [2.0.3] - 2023-12-28

### Added
- Full agents API support with team management
- Enhanced property management with additional fields
- Support for property status workflows

### Changed
- Improved API client architecture for better extensibility
- Enhanced documentation with more examples

### Fixed
- Issue with boolean field handling
- Date format consistency across endpoints

---

## [2.0.2] - 2023-12-25

### Added
- Core properties API with full CRUD operations
- Basic error handling and exception types
- Initial documentation and examples

### Changed
- Refactored client architecture for better maintainability
- Improved parameter validation

### Fixed
- Authentication header formatting
- JSON serialization edge cases

---

## [2.0.1] - 2023-12-22

### Added
- Initial client implementation with basic functionality
- Authentication support with API key management
- Basic properties endpoint support

### Fixed
- Package installation issues
- Import path corrections

---

## [2.0.0] - 2023-12-20

### Added
- Complete rewrite of the Python client
- Modern Python architecture with type hints
- Comprehensive API coverage for all endpoints
- Enhanced error handling and retry mechanisms
- Lazy loading and performance optimizations

### Changed
- **BREAKING**: New client initialization pattern
- **BREAKING**: Updated method signatures for consistency
- **BREAKING**: Restructured response formats
- Improved documentation and examples

### Removed
- **BREAKING**: Legacy v1.x client methods
- **BREAKING**: Deprecated configuration options

### Migration Guide

#### Client Initialization

**Before (v1.x):**
```python
from open_to_close import Client

client = Client(api_key="your-key")
```

**After (v2.x):**
```python
from open_to_close import OpenToCloseAPI

client = OpenToCloseAPI(api_key="your-key")
# or with environment variable
client = OpenToCloseAPI()  # Uses OPEN_TO_CLOSE_API_KEY
```

#### Method Names

**Before (v1.x):**
```python
client.get_properties()
client.create_property(data)
client.get_property(id)
```

**After (v2.x):**
```python
client.properties.list_properties()
client.properties.create_property(data)
client.properties.retrieve_property(id)
```

#### Error Handling

**Before (v1.x):**
```python
try:
    property = client.get_property(123)
except Exception as e:
    print(f"Error: {e}")
```

**After (v2.x):**
```python
from open_to_close.exceptions import NotFoundError, ValidationError

try:
    property = client.properties.retrieve_property(123)
except NotFoundError:
    print("Property not found")
except ValidationError as e:
    print(f"Validation error: {e}")
```

---

## [1.5.2] - 2023-11-15

### Fixed
- Critical security vulnerability in authentication handling
- Memory leak in long-running applications

### Changed
- Updated dependencies to latest secure versions

---

## [1.5.1] - 2023-11-10

### Added
- Support for property search with advanced filters
- Pagination support for large result sets

### Fixed
- Issue with date range queries
- Timeout handling improvements

---

## [1.5.0] - 2023-11-01

### Added
- Contacts management functionality
- Basic team and user operations
- Enhanced property metadata support

### Changed
- Improved API response caching
- Better error messages and debugging

### Deprecated
- Legacy authentication methods (will be removed in v2.0)

---

## [1.4.3] - 2023-10-20

### Fixed
- Critical bug in property update operations
- Issue with special characters in property addresses

### Security
- Updated authentication token handling

---

## [1.4.2] - 2023-10-15

### Added
- Support for property photos and documents
- Basic webhook support

### Fixed
- Issue with timezone handling in date fields
- Memory usage optimization

---

## [1.4.1] - 2023-10-10

### Fixed
- Package distribution issues
- Documentation formatting problems

---

## [1.4.0] - 2023-10-05

### Added
- Full properties CRUD operations
- Basic agents management
- Configuration file support

### Changed
- Improved client initialization
- Enhanced error handling

---

## [1.3.0] - 2023-09-20

### Added
- Initial properties API support
- Basic authentication
- Simple error handling

### Changed
- Restructured package organization

---

## [1.2.0] - 2023-09-10

### Added
- Basic API client framework
- Authentication support
- Initial documentation

---

## [1.1.0] - 2023-09-01

### Added
- Project structure and build system
- Basic package configuration

---

## [1.0.0] - 2023-08-25

### Added
- Initial release
- Basic project setup
- Package structure

---

## Version Support Policy

| Version | Status | Python Support | End of Life |
|---------|--------|----------------|-------------|
| 2.0.x | Active | 3.8+ | TBD |
| 1.5.x | Security fixes only | 3.7+ | 2024-06-01 |
| 1.4.x | End of life | 3.6+ | 2024-01-01 |
| 1.3.x | End of life | 3.6+ | 2023-12-01 |

## Breaking Changes Summary

### v2.0.0 Breaking Changes

1. **Client Initialization**
   - Changed from `Client()` to `OpenToCloseAPI()`
   - New lazy loading architecture

2. **Method Organization**
   - Methods organized by resource (e.g., `client.properties.list_properties()`)
   - Consistent naming convention across all endpoints

3. **Error Handling**
   - New exception hierarchy with specific exception types
   - More detailed error information

4. **Response Format**
   - Standardized response structure
   - Better handling of pagination and metadata

5. **Configuration**
   - New configuration options and environment variable support
   - Removed deprecated configuration methods

### v1.5.0 Breaking Changes

1. **Authentication**
   - Deprecated legacy authentication methods
   - New token-based authentication

2. **Method Signatures**
   - Updated parameter names for consistency
   - Changed return value formats

## Upgrade Guides

### Upgrading from v1.x to v2.x

1. **Update Installation**
   ```bash
   pip install --upgrade open-to-close>=2.0.0
   ```

2. **Update Imports**
   ```python
   # Old
   from open_to_close import Client
   
   # New
   from open_to_close import OpenToCloseAPI
   ```

3. **Update Client Initialization**
   ```python
   # Old
   client = Client(api_key="your-key")
   
   # New
   client = OpenToCloseAPI(api_key="your-key")
   ```

4. **Update Method Calls**
   ```python
   # Old
   properties = client.get_properties()
   property = client.get_property(123)
   
   # New
   properties = client.properties.list_properties()
   property = client.properties.retrieve_property(123)
   ```

5. **Update Error Handling**
   ```python
   # Old
   try:
       property = client.get_property(123)
   except Exception as e:
       handle_error(e)
   
   # New
   from open_to_close.exceptions import NotFoundError
   
   try:
       property = client.properties.retrieve_property(123)
   except NotFoundError:
       handle_not_found()
   ```

### Upgrading from v1.4.x to v1.5.x

1. **Update Authentication**
   ```python
   # Old (deprecated)
   client = Client(username="user", password="pass")
   
   # New
   client = Client(api_key="your-api-key")
   ```

2. **Update Search Methods**
   ```python
   # Old
   properties = client.search_properties(query="San Francisco")
   
   # New
   properties = client.search_properties(
       filters={"city": "San Francisco"}
   )
   ```

## Security Updates

### v2.0.7
- Enhanced input validation and sanitization
- Improved authentication token handling
- Updated dependencies with security patches

### v1.5.2
- **CRITICAL**: Fixed authentication bypass vulnerability
- Updated cryptographic libraries
- Enhanced request validation

### v1.4.3
- Fixed potential XSS vulnerability in error messages
- Updated authentication token expiration handling

## Performance Improvements

### v2.0.7
- Lazy loading reduces initial client creation time by 60%
- Improved response parsing performance
- Better memory usage for large result sets

### v2.0.5
- Bulk operations reduce API calls by up to 80%
- Enhanced caching mechanisms
- Optimized JSON serialization

### v1.5.0
- Response caching reduces redundant API calls
- Improved connection pooling
- Better timeout handling

## Deprecation Notices

### Current Deprecations (v2.0.7)

None currently. All deprecated features from v1.x have been removed.

### Removed in v2.0.0

- Legacy `Client` class (use `OpenToCloseAPI`)
- Old method naming convention (use resource-based methods)
- Deprecated authentication methods
- Legacy configuration options

### Previously Deprecated (v1.5.0)

- Username/password authentication (removed in v2.0.0)
- Legacy search methods (removed in v2.0.0)
- Old configuration file format (removed in v2.0.0)

---

## Contributing

We welcome contributions! Please see our [Contributing Guide](../development/contributing.md) for details on:

- Reporting bugs
- Suggesting features
- Submitting pull requests
- Development setup

## Support

- **Documentation**: [https://theperrygroup.github.io/open-to-close](https://theperrygroup.github.io/open-to-close)
- **Issues**: [GitHub Issues](https://github.com/theperrygroup/open-to-close/issues)
- **Discussions**: [GitHub Discussions](https://github.com/theperrygroup/open-to-close/discussions)

---

*For older versions and detailed commit history, see the [GitHub releases page](https://github.com/theperrygroup/open-to-close/releases).*