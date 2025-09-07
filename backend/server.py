"""
BrandForge AI - Advanced Brand Identity Generator
Main FastAPI server with advanced architecture
"""

from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import json
import base64
import google.generativeai as genai
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime, timezone

# Import models and engines
from models.brand_strategy import BusinessInput, BrandStrategy
from models.visual_assets import AssetType, AssetCollection, GeneratedAsset
from models.project_state import BrandProject, ProjectStatus
from ai_engines.emergent_strategy import EmergentStrategyEngine
from ai_engines.gemini_visual import GeminiVisualEngine
from ai_engines.consistency_manager import ConsistencyManager
from ai_engines.export_engine import ExportEngine

# Import routes
from routes.brand_routes import brand_router

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app
app = FastAPI(
    title="BrandForge AI - Advanced Brand Identity Generator",
    version="2.0.0",
    description="AI-powered brand identity creation combining strategic thinking with consistent visual generation"
)

# Create main API router
api_router = APIRouter(prefix="/api")

# Initialize AI engines
strategy_engine = EmergentStrategyEngine()
visual_engine = GeminiVisualEngine()
consistency_manager = ConsistencyManager()
export_engine = ExportEngine()

# Legacy API Routes for backward compatibility
# These routes maintain the existing API while using the new architecture

# Legacy API Routes - maintaining backward compatibility
@api_router.post("/projects", response_model=Dict[str, Any])
async def create_brand_project_legacy(business_input: BusinessInput):
    """Generate comprehensive brand strategy using EmergentStrategyEngine"""
    try:
        # Use the strategy engine to generate brand strategy
        brand_strategy = await strategy_engine.analyze_business_concept(business_input)
        
        return brand_strategy.dict()
        
    except Exception as e:
        logging.error(f"Error generating brand strategy: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate brand strategy: {str(e)}")

# Legacy visual asset functions removed - now using GeminiVisualEngine from ai_engines/
# All visual generation is handled by the visual_engine instance above


# Initialize engines (already done above)
# strategy_engine = EmergentStrategyEngine()
# visual_engine = GeminiVisualEngine()
# consistency_manager = ConsistencyManager()
# export_engine = ExportEngine()

# API Routes
@api_router.post("/projects", response_model=BrandProject)
async def create_brand_project(business_input: BusinessInput):
    """Create a new brand project"""
    try:
        project = BrandProject(business_input=business_input)
        
        # Store in database
        project_dict = project.dict()
        project_dict['created_at'] = project_dict['created_at'].isoformat()
        project_dict['updated_at'] = project_dict['updated_at'].isoformat()
        
        await db.brand_projects.insert_one(project_dict)
        
        return project
    except Exception as e:
        logging.error(f"Error creating brand project: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/projects/{project_id}/strategy")
async def generate_brand_strategy(project_id: str):
    """Generate brand strategy for a project"""
    try:
        # Get project from database
        project_data = await db.brand_projects.find_one({"id": project_id})
        if not project_data:
            raise HTTPException(status_code=404, detail="Project not found")
        
        project = BrandProject(**project_data)
        
        # Generate brand strategy
        brand_strategy = await strategy_engine.analyze_brand_strategy(project.business_input)
        
        # Update project
        project.brand_strategy = brand_strategy
        project.status = "strategy_generated"
        project.updated_at = datetime.now(timezone.utc)
        
        # Store strategy in database
        strategy_dict = brand_strategy.dict()
        strategy_dict['created_at'] = strategy_dict['created_at'].isoformat()
        
        await db.brand_strategies.insert_one(strategy_dict)
        
        # Update project in database
        project_dict = project.dict()
        project_dict['created_at'] = project_dict['created_at'].isoformat()
        project_dict['updated_at'] = project_dict['updated_at'].isoformat()
        if project_dict['brand_strategy']:
            project_dict['brand_strategy']['created_at'] = project_dict['brand_strategy']['created_at'].isoformat()
        
        await db.brand_projects.update_one(
            {"id": project_id},
            {"$set": project_dict}
        )
        
        return brand_strategy
        
    except Exception as e:
        logging.error(f"Error generating brand strategy: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/projects/{project_id}/assets/{asset_type}")
