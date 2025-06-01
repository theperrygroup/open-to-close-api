# Documentation Style Guide

This comprehensive style guide establishes standards for creating consistent, high-quality documentation across all project materials. These guidelines ensure clarity, accessibility, and maintainability of documentation.

## 📝 Writing Standards

### Tone and Voice

**Primary Tone**: Professional, helpful, and approachable
- Use active voice whenever possible
- Write directly to the reader using "you"
- Be concise but comprehensive
- Maintain consistency throughout all documentation

**Prohibited Tones**:
- ❌ Overly casual or colloquial language
- ❌ Condescending or patronizing language
- ❌ Overly technical jargon without explanation
- ❌ Vague or ambiguous statements

### Language Guidelines

#### Grammar and Punctuation

**Sentence Structure**:
- Use clear, concise sentences (maximum 25 words)
- Avoid compound sentences with more than two clauses
- Start sentences with the most important information
- Use parallel structure in lists and series

**Punctuation Rules**:
- Use Oxford/serial commas: "A, B, and C"
- End bullet points with periods only if they are complete sentences
- Use em dashes (—) for breaks in thought, not hyphens (-)
- Use straight quotes ("") not curly quotes ("")

**Capitalization**:
- Use sentence case for headings and titles
- Capitalize proper nouns and official product names
- Use title case only for navigation menu items
- API endpoint names should maintain their original casing

#### Word Choice

**Preferred Terms**:
- "click" not "click on"
- "sign in" not "login" (as a verb)
- "set up" (verb) vs "setup" (noun)
- "email" not "e-mail"
- "website" not "web site"

**Avoid These Words**:
- "Simply" or "just" (implies ease that may not exist)
- "Obviously" or "clearly" (may not be obvious to all readers)
- "Easy" or "quick" (subjective assessments)
- Gender-specific pronouns when referring to users

### Content Structure

#### Information Hierarchy

**Required Elements** (in order):
1. **Title**: Clear, descriptive H1 heading
2. **Overview**: 1-2 sentence summary of the page content
3. **Prerequisites** (if applicable): What users need before starting
4. **Main Content**: Structured with clear headings
5. **Next Steps**: Links to related content or logical next actions

**Heading Structure**:
- Use only one H1 per page
- Follow logical hierarchy (H1 → H2 → H3 → H4)
- Never skip heading levels
- Use descriptive, action-oriented headings
- Keep headings under 60 characters

#### Page Length Guidelines

**Optimal Lengths**:
- **Getting Started pages**: 800-1,200 words
- **Tutorial pages**: 1,000-2,000 words
- **Reference pages**: 500-1,500 words
- **API documentation**: 1,500-3,000 words

**When to Split Content**:
- If a page exceeds 3,000 words
- If it covers more than one primary task
- If it contains more than 10 main sections

**❌ Don't: Poor Content Organization**
```markdown
# Everything About Our API

This page covers installation, authentication, making API calls, error handling,
rate limits, webhooks, data types, examples, troubleshooting, and more!

First let's talk about installing...
Then we need to authenticate...
Now let's make some calls...
Oh wait, here's how to handle errors...
Did we mention rate limits?
...continues for 5,000+ words without clear structure...
```

**✅ Do: Well-Structured Content**
```markdown
# Getting Started Guide

Learn how to install and authenticate with the API in under 10 minutes.

## Prerequisites
- Python 3.8 or higher
- Valid API key

## Installation
[Clear installation steps]

## Authentication
[Clear authentication steps]

## Your First API Call
[Simple example]

## Next Steps
- [Advanced Usage Guide](advanced.md)
- [API Reference](api/index.md)
- [Error Handling](errors.md)
```

**❌ Don't: Poor Writing Style**
```markdown
# API Stuff

Obviously you'll want to install this thing first. It's really easy, just run the command.

The API is pretty cool and does lots of things. You can get data and stuff.

Simply authenticate by doing the authentication thing. Easy!

Here's some code:
```python
x = client.get()
```

That's it! Super simple right?
```

