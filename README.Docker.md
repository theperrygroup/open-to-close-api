# Docker Setup for Open To Close API

This document explains how to run the Open To Close API library as a background agent using Docker.

## 🚀 Quick Start

### 1. Environment Setup

Copy the example environment file and configure your API key:

```bash
cp env.example .env
```

Edit `.env` and set your API key:
```bash
OPEN_TO_CLOSE_API_KEY=your_api_key_here
```

### 2. Build and Run

**Production Mode:**
```bash
# Build and run the main agent
docker-compose up --build otc-agent

# Run in background
docker-compose up -d otc-agent
```

**Development Mode:**
```bash
# Run with hot reloading for development
docker-compose --profile dev up otc-agent-dev
```

**With Monitoring:**
```bash
# Run main agent with monitoring
docker-compose --profile monitoring up -d
```

## 📁 Project Structure

```
├── Dockerfile                 # Main container definition
├── docker-compose.yml         # Orchestration configuration
├── .dockerignore              # Files to exclude from build
├── env.example                # Environment variables template
├── agents/                    # Background agent scripts
│   ├── main_agent.py          # Main background agent
│   └── monitor_agent.py       # Monitoring agent
└── logs/                      # Container logs (auto-created)
```

## 🛠️ Available Services

### Main Agent (`otc-agent`)
- **Purpose**: Continuous background processing
- **Features**: 
  - Property synchronization
  - Contact monitoring
  - Task automation
  - Error handling and retry logic
- **Logs**: `/app/logs/agent_YYYYMMDD.log`

### Development Agent (`otc-agent-dev`)
- **Purpose**: Development with hot reloading
- **Features**: 
  - Source code mounted as volume
  - Debug logging enabled
  - Immediate code changes reflection
- **Usage**: `docker-compose --profile dev up otc-agent-dev`

### Monitor Agent (`otc-monitor`)
- **Purpose**: Health monitoring and metrics
- **Features**:
  - API health checks
  - Performance metrics
  - Log analysis
  - Alert generation
- **Usage**: `docker-compose --profile monitoring up otc-monitor`

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPEN_TO_CLOSE_API_KEY` | Your API key | - | ✅ |
| `LOG_LEVEL` | Logging level | `INFO` | ❌ |
| `ENVIRONMENT` | Environment name | `development` | ❌ |
| `AGENT_INTERVAL_SECONDS` | Agent cycle interval | `60` | ❌ |
| `AGENT_MAX_RETRIES` | Max retry attempts | `3` | ❌ |
| `HEALTH_CHECK_INTERVAL` | Monitor check interval | `30` | ❌ |
| `ENABLE_METRICS` | Save metrics to files | `false` | ❌ |

### Volume Mounts

- `./agents:/app/agents:ro` - Agent scripts (read-only in production)
- `./logs:/app/logs` - Log files
- `.:/app` - Full source code (development only)

## 🔍 Monitoring and Logs

### View Logs
```bash
# Main agent logs
docker-compose logs -f otc-agent

# Monitor agent logs
docker-compose logs -f otc-monitor

# All services
docker-compose logs -f
```

### Log Files
Logs are automatically mounted to `./logs/` directory:
- `agent_YYYYMMDD.log` - Main agent logs
- `monitor_YYYYMMDD.log` - Monitor agent logs
- `metrics_YYYYMMDD.json` - Performance metrics (if enabled)

### Health Checks
```bash
# Check container health
docker ps

# Manual health check
docker exec otc-agent python -c "import open_to_close; print('OK')"
```

## 🧪 Development Workflow

### 1. Local Development
```bash
# Start development environment
docker-compose --profile dev up

# Edit agents/main_agent.py - changes reflect immediately
# Logs show in real-time
```

### 2. Testing Changes
```bash
# Test your agent script directly
docker-compose exec otc-agent-dev python /app/agents/main_agent.py

# Run specific functions
docker-compose exec otc-agent-dev python -c "
from agents.main_agent import OpenToCloseAgent
import asyncio
async def test():
    agent = OpenToCloseAgent()
    await agent.health_check()
asyncio.run(test())
"
```

### 3. Custom Agent Scripts
Create new scripts in the `agents/` directory:

```python
# agents/my_custom_agent.py
from open_to_close import OpenToCloseAPI
import os

