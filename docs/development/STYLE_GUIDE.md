# Documentation Style Guide

This comprehensive guide ensures consistent, high-quality documentation across the Open To Close API Python Client project. Follow these standards meticulously for professional, maintainable documentation.

---

## :material-file-document: Document Structure

### File Organization

#### Directory Structure
```
docs/
├── index.md                    # Homepage (required)
├── getting-started/           # New user onboarding
│   ├── installation.md        # Setup instructions
│   └── quickstart.md          # Quick start guide
├── guides/                    # How-to guides and tutorials
│   ├── examples.md            # Usage examples & tutorials
│   └── troubleshooting.md     # Common issues & solutions
├── reference/                 # Technical reference
│   └── api-reference.md       # Complete API documentation
├── development/               # Developer documentation
│   ├── contributing.md        # Development guidelines
│   ├── STYLE_GUIDE.md         # Documentation standards
│   ├── deployment.md          # Production deployment
│   └── changelog.md           # Version history
└── assets/                    # Static assets
    ├── stylesheets/
    │   └── extra.css          # Custom styling
    └── images/                # Documentation images
```

#### File Naming Conventions
- **Use lowercase** with hyphens: `api-reference.md`, `quick-start.md`
- **Be descriptive**: `troubleshooting.md` not `issues.md`
- **Avoid abbreviations**: `application-programming-interface.md` not `api.md` (except for well-known terms)
- **Use singular nouns**: `example.md` not `examples.md` (unless containing multiple distinct items)

### Page Structure Template

Every documentation page must follow this structure:

```markdown
# Page Title

Brief description of what this page covers (1-2 sentences).

---

## :material-icon: Section Title

Content here...

### :material-icon: Subsection Title

Content here...

---

## Next Section

Continue pattern...
```

#### Required Elements
1. **H1 title** - Exactly one per page
2. **Brief description** - Immediately after title
3. **Horizontal rules** (`---`) to separate major sections
4. **Material icons** for all section headers
5. **Consistent heading hierarchy** (H1 → H2 → H3, never skip levels)

---

## :material-text: Writing Style

### Tone and Voice

#### Professional but Accessible
- **Use active voice**: "Create a new contact" not "A new contact can be created"
- **Be concise**: Remove unnecessary words and filler phrases
- **Write in second person**: "You can configure..." not "One can configure..."
- **Use present tense**: "The client connects..." not "The client will connect..."

#### Technical Accuracy
- **Be precise**: Use exact parameter names, types, and values
- **Verify examples**: All code examples must be tested and working
- **Include error cases**: Show what happens when things go wrong
- **Provide context**: Explain not just how, but when and why

### Language Standards

#### Terminology Consistency
- **API client** not "wrapper" or "SDK"
- **Method** not "function" (for class methods)
- **Parameter** not "argument" (in documentation)
- **Endpoint** not "route" or "URL"
- **Authentication** not "auth" (in formal documentation)

#### Capitalization Rules
- **Product names**: "Open To Close API", "Material for MkDocs"
- **Code elements**: Use backticks for `method_names`, `class_names`, `variables`
- **HTTP methods**: ALL CAPS when referring to the protocol (`GET`, `POST`)
- **Boolean values**: lowercase (`true`, `false`, `None`)

---

## :material-code-tags: Markdown Formatting

### Headings

#### Hierarchy Rules
```markdown
# Page Title (H1) - Exactly one per page
## Major Section (H2) - With Material icons
### Subsection (H3) - With Material icons  
#### Minor Section (H4) - No icons, use sparingly
```

#### Icon Usage
```markdown
## :material-api: API Reference        # API-related content
## :material-account: User Management  # User/contact content
## :material-home: Properties          # Property-related content
## :material-cog: Configuration        # Settings/config
## :material-alert-circle: Errors      # Error handling
## :material-book: Examples            # Code examples
## :material-rocket: Getting Started   # Quickstart content
```

### Text Formatting

