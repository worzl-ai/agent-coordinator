#!/bin/bash
# Enhanced Agent Coordinator Deployment using Cloud Build

set -e

# Configuration
PROJECT_ID="worz-acoo-001"
SERVICE_NAME="agent-coordinator"
REGION="us-central1"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"
MEMORY="2Gi"
CPU="2"
MAX_INSTANCES="10"
CONCURRENCY="100"

echo "🚀 Deploying Enhanced Agent Coordinator with Client Context Support using Cloud Build..."

# Check if logged into gcloud
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ Please login to gcloud first: gcloud auth login"
    exit 1
fi

# Set project
echo "📋 Setting project to $PROJECT_ID..."
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "🔧 Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build using Cloud Build
echo "🔨 Building image using Cloud Build..."
gcloud builds submit --tag $IMAGE_NAME:latest .

# Generate JWT secret
JWT_SECRET=$(openssl rand -base64 32)

# Deploy to Cloud Run
echo "🚢 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME:latest \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --memory $MEMORY \
    --cpu $CPU \
    --max-instances $MAX_INSTANCES \
    --concurrency $CONCURRENCY \
    --port 8080 \
    --set-env-vars "ENVIRONMENT=production,PORT=8080,LOG_LEVEL=INFO,CLIENT_STORAGE_TYPE=json_files,CLIENT_DATA_DIRECTORY=/app/data/clients,CLIENT_FILE_PATTERN={client_id}.json,JWT_SECRET_KEY=${JWT_SECRET},JWT_ALGORITHM=HS256,JWT_EXPIRY_HOURS=24,CONTENT_RESEARCH_AGENT_URL=https://content-research-agent-awlsoz4tpa-uc.a.run.app,TECHNICAL_SEO_AGENT_URL=https://technical-seo-agent-awlsoz4tpa-uc.a.run.app,PROJECT_PLANNING_AGENT_URL=https://project-planning-agent-awlsoz4tpa-uc.a.run.app,ENABLE_DETAILED_LOGGING=true,LOG_REQUESTS=true,LOG_RESPONSES=false,METRICS_ENABLED=true,MAX_CONCURRENT_REQUESTS=50,REQUEST_TIMEOUT=30,AGENT_TIMEOUT=15,RETRY_ATTEMPTS=3,RATE_LIMIT_REQUESTS_PER_MINUTE=100,RATE_LIMIT_BURST=20,HEALTH_CHECK_INTERVAL=60,AGENT_HEALTH_CHECK_TIMEOUT=10" \
    --timeout 300 \
    --execution-environment gen2

# Get the service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)')

echo "✅ Deployment completed successfully!"
echo ""
echo "🌍 Service URL: $SERVICE_URL"
echo "📊 Health Check: $SERVICE_URL/health"
echo "📖 API Documentation: $SERVICE_URL/docs"
echo "🔍 Detailed Health: $SERVICE_URL/health/detailed"
echo ""
echo "🔗 Client Context Endpoints:"
echo "   • List Clients: $SERVICE_URL/clients"
echo "   • Client Context: $SERVICE_URL/clients/{client_id}/context"
echo "   • Client-Aware Coordination: $SERVICE_URL/coordinate/client"
echo ""
echo "🧪 Testing the deployment..."

# Wait a moment for deployment to be ready
sleep 10

# Test basic health check
if curl -f "${SERVICE_URL}/health" &>/dev/null; then
    echo "✅ Health check passed"
else
    echo "❌ Health check failed"
    exit 1
fi

echo ""
echo "📝 Next Steps:"
echo "1. Configure your client card storage integration by updating environment variables"
echo "2. Test the client context endpoints with your authentication system"
echo "3. Integrate with your frontend application"
echo "4. Set up monitoring and alerting"
echo ""
echo "💡 To test client context features:"
echo "1. First get a JWT token from your auth system"
echo "2. List available clients: curl -H \"Authorization: Bearer \$TOKEN\" $SERVICE_URL/clients"
echo "3. Get client context: curl -H \"Authorization: Bearer \$TOKEN\" $SERVICE_URL/clients/promise_money/context"
echo "4. Make client-aware requests to: $SERVICE_URL/coordinate/client"
echo ""
echo "🔧 To update client storage backend, modify these environment variables:"
echo "   CLIENT_STORAGE_TYPE (json_files|database|graph_db|api_endpoint|firestore)"
echo "   And corresponding connection details in your deployment"
echo ""
echo "🎉 Enhanced Agent Coordinator with Client Context is now live!"
