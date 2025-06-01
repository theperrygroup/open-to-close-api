# Integration Patterns

This guide covers various patterns and strategies for integrating the Open To Close API into your applications, workflows, and systems. Each pattern includes implementation examples, best practices, and considerations for production use.

## Overview

The Open To Close API can be integrated into various types of applications and workflows:

- **CRM Systems**: Sync property and contact data
- **Marketing Platforms**: Automate listing distribution
- **Workflow Management**: Task automation and tracking
- **Reporting Systems**: Data aggregation and analytics
- **Mobile Applications**: Real-time property access
- **Third-party Services**: External service integration

---

## Authentication Patterns

### Environment-Based Configuration

The most secure and flexible approach for managing API credentials:

```python
import os
from open_to_close import OpenToCloseAPI

# Method 1: Environment variables (recommended)
client = OpenToCloseAPI(
    api_key=os.getenv('OPEN_TO_CLOSE_API_KEY'),
    base_url=os.getenv('OPEN_TO_CLOSE_BASE_URL', 'https://api.opentoclose.com')
)

# Method 2: Configuration file
import json

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

config = load_config()
client = OpenToCloseAPI(
    api_key=config['api_key'],
    base_url=config.get('base_url')
)

# Method 3: AWS Secrets Manager (for cloud deployments)
import boto3
import json

def get_secret(secret_name, region_name="us-east-1"):
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        secret = json.loads(get_secret_value_response['SecretString'])
        return secret
    except Exception as e:
        raise e

# Usage
secrets = get_secret("open-to-close-api-credentials")
client = OpenToCloseAPI(
    api_key=secrets['api_key'],
    base_url=secrets.get('base_url')
)
```

### Multi-Environment Setup

```python
class APIClientFactory:
    """Factory for creating API clients for different environments"""
    
    ENVIRONMENTS = {
        'development': {
            'base_url': 'https://api-dev.opentoclose.com',
            'timeout': 30
        },
        'staging': {
            'base_url': 'https://api-staging.opentoclose.com',
            'timeout': 30
        },
        'production': {
            'base_url': 'https://api.opentoclose.com',
            'timeout': 60
        }
    }
    
    @classmethod
    def create_client(cls, environment='production'):
        env_config = cls.ENVIRONMENTS.get(environment)
        if not env_config:
            raise ValueError(f"Unknown environment: {environment}")
        
        api_key = os.getenv(f'OPEN_TO_CLOSE_API_KEY_{environment.upper()}')
        if not api_key:
            raise ValueError(f"API key not found for environment: {environment}")
        
        return OpenToCloseAPI(
            api_key=api_key,
            base_url=env_config['base_url']
        )

# Usage
dev_client = APIClientFactory.create_client('development')
prod_client = APIClientFactory.create_client('production')
```

---

## Data Synchronization Patterns

### One-Way Sync (Push to Open To Close)

