# Client Storage Integration Guide

This document explains how to integrate your client card storage system with the Enhanced Agent Coordinator.

## Overview

The Agent Coordinator now includes intelligent client context integration that:
- Securely retrieves client brand guidelines, audience data, and compliance requirements
- Filters and optimizes data exposure to different agent types
- Maintains privacy and access control
- Supports multiple storage backends (JSON files, databases, APIs, etc.)

## Current State

✅ **Ready for Deployment**: The coordinator is deployed with **placeholder implementations** that:
- Work out of the box with mock data for testing
- Support multiple storage backend types via configuration
- Include comprehensive logging and error handling
- Provide clear integration points for your actual storage system

## Supported Storage Types

### 1. JSON Files (Current Default)
```bash
CLIENT_STORAGE_TYPE=json_files
CLIENT_DATA_DIRECTORY=/app/data/clients
CLIENT_FILE_PATTERN={client_id}.json
```

**Status**: ✅ Mock implementation ready  
**Use Case**: Development, testing, small-scale deployments

### 2. Database Storage
```bash
CLIENT_STORAGE_TYPE=database
CLIENT_DB_CONNECTION_STRING=postgresql://user:pass@host:5432/db
CLIENT_DB_TABLE=client_cards
CLIENT_DB_TIMEOUT=30
```

**Status**: 🔄 Placeholder ready for implementation  
**Use Case**: Traditional relational data storage

### 3. Graph Database (Neo4j)
```bash
CLIENT_STORAGE_TYPE=graph_db
CLIENT_GRAPH_URI=bolt://localhost:7687
CLIENT_GRAPH_USERNAME=neo4j
CLIENT_GRAPH_PASSWORD=password
CLIENT_GRAPH_DATABASE=client_cards
```

**Status**: 🔄 Placeholder ready for implementation  
**Use Case**: Complex relationship modeling between clients, users, and data

### 4. API Endpoint
```bash
CLIENT_STORAGE_TYPE=api_endpoint
CLIENT_API_BASE_URL=https://your-client-api.com/v1
CLIENT_API_KEY=your-api-key
CLIENT_API_TIMEOUT=30
```

**Status**: 🔄 Placeholder ready for implementation  
**Use Case**: Existing microservice architecture

### 5. Google Firestore
```bash
CLIENT_STORAGE_TYPE=firestore
GOOGLE_CLOUD_PROJECT=your-project-id
CLIENT_FIRESTORE_COLLECTION=client_cards
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

**Status**: 🔄 Placeholder ready for implementation  
**Use Case**: Google Cloud native integration

## Integration Steps

### Phase 1: Deploy with Mock Data (Current)
1. **Deploy immediately**: Use the deployment script to get the coordinator running
2. **Test client context**: Use mock data to verify client-aware coordination works
3. **Validate agent integration**: Ensure your agents can consume client context

### Phase 2: Connect Real Storage
1. **Choose your storage type**: Update `CLIENT_STORAGE_TYPE` environment variable
2. **Implement storage methods**: Replace placeholder methods in `src/client_storage.py`
3. **Test integration**: Verify real client data flows through the system
4. **Deploy updates**: Redeploy with your storage integration

## Implementation Guide

### Storage Service Methods to Implement

```python
# In src/client_storage.py

async def _get_from_your_storage(self, client_id: str) -> Optional[Dict[str, Any]]:
    """Replace with your actual storage implementation"""
    # Your implementation here
    # Return client data dictionary
    
async def _list_from_your_storage(self, user_id: str = None) -> List[str]:
    """Replace with your actual user access logic"""
    # Your implementation here
    # Return list of client IDs user can access
```

### Expected Client Data Structure

```json
{
  "client_id": "promise_money",
  "brand_guidelines": {
    "tone": "professional",
    "voice": "authoritative", 
    "avoid_words": ["cheap", "discount"],
    "messaging_pillars": ["quality", "reliability", "expertise"]
  },
  "target_audience": {
    "primary": "SME owners",
    "age_range": "35-55",
    "interests": ["business growth", "efficiency", "digital transformation"]
  },
  "compliance_requirements": ["FCA compliant", "GDPR compliant"],
  "last_updated": "2024-01-15T10:30:00Z"
}
```

## Testing the Integration

### 1. Test Mock Implementation
```bash
# Deploy and test with mock data
./deploy.sh

# Test client listing (requires auth token)
curl -H "Authorization: Bearer $TOKEN" \
  https://agent-coordinator-awlsoz4tpa-uc.a.run.app/clients

# Test client context retrieval
curl -H "Authorization: Bearer $TOKEN" \
  https://agent-coordinator-awlsoz4tpa-uc.a.run.app/clients/promise_money/context
```

### 2. Test Client-Aware Coordination
```bash
# Make a client-aware coordination request
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Create SEO strategy for bridging finance FAQ pages",
    "priority": "high", 
    "context": "business",
    "client_id": "promise_money",
    "use_client_context": true
  }' \
  https://agent-coordinator-awlsoz4tpa-uc.a.run.app/coordinate/client
```

## Security and Privacy

### Data Filtering
The coordinator automatically filters client data before sending to agents:
- **Content Research Agent**: Gets full brand voice, audience, and compliance data
- **Technical SEO Agent**: Gets limited brand tone and compliance requirements only
- **Other Agents**: Get minimal client context

### Access Control
- Users can only access clients they're authorized for
- Client access validation happens on every request
- Failed access attempts are logged for security monitoring

### Data Privacy
- Client data is never stored in logs (when configured properly)
- Sensitive fields can be filtered out per agent type
- All client data access is audited

## Performance Considerations

### Caching Strategy
Consider implementing caching for:
- Client data retrieval (cache for 5-15 minutes)
- User access lists (cache for 1-5 minutes)
- Agent-specific filtered contexts

### Example Redis Caching Implementation
```python
# Add to your storage implementation
import redis
import json

async def _get_from_database_with_cache(self, client_id: str):
    cache_key = f"client:{client_id}"
    
    # Try cache first
    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)
    
    # Fetch from database
    data = await self._fetch_from_database(client_id)
    
    # Cache for 10 minutes
    if data:
        await redis.setex(cache_key, 600, json.dumps(data))
    
    return data
```

## Next Steps

1. **Deploy Now**: Use the deployment script to get the enhanced coordinator live
2. **Test Client Context**: Validate client-aware coordination with mock data
3. **Plan Storage Integration**: Choose your storage backend and plan implementation
4. **Implement Storage**: Replace placeholder methods with your actual storage logic
5. **Add Caching**: Implement caching strategy for better performance
6. **Monitor Usage**: Set up logging and monitoring for client data access

## Support

The current implementation provides:
- ✅ Complete client context integration framework
- ✅ Multiple storage backend support 
- ✅ Security and access control
- ✅ Agent-specific data filtering
- ✅ Comprehensive logging and error handling
- ✅ Mock data for immediate testing

All placeholder implementations include detailed TODOs and examples to guide your integration.

---

**Ready to deploy?** Run `./deploy.sh` to get your enhanced coordinator with client context support live on Google Cloud Run!
