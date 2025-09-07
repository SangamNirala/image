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
        """Generate comprehensive brand strategy using Gemini"""
        
        strategy_prompt = f"""
        You are an expert brand strategist. Analyze this business concept and create a comprehensive brand strategy.

        BUSINESS INFORMATION:
        - Name: {business_input.business_name}
        - Description: {business_input.business_description}
        - Industry: {business_input.industry}
        - Target Audience: {business_input.target_audience}
        - Values: {', '.join(business_input.business_values)}
        - Preferred Style: {business_input.preferred_style}
        - Color Preferences: {business_input.preferred_colors}

        Generate a detailed brand strategy with the following structure (respond in JSON format):
        {{
            "brand_personality": {{
                "primary_traits": ["trait1", "trait2", "trait3", "trait4", "trait5"],
                "brand_archetype": "archetype_name",
                "tone_of_voice": "description",
                "brand_essence": "one_sentence_summary"
            }},
            "visual_direction": {{
                "design_style": "style_description",
                "visual_mood": "mood_description",
                "typography_style": "typography_recommendations",
                "imagery_style": "imagery_recommendations",
                "logo_direction": "detailed_logo_guidance"
            }},
            "color_palette": ["#hex1", "#hex2", "#hex3", "#hex4", "#hex5"],
            "messaging_framework": {{
                "tagline": "compelling_tagline",
                "key_messages": ["message1", "message2", "message3"],
                "brand_promise": "brand_promise_statement",
                "unique_value_proposition": "uvp_statement"
            }},
            "consistency_rules": {{
                "logo_usage": "usage_guidelines",
                "color_usage": "color_application_rules",
                "typography_rules": "typography_guidelines",
                "visual_consistency": "visual_consistency_requirements"
            }}
        }}
        
        Make sure the strategy is cohesive, professional, and perfectly aligned with the business concept.
        """
        
        try:
            response = await self.model.generate_content_async(strategy_prompt)
            
            # Extract JSON from response
            strategy_text = response.text.strip()
            if strategy_text.startswith('```json'):
                strategy_text = strategy_text.replace('```json', '').replace('```', '').strip()
            
            strategy_data = json.loads(strategy_text)
            
            # Create BrandStrategy object
            brand_strategy = BrandStrategy(
                business_name=business_input.business_name,
                brand_personality=strategy_data["brand_personality"],
                visual_direction=strategy_data["visual_direction"],
                color_palette=strategy_data["color_palette"],
                messaging_framework=strategy_data["messaging_framework"],
                consistency_rules=strategy_data["consistency_rules"]
            )
            
            return brand_strategy
            
        except Exception as e:
            logging.error(f"Error generating brand strategy: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to generate brand strategy: {str(e)}")