```python
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class PropertySyncService:
    """Service for syncing properties from external system to Open To Close"""
    
    def __init__(self, otc_client, external_data_source):
        self.otc_client = otc_client
        self.external_source = external_data_source
        self.sync_log = []
    
    def sync_properties(self, since: datetime = None) -> Dict[str, Any]:
        """Sync properties modified since given datetime"""
        if since is None:
            since = datetime.now() - timedelta(days=1)
        
        # Get modified properties from external source
        external_properties = self.external_source.get_modified_properties(since)
        
        results = {
            'processed': 0,
            'created': 0,
            'updated': 0,
            'errors': 0,
            'details': []
        }
        
        for ext_property in external_properties:
            try:
                result = self._sync_single_property(ext_property)
                results['processed'] += 1
                
                if result['action'] == 'created':
                    results['created'] += 1
                elif result['action'] == 'updated':
                    results['updated'] += 1
                
                results['details'].append(result)
                
            except Exception as e:
                results['errors'] += 1
                error_detail = {
                    'external_id': ext_property.get('id'),
                    'error': str(e),
                    'action': 'error'
                }
                results['details'].append(error_detail)
                logger.error(f"Failed to sync property {ext_property.get('id')}: {e}")
        
        return results
    
    def _sync_single_property(self, ext_property: Dict[str, Any]) -> Dict[str, Any]:
        """Sync a single property"""
        external_id = ext_property['id']
        
        # Transform external data to OTC format
        otc_data = self._transform_property_data(ext_property)
        
        # Check if property already exists in OTC
        existing_property = self._find_existing_property(external_id)
        
        if existing_property:
            # Update existing property
            updated_property = self.otc_client.properties.update_property(
                existing_property['id'], 
                otc_data
            )
            
            return {
                'external_id': external_id,
                'otc_id': updated_property['id'],
                'action': 'updated',
                'address': updated_property['address']
            }
        else:
            # Create new property
            # Add external ID for future reference
            otc_data['external_id'] = external_id
            
            new_property = self.otc_client.properties.create_property(otc_data)
            
            return {
                'external_id': external_id,
                'otc_id': new_property['id'],
                'action': 'created',
                'address': new_property['address']
            }
    
    def _transform_property_data(self, ext_property: Dict[str, Any]) -> Dict[str, Any]:
        """Transform external property data to OTC format"""
        return {
            'address': ext_property['street_address'],
            'city': ext_property['city'],
            'state': ext_property['state'],
            'zip_code': ext_property['postal_code'],
            'listing_price': ext_property['price'],
            'bedrooms': ext_property.get('bed_count'),
            'bathrooms': ext_property.get('bath_count'),
            'square_feet': ext_property.get('sqft'),
            'property_type': ext_property.get('type', 'single_family'),
            'status': self._map_status(ext_property.get('status'))
        }
    
    def _map_status(self, external_status: str) -> str:
        """Map external status to OTC status"""
        status_mapping = {
            'for_sale': 'active',
            'pending': 'under_contract',
            'sold': 'sold',
            'off_market': 'inactive'
        }
        return status_mapping.get(external_status, 'active')
    
    def _find_existing_property(self, external_id: str):
        """Find existing property by external ID"""
        try:
            properties = self.otc_client.properties.list_properties(
                params={'external_id': external_id}
            )
            return properties[0] if properties else None
        except Exception:
            return None

# Usage
class ExternalDataSource:
    """Mock external data source"""
    def get_modified_properties(self, since):
        return [
            {
                'id': 'ext_123',
                'street_address': '123 Main St',
                'city': 'San Francisco',
                'state': 'CA',
                'postal_code': '94102',
                'price': 850000,
                'bed_count': 3,
                'bath_count': 2,
                'sqft': 1800,
                'type': 'single_family',
                'status': 'for_sale'
            }
        ]

# Initialize and run sync
external_source = ExternalDataSource()
sync_service = PropertySyncService(client, external_source)
results = sync_service.sync_properties()

print(f"Sync completed: {results['created']} created, {results['updated']} updated, {results['errors']} errors")
```

### Two-Way Sync with Conflict Resolution

