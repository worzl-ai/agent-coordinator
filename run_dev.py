"""
Development startup script for the Agent Coordinator
"""

import uvicorn
import logging
from src.auth import create_test_token

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """Start the development server"""
    logger.info("Starting Agent Coordinator Development Server...")
    
    # Generate a test token for development
    test_token = create_test_token()
    logger.info(f"Test JWT Token for development: {test_token}")
    logger.info("Use this token in the 'Authorization: Bearer <token>' header for API requests")
    
    # Start the server
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