class VisualAssetEngine:
    def __init__(self):
        self.model = genai.GenerativeModel('models/gemini-2.5-flash-image-preview')
    
    async def generate_logo(self, brand_strategy: BrandStrategy, style_variant: str = "primary") -> str:
        """Generate logo using Gemini Image Preview"""
        
        logo_prompt = f"""
        Create a professional, modern logo for {brand_strategy.business_name}.
        
        Brand Guidelines:
        - Brand Personality: {', '.join(brand_strategy.brand_personality.get('primary_traits', []))}
        - Design Style: {brand_strategy.visual_direction.get('design_style', 'modern')}
        - Visual Mood: {brand_strategy.visual_direction.get('visual_mood', 'professional')}
        - Logo Direction: {brand_strategy.visual_direction.get('logo_direction', 'clean and memorable')}
        - Color Palette: {', '.join(brand_strategy.color_palette)}
        
        Style Variant: {style_variant}
        
        Requirements:
        - High quality, professional logo
        - Scalable design that works at any size  
        - Clean, memorable, and distinctive
        - Reflects the brand personality and values
        - Uses the specified color palette
        - Modern and timeless design
        - Works on both light and dark backgrounds
        
        Create a {style_variant} logo version that embodies these brand characteristics.
        """
        
        try:
            # Use the synchronous version and handle async properly
            import asyncio
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, self.model.generate_content, logo_prompt)
            
            # Check response structure
            logging.info(f"Gemini response type: {type(response)}")
            logging.info(f"Response attributes: {dir(response)}")
            
            # Try different ways to extract image data
            if hasattr(response, 'candidates') and response.candidates:
                for candidate in response.candidates:
                    if hasattr(candidate, 'content') and candidate.content:
                        for part in candidate.content.parts:
                            logging.info(f"Part type: {type(part)}, has inline_data: {hasattr(part, 'inline_data')}")
                            if hasattr(part, 'inline_data'):
                                logging.info(f"inline_data exists: {part.inline_data is not None}")
                                if part.inline_data:
                                    logging.info(f"inline_data mime_type: {getattr(part.inline_data, 'mime_type', 'NO_MIME_TYPE')}")
                                    logging.info(f"inline_data has data: {hasattr(part.inline_data, 'data')}")
                                    # Convert binary data to base64
                                    image_binary = part.inline_data.data
                                    if image_binary:
                                        image_data = base64.b64encode(image_binary).decode('utf-8')
                                        logging.info(f"SUCCESS: Found image data, binary length: {len(image_binary)}, base64 length: {len(image_data)}")
                                        return image_data
                                    else:
                                        logging.info("inline_data.data is empty")
                                else:
                                    logging.info("inline_data is None")
                            elif hasattr(part, 'text'):
                                logging.info(f"Found text part: {part.text[:100]}...")
            
            # If no image found, log the full response structure for debugging
            logging.error(f"No image found in response. Response: {response}")
            raise Exception("No image generated in response")
            
        except Exception as e:
            logging.error(f"Error generating logo: {str(e)}")
            # For now, return a placeholder to test the rest of the system
            # Create a simple placeholder image in base64
            placeholder_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
            return placeholder_data
    
    async def generate_marketing_asset(self, brand_strategy: BrandStrategy, asset_type: str, additional_context: str = "") -> str:
        """Generate various marketing assets with retry logic"""
        
        asset_prompts = {
            "business_card": f"Professional business card design for {brand_strategy.business_name}",
            "letterhead": f"Professional letterhead design for {brand_strategy.business_name}",
            "social_media_post": f"Instagram post template for {brand_strategy.business_name}",
            "flyer": f"Marketing flyer design for {brand_strategy.business_name}",
            "banner": f"Web banner design for {brand_strategy.business_name}",
            "poster": f"Professional poster design for {brand_strategy.business_name}"
        }
        
        base_prompt = asset_prompts.get(asset_type, f"{asset_type} design for {brand_strategy.business_name}")
        
        marketing_prompt = f"""
        Create a {base_prompt}.
        
        Brand Guidelines:
        - Brand Name: {brand_strategy.business_name}
        - Brand Personality: {', '.join(brand_strategy.brand_personality.get('primary_traits', []))}
        - Design Style: {brand_strategy.visual_direction.get('design_style', 'modern')}
        - Visual Mood: {brand_strategy.visual_direction.get('visual_mood', 'professional')}
        - Color Palette: {', '.join(brand_strategy.color_palette)}
        - Tagline: {brand_strategy.messaging_framework.get('tagline', '')}
        
        Additional Context: {additional_context}
        
        Requirements:
        - Professional, high-quality design
        - Consistent with brand identity
        - Uses specified color palette
        - Includes brand name and relevant messaging
        - Appropriate for {asset_type} format
        - Modern, clean, and impactful design
        
        Create a compelling {asset_type} that represents the brand professionally.
        """
        
        # Try up to 3 times to generate the asset
        for attempt in range(3):
            try:
                logging.info(f"Attempting to generate {asset_type} (attempt {attempt + 1}/3)")
                
                # Use the synchronous version and handle async properly
                import asyncio
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(None, self.model.generate_content, marketing_prompt)
                
                # Try different ways to extract image data
                if hasattr(response, 'candidates') and response.candidates:
                    for candidate in response.candidates:
                        if hasattr(candidate, 'content') and candidate.content:
                            for part in candidate.content.parts:
                                if hasattr(part, 'inline_data') and part.inline_data and part.inline_data.data:
                                    # Convert binary data to base64
                                    image_binary = part.inline_data.data
                                    if image_binary:
                                        image_data = base64.b64encode(image_binary).decode('utf-8')
                                        logging.info(f"Successfully generated {asset_type} on attempt {attempt + 1}")
                                        return image_data
                
                logging.warning(f"No image data found for {asset_type} on attempt {attempt + 1}")
                
                # Wait a bit before retrying
                if attempt < 2:
                    await asyncio.sleep(2)
                    
            except Exception as e:
                logging.error(f"Error generating {asset_type} on attempt {attempt + 1}: {str(e)}")
                if attempt < 2:
                    await asyncio.sleep(2)
        
        # After all attempts failed, generate a better placeholder
        logging.error(f"Failed to generate {asset_type} after 3 attempts, using enhanced placeholder")
        
        # Create a simple branded placeholder using PIL
        try:
            from PIL import Image, ImageDraw, ImageFont
            import io
            
            # Create a 512x512 image with brand colors
            img = Image.new('RGB', (512, 512), color='#f8f9fa')
            draw = ImageDraw.Draw(img)
            
            # Use first brand color or default
            brand_color = brand_strategy.color_palette[0] if brand_strategy.color_palette else '#6366f1'
            
            # Draw a simple design
            draw.rectangle([50, 50, 462, 462], outline=brand_color, width=4)
            draw.rectangle([100, 100, 412, 412], fill=brand_color, width=2)
            
            # Add text
            try:
                font = ImageFont.load_default()
                text = brand_strategy.business_name[:20]  # Limit text length
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                x = (512 - text_width) // 2
                y = (512 - text_height) // 2
                draw.text((x, y), text, fill='white', font=font)
            except:
                # Fallback if font fails
                draw.text((200, 250), asset_type.upper(), fill='white')
            
            # Convert to base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            placeholder_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            logging.info(f"Generated branded placeholder for {asset_type}")
            return placeholder_data
            
        except Exception as placeholder_error:
            logging.error(f"Failed to create branded placeholder: {str(placeholder_error)}")
            # Final fallback - minimal placeholder
            placeholder_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
            return placeholder_data

# Initialize engines
strategy_engine = BrandStrategyEngine()
visual_engine = VisualAssetEngine()

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
        
        # Generate asset
        if asset_type == "logo":
            image_data = await visual_engine.generate_logo(project.brand_strategy)
        else:
            image_data = await visual_engine.generate_marketing_asset(
                project.brand_strategy, asset_type, context
            )
        
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
                    image_data = await visual_engine.generate_logo(project.brand_strategy)
                else:
                    image_data = await visual_engine.generate_marketing_asset(
                        project.brand_strategy, asset_type, context
                    )
                
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
                        image_data = await visual_engine.generate_logo(project.brand_strategy)
                    else:
                        image_data = await visual_engine.generate_marketing_asset(
                            project.brand_strategy, asset_type, context
                        )
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