# Open To Close API Documentation Setup

This directory contains the complete documentation setup for the Open To Close API Python client using MkDocs with Material theme.

## Setup Overview

The documentation system includes:

- **MkDocs** with Material theme for beautiful, responsive documentation
- **Custom CSS** for real estate industry appropriate styling
- **Custom JavaScript** for enhanced functionality (copy buttons, API badges, etc.)
- **Multiple plugins** for enhanced features

## Files Structure

```
docs/
├── README_DOCUMENTATION.md    # This file
├── index.md                   # Home page
├── installation.md            # Installation guide
├── quickstart.md             # Quick start guide
├── examples.md               # Usage examples
├── api-reference.md          # Complete API reference
├── troubleshooting.md        # Troubleshooting guide
├── contributing.md           # Contributing guidelines
├── changelog.md              # Release notes
├── deployment.md             # Deployment guide
├── stylesheets/
│   └── extra.css             # Custom CSS with real estate theme
└── javascripts/
    └── extra.js              # Custom JavaScript enhancements
```

## Building Documentation

### Prerequisites

Install the documentation dependencies:

```bash
pip install -r requirements-dev.txt
```

### Local Development

To serve the documentation locally with auto-reload:

```bash
mkdocs serve
```

The documentation will be available at http://localhost:8000

### Build Static Site

To build the static documentation site:

```bash
mkdocs build
```

This creates a `site/` directory with the built documentation.

## Configuration

The main configuration is in `mkdocs.yml` at the project root. Key features:

### Theme Configuration
- **Material theme** with green color scheme (real estate appropriate)
- **Dark/light mode** toggle
- **Navigation tabs** and sections
- **Search functionality** with highlighting

### Custom Styling
- **Real estate themed colors** using CSS custom properties
- **API endpoint badges** with color coding (GET, POST, PUT, DELETE)
- **Property example highlighting** for real estate specific content
- **Enhanced code blocks** with copy functionality

### JavaScript Enhancements
- **Copy to clipboard** buttons on all code blocks
- **API method badges** automatically added to headings
- **Smooth scrolling** for anchor links
- **Status badges** for API availability
- **Table of contents highlighting**
- **Property example highlighting**

### Plugins
- **Search** with advanced separator configuration
- **Include markdown** for content reuse
- **Minify** for optimized builds
- **Version management** with mike

## Customization

### Colors and Theming

The CSS custom properties in `docs/stylesheets/extra.css` define the color scheme:

```css
:root {
  --otc-primary: #2e7d32;    /* Primary green */
  --otc-secondary: #4caf50;  /* Secondary green */
  --otc-accent: #81c784;     /* Accent green */
  --otc-dark: #1b5e20;       /* Dark green */
  --otc-light: #c8e6c9;      /* Light green */
}
```

### Adding New Features

To add new JavaScript functionality, modify `docs/javascripts/extra.js`. The file includes:
- Utility functions for DOM manipulation
- Event listeners for enhanced interactivity
- Automatic enhancement of content

## Deployment

### GitHub Pages

The configuration includes settings for GitHub Pages deployment:

```bash
mkdocs gh-deploy
```

### Version Management

Use mike for version management:

```bash
# Deploy latest version
mike deploy --push --update-aliases 1.0 latest

# Set default version
mike set-default --push latest
```

## Documentation Standards

Following the **ReZEN Documentation Process**:

1. **Google-style docstrings** for all public methods
2. **Comprehensive type hints** throughout
3. **Real-world examples** in all documentation
4. **Detailed error handling** documentation
5. **Automatic documentation updates** with code changes

## Troubleshooting

### Common Issues

1. **Build Errors**: Check that all markdown files exist and links are valid
2. **Icon Issues**: Ensure icon names are correct for Material theme
3. **Plugin Errors**: Verify all plugins are installed via requirements-dev.txt

### Missing Files

If you get missing file errors, ensure all files referenced in the navigation exist:
- index.md
- installation.md
- quickstart.md
- examples.md
- api-reference.md
- troubleshooting.md
- contributing.md
- changelog.md
- deployment.md

## Contributing to Documentation

1. **Edit markdown files** in the `docs/` directory
2. **Test locally** with `mkdocs serve`
3. **Build and verify** with `mkdocs build`
4. **Follow naming conventions** for consistency
5. **Add examples** for all new features
6. **Update navigation** in mkdocs.yml if adding new pages

## Support

For documentation issues:
- Check this README
- Review the MkDocs Material documentation
- Contact: john@theperry.group

---

**Documentation system built for The Perry Group's Open To Close API** 🏠📚 