#### Emphasis Rules
- **Bold** (`**text**`) for UI elements, important terms, field names
- *Italic* (`*text*`) for emphasis, new concepts, parameters in prose
- `Code` (`` `text` ``) for code elements, file names, commands
- ~~Strikethrough~~ for deprecated features only

#### Lists
```markdown
# Ordered lists for sequences/steps
1. First step
2. Second step
3. Third step

# Unordered lists for options/features
- Feature one
- Feature two  
- Feature three

# Nested lists (max 2 levels)
- Main item
  - Sub-item
  - Sub-item
- Main item
```

### Links and References

#### Internal Links
```markdown
# Relative links to other docs
[Installation Guide](../getting-started/installation.md)
[API Reference](../reference/api-reference.md#contacts-api)
[Contributing Guide](../development/contributing.md)

# Section anchors (auto-generated from headings)  
[Error Handling](#error-handling)
[Client Initialization](#client-initialization)
```

#### External Links
```markdown
# Open in same tab for documentation
[Python Documentation](https://docs.python.org/)

# Open in new tab for external sites (use HTML)
<a href="https://github.com/theperrygroup/open-to-close" target="_blank">GitHub Repository</a>
```

#### Code Repository Links
```markdown
# Link to specific files
[base_client.py](https://github.com/theperrygroup/open-to-close/blob/main/open_to_close/base_client.py)

# Link to specific lines
[Exception definitions](https://github.com/theperrygroup/open-to-close/blob/main/open_to_close/exceptions.py#L15-L25)
```

---

## :material-tab: Material for MkDocs Features

### Tabbed Content

#### When to Use Tabs
- **Multiple code examples** for the same concept
- **Different approaches** to solve the same problem
- **Before/after** comparisons
- **Platform-specific** instructions

#### Tab Structure
```markdown
=== "Tab Title"

    Content here with proper indentation (4 spaces).
    
    ```python
    # Code example
    ```

=== "Another Tab"

    Different content here.
    
    ```python
    # Different approach
    ```

=== "Third Option"

    Additional content.
```

#### Tab Naming Standards
- **Be descriptive**: "Basic Usage" not "Basic"
- **Use title case**: "Error Handling" not "error handling"  
- **Be parallel**: "GET Request", "POST Request", "DELETE Request"
- **Indicate complexity**: "Basic", "Advanced", "Expert Level"

### Admonitions

#### Admonition Types and Usage

```markdown
!!! info "Parameters"
    Use for method parameters, configuration options, and informational content.

!!! success "Returns"
    Use for return values, successful outcomes, and positive results.

!!! tip "Pro Tip"
    Use for helpful hints, best practices, and optimization suggestions.

!!! warning "Important"
    Use for critical information, breaking changes, and cautions.

!!! danger "Destructive Action"
    Use for irreversible operations, data loss warnings, and security concerns.

!!! note "Additional Information"
    Use for side notes, related information, and clarifications.

!!! example "Example"
    Use for extended examples that need special highlighting.

!!! quote "API Response"
    Use for actual API responses, server messages, and external quotes.
```

#### Admonition Best Practices
- **Keep titles short**: 1-3 words maximum
- **Use emoji icons**: These are automatically added via CSS
- **Be specific**: "Rate Limiting" not "Note"
- **Nest carefully**: Avoid nested admonitions when possible
- **Consistent formatting**: Always use proper markdown inside

### Code Blocks

#### Syntax Highlighting
```markdown
# Always specify language
```python
def example_function():
    return "Always use proper syntax highlighting"
```

# Common languages
```json
{"key": "value"}
```

```bash
pip install open-to-close
```

```yaml
site_name: Project Name
```

```http
GET /api/v1/contacts HTTP/1.1
Authorization: Bearer token
```
```

#### Code Block Standards
- **Include language**: Always specify syntax highlighting
- **Show full context**: Include necessary imports and setup
- **Use real examples**: Test all code before publishing
- **Add comments**: Explain complex operations
- **Format consistently**: Use proper indentation and spacing

