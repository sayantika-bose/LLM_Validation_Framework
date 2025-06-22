from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.routers import prompt

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.info("Including prompt router at /api/ask")
# Include routers
app.include_router(prompt.router, prefix="/api")


# Use FastAPI lifespan event handler for startup logging
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    logging.info("FastAPI application startup complete.")
    yield

app.router.lifespan_context = lifespan

if __name__ == "__main__":
    import uvicorn
    logging.info("Starting FastAPI app with Uvicorn...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
