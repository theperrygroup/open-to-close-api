# Documentation Style Guide

**Mandatory compliance required for all documentation contributions.**

This style guide establishes non-negotiable standards for all documentation in the Open To Close API Python Client project. Every documentation change must pass these requirements before merge.

---

## :material-gavel: Enforcement Policy

### Mandatory Compliance
- **All documentation MUST pass automated linting**
- **All code examples MUST be tested and verified working**
- **All internal links MUST be validated before commit**
- **Pull requests failing style checks will be automatically rejected**

### Automated Validation
```bash
# Required pre-commit checks (MUST pass)
markdownlint docs/**/*.md
vale docs/
pytest tests/test_docs_examples.py
mkdocs build --strict
```

---

## :material-file-document-outline: Document Structure Requirements

### File Organization (STRICT)

#### Mandatory Directory Structure
```
docs/
├── index.md                           # Homepage (REQUIRED)
├── getting-started/                   # User onboarding (REQUIRED)
│   ├── installation.md               # Setup guide (REQUIRED)
│   └── quickstart.md                 # Quick start (REQUIRED)
├── guides/                           # How-to content (REQUIRED)
│   ├── examples.md                   # Usage examples (REQUIRED)
│   └── troubleshooting.md            # Issue resolution (REQUIRED)
├── reference/                        # Technical docs (REQUIRED)
│   └── api-reference.md              # Complete API docs (REQUIRED)
├── development/                      # Developer docs (REQUIRED)
│   ├── contributing.md               # Dev guidelines (REQUIRED)
│   ├── STYLE_GUIDE.md               # Documentation standards (REQUIRED)
│   ├── deployment.md                # Production guide (REQUIRED)
│   └── changelog.md                 # Version history (REQUIRED)
└── assets/                          # Static resources (REQUIRED)
    ├── stylesheets/
    │   └── extra.css                # Custom styles (REQUIRED)
    └── images/                      # Documentation images
```

#### File Naming Rules (NON-NEGOTIABLE)
1. **MUST use lowercase only**: `api-reference.md` ✅, `API-Reference.md` ❌
2. **MUST use hyphens for spaces**: `quick-start.md` ✅, `quick_start.md` ❌
3. **MUST be descriptive**: `troubleshooting.md` ✅, `issues.md` ❌
4. **MUST use .md extension**: `readme.md` ✅, `readme.txt` ❌
5. **MUST NOT exceed 50 characters**: Including extension

### Page Structure Template (MANDATORY)

Every documentation page MUST follow this exact structure:

```markdown
# Exact Page Title

Brief description explaining the page purpose (1-2 sentences maximum).

---

## :material-icon: Section Title

### :material-icon: Subsection Title

Content here following all formatting rules.

---

## :material-icon: Next Section Title

Continue pattern with consistent formatting.

---

## :material-help-circle: Need Help?

Standard help section (required on all pages).
```

#### Required Page Elements (ENFORCED)
- [ ] **Exactly one H1 heading** (no more, no less)
- [ ] **Brief description** (immediately after H1, 1-2 sentences)
- [ ] **Horizontal rule separators** (`---`) between major sections
- [ ] **Material icons** on ALL H2 and H3 headings (no exceptions)
- [ ] **Help section** at bottom of every page
- [ ] **Proper heading hierarchy** (never skip levels: H1→H2→H3)

---

## :material-text-box: Writing Standards (STRICT)

### Language Requirements

#### Voice and Tense (NON-NEGOTIABLE)
- **MUST use active voice**: "Create a contact" ✅, "A contact can be created" ❌
- **MUST use second person**: "You configure" ✅, "One configures" ❌
- **MUST use present tense**: "The client connects" ✅, "The client will connect" ❌
- **MUST be concise**: Remove all filler words and redundancy

#### Prohibited Language
- **NEVER use**: "simply", "just", "obviously", "clearly", "easy"
- **NEVER use**: Future tense ("will", "going to")
- **NEVER use**: Passive voice constructions
- **NEVER use**: First person ("I", "we", "our")

### Terminology Dictionary (MANDATORY)

Use these exact terms consistently:

| Correct Term | Prohibited Alternatives |
|--------------|------------------------|
| API client | wrapper, SDK, library |
| method | function (for class methods) |
| parameter | argument (in documentation) |
| endpoint | route, URL, path |
| authentication | auth, login |
| configuration | config, setup |
| initialization | init, startup |

### Text Formatting Rules (ENFORCED)

#### Bold Text (`**bold**`)
- **Field names**: `**email**`, `**contact_id**`
- **UI elements**: `**Save Button**`, `**Settings Menu**`
- **Important terms**: `**required**`, `**deprecated**`
- **Parameter names in prose**: The `**limit**` parameter controls...

#### Italic Text (`*italic*`)
- **New concepts**: *rate limiting*, *webhook validation*
- **Emphasis**: *only* use when absolutely necessary
- **Book/document titles**: *Open To Close API Guide*

#### Code Formatting (`` `code` ``)
- **Method names**: `list_contacts()`, `create_contact()`
- **Class names**: `OpenToCloseAPI`, `ContactResource`
- **Variables**: `contact_id`, `api_key`
- **File names**: `requirements.txt`, `.env`
- **Environment variables**: `OPEN_TO_CLOSE_API_KEY`
- **HTTP status codes**: `200`, `404`, `500`

---

## :material-code-tags: Markdown Formatting (STRICT)

### Heading Requirements

#### Icon Assignment (MANDATORY)
Every H2 and H3 heading MUST have a Material icon:

```markdown
## :material-api: API Reference        # API-related content
## :material-account: User Management  # User/contact operations
## :material-home: Properties          # Property-related features
## :material-cog: Configuration        # Settings and config
## :material-rocket: Getting Started   # Quickstart content
## :material-book: Examples            # Code examples
## :material-alert-circle: Errors      # Error handling
## :material-check-circle: Success     # Positive outcomes
## :material-information: Information  # General information
## :material-lightbulb: Tips          # Helpful suggestions
## :material-file-document: Files      # File operations
## :material-magnify: Search          # Search functionality
## :material-plus-circle: Create      # Create operations
## :material-pencil: Update           # Update operations
## :material-delete: Delete           # Delete operations
## :material-file-find: Retrieve      # Get/read operations
```

#### Heading Hierarchy (ENFORCED)
```markdown
# Page Title (H1) - Exactly one per page
## Major Section (H2) - With required icon
### Subsection (H3) - With required icon
#### Minor Section (H4) - No icon, avoid if possible
##### Sub-minor (H5) - PROHIBITED
```

### List Formatting (STRICT)

#### Ordered Lists (For sequences only)
```markdown
1. First step in process
2. Second step in process
3. Final step in process
```

#### Unordered Lists (For options/features)
```markdown
- Feature one
- Feature two
- Feature three
```

#### Nested Lists (Maximum 2 levels)
```markdown
- Main category
  - Sub-item one
  - Sub-item two
- Another category
  - Different sub-item
```

### Link Standards (ENFORCED)

#### Internal Links (Required format)
```markdown
# Relative links to other documentation
[Installation Guide](../getting-started/installation.md)
[API Reference](../reference/api-reference.md#contacts-api)

# Section anchors (auto-generated from headings)
[Error Handling](#error-handling)
[Authentication](#authentication)
```

#### External Links (Required handling)
```markdown
# Same tab for documentation sites
[Python Documentation](https://docs.python.org/)

# New tab for external sites (MUST use HTML)
<a href="https://github.com/theperrygroup/open-to-close" target="_blank">GitHub Repository</a>

# Code repository links (specific format required)
[base_client.py](https://github.com/theperrygroup/open-to-close/blob/main/open_to_close/base_client.py)
```

---

## :material-tab: Material for MkDocs Features (STRICT)

### Tabbed Content (MANDATORY FORMAT)

#### When Tabs Are Required
- **Multiple code examples** for same concept (required)
- **Different complexity levels** (Basic/Advanced/Expert)
- **Platform-specific instructions** (Windows/macOS/Linux)
- **Before/after comparisons**