#### Inline Code
```markdown
Use `backticks` for:
- Method names: `list_contacts()`
- Class names: `OpenToCloseAPI`
- Parameter names: `contact_id`
- File names: `requirements.txt`
- Environment variables: `OPEN_TO_CLOSE_API_KEY`
- HTTP status codes: `404`, `200`
```

---

## :material-api: API Documentation Patterns

### Method Documentation Structure

Every API method must follow this exact structure:

```markdown
### :material-icon: `client.resource.method_name(parameters)`

Brief description of what the method does (one sentence).

=== "Basic Example"

    ```python
    # Simple usage example
    result = client.resource.method_name(param1)
    print(f"Result: {result}")
    ```

=== "Advanced Example"

    ```python
    # More complex usage with multiple parameters
    result = client.resource.method_name(
        param1="value1",
        param2={"nested": "data"},
        param3=True
    )
    
    # Process the result
    for item in result:
        print(f"Processing: {item['name']}")
    ```

=== "Error Handling"

    ```python
    from open_to_close import NotFoundError, ValidationError
    
    try:
        result = client.resource.method_name(param1)
    except NotFoundError:
        print("Resource not found")
    except ValidationError as e:
        print(f"Invalid data: {e}")
    ```

!!! info "Parameters"
    - **`param1`** `str` - Description of first parameter
    - **`param2`** `dict, optional` - Description of optional parameter
    - **`param3`** `bool, default=False` - Description with default value

!!! success "Returns"
    **`List[Dict[str, Any]]`** - Description of return value

!!! warning "Exceptions"
    - `NotFoundError` - When resource doesn't exist
    - `ValidationError` - When parameters are invalid
    - `AuthenticationError` - When API key is invalid
```

### Parameter Documentation

#### Parameter Format
```markdown
!!! info "Parameters"
    - **`parameter_name`** `type` - Brief description
    - **`optional_param`** `type, optional` - Description (defaults to None)
    - **`default_param`** `type, default=value` - Description with default
    - **`complex_param`** `Dict[str, Union[str, int]]` - Complex type description
```

#### Type Annotation Standards
- **Use Python type hints**: `str`, `int`, `Dict[str, Any]`, `List[str]`
- **Show optional parameters**: `str, optional` or `Optional[str]`
- **Include default values**: `bool, default=True`
- **Use Union types**: `Union[str, int]` for multiple types
- **Be specific**: `List[Dict[str, Any]]` not just `list`

### Return Value Documentation

```markdown
!!! success "Returns"
    **`ReturnType`** - Description of what is returned
    
    Example structure:
    ```json
    {
      "id": 123,
      "name": "Example",
      "created_at": "2024-01-15T10:30:00Z"
    }
    ```
```

### Exception Documentation

```markdown
!!! warning "Exceptions"
    - `ExceptionType` - When this exception occurs
    - `AnotherException` - Specific condition that triggers this
    - `ThirdException` - Another possible error case
```

---

## :material-image: Visual Elements

### Icons and Emojis

#### Section Icons (Material Icons)
```markdown
:material-api:              # API, endpoints, technical
:material-account:          # Users, contacts, people
:material-home:            # Properties, real estate
:material-cog:             # Configuration, settings  
:material-rocket:          # Getting started, quick actions
:material-book:            # Documentation, guides
:material-alert-circle:    # Errors, warnings, issues
:material-check-circle:    # Success, completion
:material-information:     # Information, details
:material-lightbulb:      # Tips, suggestions
:material-file-document:  # Files, documents
:material-magnify:        # Search, filtering
:material-format-list-bulleted: # Lists, collections
:material-plus-circle:    # Create, add operations
:material-pencil:         # Edit, update operations
:material-delete:         # Delete, remove operations
:material-file-find:      # Retrieve, get operations
```

#### Admonition Emojis (Auto-added via CSS)
- Info: 📋
- Success: ✅  
- Tip: 💡
- Warning: ⚠️
- Danger: 🚨

