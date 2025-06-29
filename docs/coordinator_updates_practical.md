# Practical Coordinator Agent Updates for Client Card Integration

## Current Coordinator Capabilities

Looking at the existing coordinator structure:
- ✅ FastAPI app with request processing
- ✅ Agent routing and load balancing  
- ✅ JWT authentication with user context
- ✅ Health monitoring and metrics
- ✅ Basic request/response models

## Specific Updates Needed

### 1. Add Client Context to Existing Models

**Update `models.py`** - Add these models to the existing file:

```python
# Add to existing models.py

class ClientCardType(str, Enum):
    BRAND_GUIDELINES = "brand_guidelines"
    TARGET_AUDIENCE = "target_audience"
    CLIENT_PROFILE = "client_profile"
    CONTENT_BRIEF = "content_brief"

class CoordinationRequestWithClient(CoordinationRequest):
    """Extended coordination request with client context"""
    client_id: Optional[str] = None
    use_client_context: bool = False

class ClientContext(BaseModel):
    """Simplified client context for agents"""
    client_id: str
    brand_voice: Optional[Dict[str, Any]] = None
    target_audience: Optional[Dict[str, Any]] = None
    compliance_notes: Optional[List[str]] = None
    
class CoordinationResponseWithClient(CoordinationResponse):
    """Extended response with client context info"""
    client_context_used: bool = False
```

### 2. Update Coordinator Class - Minimal Changes

**Update `coordinator.py`** - Add client context methods:

```python
# Add these methods to existing AgentCoordinator class

class AgentCoordinator:
    # ... existing __init__ and methods ...
    
    async def process_request_with_client(
        self, 
        request: CoordinationRequestWithClient, 
        user: User
    ) -> CoordinationResponseWithClient:
        """Enhanced request processing with optional client context"""
        
        # Get client context if requested
        client_context = None
        if request.use_client_context and request.client_id:
            client_context = await self._get_client_context(request.client_id, user)
        
        # Use existing processing with enhanced payload
        request_id = str(uuid.uuid4())
        routing_decision = self._route_request(request)
        
        # Enhance agent responses with client context
        agent_responses = await self._gather_agent_responses_with_context(
            routing_decision, 
            client_context
        )
        
        synthesized_response = self._synthesize_responses(agent_responses)
        
        return CoordinationResponseWithClient(
            request_id=request_id,
            routing_decision=routing_decision,
            agent_responses=agent_responses,
            synthesized_response=synthesized_response,
            total_processing_time=random.uniform(0.1, 3.0),
            quality_score=random.uniform(0.7, 1.0),
            client_context_used=client_context is not None
        )
    
    async def _get_client_context(self, client_id: str, user: User) -> Optional[ClientContext]:
        """Retrieve client context with basic filtering"""
        
        # Validate user has access to this client
        if not await self._validate_client_access(user, client_id):
            return None
        
        # Get client data (placeholder - would integrate with your client card system)
        client_data = await self._fetch_client_data(client_id)
        
        if not client_data:
            return None
        
        # Create filtered context
        return ClientContext(
            client_id=client_id,
            brand_voice=self._filter_brand_data(client_data.get("brand_guidelines")),
            target_audience=self._filter_audience_data(client_data.get("target_audience")),
            compliance_notes=client_data.get("compliance_requirements", [])
        )
    
    async def _gather_agent_responses_with_context(
        self, 
        routing_decision: Dict[str, Any], 
        client_context: Optional[ClientContext]
    ) -> List[AgentResponse]:
        """Enhanced agent execution with client context"""
        
        responses = []
        for agent in routing_decision["selected_agents"]:
            
            # Prepare agent-specific context
            agent_context = self._prepare_agent_context(agent, client_context)
            
            # Simulate agent call with context (replace with actual HTTP calls)
            response = AgentResponse(
                agent_id=agent["type"].value,
                agent_type=agent["type"],
                response=f"Response with context: {agent_context}",
                confidence=0.9,
                processing_time=random.uniform(0.1, 1.0),
                metadata={"client_context_used": client_context is not None}
            )
            responses.append(response)
        
        return responses
    
    def _prepare_agent_context(
        self, 
        agent: Dict[str, Any], 
        client_context: Optional[ClientContext]
    ) -> Dict[str, Any]:
        """Prepare filtered context for specific agent"""
        
        if not client_context:
            return {}
        
        agent_type = agent["type"]
        
        # Agent-specific filtering rules
        if agent_type == AgentType.CONTENT_RESEARCH:
            return {
                "brand_voice": client_context.brand_voice,
                "target_audience": client_context.target_audience,
                "compliance_notes": client_context.compliance_notes
            }
        elif agent_type == AgentType.TECHNICAL_SEO:
            return {
                "brand_voice": client_context.brand_voice.get("tone") if client_context.brand_voice else None,
                "compliance_notes": client_context.compliance_notes
            }
        else:
            return {"client_id": client_context.client_id}
    
    # Helper methods (implement based on your client card system)
    async def _validate_client_access(self, user: User, client_id: str) -> bool:
        """Validate user can access this client's data"""
        # Implement your access control logic
        return True
    
    async def _fetch_client_data(self, client_id: str) -> Optional[Dict[str, Any]]:
        """Fetch client data from your card system"""
        # This would integrate with your actual client card storage
        # For now, return mock data
        return {
            "brand_guidelines": {
                "tone": "professional",
                "voice": "authoritative",
                "avoid_words": ["cheap", "discount"]
            },
            "target_audience": {
                "primary": "SME owners",
                "age_range": "35-55",
                "interests": ["business growth", "efficiency"]
            },
            "compliance_requirements": ["FCA compliant", "GDPR compliant"]
        }
    
    def _filter_brand_data(self, brand_data: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Filter brand data for agent consumption"""
        if not brand_data:
            return None
        
        return {
            "tone": brand_data.get("tone"),
            "voice": brand_data.get("voice"),
            "restrictions": brand_data.get("avoid_words", [])
        }
    
    def _filter_audience_data(self, audience_data: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Filter audience data for agent consumption"""
        if not audience_data:
            return None
        
        return {
            "primary_audience": audience_data.get("primary"),
            "demographics": {
                "age_range": audience_data.get("age_range"),
                "interests": audience_data.get("interests", [])
            }
        }
```