def my_custom_task():
    client = OpenToCloseAPI(api_key=os.getenv("OPEN_TO_CLOSE_API_KEY"))
    # Your custom logic here
    
if __name__ == "__main__":
    my_custom_task()
```

Run your custom agent:
```bash
docker-compose exec otc-agent python /app/agents/my_custom_agent.py
```

## 🚀 Production Deployment

### 1. Build Production Image
```bash
docker build -t otc-agent:latest .
```

### 2. Run with Docker Compose
```bash
# Production deployment
docker-compose -f docker-compose.yml up -d otc-agent

# With monitoring
docker-compose -f docker-compose.yml --profile monitoring up -d
```

### 3. Docker Run (Alternative)
```bash
docker run -d \
  --name otc-agent \
  --env-file .env \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/agents:/app/agents:ro \
  --restart unless-stopped \
  otc-agent:latest \
  python /app/agents/main_agent.py
```

## 🔧 Customization

### Custom Docker Commands

Add to `docker-compose.yml`:
```yaml
services:
  my-custom-agent:
    build: .
    environment:
      - OPEN_TO_CLOSE_API_KEY=${OPEN_TO_CLOSE_API_KEY}
    volumes:
      - ./agents:/app/agents:ro
      - ./logs:/app/logs
    command: ["python", "/app/agents/my_custom_agent.py"]
```

### Multiple Agent Instances
```yaml
services:
  agent-properties:
    build: .
    environment:
      - OPEN_TO_CLOSE_API_KEY=${OPEN_TO_CLOSE_API_KEY}
      - AGENT_TYPE=properties
    command: ["python", "/app/agents/properties_agent.py"]
  
  agent-contacts:
    build: .
    environment:
      - OPEN_TO_CLOSE_API_KEY=${OPEN_TO_CLOSE_API_KEY}
      - AGENT_TYPE=contacts
    command: ["python", "/app/agents/contacts_agent.py"]
```

## 🐛 Troubleshooting

### Common Issues

**1. Permission Errors**
```bash
# Fix log directory permissions
chmod 755 logs/
sudo chown -R $USER:$USER logs/
```

**2. API Key Not Found**
```bash
# Verify environment file
cat .env | grep OPEN_TO_CLOSE_API_KEY

# Check container environment
docker-compose exec otc-agent printenv | grep OPEN_TO_CLOSE
```

**3. Container Won't Start**
```bash
# Check build logs
docker-compose build --no-cache

# Check container logs
docker-compose logs otc-agent
```

**4. Import Errors**
```bash
# Verify package installation
docker-compose exec otc-agent pip list | grep open-to-close

# Reinstall if needed
docker-compose exec otc-agent pip install -e .
```

### Debug Mode
```bash
# Run with debug logging
LOG_LEVEL=DEBUG docker-compose up otc-agent

# Interactive debugging
docker-compose exec otc-agent bash
python -c "from open_to_close import OpenToCloseAPI; print('Import successful')"
```

## 📊 Metrics and Monitoring

### Enable Metrics Collection
```bash
# Set in .env
ENABLE_METRICS=true

# Restart services
docker-compose restart
```

### View Metrics
```bash
# Check metrics file
cat logs/metrics_$(date +%Y%m%d).json | jq .

# Monitor API health
docker-compose exec otc-monitor python -c "
import asyncio
from agents.monitor_agent import MonitorAgent
async def check():
    monitor = MonitorAgent()
    health = await monitor.check_api_health()
    print(health)
asyncio.run(check())
"
```

## 🔗 Integration with Cursor

### Running in Cursor Terminal
```bash
# From Cursor terminal, navigate to project directory
cd /path/to/open_to_close

# Start background agent
docker-compose up -d otc-agent

# View logs in Cursor
docker-compose logs -f otc-agent
```

### Cursor Workspace Integration
Add to your `.cursor/` workspace settings:
```json
{
  "docker.compose.files": ["docker-compose.yml"],
  "docker.compose.projectName": "open-to-close"
}
```

This allows Cursor to recognize and manage your Docker containers directly from the IDE.

## 🆘 Support

- **Documentation**: [Full API Documentation](https://theperrygroup.github.io/open-to-close/)
- **Issues**: [GitHub Issues](https://github.com/theperrygroup/open-to-close/issues)
- **Docker Hub**: Coming soon
- **Examples**: Check `agents/` directory for sample implementations 