#### Text Emojis (Use Sparingly)
```markdown
✅ Completed features
❌ Known issues  
🚧 Work in progress
🎯 Important points
📚 Documentation
🔧 Configuration
🌟 New features
```

### Tables

#### Parameter Tables
```markdown
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | `str` | Yes | Contact name |
| `email` | `str` | Yes | Email address |
| `phone` | `str` | No | Phone number |
```

#### Comparison Tables
```markdown
| Feature | Basic Plan | Pro Plan | Enterprise |
|---------|------------|----------|------------|
| API Calls | 1,000/month | 10,000/month | Unlimited |
| Support | Email | Priority | 24/7 Phone |
```

#### Status Tables
```markdown
| Endpoint | Status | Notes |
|----------|--------|-------|
| `/contacts` | ✅ Complete | All CRUD operations |
| `/properties` | 🚧 In Progress | Read-only for now |
| `/reports` | ❌ Planned | Future release |
```

---

## :material-code-braces: Code Examples

### Example Quality Standards

#### Complete and Runnable
```python
# Good: Complete example with imports and context
from open_to_close import OpenToCloseAPI

client = OpenToCloseAPI()
contact = client.contacts.create_contact({
    "first_name": "John",
    "last_name": "Doe", 
    "email": "john@example.com"
})
print(f"Created contact with ID: {contact['id']}")
```

```python
# Bad: Incomplete example
contact = create_contact(data)
```

#### Error Handling Examples
```python
# Always show proper error handling
from open_to_close import OpenToCloseAPI, NotFoundError, ValidationError

try:
    client = OpenToCloseAPI()
    contact = client.contacts.retrieve_contact(123)
    print(f"Found: {contact['first_name']} {contact['last_name']}")
except NotFoundError:
    print("Contact not found")
except ValidationError as e:
    print(f"Invalid request: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

#### Real-World Context
```python
# Good: Shows real-world usage
def sync_contacts_from_crm(crm_contacts):
    """Sync contacts from external CRM system."""
    client = OpenToCloseAPI()
    synced_contacts = []
    
    for crm_contact in crm_contacts:
        try:
            # Try to find existing contact
            existing = client.contacts.list_contacts(params={
                "email": crm_contact['email']
            })
            
            if existing:
                # Update existing contact
                contact = client.contacts.update_contact(
                    existing[0]['id'],
                    {
                        "phone": crm_contact.get('phone'),
                        "last_updated": datetime.now().isoformat()
                    }
                )
            else:
                # Create new contact
                contact = client.contacts.create_contact({
                    "first_name": crm_contact['first_name'],
                    "last_name": crm_contact['last_name'],
                    "email": crm_contact['email'],
                    "phone": crm_contact.get('phone')
                })
            
            synced_contacts.append(contact)
            
        except ValidationError as e:
            print(f"Skipping invalid contact {crm_contact['email']}: {e}")
            continue
    
    return synced_contacts
```

### Code Comments

#### In-Code Documentation
```python
# Good: Explanatory comments
client = OpenToCloseAPI()

# Search for contacts created in the last 30 days
from datetime import datetime, timedelta
thirty_days_ago = datetime.now() - timedelta(days=30)

recent_contacts = client.contacts.list_contacts(params={
    "created_after": thirty_days_ago.isoformat(),
    "limit": 100  # Batch size for processing
})

# Process contacts in batches to avoid memory issues
for i in range(0, len(recent_contacts), 50):
    batch = recent_contacts[i:i+50]
    process_contact_batch(batch)