**✅ Do: Professional Writing Style**
```markdown
# API Quick Start

Install and configure the API client to start making requests.

## Installation

Install the client using pip:

```bash
pip install api-client
```

## Authentication

Configure your API key in the environment:

```bash
export API_KEY="your_key_here"
```

## First Request

Make your first API call:

```python
from api_client import Client

client = Client()
data = client.get_resources()
print(f"Retrieved {len(data)} resources")
```

## Next Steps

- [Authentication Guide](auth.md) - Detailed authentication setup
- [API Reference](api/index.md) - Complete method documentation
```

## 🎨 Modern Visual Layout and Styling

### Material Design Grid Cards

**Primary Navigation Pattern**: Use Material Design grid cards for section overviews and navigation. This creates a modern, scannable layout that guides users visually.

**Card Structure**:
```markdown
<div class="grid cards" markdown>

-   :material-icon-name:{ .lg .middle } **Section Title**

    ---

    Brief description of what this section contains

    [:octicons-arrow-right-24: Link Text](link-destination.md)

-   :material-another-icon:{ .lg .middle } **Another Section**

    ---

    Another brief description

    [:octicons-arrow-right-24: Link Text](link-destination.md)

</div>
```

**Card Guidelines**:
- Use meaningful Material Design icons (`:material-home:`, `:material-api:`, etc.)
- Keep descriptions under 15 words
- Use consistent arrow links with descriptive text
- Group 2-6 cards per grid for optimal visual balance
- Always include the `{ .lg .middle }` classes for proper icon sizing

**❌ Don't: Poor Card Implementation**
```markdown
<div class="grid cards" markdown>

-   **Stuff**

    Some things you can do

    [Click here](page.md)

-   **More Stuff**

    Other things

    [Link](another-page.md)

</div>
```

**✅ Do: Professional Card Implementation**
```markdown
<div class="grid cards" markdown>

-   :material-api:{ .lg .middle } **API Reference**

    ---

    Complete method documentation with examples and parameters

    [:octicons-arrow-right-24: View API Docs](api/index.md)

-   :material-rocket-launch:{ .lg .middle } **Quick Start**

    ---

    Get up and running in under 5 minutes

    [:octicons-arrow-right-24: Start Tutorial](getting-started/quickstart.md)

</div>
```

### Tabbed Content Organization

**Use Case**: Organize related information that users might want to compare or choose between.

**Tabbed Structure**:
```markdown
=== "Tab Name 1"
    Content for first tab with examples and explanations.

=== "Tab Name 2"
    Content for second tab with different approach or information.

=== "Tab Name 3"
    Content for third tab with additional variations.
```

**Tab Guidelines**:
- Use for code examples with different languages/approaches
- Organize beginner vs advanced content
- Present different operating system instructions
- Show before/after examples
- Maximum 5 tabs per section for usability

**❌ Don't: Confusing Tab Organization**
```markdown
=== "Example"
    Some code here without context or explanation.

=== "Another Thing"
    Different topic entirely that doesn't relate to the first tab.

=== "Tab 3"
    Vague title with unclear content organization.
```

**✅ Do: Clear Tab Organization**
```markdown
=== ":material-rocket-launch: Basic Operation"

    ```python
    # Simple resource creation
    client = APIClient()
    resource = client.create_resource(
        name="example",
        type="standard"
    )
    ```

=== ":material-cog: Advanced Configuration"

    ```python
    # Advanced setup with configuration
    client = APIClient()
    resource = client.create_resource(
        name="example",
        configuration=config_data,
        options=advanced_options
    )
    ```
```

### Visual Admonitions with Emojis

**Modern Callout System**: Use rich admonitions with emojis for visual scanning and clear messaging hierarchy.

**Admonition Types**:

