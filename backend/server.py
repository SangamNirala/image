from fastapi import FastAPI, APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone
import google.generativeai as genai
import base64
import io
from PIL import Image
import aiofiles
import json
import asyncio

# Import the new advanced models and engines
from models.brand_strategy import BusinessInput, BrandStrategy
from models.visual_assets import GeneratedAsset, AssetGenerationRequest
from models.project_state import BrandProject, ProjectProgress, ProjectAnalytics
from ai_engines.emergent_strategy import BrandStrategyEngine
from ai_engines.gemini_visual import GeminiVisualEngine
from ai_engines.consistency_manager import ConsistencyManager
from ai_engines.export_engine import ProfessionalExportEngine

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Configure Gemini API
genai.configure(api_key=os.environ['GEMINI_API_KEY'])

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="BrandForge AI", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Initialize AI Engines
brand_strategy_engine = BrandStrategyEngine()
visual_engine = GeminiVisualEngine()
consistency_manager = ConsistencyManager()
export_engine = ProfessionalExportEngine()

# Route handlers using the new advanced AI engines

@api_router.post("/projects", response_model=Dict[str, Any])
async def create_project(business_input: BusinessInput):
    """Create a new brand project"""
    try:
        project = BrandProject(business_input=business_input)
        
        # Convert to dict for MongoDB storage
        project_dict = project.dict()
        project_dict['created_at'] = project_dict['created_at'].isoformat()
        project_dict['updated_at'] = project_dict['updated_at'].isoformat()
        
        # Store in database
        await db.brand_projects.insert_one(project_dict)
        
        return {
            "project_id": project.id,
            "status": project.status,
            "business_name": business_input.business_name,
            "created_at": project.created_at.isoformat()
        }
        
    except Exception as e:
        logging.error(f"Error creating project: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create project: {str(e)}")

@api_router.post("/projects/{project_id}/strategy", response_model=BrandStrategy)
async def generate_brand_strategy(project_id: str, advanced_analysis: bool = True):
    """Generate comprehensive brand strategy using advanced AI analysis"""
    try:
        # Get project from database
        project_doc = await db.brand_projects.find_one({"id": project_id})
        if not project_doc:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Convert back to Pydantic model
        project_doc['created_at'] = datetime.fromisoformat(project_doc['created_at'])
        project_doc['updated_at'] = datetime.fromisoformat(project_doc['updated_at'])
        project = BrandProject(**project_doc)
        
        # Generate strategy using advanced AI engine
        if advanced_analysis:
            brand_strategy = await brand_strategy_engine.generate_comprehensive_strategy(project.business_input)
        else:
            # Fallback to simpler generation
            brand_strategy = await brand_strategy_engine.analyze_brand_strategy(project.business_input)
        
        # Initialize consistency management
        consistency_manager.initialize_brand_consistency(brand_strategy)
        
        # Update project with strategy
        project.brand_strategy = brand_strategy
        project.status = "strategy_generated"
        project.updated_at = datetime.now(timezone.utc)
        project.consistency_seed = brand_strategy.id
        
        # Store strategy in database
        strategy_dict = brand_strategy.dict()
        strategy_dict['created_at'] = strategy_dict['created_at'].isoformat()
        
        await db.brand_strategies.insert_one(strategy_dict)
        
        # Update project in database
        project_dict = project.dict()
        project_dict['created_at'] = project_dict['created_at'].isoformat()
        project_dict['updated_at'] = project_dict['updated_at'].isoformat()
        project_dict['brand_strategy']['created_at'] = project_dict['brand_strategy']['created_at'].isoformat()
        
        await db.brand_projects.update_one(
            {"id": project_id},
            {"$set": project_dict}
        )
        
        return brand_strategy
        
    except Exception as e:
        logging.error(f"Error generating brand strategy: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate brand strategy: {str(e)}")

# Health check endpoint
@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "BrandForge AI"}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()