# Security Policy

## Supported Versions

We actively support the following versions of the Open To Close API Python Client with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 2.x.x   | :white_check_mark: |
| 1.x.x   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in this project, please report it responsibly.

### How to Report

1. **Email**: Send details to [john@theperry.group](mailto:john@theperry.group)
2. **Subject**: Include "SECURITY" in the subject line
3. **Details**: Provide a detailed description of the vulnerability

### What to Include

Please include the following information in your report:

- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact and attack scenarios
- Any suggested fixes or mitigations
- Your contact information for follow-up

### Response Timeline

- **Initial Response**: Within 24 hours
- **Status Update**: Within 72 hours
- **Fix Timeline**: Varies based on severity (usually 1-14 days)
- **Public Disclosure**: After fix is released and users have had time to update

## Security Best Practices

### API Key Management

- **Never commit API keys** to version control
- Use environment variables or secure configuration files
- Rotate API keys regularly
- Use different keys for different environments (dev, staging, production)

### Environment Variables

```bash
# Good - Use environment variables
export OPEN_TO_CLOSE_API_KEY="your_api_key_here"

# Bad - Don't hardcode in your application
api_key = "MWI2TnluVjdxRVZPdm00..."  # Never do this!
```

### Secure Usage Examples

```python
# Good - Load from environment
from open_to_close import OpenToCloseAPI
import os

client = OpenToCloseAPI()  # Loads from OPEN_TO_CLOSE_API_KEY

# Alternative - explicit but secure
api_key = os.getenv("OPEN_TO_CLOSE_API_KEY")
client = OpenToCloseAPI(api_key=api_key)
```

### Network Security

- Always use HTTPS (which this client enforces)
- Implement proper timeout handling
- Use proper error handling to avoid information leakage
- Consider implementing rate limiting on your side

### Data Handling

- Validate all input data before sending to the API
- Sanitize any user-provided data
- Don't log sensitive information (API keys, personal data)
- Implement proper data retention policies

## Security Features

This library includes several security features:

### Built-in Protections

- **HTTPS Only**: All requests use HTTPS
- **Input Validation**: Type hints and validation for API calls
- **Error Handling**: Specific exceptions that don't leak sensitive data
- **No Credential Storage**: API keys are not stored in the client

### Dependencies

We regularly audit and update dependencies for security vulnerabilities:

- `requests` - HTTP library with security features
- `python-dotenv` - Secure environment variable loading

### Development Security

- **Bandit**: Static security analysis for Python code
- **Pre-commit hooks**: Automated security checks before commits
- **Dependency scanning**: Regular vulnerability scans of dependencies

## Vulnerability Disclosure Policy

### Coordinated Disclosure

We follow responsible disclosure practices:

1. Report received and acknowledged
2. Vulnerability confirmed and severity assessed
3. Fix developed and tested
4. Security advisory prepared
5. Fix released with security advisory
6. Public disclosure after users have time to update

### Recognition

We appreciate security researchers who help keep our users safe. With your permission, we'll acknowledge your contribution in:

- Security advisory
- Project documentation
- Release notes

## Security Contacts

- **Primary**: john@theperry.group
- **Organization**: The Perry Group
- **Response Time**: 24 hours for initial response

## Additional Resources

- [Open To Close API Security Documentation](https://api.opentoclose.com/security)
- [Python Security Best Practices](https://python.org/dev/security/)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)

---

*This security policy is effective as of June 2024 and may be updated periodically.* 