```python
from datetime import datetime
from typing import Optional, Dict, Any
import hashlib

class TwoWayPropertySync:
    """Two-way synchronization with conflict resolution"""
    
    def __init__(self, otc_client, external_client):
        self.otc_client = otc_client
        self.external_client = external_client
        self.conflict_resolution = 'latest_wins'  # or 'manual', 'otc_wins', 'external_wins'
    
    def sync_bidirectional(self, since: datetime = None) -> Dict[str, Any]:
        """Perform bidirectional sync"""
        results = {
            'otc_to_external': {'created': 0, 'updated': 0, 'conflicts': 0},
            'external_to_otc': {'created': 0, 'updated': 0, 'conflicts': 0},
            'conflicts': []
        }
        
        # Get changes from both systems
        otc_changes = self._get_otc_changes(since)
        external_changes = self._get_external_changes(since)
        
        # Identify conflicts
        conflicts = self._identify_conflicts(otc_changes, external_changes)
        
        # Process non-conflicting changes
        for change in otc_changes:
            if change['id'] not in conflicts:
                result = self._push_to_external(change)
                if result['action'] == 'created':
                    results['otc_to_external']['created'] += 1
                elif result['action'] == 'updated':
                    results['otc_to_external']['updated'] += 1
        
        for change in external_changes:
            if change['id'] not in conflicts:
                result = self._push_to_otc(change)
                if result['action'] == 'created':
                    results['external_to_otc']['created'] += 1
                elif result['action'] == 'updated':
                    results['external_to_otc']['updated'] += 1
        
        # Handle conflicts
        for conflict_id in conflicts:
            conflict_result = self._resolve_conflict(
                conflicts[conflict_id]['otc'],
                conflicts[conflict_id]['external']
            )
            results['conflicts'].append(conflict_result)
        
        return results
    
    def _identify_conflicts(self, otc_changes, external_changes) -> Dict[str, Dict]:
        """Identify properties changed in both systems"""
        conflicts = {}
        
        otc_ids = {change['id'] for change in otc_changes}
        external_ids = {change['id'] for change in external_changes}
        
        conflict_ids = otc_ids.intersection(external_ids)
        
        for conflict_id in conflict_ids:
            otc_change = next(c for c in otc_changes if c['id'] == conflict_id)
            external_change = next(c for c in external_changes if c['id'] == conflict_id)
            
            conflicts[conflict_id] = {
                'otc': otc_change,
                'external': external_change
            }
        
        return conflicts
    
    def _resolve_conflict(self, otc_change, external_change) -> Dict[str, Any]:
        """Resolve conflict between two changes"""
        if self.conflict_resolution == 'latest_wins':
            if otc_change['modified_at'] > external_change['modified_at']:
                # OTC wins
                result = self._push_to_external(otc_change)
                result['resolution'] = 'otc_wins'
            else:
                # External wins
                result = self._push_to_otc(external_change)
                result['resolution'] = 'external_wins'
        
        elif self.conflict_resolution == 'otc_wins':
            result = self._push_to_external(otc_change)
            result['resolution'] = 'otc_wins'
        
        elif self.conflict_resolution == 'external_wins':
            result = self._push_to_otc(external_change)
            result['resolution'] = 'external_wins'
        
        else:  # manual resolution
            result = {
                'id': otc_change['id'],
                'action': 'conflict',
                'resolution': 'manual_required',
                'otc_data': otc_change,
                'external_data': external_change
            }
        
        return result
    
    def _get_otc_changes(self, since: datetime):
        """Get changes from OTC since given time"""
        # Implementation depends on OTC change tracking
        # This is a simplified example
        properties = self.otc_client.properties.list_properties(
            params={'modified_since': since.isoformat()} if since else {}
        )
        return [{'id': p['id'], 'data': p, 'modified_at': p['updated_at']} for p in properties]
    
    def _get_external_changes(self, since: datetime):
        """Get changes from external system since given time"""
        # Implementation depends on external system
        return self.external_client.get_changes(since)
    
    def _push_to_external(self, otc_change):
        """Push OTC change to external system"""
        # Transform and push data
        external_data = self._transform_otc_to_external(otc_change['data'])
        return self.external_client.update_property(otc_change['id'], external_data)
    
    def _push_to_otc(self, external_change):
        """Push external change to OTC"""
        # Transform and push data
        otc_data = self._transform_external_to_otc(external_change['data'])
        return self.otc_client.properties.update_property(external_change['id'], otc_data)
```

---

## Event-Driven Patterns

### Webhook Integration