### 3. Add New Endpoint to Main App

**Update `main.py`** - Add client-aware endpoint:

```python
# Add to existing main.py

@app.post("/coordinate/client", response_model=CoordinationResponseWithClient)
async def coordinate_request_with_client(
    request: CoordinationRequestWithClient,
    current_user: User = Depends(get_current_user)
):
    """
    Client-aware coordination endpoint
    Processes requests with optional client context integration
    """
    try:
        start_time = time.time()
        
        logger.info(f"Client-aware coordination request from {current_user.email} for client {request.client_id}")
        
        # Process with client context
        response = await coordinator.process_request_with_client(request, current_user)
        
        # Check SLA compliance
        processing_time = time.time() - start_time
        if processing_time > 2.0:
            logger.warning(f"SLA violation: Client request took {processing_time:.2f}s")
        
        return response
        
    except Exception as e:
        logger.error(f"Client coordination error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Client coordination failed: {str(e)}")

# Optional: Add client context validation endpoint
@app.get("/clients/{client_id}/context")
async def get_client_context_preview(
    client_id: str,
    current_user: User = Depends(get_current_user)
):
    """Preview what client context would be available"""
    context = await coordinator._get_client_context(client_id, current_user)
    if not context:
        raise HTTPException(status_code=404, detail="Client not found or access denied")
    
    return {
        "client_id": context.client_id,
        "has_brand_voice": context.brand_voice is not None,
        "has_target_audience": context.target_audience is not None,
        "compliance_requirements_count": len(context.compliance_notes or [])
    }
```

### 4. Agent Integration Points

**For existing agents to receive client context:**

```python
# Example: How agents would receive enhanced payloads

# Before (current):
{
    "query": "Write a blog post about AI",
    "context": {"priority": "high"}
}

# After (with client context):
{
    "query": "Write a blog post about AI", 
    "context": {"priority": "high"},
    "client_context": {
        "brand_voice": {
            "tone": "professional",
            "voice": "authoritative", 
            "restrictions": ["cheap", "discount"]
        },
        "target_audience": {
            "primary_audience": "SME owners",
            "demographics": {
                "age_range": "35-55",
                "interests": ["business growth", "efficiency"]
            }
        },
        "compliance_notes": ["FCA compliant", "GDPR compliant"]
    }
}
```

## Implementation Steps

### Phase 1: Basic Integration (Week 1)
1. ✅ Add new models to `models.py`
2. ✅ Add client context methods to `coordinator.py`
3. ✅ Add new endpoint to `main.py`
4. ✅ Test with mock client data

### Phase 2: Real Integration (Week 2)
1. 🔄 Replace `_fetch_client_data()` with actual client card system calls
2. 🔄 Implement proper access control in `_validate_client_access()`
3. 🔄 Add caching for client contexts
4. 🔄 Update agents to handle client context

### Phase 3: Enhancement (Week 3)
1. 🚀 Add intelligent filtering based on agent type
2. 🚀 Implement context performance tracking
3. 🚀 Add client context audit logging
4. 🚀 Performance optimization

## Benefits of This Approach

### ✅ **Minimal Disruption**
- Keeps existing coordinator functionality intact
- Adds new capabilities without breaking changes
- Agents can gradually adopt client context

### ✅ **Practical Implementation**
- Uses existing authentication and routing
- Builds on current FastAPI structure
- Simple integration points for client card system

### ✅ **Immediate Value**
- Agents get richer context for better responses
- Client data flows intelligently to appropriate agents
- Foundation for more sophisticated features

## Next Steps

1. **Test the new endpoint** with mock data
2. **Integrate with your client card storage** system
3. **Update one agent** to use client context
4. **Expand to other agents** progressively
5. **Add performance monitoring** for client context usage

This approach gives you client card integration with minimal risk and maximum compatibility with your existing coordinator.
