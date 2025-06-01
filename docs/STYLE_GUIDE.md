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

**Advanced Admonition Examples**:

```markdown
!!! example "Live Example"
    Working code example with explanation of each step.

!!! success "Service Status: Available ✅"
    Current status and availability information.

!!! warning "Temporary Limitation ⚠️"
    Known issues or temporary restrictions.

!!! info "Developer Note 📝"
    Technical insights and implementation details.

!!! tip "Pro Tip 💡"
    Expert advice and optimization suggestions.
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

#### Admonitions and Callouts

**Usage Guidelines**:

**Note** (general information):
!!! note "Optional Title"
    General information that provides additional context or background.

**Tip** (helpful suggestions):
!!! tip "Pro Tip"
    Helpful suggestions or best practices that can improve the user experience.

**Warning** (important cautions):
!!! warning "Important"
    Information about potential problems or important considerations.

**Danger** (critical alerts):
!!! danger "Critical"
    Information about actions that could cause data loss or system problems.

**Requirements**:
- Use sparingly (maximum 3 per page)
- Keep content under 100 words
- Always include a descriptive title
- Use appropriate emoji for visual scanning

#### Tables

**Structure Requirements**:
- Include clear, descriptive headers
- Use sentence case for headers
- Left-align text content
- Right-align numerical data
- Keep cell content under 50 words

**API Documentation Tables**:

For method parameters (matches mkdocstrings output):
| Name | Type | Description | Default |
|------|------|-------------|---------|
| **kwargs | Any | Additional OData parameters (top, select, orderby, etc.) | {} |

For method returns:
| Type | Description |
|------|-------------|
| Dict[str, Any] | Dictionary containing active property listings |

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

**Link Types**:
- **Internal links**: Use relative paths (`../guides/setup.md`)
- **External links**: Always open in same tab unless specifically noted
- **Code references**: Link to specific lines when possible
- **API references**: Link to exact method or endpoint

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

## 🎯 User Experience Guidelines

### Navigation and Structure

#### Information Architecture

**Page Organization**:
- Group related information together
- Use progressive disclosure (simple → complex)
- Provide multiple entry points for different user types
- Include clear navigation paths between related topics

**Table of Contents**:
- Required for pages over 1,000 words
- Maximum 3 levels deep
- Use descriptive, scannable titles
- Include estimated reading time for long sections

#### Cross-References

**Internal Linking Strategy**:
- Link to relevant information contextually
- Provide "See Also" sections for related topics
- Use consistent link text for the same destinations
- Avoid excessive linking within paragraphs

### Accessibility Standards

#### Content Accessibility

**Requirements**:
- Use descriptive alt text for all images
- Provide text alternatives for video content
- Use sufficient color contrast (4.5:1 minimum)
- Structure content with proper heading hierarchy
- Write at a 9th-grade reading level or lower

**Image Guidelines**:
- Alt text should describe the image content and context
- Use empty alt text (`alt=""`) for decorative images
- Keep alt text under 125 characters
- Don't start with "Image of" or "Picture of"

#### Screen Reader Compatibility

**Best Practices**:
- Use semantic HTML elements
- Provide skip navigation links
- Use descriptive link text
- Include form labels and instructions
- Test with screen reader software

### International Considerations

#### Writing for Global Audiences

**Guidelines**:
- Avoid idioms, slang, and cultural references
- Use simple sentence structures
- Define technical terms on first use
- Provide glossaries for complex terminology
- Consider right-to-left reading patterns in design

#### Localization Preparation

**Requirements**:
- Avoid embedding text in images
- Use flexible layouts that accommodate text expansion
- Separate content from formatting
- Use Unicode-compliant text encoding
- Plan for date/time format variations

## 📊 Quality Assurance

### Content Review Process

#### Review Checklist

**Technical Accuracy**:
- [ ] All code examples tested and functional
- [ ] API endpoints verified and current
- [ ] Screenshots current and accurate
- [ ] Links functional and pointing to correct destinations
- [ ] Version numbers and compatibility information current

**Editorial Quality**:
- [ ] Grammar and spelling checked
- [ ] Tone consistent with style guide
- [ ] Headings follow hierarchy rules
- [ ] Lists use parallel structure
- [ ] Formatting follows style guide conventions

**User Experience**:
- [ ] Information architecture logical
- [ ] Prerequisites clearly stated
- [ ] Next steps provided
- [ ] Error scenarios addressed
- [ ] Multiple user paths considered

### Maintenance Standards

#### Update Frequency

**Content Types and Update Schedule**:
- **Getting Started guides**: Review monthly
- **API documentation**: Update with each release
- **Screenshots**: Update quarterly or with UI changes
- **Code examples**: Test with each major version
- **External links**: Check quarterly

#### Version Control

**Documentation Versioning**:
- Tag documentation versions with software releases
- Maintain changelog for documentation updates
- Archive outdated versions but keep accessible
- Use semantic versioning for major documentation changes

#### Metrics and Analytics

**Track These Metrics**:
- Page views and time on page
- User feedback scores and comments
- Search query analysis
- Exit points and bounce rates
- Mobile vs desktop usage patterns

**Regular Reviews**:
- Monthly analytics review
- Quarterly user feedback analysis
- Annual comprehensive content audit
- Ongoing competitor analysis

## 🛠️ Tools and Automation

### Writing Tools

#### Required Tools

**Grammar and Style**:
- Grammar checker (Grammarly, ProWritingAid, or similar)
- Readability analyzer (Hemingway Editor or similar)
- Spell checker with technical dictionary
- Markdown linter for formatting consistency

**Testing Tools**:
- Link checker for broken links
- Accessibility scanner (WAVE, aXe, or similar)
- Mobile responsiveness tester
- Performance monitoring tools

### Style Enforcement

#### Automated Checks

**Implement These Checks**:
- Markdown formatting validation
- Heading structure verification
- Link validation (internal and external)
- Image alt text presence
- Code block language specification

**Style Guide Automation**:
- Create custom dictionaries for spell checkers
- Develop style guide templates
- Set up automated style checking in CI/CD
- Use consistent file naming conventions

### Content Management

#### File Organization

**Directory Structure**:
```
docs/
├── index.md                    # Landing page
├── getting-started/           # User onboarding
├── guides/                   # How-to documentation
├── api/                     # API reference
├── examples/               # Code examples
├── reference/             # Quick reference
├── development/          # Contributor docs
├── assets/              # Images and media
│   ├── images/
│   ├── videos/
│   └── downloads/
└── templates/          # Documentation templates
    ├── guide-template.md
    ├── api-template.md
    └── tutorial-template.md