```

#### Bad Comments
```python
# Bad: Obvious or unhelpful comments
client = OpenToCloseAPI()  # Create client
contacts = client.contacts.list_contacts()  # Get contacts
print(contacts)  # Print contacts
```

---

## :material-file-check: Content Guidelines

### Page-Specific Standards

#### Installation Guide
- **System requirements** first
- **Step-by-step instructions** with verification
- **Multiple installation methods** (pip, conda, source)
- **Troubleshooting** common issues
- **Next steps** links

#### API Reference
- **Alphabetical organization** by resource
- **Complete method signatures** with types
- **Multiple examples** per method
- **Error handling** for each method
- **Related methods** cross-references

#### Examples Page
- **Real-world scenarios** not toy examples
- **Progressive complexity** (basic → advanced)
- **Complete working code** with setup
- **Expected output** shown
- **Explanation** of each example

#### Troubleshooting Guide
- **Common error messages** with solutions
- **Diagnostic steps** to identify issues
- **Environment-specific** problems
- **Contact information** for additional help

### Cross-References

#### Internal Linking Strategy
```markdown
# Link to specific sections
See the [Authentication section](../getting-started/installation.md#authentication) for setup details.

# Link to methods in API reference  
Use the [`create_contact()`](../reference/api-reference.md#create-contact) method to add new contacts.

# Link to examples
For a complete example, see [Contact Management](../guides/examples.md#contact-management).
```

#### External References
```markdown
# Official documentation
Refer to the [Open To Close API Documentation](https://api.opentoclose.com/docs) for server-side details.

# Python ecosystem
This follows [PEP 8](https://peps.python.org/pep-0008/) coding standards.

# Dependencies
Built on [Requests](https://requests.readthedocs.io/) for HTTP functionality.
```

---

## :material-check-circle: Quality Checklist

### Pre-Publication Review

#### Content Review
- [ ] **Accuracy**: All code examples tested and working
- [ ] **Completeness**: All required sections present
- [ ] **Clarity**: Technical concepts explained clearly
- [ ] **Currency**: Information is up-to-date
- [ ] **Consistency**: Follows all style guide rules

#### Technical Review
- [ ] **Links**: All internal and external links work
- [ ] **Code**: Syntax highlighting applied correctly
- [ ] **Images**: All images load and are relevant
- [ ] **Mobile**: Content readable on mobile devices
- [ ] **Search**: Key terms are searchable

#### Style Review
- [ ] **Grammar**: No grammatical errors
- [ ] **Spelling**: All words spelled correctly
- [ ] **Formatting**: Consistent markdown formatting
- [ ] **Tone**: Professional and accessible
- [ ] **Structure**: Logical information hierarchy

### MkDocs Build Verification

#### Local Testing
```bash
# Build and test locally before publishing
mkdocs build --clean
mkdocs serve

# Check for build warnings
mkdocs build 2>&1 | grep -i warning

# Validate all links
mkdocs build --verbose
```

#### Deployment Checklist
- [ ] **Build succeeds** without errors or warnings
- [ ] **All pages load** correctly in browser
- [ ] **Navigation works** and is logical
- [ ] **Search functions** properly
- [ ] **Mobile responsive** design verified
- [ ] **Performance** acceptable (< 3 second load times)

---

## :material-update: Maintenance

### Regular Updates

#### Content Maintenance Schedule
- **Weekly**: Check for broken links
- **Monthly**: Review and update examples
- **Quarterly**: Comprehensive style guide compliance review
- **Per Release**: Update all version-specific information

#### Version Control
- **Commit messages**: Use conventional commit format
- **Branch strategy**: Feature branches for major documentation updates
- **Review process**: All documentation changes require review
- **Changelog**: Document all significant documentation changes

### Style Evolution

#### When to Update This Guide
- **New MkDocs features** are adopted
- **User feedback** suggests improvements  
- **Inconsistencies** are discovered
- **Team decisions** change standards

#### Change Management
1. **Propose changes** via GitHub issues
2. **Discuss impact** with team
3. **Update guide** and examples
4. **Migrate existing content** gradually
5. **Communicate changes** to all contributors

---

*This style guide is a living document. Report inconsistencies or suggestions via [GitHub Issues](https://github.com/theperrygroup/open-to-close/issues).* 