```markdown
!!! example "Quick Start"
    Use for hands-on examples and getting started content.

!!! tip "Pro Tip"
    💡 Use for helpful suggestions and best practices.

!!! info "Good to Know"
    📝 Use for additional context and background information.

!!! warning "Important"
    ⚠️ Use for important considerations and potential issues.

!!! success "Available"
    ✅ Use for confirmed working features and positive status.

!!! note "Prerequisites"
    📋 Use for requirements and things users need before starting.
```

**Visual Guidelines**:
- Always include descriptive titles
- Use appropriate emojis for quick visual recognition
- Keep content under 100 words for scanability
- Use sparingly (maximum 3 per page)
- Choose colors that support the message intent

**❌ Don't: Admonition Overuse and Misuse**
```markdown
!!! warning "Warning"
    This is important.

!!! warning "Another Warning"
    This is also important.

!!! info "Note"
    Just some regular information that could be normal text.

!!! tip "Tip"
    Something obvious that everyone already knows.

!!! example "Example"
    # Bad code example without explanation
    x = 1
```

**✅ Do: Strategic Admonition Usage**
```markdown
!!! warning "Security Considerations ⚠️"
    Never log sensitive credentials in error messages. Always sanitize authentication errors before logging.

!!! example "Complete Usage Example"
    ```python
    # Initialize client with proper error handling
    try:
        client = APIClient()
        data = client.fetch_items(status="active")
        print(f"Found {len(data)} active items")
    except AuthenticationError:
        print("Please check your API key configuration")
    ```
```

### Visual Status System

**Service Status Indicators**: Create clear visual hierarchy for different types of information:

```markdown
<!-- Service Available -->
!!! success "✅ Properties API"
    Fully operational with real-time data access.

<!-- Service Issues -->
!!! warning "⚠️ Member Data Service"
    Experiencing intermittent delays (< 5 second impact).

<!-- Feature Status -->
!!! info "🚀 New Feature"
    Recently added functionality - see examples below.
```

**Implementation Status Patterns**:
- ✅ **Available**: Feature is fully implemented and tested
- 🚧 **In Development**: Feature is being actively developed
- 📋 **Planned**: Feature is planned for future releases
- ⚠️ **Limited**: Feature has known limitations or constraints
- ❌ **Deprecated**: Feature will be removed in future versions

### Professional Page Structure

**Required Visual Hierarchy**:

1. **Hero Section**: Title + brief overview with visual elements
2. **Navigation Cards**: Grid of options for major sections
3. **Tabbed Examples**: Organized code/content with clear labels
4. **Progressive Sections**: Simple → intermediate → advanced
5. **Visual Callouts**: Strategic admonitions for key information
6. **Cross-References**: Clear "Next Steps" with visual elements

**Example Page Layout**:
```markdown
# Page Title

Brief engaging overview that explains value and scope.

## 🎯 Quick Navigation

<div class="grid cards" markdown>
[Grid cards for main sections]
</div>

## Core Content

### Basic Usage

=== "Simple Example"
    Basic code example with explanation

=== "Advanced Example"
    More complex example with additional features

!!! tip "Best Practice"
    Key insight that helps users succeed

### Advanced Topics

More detailed content organized in clear sections.

## What's Next?

- 📚 [Related Guide](link.md) - Brief description
- 🚀 [Next Steps](link.md) - Logical progression
- 💡 [Examples](link.md) - Practical applications
```

### Information Architecture Strategy

**Progressive Disclosure Approach**: Structure all documentation to follow a clear progression from simple to complex, allowing users to dive as deep as they need.

**Documentation Hierarchy**:
1. **Getting Started** - Onboarding journey with clear steps
2. **Guides** - Task-oriented how-to documentation
3. **API Reference** - Complete technical documentation
4. **Examples** - Practical code samples by complexity
5. **Reference** - Quick lookup materials
6. **Development** - Contributor and advanced user content

**Section Landing Pages**: Every major section should have an index page with:
- Brief section overview
- Grid cards for subsections
- Learning path recommendations
- Quick access to popular content
- Cross-references to related sections