```

**File Naming Conventions**:
- Use lowercase with hyphens: `user-management.md`
- Be descriptive but concise: `api-authentication-guide.md`
- Use consistent prefixes for related files: `api-*.md`
- Include version numbers for versioned docs: `migration-v2-to-v3.md`

## 📋 Templates and Examples

### Page Templates

#### Guide Template

```markdown
# Page Title

Brief overview paragraph explaining what this guide covers and who it's for.

## Prerequisites

- List any required knowledge
- Include links to prerequisite reading
- Mention required tools or setup

## Overview

More detailed explanation of what users will accomplish.

## Step-by-step Instructions

### Step 1: Descriptive heading

Detailed instructions with code examples.

### Step 2: Next step

Continue with clear, actionable steps.

## Troubleshooting

Common issues and solutions.

## Next Steps

- Link to related guides
- Suggest logical next actions
- Point to additional resources

## Additional Resources

- Links to related documentation
- External references
- Community resources
```

#### API Reference Template

```markdown
# API Endpoint Name

Brief description of what this endpoint does.

## HTTP Request

```
METHOD /api/v1/endpoint
```

## Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| param1 | string | Yes | Description | "value" |

## Request Example

```language
Code example here
```

## Response Example

```json
{
  "example": "response"
}
```

## Error Responses