async def generate_asset(project_id: str, asset_type: str, context: Optional[str] = ""):
    """Generate specific brand asset"""
    try:
        # Get project from database
        project_data = await db.brand_projects.find_one({"id": project_id})
        if not project_data:
            raise HTTPException(status_code=404, detail="Project not found")
        
        project = BrandProject(**project_data)
        
        if not project.brand_strategy:
            raise HTTPException(status_code=400, detail="Brand strategy not generated yet")
        
        # Generate asset using proper GeminiVisualEngine
        if asset_type == "logo":
            asset = await visual_engine.generate_asset(
                brand_strategy=project.brand_strategy,
                asset_type=AssetType.LOGO,
                additional_context=context
            )
            image_data = asset.asset_url.split(",")[1]  # Extract base64 from data URL
        else:
            # Map string asset_type to AssetType enum
            asset_type_enum = getattr(AssetType, asset_type.upper(), AssetType.FLYER)
            asset = await visual_engine.generate_asset(
                brand_strategy=project.brand_strategy,
                asset_type=asset_type_enum,
                additional_context=context
            )
            image_data = asset.asset_url.split(",")[1]  # Extract base64 from data URL
        
        # Create asset record
        asset = GeneratedAsset(
            project_id=project_id,
            asset_type=asset_type,
            asset_url=f"data:image/png;base64,{image_data}",
            metadata={"context": context, "generated_at": datetime.now(timezone.utc).isoformat()}
        )
        
        # Store asset in database
        asset_dict = asset.dict()
        asset_dict['created_at'] = asset_dict['created_at'].isoformat()
        
        await db.generated_assets.insert_one(asset_dict)
        
        # Update project
        project.generated_assets.append(asset)
        if len(project.generated_assets) >= 3:  # Consider complete after 3+ assets
            project.status = "completed"
        else:
            project.status = "assets_generated"
        
        project.updated_at = datetime.now(timezone.utc)
        
        # Update project in database
        project_dict = project.dict()
        project_dict['created_at'] = project_dict['created_at'].isoformat()
        project_dict['updated_at'] = project_dict['updated_at'].isoformat()
        if project_dict['brand_strategy']:
            project_dict['brand_strategy']['created_at'] = project_dict['brand_strategy']['created_at'].isoformat()
        for generated_asset in project_dict['generated_assets']:
            generated_asset['created_at'] = generated_asset['created_at'].isoformat()
        
        await db.brand_projects.update_one(
            {"id": project_id},
            {"$set": project_dict}
        )
        
        return asset
        
    except Exception as e:
        logging.error(f"Error generating asset: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/projects/{project_id}")
async def get_project(project_id: str):
    """Get project details"""
    try:
        project_data = await db.brand_projects.find_one({"id": project_id})
        if not project_data:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Convert ObjectId to string for JSON serialization
        if "_id" in project_data:
            project_data["_id"] = str(project_data["_id"])
        
        return project_data
        
    except Exception as e:
        logging.error(f"Error getting project: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/projects")
async def get_projects():
    """Get all projects"""
    try:
        projects = await db.brand_projects.find().to_list(100)
        
        # Convert ObjectId to string for JSON serialization
        for project in projects:
            if "_id" in project:
                project["_id"] = str(project["_id"])
        
        return projects
        
    except Exception as e:
        logging.error(f"Error getting projects: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/projects/{project_id}/complete-package")