**Visual Navigation Patterns**:
- Use consistent grid card layouts for navigation
- Implement tabbed content for comparing options
- Include "Next Steps" sections with visual elements
- Provide breadcrumb-style progress indicators
- Use visual callouts to highlight key information

### Modern Documentation Design Elements

**Card-Based Navigation**: Replace traditional text lists with visually appealing cards that include:
- Meaningful icons for quick recognition
- Descriptive titles that indicate functionality
- Brief descriptions that explain value
- Clear call-to-action links

**Content Organization Strategies**:
- **Tabbed Examples**: Group related code examples, different approaches, or platform-specific instructions
- **Collapsible Sections**: Use for detailed field information, advanced options, or troubleshooting details
- **Quick Reference Tables**: Provide scannable information with clear headers and consistent formatting
- **Visual Status Indicators**: Use colors and icons to show feature availability, importance levels, and current status

### Collapsible Content Sections

**Use Cases for Collapsible Content**:
- Code examples that are long but important
- Detailed parameter explanations
- Advanced configuration options
- Troubleshooting steps
- Optional/advanced features

**Implementation Patterns**:

```markdown
??? example "Code Example"
    ```python
    # Detailed code example here
    result = client.method(parameter="value")
    ```

??? info "Advanced Configuration"
    Additional details that experienced users might need
    but beginners can skip initially.

??? note "Parameter Details"
    Comprehensive explanation of all available parameters
    and their effects on the API call.
```

**Collapsible Guidelines**:
- Use descriptive titles that indicate the content value
- Start with closed state for optional information
- Use open state (`???+`) for important examples
- Keep titles under 50 characters
- Include appropriate icons for visual clarity
- Group related collapsible sections together

**Real-World Integration Examples**: Go beyond basic API calls to show:
- Complete application examples with multiple components
- Production-ready code with error handling
- Performance optimization tips and implementation
- Integration patterns with external systems
- Dashboard and analytics implementations

---

## 🎭 Advanced Visual Design System

### Comprehensive Visual Hierarchy

**Strategic Use of Horizontal Rules**: Create clear visual breaks and sections using horizontal rules (`---`) to:
- Separate major sections of content
- Create breathing room between dense information
- Establish clear content boundaries
- Guide the reader's eye through the page flow

**Implementation Pattern**:
```markdown
# Main Page Title

Opening description that sets context.

---

## 🚀 Primary Section

Main content with grid cards or key information.

---

## 📋 Secondary Section

Supporting content with examples or references.

---

## 🎯 Final Section

Conclusion, next steps, or additional resources.
```

### Advanced Grid Card Patterns

**Multi-Level Card Systems**: Use different card layouts for different information types:

**Primary Navigation Cards** (Section landing pages):
```markdown
<div class="grid cards" markdown>

-   :material-api:{ .lg .middle } **Core API**

    ---

    Create and manage primary resources with full CRUD operations

    [:octicons-arrow-right-24: Core API Reference](core-api.md)

-   :material-database:{ .lg .middle } **Data Management**

    ---

    Work with live data, manage relationships, and handle processing

    [:octicons-arrow-right-24: Data API](data-api.md)

</div>
```

**Feature Overview Cards** (Highlighting capabilities):
```markdown
<div class="grid cards" markdown>

-   :material-home: **Resource Management**

    ---

    Complete resource lifecycle from creation to completion with automated workflows

-   :material-account-group: **User & Team Operations**

    ---

    Comprehensive user search, team management, and relationship tools

</div>
```

**Quick Action Cards** (Getting started flows):
```markdown
<div class="grid cards" markdown>

-   :material-download:{ .lg .middle } **Installation**

    ---

    Install the Python client and set up your development environment

    [:octicons-arrow-right-24: Install Now](installation.md)

</div>
```

### Strategic Tabbed Content Design

**Multi-Pattern Tab Usage**: Use tabs for different organizational needs:

**Code Example Tabs** (Different approaches):
```markdown
=== ":material-rocket-launch: Basic Operation"

    ```python
    # Simple resource creation
    client = APIClient()
    resource = client.create_resource(
        name="example",
        type="standard"
    )
    ```

=== ":material-cog: Advanced Configuration"

    ```python
    # Advanced setup with configuration
    client = APIClient()
    resource = client.create_resource(
        name="example",
        configuration=config_data,
        options=advanced_options
    )
    ```
```

**Feature Comparison Tabs** (Different options):
```markdown
=== ":material-auto-fix: Automatic (Recommended)"

    The client automatically detects your API key from environment variables.

=== ":material-key-variant: Explicit"

    Pass your API key directly to the client constructor.
```

**Progressive Complexity Tabs** (Skill levels):
```markdown
=== "Basic Usage"

    Simple examples for getting started quickly.

=== "Error Handling"

    Production-ready examples with comprehensive error handling.

=== "Advanced Filtering"

    Complex queries with filtering, sorting, and pagination.
```

### Advanced Admonition Strategy

**Color-Coded Information Architecture**: Use admonitions to create a visual information hierarchy:

**Success/Available (Green)**:
```markdown
!!! success "✅ Properties API"
    Fully operational with real-time data access.

!!! abstract "Main Client"
    The **`APIClient`** serves as the main entry point, providing access to all API modules through a unified interface.
```

**Information/Tips (Blue)**:
```markdown
!!! info "Getting Started"
    Before using any API methods, you need to set up authentication.

!!! tip "Additional Resources"
    - **[Data Types & Enums](link.md)** - Type definitions
    - **[Exception Reference](link.md)** - Error handling guide
```

**Warnings/Important (Orange)**:
```markdown
!!! warning "Security Considerations"
    Never log API keys in error messages.

!!! warning "Temporary Limitation ⚠️"
    Known issues or temporary restrictions.
```

**Examples/Code (Gray)**:
```markdown
!!! example "Live Example"
    Working code example with explanation of each step.
```

### Professional Typography Hierarchy

**Emoji-Enhanced Headers**: Use strategic emoji placement for visual scanning:

```markdown
## 🚀 API Overview        # Primary feature sections
## 📋 Quick Reference     # Reference/lookup sections
## 🔧 Client Setup        # Configuration/setup
## 📖 API Endpoints       # Documentation sections
## 🎯 Key Features        # Highlighting capabilities
## 📚 Related Documentation # Cross-references
## 🔍 Method Lookup       # Search/navigation aids
```

**Semantic Header Patterns**:
- **🚀** - Getting started, launching, primary actions
- **📋** - Lists, references, quick access information
- **🔧** - Setup, configuration, technical implementation
- **📖** - Documentation, guides, learning materials
- **🎯** - Goals, objectives, key points
- **📚** - Resources, additional information
- **🔍** - Search, lookup, finding information
- **💡** - Tips, insights, best practices
- **⚡** - Quick actions, shortcuts
- **🆘** - Help, troubleshooting, support

### Advanced Cross-Reference Systems

**Multi-Level Reference Patterns**: Create comprehensive navigation systems:

**End-of-Page Reference Blocks**:
```markdown
---

## 📚 Related Documentation

!!! tip "Additional Resources"

    - **[Data Types & Enums](../reference/data-types.md)** - Type definitions and constants
    - **[Exception Reference](../reference/exceptions.md)** - Error handling guide
    - **[Examples & Guides](../guides/examples.md)** - Practical usage examples
    - **[Authentication Setup](../getting-started/authentication.md)** - Client configuration

---

## 🚀 Quick Start

New to the API? Start here:

1. **[Install the client](../getting-started/installation.md)** - Get up and running
2. **[Configure authentication](../getting-started/authentication.md)** - Set up your API key
3. **[Try the quick start](../getting-started/quickstart.md)** - Make your first API call
4. **[Explore examples](../guides/examples.md)** - See real-world use cases
```