List common error scenarios.

## Rate Limiting

Explain any rate limits.
```

#### Method Documentation Template (mkdocstrings)

For Python method documentation that auto-generates with mkdocstrings, ensure your docstrings follow this pattern:

```python
def get_active_properties(self, **kwargs) -> Dict[str, Any]:
    """
    Get properties with Active status.
    
    Convenience method to retrieve only active property listings. This is one of the most common
    queries for real estate applications.
    
    Args:
        **kwargs: Additional OData parameters (top, select, orderby, etc.)
        
    Returns:
        Dictionary containing active property listings
        
    Example:
        ```python
        # Get all active properties
        active_properties = client.property.get_active_properties(top=100)
        
        # Get active properties with specific fields
        active_properties = client.property.get_active_properties(
            select=["ListingId", "ListPrice", "UnparsedAddress"],
            orderby="ListPrice"
        )
        ```
        
    Raises:
        WFRMLSError: If the request fails
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

**mkdocstrings Integration Tips:**
- Use Google-style docstrings for best formatting
- Include realistic examples in docstring Example blocks
- Use proper type hints for parameter and return type display
- Keep examples concise but functional
- Use meaningful variable names in examples

### Content Examples

#### Effective vs Ineffective Examples

**❌ Poor Example**:
```markdown
# Setup

Just run the install command and you're good to go! It's really easy.

```bash
npm install
```

That's it!
```

**✅ Good Example**:
```markdown
# Installation

Install the package using npm to add it to your project dependencies.

## Prerequisites

- Node.js 14.0 or higher
- npm 6.0 or higher

## Install Command

```bash
# Install the package
npm install package-name

# Verify installation
npm list package-name
```

## Verification

Confirm the installation was successful:

```javascript
const package = require('package-name');
console.log(package.version); // Should output version number
```

## Next Steps

- [Configure the package](configuration.md)
- [View usage examples](examples.md)
```

## 🎯 Visual Design Principles

### Color and Visual Hierarchy

**Status Colors**: Use consistent color coding throughout documentation:
- **Green (✅)**: Available features, success states, working examples
- **Orange (⚠️)**: Warnings, important considerations, temporary issues  
- **Red (❌)**: Errors, deprecated features, critical issues
- **Blue (📝)**: Information, tips, additional context
- **Purple (🚀)**: Advanced features, next steps, future features

### Icon Usage Standards

**Material Design Icons**: Use meaningful, consistent icons throughout:
- `:material-home:` - Properties, main sections
- `:material-account-group:` - Members, users, people
- `:material-office-building:` - Offices, organizations
- `:material-calendar:` - Events, scheduling, time-based
- `:material-api:` - APIs, technical interfaces
- `:material-code:` - Code examples, development
- `:material-book:` - Documentation, guides, learning
- `:material-rocket:` - Getting started, quick actions

**Emoji Enhancement**: Strategic emoji use for quick visual scanning:
- 🎯 for goals, objectives, targeting
- 📚 for learning, documentation, guides  
- 🚀 for getting started, quick actions
- 💡 for tips, insights, ideas
- ⚠️ for warnings, important notes
- ✅ for success, available features
- 🔧 for tools, technical setup
- 📊 for data, analytics, reporting

### Responsive Visual Design

**Mobile-First Considerations**:
- Grid cards stack vertically on mobile
- Tabs remain functional on small screens
- Code blocks scroll horizontally when needed
- Navigation cards maintain readability
- Admonitions work well on all screen sizes

This style guide creates modern, professional documentation that users can navigate intuitively while maintaining technical accuracy and comprehensive coverage.

---

*Last updated: [Date] | Version: 1.0 | Next review: [Date + 6 months]* 