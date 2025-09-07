"""
Gemini Visual Engine
Advanced visual asset generation with consistency management
"""

import logging
import base64
import json
import asyncio
import hashlib
import os
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timezone
from PIL import Image, ImageDraw, ImageFont
import io
import google.generativeai as genai
from models.brand_strategy import BrandStrategy, VisualDirection
from models.visual_assets import GeneratedAsset, AssetType, AssetMetadata

class GeminiVisualEngine:
    """Advanced visual asset generation with consistency management"""
    
    def __init__(self):
        # Configure Gemini API
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
        
        self.model = genai.GenerativeModel('models/gemini-2.5-flash-image-preview')
        self.consistency_seed = None
        self.brand_dna = None
        self.logger = logging.getLogger(__name__)
        
        # Asset generation configurations
        self.asset_configs = {
            AssetType.LOGO: {
                "base_prompt": "Professional logo design",
                "requirements": [
                    "Scalable vector-style design",
                    "Works on light and dark backgrounds", 
                    "Memorable and distinctive",
                    "Professional quality"
                ],
                "dimensions": "512x512",
                "style_focus": "logo_direction"
            },
            AssetType.BUSINESS_CARD: {
                "base_prompt": "Professional business card design",
                "requirements": [
                    "Standard business card proportions",
                    "Clear contact information layout",
                    "Professional typography",
                    "Brand-consistent design"
                ],
                "dimensions": "512x320",
                "style_focus": "layout_principles"
            },
            AssetType.LETTERHEAD: {
                "base_prompt": "Professional letterhead design",
                "requirements": [
                    "Corporate letterhead format",
                    "Logo placement and branding",
                    "Clean, professional layout",
                    "Consistent with brand identity"
                ],
                "dimensions": "512x700",
                "style_focus": "layout_principles"
            },
            AssetType.SOCIAL_MEDIA_POST: {
                "base_prompt": "Social media post template",
                "requirements": [
                    "Square format for Instagram",
                    "Eye-catching visual design",
                    "Brand-consistent styling",
                    "Space for text overlay"
                ],
                "dimensions": "512x512",
                "style_focus": "imagery_style"
            },
            AssetType.FLYER: {
                "base_prompt": "Marketing flyer design",
                "requirements": [
                    "Attention-grabbing design",
                    "Clear information hierarchy",
                    "Professional layout",
                    "Brand-aligned visual style"
                ],
                "dimensions": "512x700",
                "style_focus": "layout_principles"
            },
            AssetType.BANNER: {
                "base_prompt": "Web banner design",
                "requirements": [
                    "Wide banner format",
                    "Web-optimized design",
                    "Clear call-to-action space",
                    "Brand-consistent styling"
                ],
                "dimensions": "768x256",
                "style_focus": "imagery_style"
            }
        }
    
    async def initialize_brand_dna(self, brand_strategy: BrandStrategy) -> None:
        """Initialize visual DNA for consistency across assets"""
        
        # Create brand DNA fingerprint
        brand_elements = {
            "primary_traits": brand_strategy.brand_personality.primary_traits,
            "design_style": brand_strategy.visual_direction.design_style,
            "visual_mood": brand_strategy.visual_direction.visual_mood,
            "primary_colors": brand_strategy.visual_direction.color_strategy.get("primary_colors", []),
            "brand_essence": brand_strategy.brand_personality.brand_essence
        }
        
        # Generate consistency seed
        brand_string = json.dumps(brand_elements, sort_keys=True)
        self.consistency_seed = hashlib.md5(brand_string.encode()).hexdigest()[:8]
        
        self.brand_dna = {
            "visual_signature": brand_elements,
            "consistency_seed": self.consistency_seed,
            "generation_rules": self._extract_generation_rules(brand_strategy)
        }
        
        self.logger.info(f"Initialized brand DNA with consistency seed: {self.consistency_seed}")
    
    def _extract_generation_rules(self, brand_strategy: BrandStrategy) -> Dict[str, Any]:
        """Extract specific generation rules from brand strategy"""
        
        return {
            "color_palette": brand_strategy.visual_direction.color_strategy.get("primary_colors", []),
            "style_keywords": [
                brand_strategy.visual_direction.design_style,
                brand_strategy.visual_direction.visual_mood,
                *brand_strategy.brand_personality.primary_traits[:3]
            ],
            "avoid_elements": [
                "inconsistent colors",
                "conflicting styles", 
                "off-brand personality"
            ],
            "mandatory_elements": [
                brand_strategy.business_name,
                "consistent visual style",
                "brand color palette"
            ]
        }
    
    async def generate_logo_suite(self, brand_strategy: BrandStrategy) -> Dict[str, GeneratedAsset]:
        """Generate comprehensive logo suite with variations"""
        
        if not self.brand_dna:
            await self.initialize_brand_dna(brand_strategy)
        
        logo_suite = {}
        
        # Primary Logo Generation
        primary_logo = await self.generate_asset(
            brand_strategy=brand_strategy,
            asset_type=AssetType.LOGO,
            variant="primary",
            additional_context="Primary brand logo - main version"
        )
        logo_suite["primary"] = primary_logo
        
        # Logo Variations
        variations = [
            ("horizontal", "Horizontal logo layout"),
            ("vertical", "Vertical logo layout"), 
            ("icon_only", "Logo symbol/icon without text"),
            ("monochrome", "Single color logo version")
        ]
        
        for variant_type, context in variations:
            try:
                variant = await self.generate_logo_variant(
                    brand_strategy, primary_logo, variant_type, context
                )
                logo_suite[variant_type] = variant
            except Exception as e:
                self.logger.warning(f"Failed to generate {variant_type} logo variant: {str(e)}")
        
        return logo_suite
    
    async def generate_logo_variant(
        self,
        brand_strategy: BrandStrategy,
        base_logo: GeneratedAsset,
        variant_type: str,
        context: str
    ) -> GeneratedAsset:
        """Generate logo variant maintaining consistency with base logo"""
        
        variant_prompts = {
            "horizontal": f"Create horizontal layout version of logo for {brand_strategy.business_name}",
            "vertical": f"Create vertical stacked version of logo for {brand_strategy.business_name}",
            "icon_only": f"Create icon-only version without text for {brand_strategy.business_name}",
            "monochrome": f"Create single-color version of logo for {brand_strategy.business_name}"
        }
        
        base_prompt = variant_prompts.get(variant_type, f"{variant_type} logo variant")
        
        return await self.generate_asset(
            brand_strategy=brand_strategy,
            asset_type=AssetType.LOGO,
            variant=variant_type,
            additional_context=f"{context}. Maintain visual consistency with brand identity.",
            consistency_reference=base_logo
        )
    
    async def generate_asset(
        self,
        brand_strategy: BrandStrategy,
        asset_type: AssetType,
        variant: str = "standard",
        additional_context: str = "",
        consistency_reference: Optional[GeneratedAsset] = None,
        retry_count: int = 3
    ) -> GeneratedAsset:
        """Generate individual asset with advanced consistency management"""
        
        if not self.brand_dna:
            await self.initialize_brand_dna(brand_strategy)
        
        config = self.asset_configs[asset_type]
        
        # Build comprehensive generation prompt
        generation_prompt = self._build_generation_prompt(
            brand_strategy=brand_strategy,
            asset_type=asset_type,
            config=config,
            variant=variant,
            additional_context=additional_context,
            consistency_reference=consistency_reference
        )
        
        # Attempt generation with retry logic
        for attempt in range(retry_count):
            try:
                self.logger.info(f"Generating {asset_type.value} (attempt {attempt + 1}/{retry_count})")
                
                # Generate with Gemini
                image_data = await self._generate_with_gemini(generation_prompt)
                
                if image_data:
                    # Create asset metadata
                    metadata = AssetMetadata(
                        generation_prompt=generation_prompt[:500],  # Truncated for storage
                        consistency_seed=self.consistency_seed,
                        variant=variant,
                        attempt_number=attempt + 1,
                        generation_time=datetime.now(timezone.utc),
                        quality_score=await self._assess_asset_quality(image_data, brand_strategy)
                    )
                    
                    asset = GeneratedAsset(
                        asset_type=asset_type,
                        asset_url=f"data:image/png;base64,{image_data}",
                        metadata=metadata,
                        variant=variant
                    )
                    
                    self.logger.info(f"Successfully generated {asset_type.value} on attempt {attempt + 1}")
                    return asset
                
                self.logger.warning(f"No image data received for {asset_type.value} on attempt {attempt + 1}")
                
                if attempt < retry_count - 1:
                    await asyncio.sleep(2)
                    
            except Exception as e:
                self.logger.error(f"Error generating {asset_type.value} on attempt {attempt + 1}: {str(e)}")
                if attempt < retry_count - 1:
                    await asyncio.sleep(2)
        
        # Generate fallback asset if all attempts failed
        self.logger.error(f"Failed to generate {asset_type.value} after {retry_count} attempts, creating fallback")
        return await self._create_fallback_asset(brand_strategy, asset_type, variant)
    
    def _build_generation_prompt(
        self,
        brand_strategy: BrandStrategy,
        asset_type: AssetType,
        config: Dict[str, Any],
        variant: str,
        additional_context: str,
        consistency_reference: Optional[GeneratedAsset]
    ) -> str:
        """Build comprehensive generation prompt with consistency constraints"""
        
        # Base prompt construction
        base_prompt = config["base_prompt"]
        requirements = "\n".join([f"- {req}" for req in config["requirements"]])
        
        # Brand context
        brand_context = f"""
        BRAND IDENTITY:
        - Brand Name: {brand_strategy.business_name}
        - Brand Personality: {', '.join(brand_strategy.brand_personality.primary_traits)}
        - Brand Essence: {brand_strategy.brand_personality.brand_essence}
        - Brand Archetype: {brand_strategy.brand_personality.brand_archetype}
        
        VISUAL DIRECTION:
        - Design Style: {brand_strategy.visual_direction.design_style}
        - Visual Mood: {brand_strategy.visual_direction.visual_mood}
        - Primary Colors: {', '.join(brand_strategy.visual_direction.color_strategy.get('primary_colors', []))}
        - Typography Style: {brand_strategy.visual_direction.typography_direction.get('logo_typography', 'professional')}
        """
        
        # Consistency constraints
        consistency_context = f"""
        CONSISTENCY REQUIREMENTS:
        - Brand DNA Seed: {self.consistency_seed}
        - Visual Signature: Maintain consistent {brand_strategy.visual_direction.design_style} style
        - Color Consistency: Use specified brand colors: {', '.join(brand_strategy.visual_direction.color_strategy.get('primary_colors', []))}
        - Style Consistency: Reflect {brand_strategy.brand_personality.brand_essence}
        """
        
        # Asset-specific focus
        focus_area = config.get("style_focus", "design_style")
        if focus_area == "logo_direction":
            specific_guidance = brand_strategy.visual_direction.logo_direction
        elif focus_area == "layout_principles":
            specific_guidance = brand_strategy.visual_direction.layout_principles
        elif focus_area == "imagery_style":
            specific_guidance = brand_strategy.visual_direction.imagery_style
        else:
            specific_guidance = {}
        
        specific_context = f"""
        SPECIFIC GUIDANCE FOR {asset_type.value.upper()}:
        {json.dumps(specific_guidance, indent=2) if specific_guidance else 'Follow general brand guidelines'}
        """
        
        # Consistency reference
        reference_context = ""
        if consistency_reference:
            reference_context = f"""
            CONSISTENCY REFERENCE:
            - Maintain visual consistency with existing brand assets
            - Use similar visual elements, colors, and styling approach
            - Ensure this asset feels part of the same brand family
            """
        
        # Final prompt assembly
        full_prompt = f"""
        Create a {base_prompt} for {brand_strategy.business_name}.
        
        {brand_context}
        
        {consistency_context}
        
        {specific_context}
        
        {reference_context}
        
        TECHNICAL REQUIREMENTS:
        {requirements}
        - Dimensions: {config.get('dimensions', '512x512')}
        - Professional quality and resolution
        - Clean, modern design execution
        
        VARIANT: {variant}
        ADDITIONAL CONTEXT: {additional_context}
        
        Create a compelling {asset_type.value} that perfectly represents this brand identity and maintains visual consistency across the brand system.
        """
        
        return full_prompt
    
    async def _generate_with_gemini(self, prompt: str) -> Optional[str]:
        """Generate image using Gemini with error handling"""
        
        try:
            # Use executor for async handling
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, self.model.generate_content, prompt)
            
            # Extract image data
            if hasattr(response, 'candidates') and response.candidates:
                for candidate in response.candidates:
                    if hasattr(candidate, 'content') and candidate.content:
                        for part in candidate.content.parts:
                            if hasattr(part, 'inline_data') and part.inline_data and part.inline_data.data:
                                image_binary = part.inline_data.data
                                if image_binary:
                                    image_data = base64.b64encode(image_binary).decode('utf-8')
                                    return image_data
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error in Gemini generation: {str(e)}")
            return None
    
    async def _assess_asset_quality(self, image_data: str, brand_strategy: BrandStrategy) -> float:
        """Assess generated asset quality (simplified scoring)"""
        
        try:
            # Basic quality checks
            data_size = len(image_data)
            
            # Size-based quality score (larger generally better for our use case)
            size_score = min(1.0, data_size / 500000)  # Normalize to reasonable size
            
            # Could add more sophisticated quality assessment here
            # For now, return size-based score
            return size_score
            
        except Exception as e:
            self.logger.error(f"Error assessing asset quality: {str(e)}")
            return 0.5  # Default score
    
    async def _create_fallback_asset(
        self, 
        brand_strategy: BrandStrategy, 
        asset_type: AssetType, 
        variant: str
    ) -> GeneratedAsset:
        """Create branded fallback asset when generation fails"""
        
        try:
            # Create branded placeholder with PIL
            img = Image.new('RGB', (512, 512), color='#f8f9fa')
            draw = ImageDraw.Draw(img)
            
            # Use brand colors
            primary_colors = brand_strategy.visual_direction.color_strategy.get("primary_colors", ["#6366f1"])
            brand_color = primary_colors[0] if primary_colors else '#6366f1'
            
            # Create design based on asset type
            if asset_type == AssetType.LOGO:
                self._draw_logo_fallback(draw, brand_strategy.business_name, brand_color)
            elif asset_type == AssetType.BUSINESS_CARD:
                self._draw_business_card_fallback(draw, brand_strategy.business_name, brand_color)
            else:
                self._draw_generic_fallback(draw, brand_strategy.business_name, asset_type.value, brand_color)
            
            # Convert to base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            # Create metadata
            metadata = AssetMetadata(
                generation_prompt="Fallback asset generation",
                consistency_seed=self.consistency_seed,
                variant=variant,
                attempt_number=999,  # Indicates fallback
                generation_time=datetime.now(timezone.utc),
                quality_score=0.3,  # Lower score for fallback
                is_fallback=True
            )
            
            return GeneratedAsset(
                asset_type=asset_type,
                asset_url=f"data:image/png;base64,{image_data}",
                metadata=metadata,
                variant=variant
            )
            
        except Exception as e:
            self.logger.error(f"Error creating fallback asset: {str(e)}")
            
            # Final fallback - minimal asset
            minimal_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
            
            metadata = AssetMetadata(
                generation_prompt="Minimal fallback",
                consistency_seed="",
                variant=variant,
                attempt_number=999,
                generation_time=datetime.now(timezone.utc),
                quality_score=0.1,
                is_fallback=True
            )
            
            return GeneratedAsset(
                asset_type=asset_type,
                asset_url=f"data:image/png;base64,{minimal_data}",
                metadata=metadata,
                variant=variant
            )
    
    def _draw_logo_fallback(self, draw: ImageDraw.Draw, business_name: str, color: str):
        """Draw logo-style fallback"""
        # Circle background
        draw.ellipse([100, 100, 412, 412], fill=color, outline='white', width=4)
        
        # Business initial or name
        try:
            font = ImageFont.load_default()
            text = business_name[0].upper() if business_name else "B"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (512 - text_width) // 2
            y = (512 - text_height) // 2
            draw.text((x, y), text, fill='white', font=font)
        except:
            draw.text((240, 240), "LOGO", fill='white')
    
    def _draw_business_card_fallback(self, draw: ImageDraw.Draw, business_name: str, color: str):
        """Draw business card-style fallback"""
        # Card background
        draw.rectangle([50, 150, 462, 362], fill='white', outline=color, width=2)
        
        # Header bar
        draw.rectangle([50, 150, 462, 200], fill=color)
        
        # Business name
        try:
            font = ImageFont.load_default()
            draw.text((70, 210), business_name[:20], fill=color, font=font)
            draw.text((70, 230), "Business Card", fill='gray', font=font)
        except:
            draw.text((70, 210), "BUSINESS", fill=color)
            draw.text((70, 230), "CARD", fill='gray')
    
    def _draw_generic_fallback(self, draw: ImageDraw.Draw, business_name: str, asset_type: str, color: str):
        """Draw generic branded fallback"""
        # Background with brand color
        draw.rectangle([50, 50, 462, 462], fill=color, outline='white', width=4)
        
        # Text content
        try:
            font = ImageFont.load_default()
            draw.text((100, 200), business_name[:15], fill='white', font=font)
            draw.text((100, 220), asset_type.upper(), fill='white', font=font)
        except:
            draw.text((200, 200), "BRAND", fill='white')
            draw.text((200, 220), asset_type.upper(), fill='white')
    
    async def maintain_visual_consistency(
        self, 
        existing_assets: List[GeneratedAsset], 
        new_asset_type: AssetType,
        brand_strategy: BrandStrategy
    ) -> GeneratedAsset:
        """Generate new asset maintaining consistency with existing assets"""
        
        if not existing_assets:
            return await self.generate_asset(brand_strategy, new_asset_type)
        
        # Extract visual DNA from existing assets
        visual_dna = self._extract_visual_dna(existing_assets)
        
        # Generate with consistency constraints
        consistency_context = f"""
        VISUAL DNA CONSISTENCY:
        - Maintain visual harmony with existing {len(existing_assets)} brand assets
        - Visual consistency score target: >90%
        - Extracted visual patterns: {visual_dna}
        """
        
        return await self.generate_asset(
            brand_strategy=brand_strategy,
            asset_type=new_asset_type,
            additional_context=consistency_context,
            consistency_reference=existing_assets[0] if existing_assets else None
        )
    
    def _extract_visual_dna(self, assets: List[GeneratedAsset]) -> Dict[str, Any]:
        """Extract visual DNA patterns from existing assets"""
        
        # Simplified visual DNA extraction
        # In production, this could analyze actual image content
        
        dna = {
            "asset_count": len(assets),
            "consistency_seeds": list(set([
                asset.metadata.consistency_seed 
                for asset in assets 
                if asset.metadata.consistency_seed
            ])),
            "variants": [asset.variant for asset in assets],
            "generation_patterns": "consistent brand application"
        }
        
        return dna
    
    async def validate_asset_consistency(
        self, 
        asset: GeneratedAsset, 
        reference_assets: List[GeneratedAsset]
    ) -> float:
        """Validate consistency of generated asset against reference assets"""
        
        if not reference_assets:
            return 1.0
        
        # Simplified consistency validation
        # Check consistency seed matching
        asset_seed = asset.metadata.consistency_seed
        reference_seeds = [a.metadata.consistency_seed for a in reference_assets]
        
        if asset_seed in reference_seeds:
            return 0.9  # High consistency
        else:
            return 0.6  # Medium consistency
    
    async def generate_asset_variations(
        self,
        base_asset: GeneratedAsset,
        brand_strategy: BrandStrategy,
        variation_types: List[str]
    ) -> Dict[str, GeneratedAsset]:
        """Generate multiple variations of a base asset"""
        
        variations = {}
        
        for variation_type in variation_types:
            try:
                variation = await self.generate_asset(
                    brand_strategy=brand_strategy,
                    asset_type=base_asset.asset_type,
                    variant=variation_type,
                    additional_context=f"Create {variation_type} variation maintaining brand consistency",
                    consistency_reference=base_asset
                )
                variations[variation_type] = variation
                
            except Exception as e:
                self.logger.warning(f"Failed to generate {variation_type} variation: {str(e)}")
        
        return variations