```python
from flask import Flask, request, jsonify
import hmac
import hashlib
import json
from datetime import datetime

app = Flask(__name__)

class WebhookHandler:
    """Handle webhooks from Open To Close"""
    
    def __init__(self, webhook_secret: str):
        self.webhook_secret = webhook_secret
        self.handlers = {}
    
    def register_handler(self, event_type: str, handler_func):
        """Register a handler for specific event type"""
        self.handlers[event_type] = handler_func
    
    def verify_signature(self, payload: bytes, signature: str) -> bool:
        """Verify webhook signature"""
        expected_signature = hmac.new(
            self.webhook_secret.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(f"sha256={expected_signature}", signature)
    
    def process_webhook(self, payload: bytes, signature: str) -> Dict[str, Any]:
        """Process incoming webhook"""
        # Verify signature
        if not self.verify_signature(payload, signature):
            raise ValueError("Invalid webhook signature")
        
        # Parse payload
        data = json.loads(payload.decode())
        event_type = data.get('event_type')
        
        # Find and execute handler
        handler = self.handlers.get(event_type)
        if handler:
            return handler(data)
        else:
            return {'status': 'ignored', 'reason': f'No handler for {event_type}'}

# Initialize webhook handler
webhook_handler = WebhookHandler(os.getenv('WEBHOOK_SECRET'))

# Register event handlers
def handle_property_created(data):
    """Handle property creation events"""
    property_data = data['property']
    
    # Example: Send to CRM system
    crm_client.create_property(property_data)
    
    # Example: Trigger marketing workflow
    marketing_service.create_listing_campaign(property_data)
    
    return {'status': 'processed', 'actions': ['crm_sync', 'marketing_campaign']}

def handle_property_status_changed(data):
    """Handle property status change events"""
    property_data = data['property']
    old_status = data['previous_status']
    new_status = property_data['status']
    
    # Example: Update external systems
    if new_status == 'under_contract':
        # Start closing workflow
        closing_service.initiate_closing_process(property_data)
    elif new_status == 'sold':
        # Archive property and update reporting
        archive_service.archive_property(property_data)
        reporting_service.record_sale(property_data)
    
    return {'status': 'processed', 'old_status': old_status, 'new_status': new_status}

def handle_task_completed(data):
    """Handle task completion events"""
    task_data = data['task']
    property_id = task_data['property_id']
    
    # Example: Check if all closing tasks are complete
    if task_data['category'] == 'closing':
        closing_service.check_closing_readiness(property_id)
    
    return {'status': 'processed', 'task_id': task_data['id']}

# Register handlers
webhook_handler.register_handler('property.created', handle_property_created)
webhook_handler.register_handler('property.status_changed', handle_property_status_changed)
webhook_handler.register_handler('task.completed', handle_task_completed)

@app.route('/webhook/otc', methods=['POST'])
def webhook_endpoint():
    """Webhook endpoint for Open To Close events"""
    try:
        signature = request.headers.get('X-OTC-Signature')
        if not signature:
            return jsonify({'error': 'Missing signature'}), 400
        
        result = webhook_handler.process_webhook(request.data, signature)
        return jsonify(result)
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        # Log error
        app.logger.error(f"Webhook processing error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Message Queue Integration

```python
import json
import pika
from celery import Celery
from datetime import datetime

# Celery configuration for async processing
celery_app = Celery('otc_integration')
celery_app.config_from_object({
    'broker_url': 'redis://localhost:6379/0',
    'result_backend': 'redis://localhost:6379/0',
    'task_serializer': 'json',
    'accept_content': ['json'],
    'result_serializer': 'json',
    'timezone': 'UTC',
    'enable_utc': True,
})

