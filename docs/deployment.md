# Deployment Guide

This guide covers deployment strategies and hosting options for applications using the Open To Close API Python Client.

## Table of Contents

- [Production Environment Setup](#production-environment-setup)
- [Environment Configuration](#environment-configuration)
- [Docker Deployment](#docker-deployment)
- [Cloud Platform Deployment](#cloud-platform-deployment)
- [CI/CD Pipeline](#cicd-pipeline)
- [Monitoring and Logging](#monitoring-and-logging)
- [Security Considerations](#security-considerations)
- [Performance Optimization](#performance-optimization)

## Production Environment Setup

### Python Environment

```bash
# Create production virtual environment
python -m venv /opt/app/.venv
source /opt/app/.venv/bin/activate

# Install production dependencies
pip install --no-dev open-to-close-api

# Or from requirements.txt
pip install -r requirements.txt
```

### System Dependencies

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv nginx supervisor

# CentOS/RHEL
sudo yum install -y python3-pip python3-venv nginx supervisor
```

## Environment Configuration

### Environment Variables

**Required:**
```bash
export OPEN_TO_CLOSE_API_KEY="your_production_api_key"
export ENVIRONMENT="production"
export LOG_LEVEL="INFO"
```

**Optional:**
```bash
export OPEN_TO_CLOSE_BASE_URL="https://api.opentoclose.com"
export REQUEST_TIMEOUT="30"
export MAX_RETRIES="3"
export RATE_LIMIT_ENABLED="true"
```

### Configuration File

`config/production.py`:
```python
import os
from typing import Optional

class ProductionConfig:
    """Production configuration settings."""
    
    # API Configuration
    OPEN_TO_CLOSE_API_KEY: str = os.getenv("OPEN_TO_CLOSE_API_KEY")
    OPEN_TO_CLOSE_BASE_URL: str = os.getenv(
        "OPEN_TO_CLOSE_BASE_URL", 
        "https://api.opentoclose.com"
    )
    
    # Request Configuration
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "30"))
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"
    RATE_LIMIT_CALLS: int = int(os.getenv("RATE_LIMIT_CALLS", "100"))
    RATE_LIMIT_PERIOD: int = int(os.getenv("RATE_LIMIT_PERIOD", "60"))
    
    @classmethod
    def validate(cls) -> None:
        """Validate required configuration."""
        if not cls.OPEN_TO_CLOSE_API_KEY:
            raise ValueError("OPEN_TO_CLOSE_API_KEY environment variable is required")
```

### Secrets Management

#### Using HashiCorp Vault
```python
import hvac

def get_api_key_from_vault():
    """Retrieve API key from Vault."""
    client = hvac.Client(url='https://vault.company.com')
    client.token = os.getenv('VAULT_TOKEN')
    
    secret = client.secrets.kv.v2.read_secret_version(
        path='open-to-close/api-key'
    )
    return secret['data']['data']['api_key']
```

#### Using AWS Secrets Manager
```python
import boto3
import json

def get_api_key_from_aws():
    """Retrieve API key from AWS Secrets Manager."""
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name='us-west-2'
    )
    
    response = client.get_secret_value(SecretId='open-to-close-api-key')
    secret = json.loads(response['SecretString'])
    return secret['api_key']
```

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Start application
CMD ["python", "-m", "app.main"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPEN_TO_CLOSE_API_KEY=${OPEN_TO_CLOSE_API_KEY}
      - ENVIRONMENT=production
      - LOG_LEVEL=INFO
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - app
    restart: unless-stopped

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  redis_data:
```

### Building and Running

```bash
# Build image
docker build -t open-to-close-app .

# Run with environment file
docker run --env-file .env -p 8000:8000 open-to-close-app

# Using docker-compose
docker-compose up -d
```

## Cloud Platform Deployment

### AWS Deployment

#### Using AWS Lambda

```python
# lambda_handler.py
import json
import os
from open_to_close_api import OpenToCloseAPI

def lambda_handler(event, context):
    """AWS Lambda handler for Open To Close API operations."""
    
    # Initialize client
    client = OpenToCloseAPI(
        api_key=os.environ['OPEN_TO_CLOSE_API_KEY']
    )
    
    try:
        # Process request
        operation = event.get('operation')
        
        if operation == 'list_contacts':
            result = client.contacts.list_contacts()
        elif operation == 'create_contact':
            result = client.contacts.create_contact(event.get('contact_data'))
        else:
            raise ValueError(f"Unsupported operation: {operation}")
        
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

#### Using ECS Fargate

```yaml
# task-definition.json
{
  "family": "open-to-close-app",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::ACCOUNT:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::ACCOUNT:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "app",
      "image": "your-account.dkr.ecr.region.amazonaws.com/open-to-close-app:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "ENVIRONMENT",
          "value": "production"
        }
      ],
      "secrets": [
        {
          "name": "OPEN_TO_CLOSE_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:open-to-close-api-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/open-to-close-app",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### Google Cloud Platform

#### Using Cloud Run

```yaml
# cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'build'
      - '-t'
      - 'gcr.io/$PROJECT_ID/open-to-close-app:$COMMIT_SHA'
      - '.'
  
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'push'
      - 'gcr.io/$PROJECT_ID/open-to-close-app:$COMMIT_SHA'
  
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'open-to-close-app'
      - '--image=gcr.io/$PROJECT_ID/open-to-close-app:$COMMIT_SHA'
      - '--region=us-central1'
      - '--platform=managed'
      - '--allow-unauthenticated'
```

### Azure Deployment

#### Using Container Instances

```bash
# Deploy to Azure Container Instances
az container create \
    --resource-group myResourceGroup \
    --name open-to-close-app \
    --image your-registry.azurecr.io/open-to-close-app:latest \
    --cpu 1 \
    --memory 1 \
    --ports 8000 \
    --environment-variables ENVIRONMENT=production \
    --secure-environment-variables OPEN_TO_CLOSE_API_KEY=$API_KEY \
    --restart-policy Always
```

## CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements-dev.txt
          pip install -e .
      
      - name: Run tests
        run: pytest tests/
        env:
          OPEN_TO_CLOSE_API_KEY: ${{ secrets.TEST_API_KEY }}

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-west-2
      
      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster production \
            --service open-to-close-app \
            --force-new-deployment
```

### GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

test:
  stage: test
  image: python:3.11
  script:
    - pip install -r requirements-dev.txt
    - pip install -e .
    - pytest tests/
  variables:
    OPEN_TO_CLOSE_API_KEY: $TEST_API_KEY

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  only:
    - main

deploy:
  stage: deploy
  image: alpine:latest
  script:
    - apk add --no-cache curl
    - curl -X POST "$DEPLOYMENT_WEBHOOK_URL"
  only:
    - main
```

## Monitoring and Logging

### Application Logging

```python
import logging
import structlog
from pythonjsonlogger import jsonlogger

def setup_logging():
    """Configure structured logging for production."""
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Configure standard logging
    handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter()
    handler.setFormatter(formatter)
    
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)

# Usage in application
logger = structlog.get_logger(__name__)

def process_contacts():
    """Process contacts with structured logging."""
    logger.info("Starting contact processing")
    
    try:
        client = OpenToCloseAPI()
        contacts = client.contacts.list_contacts()
        
        logger.info(
            "Contact processing completed",
            contact_count=len(contacts)
        )
        
    except Exception as e:
        logger.error(
            "Contact processing failed",
            error=str(e),
            exc_info=True
        )
        raise
```

### Health Checks

```python
from flask import Flask, jsonify
from open_to_close_api import OpenToCloseAPI
import time

app = Flask(__name__)

@app.route('/health')
def health_check():
    """Comprehensive health check endpoint."""
    
    health_status = {
        'status': 'healthy',
        'timestamp': time.time(),
        'checks': {}
    }
    
    # Check API connectivity
    try:
        client = OpenToCloseAPI()
        # Simple API call to verify connectivity
        client.contacts.list_contacts(params={'limit': 1})
        health_status['checks']['api_connectivity'] = 'ok'
    except Exception as e:
        health_status['status'] = 'unhealthy'
        health_status['checks']['api_connectivity'] = f'failed: {str(e)}'
    
    # Check memory usage
    import psutil
    memory_percent = psutil.virtual_memory().percent
    if memory_percent > 90:
        health_status['status'] = 'unhealthy'
        health_status['checks']['memory'] = f'high usage: {memory_percent}%'
    else:
        health_status['checks']['memory'] = 'ok'
    
    status_code = 200 if health_status['status'] == 'healthy' else 503
    return jsonify(health_status), status_code
```

### Metrics Collection

```python
from prometheus_client import Counter, Histogram, generate_latest
import time

# Metrics
api_requests_total = Counter(
    'open_to_close_api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status']
)

api_request_duration = Histogram(
    'open_to_close_api_request_duration_seconds',
    'API request duration'
)

def track_api_call(func):
    """Decorator to track API call metrics."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            api_requests_total.labels(
                method='GET',
                endpoint=func.__name__,
                status='success'
            ).inc()
            return result
            
        except Exception as e:
            api_requests_total.labels(
                method='GET',
                endpoint=func.__name__,
                status='error'
            ).inc()
            raise
            
        finally:
            duration = time.time() - start_time
            api_request_duration.observe(duration)
    
    return wrapper
```

## Security Considerations

### Network Security

```nginx
# nginx.conf - SSL/TLS configuration
server {
    listen 443 ssl http2;
    server_name api.yourcompany.com;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    # Security headers
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20 nodelay;
    
    location / {
        proxy_pass http://app:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### API Key Rotation

```python
class APIKeyManager:
    """Manage API key rotation and validation."""
    
    def __init__(self):
        self.current_key = os.getenv('OPEN_TO_CLOSE_API_KEY')
        self.backup_key = os.getenv('OPEN_TO_CLOSE_API_KEY_BACKUP')
    
    def get_working_key(self):
        """Get a working API key with fallback."""
        
        # Try current key first
        client = OpenToCloseAPI(api_key=self.current_key)
        try:
            client.contacts.list_contacts(params={'limit': 1})
            return self.current_key
        except AuthenticationError:
            logger.warning("Primary API key failed, trying backup")
        
        # Try backup key
        if self.backup_key:
            client = OpenToCloseAPI(api_key=self.backup_key)
            try:
                client.contacts.list_contacts(params={'limit': 1})
                return self.backup_key
            except AuthenticationError:
                logger.error("Both API keys failed")
                raise
        
        raise AuthenticationError("No working API key available")
```

## Performance Optimization

### Connection Pooling

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class OptimizedOpenToCloseAPI(OpenToCloseAPI):
    """Optimized client with connection pooling."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configure session with connection pooling
        self.session = requests.Session()
        
        # Retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        # HTTP adapter with connection pooling
        adapter = HTTPAdapter(
            pool_connections=20,
            pool_maxsize=20,
            max_retries=retry_strategy
        )
        
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
```

### Caching

```python
import redis
import json
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_result(expiration=300):
    """Cache API results with expiration."""
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            cached_result = redis_client.get(cache_key)
            if cached_result:
                return json.loads(cached_result)
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            redis_client.setex(
                cache_key,
                expiration,
                json.dumps(result)
            )
            
            return result
        return wrapper
    return decorator

# Usage
@cache_result(expiration=600)  # Cache for 10 minutes
def get_contacts():
    client = OpenToCloseAPI()
    return client.contacts.list_contacts()
```

### Batch Operations

```python
async def process_contacts_batch(contact_data_list, batch_size=50):
    """Process contacts in batches for better performance."""
    
    results = []
    client = OpenToCloseAPI()
    
    for i in range(0, len(contact_data_list), batch_size):
        batch = contact_data_list[i:i + batch_size]
        
        # Process batch
        batch_results = []
        for contact_data in batch:
            try:
                result = client.contacts.create_contact(contact_data)
                batch_results.append(result)
            except Exception as e:
                logger.error(f"Failed to create contact: {e}")
                batch_results.append(None)
        
        results.extend(batch_results)
        
        # Small delay between batches to avoid rate limits
        await asyncio.sleep(0.1)
    
    return results
```

This deployment guide provides comprehensive coverage of production deployment scenarios for applications using the Open To Close API Python Client. 