async def generate_complete_package(project_id: str):
    """Generate complete brand package with multiple assets"""
    try:
        # Get project from database
        project_data = await db.brand_projects.find_one({"id": project_id})
        if not project_data:
            raise HTTPException(status_code=404, detail="Project not found")
        
        project = BrandProject(**project_data)
        
        if not project.brand_strategy:
            raise HTTPException(status_code=400, detail="Brand strategy not generated yet")
        
        # Asset types to generate
        asset_types = [
            ("logo", "Primary logo design"),
            ("business_card", "Professional business card"),
            ("letterhead", "Company letterhead"),
            ("social_media_post", "Instagram post template"),
            ("flyer", "Marketing flyer"),
            ("banner", "Web banner")
        ]
        
        generated_assets = []
        
        for asset_type, context in asset_types:
            try:
                if asset_type == "logo":
                    asset = await visual_engine.generate_asset(
                        brand_strategy=project.brand_strategy,
                        asset_type=AssetType.LOGO,
                        additional_context=context
                    )
                    image_data = asset.asset_url.split(",")[1]  # Extract base64 from data URL
                else:
                    # Map string asset_type to AssetType enum
                    asset_type_enum = getattr(AssetType, asset_type.upper(), AssetType.FLYER)
                    asset = await visual_engine.generate_asset(
                        brand_strategy=project.brand_strategy,
                        asset_type=asset_type_enum,
                        additional_context=context
                    )
                    image_data = asset.asset_url.split(",")[1]  # Extract base64 from data URL
                
                # Create asset record
                asset = GeneratedAsset(
                    project_id=project_id,
                    asset_type=asset_type,
                    asset_url=f"data:image/png;base64,{image_data}",
                    metadata={"context": context, "generated_at": datetime.now(timezone.utc).isoformat()}
                )
                
                generated_assets.append(asset)
                
                # Store asset in database
                asset_dict = asset.dict()
                asset_dict['created_at'] = asset_dict['created_at'].isoformat()
                
                await db.generated_assets.insert_one(asset_dict)
                
            except Exception as asset_error:
                logging.error(f"Failed to generate {asset_type}: {str(asset_error)}")
                # With improved retry logic in generate_marketing_asset, 
                # this should rarely happen, but if it does, we still create the asset
                # The generate_marketing_asset method now handles its own fallbacks
                
                # Use the same generation methods but with error handling
                try:
                    if asset_type == "logo":
                        asset = await visual_engine.generate_asset(
                            brand_strategy=project.brand_strategy,
                            asset_type=AssetType.LOGO,
                            additional_context=context
                        )
                        image_data = asset.asset_url.split(",")[1]  # Extract base64 from data URL
                    else:
                        # Map string asset_type to AssetType enum
                        asset_type_enum = getattr(AssetType, asset_type.upper(), AssetType.FLYER)
                        asset = await visual_engine.generate_asset(
                            brand_strategy=project.brand_strategy,
                            asset_type=asset_type_enum,
                            additional_context=context
                        )
                        image_data = asset.asset_url.split(",")[1]  # Extract base64 from data URL
                except:
                    # Final fallback - branded placeholder
                    from PIL import Image, ImageDraw
                    import io
                    
                    img = Image.new('RGB', (512, 512), color='#f0f0f0')
                    draw = ImageDraw.Draw(img)
                    draw.rectangle([50, 50, 462, 462], outline='#6366f1', width=4)
                    draw.text((200, 250), asset_type.upper(), fill='#6366f1')
                    
                    buffer = io.BytesIO()
                    img.save(buffer, format='PNG')
                    image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
                
                asset = GeneratedAsset(
                    project_id=project_id,
                    asset_type=asset_type,
                    asset_url=f"data:image/png;base64,{image_data}",
                    metadata={"context": context, "generated_at": datetime.now(timezone.utc).isoformat(), "retry_used": True}
                )
                
                generated_assets.append(asset)
                
                # Store asset in database
                asset_dict = asset.dict()
                asset_dict['created_at'] = asset_dict['created_at'].isoformat()
                
                await db.generated_assets.insert_one(asset_dict)
        
        # Update project
        project.generated_assets.extend(generated_assets)
        project.status = "completed"
        project.updated_at = datetime.now(timezone.utc)
        
        # Update project in database
        project_dict = project.dict()
        project_dict['created_at'] = project_dict['created_at'].isoformat()
        project_dict['updated_at'] = project_dict['updated_at'].isoformat()
        if project_dict['brand_strategy']:
            project_dict['brand_strategy']['created_at'] = project_dict['brand_strategy']['created_at'].isoformat()
        for generated_asset in project_dict['generated_assets']:
            generated_asset['created_at'] = generated_asset['created_at'].isoformat()
        
        await db.brand_projects.update_one(
            {"id": project_id},
            {"$set": project_dict}
        )
        
        return {
            "project_id": project_id,
            "generated_assets": generated_assets,
            "total_assets": len(generated_assets),
            "status": "completed"
        }
        
    except Exception as e:
        logging.error(f"Error generating complete package: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "BrandForge AI"}

# Include the routers in the main app
app.include_router(api_router)
app.include_router(brand_router)

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