class MessageQueueIntegration:
    """Integration using message queues for async processing"""
    
    def __init__(self, otc_client):
        self.otc_client = otc_client
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost')
        )
        self.channel = self.connection.channel()
        self._setup_queues()
    
    def _setup_queues(self):
        """Setup RabbitMQ queues"""
        queues = [
            'property_updates',
            'task_notifications',
            'document_processing',
            'email_notifications'
        ]
        
        for queue in queues:
            self.channel.queue_declare(queue=queue, durable=True)
    
    def publish_property_update(self, property_data):
        """Publish property update to queue"""
        message = {
            'event_type': 'property_updated',
            'property_id': property_data['id'],
            'data': property_data,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        self.channel.basic_publish(
            exchange='',
            routing_key='property_updates',
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2)  # Make message persistent
        )
    
    def start_consuming(self):
        """Start consuming messages from queues"""
        self.channel.basic_consume(
            queue='property_updates',
            on_message_callback=self._handle_property_update,
            auto_ack=False
        )
        
        self.channel.basic_consume(
            queue='task_notifications',
            on_message_callback=self._handle_task_notification,
            auto_ack=False
        )
        
        print("Starting message consumption...")
        self.channel.start_consuming()
    
    def _handle_property_update(self, ch, method, properties, body):
        """Handle property update messages"""
        try:
            message = json.loads(body)
            property_id = message['property_id']
            
            # Process the update asynchronously
            process_property_update.delay(property_id, message['data'])
            
            # Acknowledge message
            ch.basic_ack(delivery_tag=method.delivery_tag)
            
        except Exception as e:
            print(f"Error processing property update: {e}")
            # Reject and requeue message
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
    
    def _handle_task_notification(self, ch, method, properties, body):
        """Handle task notification messages"""
        try:
            message = json.loads(body)
            
            # Process the notification asynchronously
            process_task_notification.delay(message)
            
            ch.basic_ack(delivery_tag=method.delivery_tag)
            
        except Exception as e:
            print(f"Error processing task notification: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

# Celery tasks for async processing
@celery_app.task(bind=True, max_retries=3)
def process_property_update(self, property_id, property_data):
    """Process property update asynchronously"""
    try:
        # Update external CRM
        crm_client.update_property(property_id, property_data)
        
        # Update search index
        search_service.index_property(property_data)
        
        # Send notifications if needed
        if property_data.get('status') == 'sold':
            notification_service.send_sale_notification(property_data)
        
        return {'status': 'success', 'property_id': property_id}
        
    except Exception as e:
        # Retry with exponential backoff
        raise self.retry(exc=e, countdown=60 * (2 ** self.request.retries))

@celery_app.task
def process_task_notification(message):
    """Process task notification asynchronously"""
    task_data = message['task']
    
    # Send email notification
    if task_data['assignee']:
        email_service.send_task_notification(task_data)
    
    # Update project management system
    pm_system.update_task_status(task_data)
    
    return {'status': 'success', 'task_id': task_data['id']}

# Usage
mq_integration = MessageQueueIntegration(client)

# Start consuming in a separate process
# mq_integration.start_consuming()
```

---

## Caching and Performance Patterns

### Redis Caching Layer

```python
import redis
import json
import pickle
from datetime import datetime, timedelta
from typing import Optional, Any, Callable

class CachedOTCClient:
    """Open To Close client with Redis caching layer"""
    
    def __init__(self, otc_client, redis_client=None, default_ttl=300):
        self.otc_client = otc_client
        self.redis_client = redis_client or redis.Redis(host='localhost', port=6379, db=0)
        self.default_ttl = default_ttl
    
    def _cache_key(self, prefix: str, *args) -> str:
        """Generate cache key"""
        key_parts = [prefix] + [str(arg) for arg in args]
        return ':'.join(key_parts)
    
    def _get_cached(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            cached_data = self.redis_client.get(key)
            if cached_data:
                return pickle.loads(cached_data)
        except Exception:
            pass
        return None
    
    def _set_cache(self, key: str, value: Any, ttl: int = None) -> None:
        """Set value in cache"""
        try:
            ttl = ttl or self.default_ttl
            self.redis_client.setex(key, ttl, pickle.dumps(value))
        except Exception:
            pass
    
    def _invalidate_cache(self, pattern: str) -> None:
        """Invalidate cache entries matching pattern"""
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
        except Exception:
            pass
    
    def get_property(self, property_id: int, use_cache: bool = True) -> dict:
        """Get property with caching"""
        cache_key = self._cache_key('property', property_id)
        
        if use_cache:
            cached_property = self._get_cached(cache_key)
            if cached_property:
                return cached_property
        
        # Fetch from API
        property_data = self.otc_client.properties.retrieve_property(property_id)
        
        # Cache the result
        self._set_cache(cache_key, property_data, ttl=600)  # 10 minutes
        
        return property_data
    
    def list_properties(self, params: dict = None, use_cache: bool = True, ttl: int = 300) -> list:
        """List properties with caching"""
        # Create cache key from parameters
        cache_key = self._cache_key('properties_list', json.dumps(params or {}, sort_keys=True))
        
        if use_cache:
            cached_properties = self._get_cached(cache_key)
            if cached_properties:
                return cached_properties
        
        # Fetch from API
        properties = self.otc_client.properties.list_properties(params)
        
        # Cache the result
        self._set_cache(cache_key, properties, ttl=ttl)
        
        return properties
    
    def update_property(self, property_id: int, data: dict) -> dict:
        """Update property and invalidate cache"""
        # Update via API
        updated_property = self.otc_client.properties.update_property(property_id, data)
        
        # Invalidate related cache entries
        self._invalidate_cache(f'property:{property_id}')
        self._invalidate_cache('properties_list:*')
        
        # Cache the updated property
        cache_key = self._cache_key('property', property_id)
        self._set_cache(cache_key, updated_property, ttl=600)
        
        return updated_property
    
    def get_property_with_details(self, property_id: int, use_cache: bool = True) -> dict:
        """Get property with all related data (notes, tasks, documents)"""
        cache_key = self._cache_key('property_details', property_id)
        
        if use_cache:
            cached_details = self._get_cached(cache_key)
            if cached_details:
                return cached_details
        
        # Fetch all data
        property_data = self.get_property(property_id, use_cache=False)
        notes = self.otc_client.property_notes.list_property_notes(property_id)
        tasks = self.otc_client.property_tasks.list_property_tasks(property_id)
        documents = self.otc_client.property_documents.list_property_documents(property_id)
        
        # Combine all data
        detailed_property = {
            'property': property_data,
            'notes': notes,
            'tasks': tasks,
            'documents': documents,
            'cached_at': datetime.utcnow().isoformat()
        }
        
        # Cache for 5 minutes (shorter TTL for detailed data)
        self._set_cache(cache_key, detailed_property, ttl=300)
        
        return detailed_property

# Usage with cache warming
class CacheWarmer:
    """Service to warm up cache with frequently accessed data"""
    
    def __init__(self, cached_client):
        self.cached_client = cached_client
    
    def warm_popular_properties(self):
        """Warm cache with popular properties"""
        # Get active properties
        active_properties = self.cached_client.list_properties(
            params={'status': 'active'}, 
            use_cache=False
        )
        
        # Cache individual properties
        for prop in active_properties[:50]:  # Top 50 properties
            self.cached_client.get_property(prop['id'], use_cache=False)
            
        print(f"Warmed cache for {len(active_properties[:50])} properties")
    
    def warm_team_data(self):
        """Warm cache with team-related data"""
        teams = self.cached_client.otc_client.teams.list_teams()
        for team in teams:
            # Cache team data
            team_key = f"team:{team['id']}"
            self.cached_client._set_cache(team_key, team, ttl=3600)  # 1 hour
        
        print(f"Warmed cache for {len(teams)} teams")

# Initialize cached client
cached_client = CachedOTCClient(client)
cache_warmer = CacheWarmer(cached_client)

# Warm cache on startup
cache_warmer.warm_popular_properties()
cache_warmer.warm_team_data()
```

### Database Caching with SQLAlchemy

```python
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import json

Base = declarative_base()

class PropertyCache(Base):
    __tablename__ = 'property_cache'
    
    id = Column(Integer, primary_key=True)
    property_id = Column(Integer, unique=True, index=True)
    data = Column(JSON)
    cached_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)

class PropertyListCache(Base):
    __tablename__ = 'property_list_cache'
    
    id = Column(Integer, primary_key=True)
    cache_key = Column(String(255), unique=True, index=True)
    data = Column(JSON)
    cached_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)