#### Tab Structure (EXACT FORMAT)
```markdown
=== "Basic Usage"

    Simple example with minimal parameters.
    
    ```python
    client = OpenToCloseAPI()
    result = client.contacts.list_contacts()
    ```

=== "Advanced Usage"

    Complex example with full parameter set.
    
    ```python
    client = OpenToCloseAPI(api_key="your_key")
    result = client.contacts.list_contacts(
        limit=100,
        filters={"status": "active"}
    )
    ```

=== "Error Handling"

    Production-ready example with exception handling.
    
    ```python
    from open_to_close import OpenToCloseAPI, ValidationError
    
    try:
        client = OpenToCloseAPI()
        result = client.contacts.list_contacts()
    except ValidationError as e:
        logger.error(f"Validation failed: {e}")
    ```
```

#### Tab Naming Standards (ENFORCED)
- **MUST use title case**: "Basic Usage" ✅, "basic usage" ❌
- **MUST be descriptive**: "Error Handling" ✅, "Errors" ❌
- **MUST indicate complexity**: "Basic", "Advanced", "Expert Level"
- **MUST be parallel**: "GET Request", "POST Request", "DELETE Request"

### Admonitions (MANDATORY USAGE)

#### Required Admonition Types
```markdown
!!! info "Parameters"
    For method parameters and configuration options.

!!! success "Returns"
    For return values and successful outcomes.

!!! tip "Best Practice"
    For optimization suggestions and helpful hints.

!!! warning "Important"
    For critical information and breaking changes.

!!! danger "Destructive Action"
    For irreversible operations and data loss warnings.

!!! note "Additional Information"
    For side notes and clarifications.

!!! example "Code Example"
    For extended examples requiring special highlighting.

!!! quote "API Response"
    For actual server responses and external quotes.
```

#### Admonition Rules (ENFORCED)
- **MUST have descriptive titles**: "Rate Limiting" ✅, "Note" ❌
- **MUST be 1-3 words maximum** for titles
- **MUST use proper markdown** inside admonitions
- **MUST NOT nest** admonitions (prohibited)

---

## :material-code-braces: Code Documentation (STRICT)

### Code Block Requirements (MANDATORY)

#### Language Specification (REQUIRED)
```markdown
# ALWAYS specify language (no exceptions)
```python
def example_function():
    return "Proper syntax highlighting required"
```

# Common required languages
```json
{"status": "success", "data": []}
```

```bash
pip install open-to-close
```

```yaml
site_name: Open To Close
```

```http
GET /api/v1/contacts HTTP/1.1
Authorization: Bearer your_api_key
```
```

#### Code Quality Standards (ENFORCED)
- [ ] **MUST include language specification** (no generic code blocks)
- [ ] **MUST show complete context** (imports, setup, teardown)
- [ ] **MUST be tested and verified working**
- [ ] **MUST include error handling** in production examples
- [ ] **MUST use proper indentation** (4 spaces for Python)
- [ ] **MUST include explanatory comments**

### API Method Documentation (EXACT TEMPLATE)

Every API method MUST follow this exact format:

```markdown
### :material-api: `client.resource.method_name(parameter1, parameter2=None)`

Single sentence describing what this method does and its primary purpose.

=== "Basic Example"

    ```python
    # Minimal working example
    from open_to_close import OpenToCloseAPI
    
    client = OpenToCloseAPI()
    result = client.resource.method_name("required_param")
    print(f"Result: {result}")
    ```

=== "Advanced Example"

    ```python
    # Production-ready example with all parameters
    from open_to_close import OpenToCloseAPI
    
    client = OpenToCloseAPI(api_key="your_key")
    result = client.resource.method_name(
        parameter1="value1",
        parameter2={"nested": "data"},
        timeout=30
    )
    
    # Process the response
    for item in result:
        print(f"Processing: {item['name']}")
    ```

=== "Error Handling"

    ```python
    # Complete error handling pattern
    from open_to_close import (
        OpenToCloseAPI, 
        NotFoundError, 
        ValidationError,
        RateLimitError
    )
    import logging
    
    logger = logging.getLogger(__name__)
    
    try:
        client = OpenToCloseAPI()
        result = client.resource.method_name("param")
        logger.info(f"Successfully processed {len(result)} items")
    except NotFoundError:
        logger.warning("Resource not found, continuing with defaults")
        result = []
    except ValidationError as e:
        logger.error(f"Invalid parameters: {e}")
        raise
    except RateLimitError:
        logger.warning("Rate limit exceeded, implementing backoff")
        time.sleep(60)
        # Retry logic here
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
    ```

!!! info "Parameters"
    - **`parameter1`** `str` - Required parameter description with specific constraints
    - **`parameter2`** `dict, optional` - Optional parameter (defaults to None)
    - **`timeout`** `int, default=30` - Request timeout in seconds (1-300 range)

!!! success "Returns"
    **`List[Dict[str, Any]]`** - List of resource objects with the following structure:
    
    ```json
    [
      {
        "id": 123,
        "name": "Example Resource",
        "created_at": "2024-01-15T10:30:00Z",
        "status": "active"
      }
    ]
    ```

!!! warning "Exceptions"
    - `NotFoundError` - When the specified resource does not exist
    - `ValidationError` - When parameters fail validation rules
    - `RateLimitError` - When API rate limits are exceeded
    - `AuthenticationError` - When API key is invalid or expired

!!! tip "Best Practice"
    Always implement exponential backoff for rate limiting and include comprehensive logging for production applications.
```

### Parameter Documentation (EXACT FORMAT)

```markdown
!!! info "Parameters"
    - **`parameter_name`** `type` - Description with constraints and examples
    - **`optional_param`** `type, optional` - Description (defaults to None)
    - **`default_param`** `type, default=value` - Description with default
    - **`complex_param`** `Dict[str, Union[str, int]]` - Complex type with structure
```

#### Type Annotation Requirements (MANDATORY)
- **MUST use Python type hints**: `str`, `int`, `Dict[str, Any]`, `List[str]`
- **MUST show optional status**: `str, optional` or `Optional[str]`
- **MUST include defaults**: `bool, default=True`
- **MUST use Union types**: `Union[str, int]` for multiple types
- **MUST be specific**: `List[Dict[str, Any]]` not `list`

---

## :material-image: Visual Standards (STRICT)

### Required Icons

#### Material Icons (MANDATORY)
Must use these exact icons for consistency:

```
:material-api:              → API endpoints and technical content
:material-account:          → Users, contacts, and people
:material-home:            → Properties and real estate features
:material-cog:             → Configuration and settings
:material-rocket:          → Getting started and quick actions
:material-book:            → Documentation and guides
:material-alert-circle:    → Errors, warnings, and issues
:material-check-circle:    → Success states and completion
:material-information:     → General information and details
:material-lightbulb:      → Tips, suggestions, and best practices
:material-file-document:  → Files and documents
:material-magnify:        → Search and filtering
:material-plus-circle:    → Create and add operations
:material-pencil:         → Edit and update operations
:material-delete:         → Delete and remove operations
:material-file-find:      → Retrieve and get operations
```

### Table Formatting (EXACT REQUIREMENTS)

#### Parameter Tables (MANDATORY FORMAT)
```markdown
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `name` | `str` | Yes | N/A | Contact full name (1-100 chars) |
| `email` | `str` | Yes | N/A | Valid email address |
| `phone` | `str` | No | `None` | Phone number in E.164 format |
```

#### Status Tables (REQUIRED FORMAT)
```markdown
| Endpoint | Status | Coverage | Notes |
|----------|--------|----------|-------|
| `/contacts` | ✅ Complete | 100% | All CRUD operations implemented |
| `/properties` | 🚧 Partial | 60% | Read operations only |
| `/reports` | ❌ Planned | 0% | Scheduled for v3.0 |
```

---

## :material-shield-check: Quality Assurance (ENFORCED)

### Pre-Commit Requirements (MANDATORY)

Every documentation change MUST pass:

```bash
# Markdown linting (zero tolerance for failures)
markdownlint docs/**/*.md --config .markdownlint.json

# Vale prose linting (all rules must pass)
vale docs/

# Link validation (all links must work)
markdown-link-check docs/**/*.md

# Code example testing (all examples must execute)
pytest tests/test_docs_examples.py -v

# MkDocs build (strict mode, no warnings)
mkdocs build --strict --verbose

# Spelling check (US English)
cspell "docs/**/*.md"
```