**In-Content Cross-References**:
```markdown
### **🏗️ Core Features**
Build and manage primary application resources:

- **[Core API](core-api.md)** - Create new resources with full configuration
- **[Data Management](data-management.md)** - Manage live data and processing

### **👥 Users & Organizations**
Work with users, teams, and contacts:

- **[User Management](users.md)** - Search and manage user information
- **[Team Operations](teams.md)** - User search and team management
```

### Advanced Page Structure Templates

**Landing Page Template**:
```markdown
# Section Title

Brief engaging overview that explains value and scope.

---

## 🚀 Quick Navigation

<div class="grid cards" markdown>
[2-6 primary navigation cards]
</div>

---

## 📋 Quick Reference

### Core Components

!!! abstract "Main Concept"
    Brief explanation of the main concept or entry point.

!!! abstract "Specialized Components"
    - **Component 1**: Brief description
    - **Component 2**: Brief description

### Common Patterns

=== "Basic Usage"
    Simple example with minimal configuration.

=== "Error Handling"
    Production-ready example with error handling.

=== "Advanced Features"
    Complex example showing advanced capabilities.

---

## 🔧 Setup Section

!!! info "Getting Started"
    Prerequisites and initial setup information.

### Quick Setup
[Code example for basic setup]

---

## 📖 Detailed Sections by Category

### **🏗️ Category 1**
Description and overview:
- **[Item 1](link.md)** - Brief description
- **[Item 2](link.md)** - Brief description

### **👥 Category 2**
Description and overview:
- **[Item 3](link.md)** - Brief description
- **[Item 4](link.md)** - Brief description

---

## 🎯 Key Features

### **Feature 1**
- Bullet point highlighting capability
- Technical details and benefits

### **Feature 2**
- Another capability
- More technical details

---

## 📚 Related Documentation

!!! tip "Additional Resources"
    - **[Related Guide](link.md)** - Description
    - **[Another Resource](link.md)** - Description

---

## 🚀 Quick Start

Logical progression for new users:
1. **[Step 1](link.md)** - Description
2. **[Step 2](link.md)** - Description

---

## 🔍 Quick Lookup

[Final navigation section for specific searches]
```

**Content Page Template**:
```markdown
# Page Title

Brief overview paragraph explaining what this page covers.

---

## Overview Section

Detailed explanation with visual elements.

### Subsection

=== ":material-icon: Option 1"
    Content for first approach/option.

=== ":material-icon: Option 2"
    Content for second approach/option.

!!! tip "Best Practice"
    Strategic admonition with actionable advice.

### Another Subsection

More content with examples and explanations.

---

## Advanced Topics

More detailed content for experienced users.

---

## Cross-References

- **[Related Page](link.md)** - Brief description
- **[Another Page](link.md)** - Brief description
```

### Visual Scanning Optimization

**Strategic Information Density**: Balance dense technical information with visual breathing room:

**Dense Information Blocks**: Use tables, lists, and code blocks for comprehensive reference.

**Visual Relief Elements**: Use horizontal rules, admonitions, and white space to prevent cognitive overload.

**Scannable Elements**: Use emojis, icons, and consistent formatting to enable quick visual scanning.

**Progressive Disclosure**: Start with overview cards, then provide detailed sections, ending with comprehensive reference materials.

This comprehensive visual design system creates documentation that is both professional and highly functional, enabling users to quickly find information while providing the depth needed for complex technical tasks.

---

## 🎨 Formatting Standards

### Markdown Conventions

#### Text Formatting

**Bold Text** (`**text**`):
- UI elements (buttons, menu items, field names)
- Important warnings or key concepts
- File names and directory names
- First occurrence of important terms

**Italic Text** (`*text*`):
- Emphasis within sentences
- Variable names in explanations
- Book titles and publication names
- Foreign words or phrases

**Code Formatting** (`` `text` ``):
- Code snippets, commands, and file paths
- API endpoints and parameter names
- Environment variables
- Technical terms that are literals

#### Lists and Organization

**Unordered Lists**:
- Use `-` (hyphens) consistently, not `*` or `+`
- Maintain parallel structure across all items
- Use sentence case for list items
- End with periods only if items are complete sentences