class DatabaseCachedClient:
    """OTC client with database caching"""
    
    def __init__(self, otc_client, db_url="sqlite:///otc_cache.db"):
        self.otc_client = otc_client
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def get_property(self, property_id: int, use_cache: bool = True, ttl_minutes: int = 10) -> dict:
        """Get property with database caching"""
        if use_cache:
            # Check cache
            cached = self.session.query(PropertyCache).filter(
                PropertyCache.property_id == property_id,
                PropertyCache.expires_at > datetime.utcnow()
            ).first()
            
            if cached:
                return cached.data
        
        # Fetch from API
        property_data = self.otc_client.properties.retrieve_property(property_id)
        
        # Update cache
        expires_at = datetime.utcnow() + timedelta(minutes=ttl_minutes)
        
        # Upsert cache entry
        cached = self.session.query(PropertyCache).filter(
            PropertyCache.property_id == property_id
        ).first()
        
        if cached:
            cached.data = property_data
            cached.cached_at = datetime.utcnow()
            cached.expires_at = expires_at
        else:
            cached = PropertyCache(
                property_id=property_id,
                data=property_data,
                expires_at=expires_at
            )
            self.session.add(cached)
        
        self.session.commit()
        return property_data
    
    def cleanup_expired_cache(self):
        """Remove expired cache entries"""
        expired_properties = self.session.query(PropertyCache).filter(
            PropertyCache.expires_at < datetime.utcnow()
        ).delete()
        
        expired_lists = self.session.query(PropertyListCache).filter(
            PropertyListCache.expires_at < datetime.utcnow()
        ).delete()
        
        self.session.commit()
        
        return {
            'expired_properties': expired_properties,
            'expired_lists': expired_lists
        }