### Automated Validation Rules

#### Markdown Linting (.markdownlint.json)
```json
{
  "MD007": { "indent": 4 },
  "MD013": { "line_length": 100 },
  "MD033": false,
  "MD041": false,
  "line-length": {
    "line_length": 100,
    "heading_line_length": 60,
    "code_block_line_length": 120
  }
}
```

#### Vale Configuration (.vale.ini)
```ini
StylesPath = .vale/styles
MinAlertLevel = error

[*.md]
BasedOnStyles = Microsoft, alex
Microsoft.Contractions = NO
alex.ProfanityUnlikely = NO
```

### Testing Requirements (MANDATORY)

#### Code Example Testing
All code examples MUST have corresponding tests:

```python
# tests/test_docs_examples.py
def test_basic_usage_example():
    """Test the basic usage example from getting-started/quickstart.md"""
    # Extract and execute code from documentation
    # Verify expected output
    pass

def test_api_method_examples():
    """Test all API method examples from reference/api-reference.md"""
    # Test each code block in the API documentation
    # Ensure all examples execute successfully
    pass
```

### Performance Requirements (ENFORCED)

#### Page Load Standards
- **Initial page load**: < 2 seconds
- **Search response**: < 500ms
- **Navigation**: < 200ms
- **Image loading**: < 1 second

#### Build Performance
- **Full site build**: < 30 seconds
- **Incremental build**: < 5 seconds
- **Search index**: < 10 seconds

---

## :material-gavel: Enforcement Mechanisms

### Automated Checks (REQUIRED)

#### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/igorshubovych/markdownlint-cli
    rev: v0.37.0
    hooks:
      - id: markdownlint
        args: ['--config', '.markdownlint.json']
        
  - repo: https://github.com/errata-ai/vale
    rev: v2.29.0
    hooks:
      - id: vale
        args: ['--config', '.vale.ini']
        
  - repo: local
    hooks:
      - id: test-docs-examples
        name: Test documentation examples
        entry: pytest tests/test_docs_examples.py
        language: system
        files: '^docs/.*\.md$'
```

#### GitHub Actions (MANDATORY)
```yaml
# .github/workflows/docs-quality.yml
name: Documentation Quality

on:
  pull_request:
    paths: ['docs/**']

jobs:
  validate-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate documentation
        run: |
          # All validation commands here
          # Fail the build if any check fails
```

### Review Requirements (MANDATORY)

#### Pull Request Checklist
- [ ] All automated checks pass
- [ ] Style guide compliance verified
- [ ] Code examples tested manually
- [ ] Links validated manually
- [ ] Mobile responsiveness checked
- [ ] Search functionality verified
- [ ] Performance benchmarks met

---

## :material-update: Maintenance Schedule (REQUIRED)

### Regular Audits

#### Weekly (MANDATORY)
- Link validation across all pages
- Search functionality verification
- Mobile responsiveness check

#### Monthly (MANDATORY)
- Code example testing and updates
- Style guide compliance audit
- Performance benchmarking

#### Quarterly (MANDATORY)
- Complete style guide review
- User feedback integration
- Accessibility compliance check

### Version Control Standards

#### Commit Messages (ENFORCED)
```
docs: add API authentication examples

- Add comprehensive auth examples to quickstart
- Include error handling patterns
- Test all code examples
- Validate all internal links

Refs: #123
```

#### Branch Strategy (REQUIRED)
- `docs/feature-name` for new documentation
- `docs/fix-issue-number` for corrections
- `docs/update-section` for content updates

---

## :material-alert: Violation Consequences

### Immediate Actions
- **Failed checks**: PR automatically rejected
- **Style violations**: Build fails, no merge allowed
- **Broken examples**: Documentation deployment blocked

### Escalation Process
1. **First violation**: Automated comment with specific requirements
2. **Second violation**: Manual review required before merge
3. **Third violation**: Documentation permissions review

---

*This style guide is MANDATORY and ENFORCED. All violations will result in automatic rejection. Contact the documentation team for clarifications.* 