**Ordered Lists**:
- Use for sequential steps or ranked items
- Start each item with a verb when describing actions
- Use numbers, not letters (1, 2, 3 not a, b, c)
- Restart numbering for separate procedures

**Definition Lists**:
- Use for term/definition pairs
- Keep definitions concise (under 50 words)
- Maintain alphabetical order when possible

### Code Examples

#### Code Block Standards

**Required Elements**:
- Language specification for syntax highlighting
- Complete, runnable examples when possible
- Comments explaining non-obvious sections
- Consistent indentation (2 or 4 spaces, never tabs)

**Example Structure**:
```python
# Clear, descriptive comment
def example_function(parameter: str) -> dict:
    """
    Brief description of what the function does.

    Args:
        parameter: Description of the parameter

    Returns:
        Description of return value
    """
    # Implementation comment
    result = {"status": "success", "data": parameter}
    return result

# Usage example
response = example_function("test_data")
print(response)  # Expected output
```

**Code Quality Requirements**:
- All code examples must be tested and functional
- Use realistic, meaningful variable names
- Include error handling where appropriate
- Show expected output or results
- Follow the project's code style conventions

**❌ Don't: Poor Code Examples**
```python
# Bad example - unclear, untested, no context
def func(x):
    y = api.call(x)
    return y

# Usage
result = func("stuff")
```

**✅ Do: Quality Code Examples**
```python
# Clear, descriptive example with context
def fetch_user_data(user_id: str) -> Dict[str, Any]:
    """
    Retrieve user information by ID.

    Args:
        user_id: Unique identifier for the user

    Returns:
        Dictionary containing user profile data

    Raises:
        UserNotFoundError: If user doesn't exist
    """
    try:
        response = api_client.get_user(user_id)
        return response.data
    except APIError as e:
        logger.error(f"Failed to fetch user {user_id}: {e}")
        raise

# Usage example
user_data = fetch_user_data("user123")
print(f"Retrieved data for {user_data['name']}")
# Expected output: Retrieved data for John Doe
```

#### Command Line Examples

**Format**:
```bash
# Description of what this command does
$ command --option value

# Expected output:
Output text here
```

**Requirements**:
- Include the `$` prompt for clarity
- Show expected output when helpful
- Use long-form flags when available (`--help` not `-h`)
- Include comments for complex commands

### Visual Elements

#### Links and References

**Link Text**:
- Use descriptive, action-oriented text
- Never use "click here" or "read more"
- Keep link text under 60 characters
- Make context clear without surrounding text

**Examples**:
- ✅ "View the installation guide"
- ✅ "Download the latest release"
- ❌ "Click here for more information"
- ❌ "Read more"

**❌ Don't: Poor Link Patterns**
```markdown
For more information, [click here](link.md).

You can [read more](link.md) about this topic.

Check out [this](link1.md) and [this](link2.md) and [this](link3.md).

See the documentation [here](link.md) for details.
```

**✅ Do: Descriptive Link Patterns**
```markdown
Learn more in the [Authentication Setup Guide](auth.md).

Download the [latest Python client](downloads.md).

Explore [API examples](examples.md), [error handling patterns](errors.md),
and [best practices guide](best-practices.md).

Review the [complete API reference](api/index.md) for detailed method documentation.
```

**Link Types**:
- **Internal links**: Use relative paths (`../guides/setup.md`)
- **External links**: Always open in same tab unless specifically noted
- **Code references**: Link to specific lines when possible
- **API references**: Link to exact method or endpoint

#### Tables

**Structure Requirements**:
- Include clear, descriptive headers
- Use sentence case for headers
- Left-align text content
- Right-align numerical data
- Keep cell content under 50 words

**API Documentation Tables**:

For method parameters (matches mkdocstrings output):
| Name | Type | Required | Description | Default |
|------|------|----------|-------------|---------|
| **kwargs | Any | Additional OData parameters (top, select, orderby, etc.) | {} |