```

---

## Monitoring and Observability

### API Monitoring with Metrics

```python
import time
import logging
from functools import wraps
from typing import Dict, Any
from prometheus_client import Counter, Histogram, Gauge, start_http_server

# Prometheus metrics
api_requests_total = Counter(
    'otc_api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status']
)

api_request_duration = Histogram(
    'otc_api_request_duration_seconds',
    'API request duration',
    ['method', 'endpoint']
)

api_errors_total = Counter(
    'otc_api_errors_total',
    'Total API errors',
    ['method', 'endpoint', 'error_type']
)

cache_hits_total = Counter(
    'otc_cache_hits_total',
    'Total cache hits',
    ['cache_type']
)

cache_misses_total = Counter(
    'otc_cache_misses_total',
    'Total cache misses',
    ['cache_type']
)

class MonitoredOTCClient:
    """OTC client with monitoring and metrics"""
    
    def __init__(self, otc_client):
        self.otc_client = otc_client
        self.logger = logging.getLogger(__name__)
    
    def _monitor_api_call(self, method: str, endpoint: str):
        """Decorator to monitor API calls"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                
                try:
                    result = func(*args, **kwargs)
                    
                    # Record success metrics
                    duration = time.time() - start_time
                    api_requests_total.labels(
                        method=method, 
                        endpoint=endpoint, 
                        status='success'
                    ).inc()
                    api_request_duration.labels(
                        method=method, 
                        endpoint=endpoint
                    ).observe(duration)
                    
                    self.logger.info(
                        f"API call successful: {method} {endpoint} ({duration:.3f}s)"
                    )
                    
                    return result
                    
                except Exception as e:
                    # Record error metrics
                    duration = time.time() - start_time
                    error_type = type(e).__name__
                    
                    api_requests_total.labels(
                        method=method, 
                        endpoint=endpoint, 
                        status='error'
                    ).inc()
                    api_errors_total.labels(
                        method=method, 
                        endpoint=endpoint, 
                        error_type=error_type
                    ).inc()
                    
                    self.logger.error(
                        f"API call failed: {method} {endpoint} ({duration:.3f}s) - {error_type}: {e}"
                    )
                    
                    raise
            
            return wrapper
        return decorator
    
    @_monitor_api_call('GET', '/properties/{id}')
    def get_property(self, property_id: int) -> dict:
        """Get property with monitoring"""
        return self.otc_client.properties.retrieve_property(property_id)
    
    @_monitor_api_call('GET', '/properties')
    def list_properties(self, params: dict = None) -> list:
        """List properties with monitoring"""
        return self.otc_client.properties.list_properties(params)
    
    @_monitor_api_call('POST', '/properties')
    def create_property(self, data: dict) -> dict:
        """Create property with monitoring"""
        return self.otc_client.properties.create_property(data)
    
    @_monitor_api_call('PUT', '/properties/{id}')
    def update_property(self, property_id: int, data: dict) -> dict:
        """Update property with monitoring"""
        return self.otc_client.properties.update_property(property_id, data)

# Health check endpoint
from flask import Flask, jsonify

monitoring_app = Flask(__name__)

@monitoring_app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        # Test API connectivity
        client = OpenToCloseAPI()
        # Make a lightweight API call
        client.properties.list_properties(params={'limit': 1})
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'api_connectivity': 'ok'
        })
    
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'timestamp': datetime.utcnow().isoformat(),
            'api_connectivity': 'failed',
            'error': str(e)
        }), 503

@monitoring_app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint"""
    from prometheus_client import generate_latest
    return generate_latest()

# Start monitoring server
if __name__ == '__main__':
    # Start Prometheus metrics server
    start_http_server(8000)
    
    # Start health check server
    monitoring_app.run(host='0.0.0.0', port=8080)
```

This comprehensive integration patterns guide covers the most common and effective ways to integrate with the Open To Close API, from basic authentication to advanced monitoring and caching strategies. Each pattern is designed to be production-ready and scalable.

---

## Related Resources

- [Examples](examples.md) - Practical usage examples
- [Best Practices](best-practices.md) - Development best practices
- [Error Handling Guide](error-handling.md) - Comprehensive error handling
- [API Reference](../api/index.md) - Complete API documentation