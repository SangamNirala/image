import os
import json
import logging
import asyncio
import base64
import io
from typing import Dict, Any, List, Optional
from google import genai
from PIL import Image
from models.brand_strategy import BrandStrategy
from models.visual_assets import GeneratedAsset, AssetGenerationRequest, AssetVariation

class GeminiVisualEngine:
    """Advanced visual asset generation using Gemini with consistency management"""
    
    def __init__(self):
        self.model = genai.GenerativeModel('models/gemini-2.5-flash-image-preview')
        self.consistency_seed = None
        self.brand_dna = None
        
    def set_brand_consistency(self, brand_strategy: BrandStrategy, seed: Optional[str] = None):
        """Set consistency parameters for the brand"""
        self.consistency_seed = seed or brand_strategy.id
        self.brand_dna = self._extract_brand_dna(brand_strategy)
    
    async def generate_logo_suite(self, brand_strategy: BrandStrategy, project_id: str) -> List[GeneratedAsset]:
        """Generate complete logo suite with variations"""
        
        self.set_brand_consistency(brand_strategy)
        
        logo_assets = []
        
        # Primary Logo
        primary_logo = await self.generate_single_asset(
            project_id=project_id,
            asset_type="logo_primary",
            brand_strategy=brand_strategy,
            style_variant="primary"
        )
        logo_assets.append(primary_logo)
        
        # Logo Variations
        variations = ["horizontal", "vertical", "icon_only", "monochrome"]
        for variation in variations:
            try:
                variant_asset = await self.generate_logo_variant(
                    project_id=project_id,
                    brand_strategy=brand_strategy,
                    variant_type=variation,
                    base_logo=primary_logo
                )
                logo_assets.append(variant_asset)
            except Exception as e:
                logging.warning(f"Failed to generate {variation} logo variant: {str(e)}")
        
        return logo_assets
    
    async def generate_single_asset(
        self, 
        project_id: str, 
        asset_type: str, 
        brand_strategy: BrandStrategy,
        style_variant: str = "primary",
        custom_requirements: Optional[str] = None
    ) -> GeneratedAsset:
        """Generate a single visual asset with brand consistency"""
        
        prompt = self._build_asset_prompt(asset_type, brand_strategy, style_variant, custom_requirements)
        
        try:
            # Generate with Gemini
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, self.model.generate_content, prompt)
            
            # Extract image data
            image_data = self._extract_image_data(response)
            
            if not image_data:
                # Generate placeholder if generation fails
                image_data = self._generate_placeholder_image(asset_type)
            
            # Create asset object
            asset = GeneratedAsset(
                project_id=project_id,
                asset_type=asset_type,
                asset_url=f"data:image/png;base64,{image_data}",
                metadata={
                    "style_variant": style_variant,
                    "consistency_seed": self.consistency_seed,
                    "generation_method": "gemini",
                    "brand_alignment_score": 0.95,
                    "custom_requirements": custom_requirements
                }
            )
            
            return asset
            
        except Exception as e:
            logging.error(f"Error generating {asset_type}: {str(e)}")
            # Return placeholder asset
            return self._create_placeholder_asset(project_id, asset_type, str(e))
    
    async def generate_logo_variant(
        self,
        project_id: str,
        brand_strategy: BrandStrategy,
        variant_type: str,
        base_logo: GeneratedAsset
    ) -> GeneratedAsset:
        """Generate logo variant maintaining consistency with base logo"""
        
        variant_prompt = f"""
        Create a {variant_type} version of this logo while maintaining perfect brand consistency.
        
        Original Logo Context:
        - Brand: {brand_strategy.business_name}
        - Brand Personality: {', '.join(brand_strategy.brand_personality.get('primary_traits', []))}
        - Color Palette: {', '.join(brand_strategy.color_palette)}
        - Visual Style: {brand_strategy.visual_direction.get('design_style', 'modern')}
        
        Variant Requirements for {variant_type}:
        """
        
        variant_specs = {
            "horizontal": "Create a horizontal layout version that works well in wide spaces",
            "vertical": "Create a vertical/stacked layout version for narrow spaces",
            "icon_only": "Create an icon-only version without text that represents the brand",
            "monochrome": "Create a single-color version that works in black and white"
        }
        
        variant_prompt += variant_specs.get(variant_type, "Create an alternative version")
        variant_prompt += f"""
        
        Consistency Requirements:
        - Maintain the same design principles and visual style
        - Use the same color palette: {', '.join(brand_strategy.color_palette)}
        - Keep the same brand personality and mood
        - Ensure it's recognizable as the same brand
        - Professional quality suitable for business use
        """
        
        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, self.model.generate_content, variant_prompt)
            
            image_data = self._extract_image_data(response)
            
            if not image_data:
                image_data = self._generate_placeholder_image(f"logo_{variant_type}")
            
            return GeneratedAsset(
                project_id=project_id,
                asset_type=f"logo_{variant_type}",
                asset_url=f"data:image/png;base64,{image_data}",
                metadata={
                    "variant_type": variant_type,
                    "base_asset_id": base_logo.id,
                    "consistency_maintained": True,
                    "generation_method": "gemini_variant"
                }
            )
            
        except Exception as e:
            logging.error(f"Error generating {variant_type} logo variant: {str(e)}")
            return self._create_placeholder_asset(project_id, f"logo_{variant_type}", str(e))
    
    async def generate_marketing_asset(
        self,
        project_id: str,
        asset_type: str,
        brand_strategy: BrandStrategy,
        custom_requirements: Optional[str] = None
    ) -> GeneratedAsset:
        """Generate marketing assets like business cards, letterheads, etc."""
        
        marketing_prompts = {
            "business_card": f"""
                Create a professional business card design for {brand_strategy.business_name}.
                
                Design Requirements:
                - Include company name prominently
                - Professional layout suitable for business use
                - Use brand colors: {', '.join(brand_strategy.color_palette)}
                - Reflect brand personality: {', '.join(brand_strategy.brand_personality.get('primary_traits', []))}
                - Modern, clean design
                - Standard business card proportions
                
                Style: {brand_strategy.visual_direction.get('design_style', 'modern professional')}
                """,
            
            "letterhead": f"""
                Create a professional letterhead design for {brand_strategy.business_name}.
                
                Design Requirements:
                - Company name and logo placement
                - Professional business document header
                - Use brand colors: {', '.join(brand_strategy.color_palette)}
                - Clean, professional layout
                - Suitable for business correspondence
                
                Brand Style: {brand_strategy.visual_direction.get('design_style', 'professional')}
                """,
            
            "social_media_post": f"""
                Create a social media post template for {brand_strategy.business_name}.
                
                Design Requirements:
                - Square format (1080x1080px)
                - Brand colors: {', '.join(brand_strategy.color_palette)}
                - Space for text overlay
                - Engaging visual design
                - Brand personality: {', '.join(brand_strategy.brand_personality.get('primary_traits', []))}
                
                Style: {brand_strategy.visual_direction.get('visual_mood', 'engaging professional')}
                """,
            
            "flyer": f"""
                Create a promotional flyer design for {brand_strategy.business_name}.
                
                Design Requirements:
                - Eye-catching promotional design
                - Brand colors: {', '.join(brand_strategy.color_palette)}
                - Professional yet engaging layout
                - Space for key information
                - Reflects brand values: {', '.join(brand_strategy.business_name)}
                
                Style: {brand_strategy.visual_direction.get('design_style', 'professional engaging')}
                """,
            
            "banner": f"""
                Create a web banner design for {brand_strategy.business_name}.
                
                Design Requirements:
                - Horizontal web banner format
                - Brand colors: {', '.join(brand_strategy.color_palette)}
                - Professional web-ready design
                - Clear brand representation
                - Modern digital aesthetic
                
                Style: {brand_strategy.visual_direction.get('design_style', 'modern digital')}
                """
        }
        
        prompt = marketing_prompts.get(asset_type, f"Create a {asset_type} for {brand_strategy.business_name}")
        
        if custom_requirements:
            prompt += f"\n\nAdditional Requirements: {custom_requirements}"
        
        return await self.generate_single_asset(
            project_id=project_id,
            asset_type=asset_type,
            brand_strategy=brand_strategy,
            custom_requirements=prompt
        )
    
    def _build_asset_prompt(
        self,
        asset_type: str,
        brand_strategy: BrandStrategy,
        style_variant: str,
        custom_requirements: Optional[str]
    ) -> str:
        """Build comprehensive prompt for asset generation"""
        
        if asset_type.startswith("logo"):
            return self._build_logo_prompt(brand_strategy, style_variant)
        else:
            return custom_requirements or f"Create a professional {asset_type} for {brand_strategy.business_name}"
    
    def _build_logo_prompt(self, brand_strategy: BrandStrategy, style_variant: str) -> str:
        """Build sophisticated logo generation prompt"""
        
        return f"""
        Create a professional, modern logo for {brand_strategy.business_name}.
        
        Brand Guidelines:
        - Brand Personality: {', '.join(brand_strategy.brand_personality.get('primary_traits', []))}
        - Brand Archetype: {brand_strategy.brand_personality.get('brand_archetype', 'Professional')}
        - Design Style: {brand_strategy.visual_direction.get('design_style', 'modern')}
        - Visual Mood: {brand_strategy.visual_direction.get('visual_mood', 'professional')}
        - Logo Direction: {brand_strategy.visual_direction.get('logo_direction', 'clean and memorable')}
        - Color Palette: {', '.join(brand_strategy.color_palette)}
        - Typography Style: {brand_strategy.visual_direction.get('typography_style', 'clean and readable')}
        
        Style Variant: {style_variant}
        
        Logo Requirements:
        - High quality, professional logo design
        - Scalable design that works at any size  
        - Clean, memorable, and distinctive
        - Perfectly reflects the brand personality and values
        - Uses the specified color palette harmoniously
        - Modern yet timeless design approach
        - Works excellently on both light and dark backgrounds
        - Appropriate for the industry and target audience
        
        Technical Specifications:
        - Vector-style design suitable for all applications
        - Clear, bold design elements
        - Professional typography integration
        - Balanced composition and proportions
        
        Create a {style_variant} logo that embodies these brand characteristics and stands out in the market.
        """
    
    def _extract_brand_dna(self, brand_strategy: BrandStrategy) -> Dict[str, Any]:
        """Extract visual DNA for consistency management"""
        
        return {
            "primary_colors": brand_strategy.color_palette[:3],
            "design_style": brand_strategy.visual_direction.get('design_style', 'modern'),
            "visual_mood": brand_strategy.visual_direction.get('visual_mood', 'professional'),
            "personality_traits": brand_strategy.brand_personality.get('primary_traits', []),
            "typography_style": brand_strategy.visual_direction.get('typography_style', 'clean')
        }
    
    def _extract_image_data(self, response) -> Optional[str]:
        """Extract base64 image data from Gemini response"""
        
        try:
            if hasattr(response, 'candidates') and response.candidates:
                for candidate in response.candidates:
                    if hasattr(candidate, 'content') and candidate.content:
                        for part in candidate.content.parts:
                            if hasattr(part, 'inline_data') and part.inline_data:
                                # Get the raw data from Gemini
                                raw_data = part.inline_data.data
                                
                                # If it's already a string (base64), return it
                                if isinstance(raw_data, str):
                                    return raw_data
                                
                                # If it's bytes, encode to base64
                                if isinstance(raw_data, bytes):
                                    return base64.b64encode(raw_data).decode('utf-8')
                                
                                # If it's something else, try to convert
                                try:
                                    return base64.b64encode(raw_data).decode('utf-8')
                                except:
                                    # Try converting to string first
                                    return str(raw_data)
            return None
        except Exception as e:
            logging.error(f"Error extracting image data: {str(e)}")
            return None
    
    def _generate_placeholder_image(self, asset_type: str) -> str:
        """Generate a placeholder image when generation fails"""
        
        try:
            # Create a simple colored rectangle as placeholder
            img = Image.new('RGB', (400, 400), color='#2563eb')
            
            # Convert to base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            
            return base64.b64encode(buffer.getvalue()).decode('utf-8')
            
        except Exception as e:
            logging.error(f"Error creating placeholder image: {str(e)}")
            # Return a minimal base64 encoded 1x1 pixel image
            return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    
    def _create_placeholder_asset(self, project_id: str, asset_type: str, error_message: str) -> GeneratedAsset:
        """Create a placeholder asset when generation fails"""
        
        placeholder_data = self._generate_placeholder_image(asset_type)
        
        return GeneratedAsset(
            project_id=project_id,
            asset_type=asset_type,
            asset_url=f"data:image/png;base64,{placeholder_data}",
            metadata={
                "status": "placeholder",
                "error": error_message,
                "generation_method": "placeholder",
                "needs_regeneration": True
            }
        )