For method returns:
| Type | Description |
|------|-------------|
| Dict[str, Any] | Dictionary containing active resource data |

**Table Formatting Guidelines**:
- Use consistent column widths for readability
- Bold parameter names for emphasis when needed
- Include type information in monospace font when possible
- Keep descriptions concise but informative
- Show default values clearly
- Use proper technical terminology

**Example**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | User's full name |
| email | string | Yes | Valid email address |
| age | integer | No | User's age in years |

**❌ Don't: Poor Table Structure**
| Param | Desc |
|-------|------|
| stuff | does things |
| other | also does things that are really long and wordy and hard to read in a table cell |
| ??? | unclear purpose |

**✅ Do: Clear Table Structure**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | string | Yes | Unique user identifier |
| include_metadata | boolean | No | Include additional user metadata |
| format | string | No | Response format (json, xml) |

---

## 🔧 Technical Documentation

### API Documentation

#### Endpoint Documentation

**Required Sections**:
1. **Description**: What the endpoint does
2. **HTTP Method and URL**: Complete endpoint path
3. **Parameters**: All parameters with types and descriptions
4. **Request Example**: Complete, working request
5. **Response Example**: Complete response with all fields
6. **Error Responses**: Common error cases and codes

**Parameter Documentation**:
```markdown
| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| user_id | integer | Yes | Unique user identifier | 12345 |
| include_deleted | boolean | No | Include deleted records | false |
```

#### Code Documentation

**Function/Method Documentation**:
- Include purpose, parameters, return values, and exceptions
- Provide working usage examples
- Document any side effects or state changes
- Include version information for deprecated methods

#### Method Documentation Template (mkdocstrings)

For Python method documentation that auto-generates with mkdocstrings, ensure your docstrings follow this pattern:

```python
def get_active_resources(self, **kwargs) -> Dict[str, Any]:
    """
    Get resources with Active status.

    Convenience method to retrieve only active resource entries. This is one of the most common
    queries for data-driven applications.

    Args:
        **kwargs: Additional query parameters (limit, fields, sort, etc.)

    Returns:
        Dictionary containing active resource data

    Example:
        ```python
        # Get all active resources
        active_resources = client.resources.get_active_resources(limit=100)

        # Get active resources with specific fields
        active_resources = client.resources.get_active_resources(
            fields=["id", "name", "status"],
            sort="name"
        )
        ```

    Raises:
        APIError: If the request fails
        ValidationError: If parameters are invalid
    """
```

**Key Documentation Elements for Methods:**

1. **Method Signature**: Clear method name with parameters
2. **Brief Description**: One-line summary of functionality
3. **Detailed Description**: Explain use cases and context
4. **Parameters Table**: Auto-generated from Args docstring section
5. **Returns Table**: Auto-generated from Returns docstring section
6. **Collapsible Examples**: Use example blocks in docstrings
7. **Error Information**: Document exceptions in Raises section

**mkdocstrings Integration Tips**:
- Use Google-style docstrings for best formatting
- Include realistic examples in docstring Example blocks
- Use proper type hints for parameter and return type display
- Keep examples concise but functional
- Use meaningful variable names in examples

### Error Documentation

#### Error Message Standards

**Structure**:
1. **Error Code**: Consistent format (e.g., ERR_001)
2. **Error Message**: Clear, actionable message
3. **Description**: Detailed explanation of the cause
4. **Resolution**: Step-by-step solution
5. **Related Information**: Links to relevant documentation

**Example**:
```markdown
### ERR_AUTH_001: Invalid Authentication Token

**Message**: "Authentication failed: Invalid or expired token"

**Cause**: The provided authentication token is either malformed, expired, or invalid.

**Resolution**:
1. Verify your token is correctly set in the environment variable
2. Check that the token hasn't expired
3. Ensure there are no extra spaces or characters
4. Generate a new token if necessary

**See Also**: [Authentication Guide](../guides/authentication.md)
```

---

*Last updated: [Date] | Version: 1.0 | Next review: [Date + 6 months]*
