# Open To Close API Documentation

## Overview

Open To Close is a real estate transaction management software platform that provides an API for integrating with their system. The API allows developers to manage contacts, properties, agents, teams, documents, tasks, and other real estate-related operations.

## Base Information

- **Company**: Open To Close, Inc.
- **Website**: https://opentoclose.com
- **App**: https://app.opentoclose.com
- **Documentation**: https://docs.opentoclose.com (Limited access)
- **Industry**: Real Estate Transaction Management

## API Details

### Base URL
Current implementation uses: `https://api.opentoclose.com/v1`

### Authentication
- Uses API key authentication via `api_token` parameter
- API key can be set via environment variable: `OPEN_TO_CLOSE_API_KEY`

### Available Resources

Based on the current implementation, the following API resources are available:

#### Core Resources
- **Agents** (`/agents`) - Real estate agent management
- **Contacts** (`/contacts`) - Customer contact management  
- **Properties** (`/properties`) - Property management
- **Teams** (`/teams`) - Team management
- **Tags** (`/tags`) - Tagging system
- **Users** (`/users`) - User management

#### Property Sub-Resources
- **Property Contacts** (`/properties/{id}/contacts`) - Property-contact relationships
- **Property Documents** (`/properties/{id}/documents`) - Document management
- **Property Emails** (`/properties/{id}/emails`) - Email tracking
- **Property Notes** (`/properties/{id}/notes`) - Note management
- **Property Tasks** (`/properties/{id}/tasks`) - Task management

### API Operations

Each resource typically supports CRUD operations:
- `GET` - List/retrieve resources
- `POST` - Create new resources
- `PUT` - Update existing resources
- `DELETE` - Delete resources

## Implementation Notes

The current Python wrapper implementation includes:
- Comprehensive error handling with custom exceptions
- Type hints and Google-style docstrings
- Environment variable support for API keys
- Response data processing and validation

## Known Issues

Based on the workspace notes, there appear to be endpoint URL issues that need investigation and correction by reviewing the official documentation. 