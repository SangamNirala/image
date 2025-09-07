"""
Export Engine
Professional-grade export and packaging system for brand assets
"""

import logging
import json
import zipfile
import io
import base64
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timezone
from pathlib import Path

from models.brand_strategy import BrandStrategy
from models.visual_assets import AssetCollection, GeneratedAsset, AssetType, AssetExportConfiguration
from models.project_state import BrandProject

class ExportEngine:
    """Professional export engine for complete brand packages"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.export_templates = {
            "professional": {
                "include_guidelines": True,
                "include_color_palette": True,
                "include_usage_guide": True,
                "include_mockups": True,
                "folder_structure": "professional"
            },
            "basic": {
                "include_guidelines": False,
                "include_color_palette": True,
                "include_usage_guide": False,
                "include_mockups": False,
                "folder_structure": "simple"
            },
            "developer": {
                "include_guidelines": True,
                "include_color_palette": True,
                "include_usage_guide": True,
                "include_mockups": False,
                "folder_structure": "by_type",
                "include_css_colors": True,
                "include_json_metadata": True
            }
        }
    
    def generate_complete_brand_package(
        self, 
        project: BrandProject,
        export_config: Optional[AssetExportConfiguration] = None
    ) -> Dict[str, Any]:
        """Generate complete professional brand package"""
        
        if not project.is_ready_for_export():
            raise ValueError("Project not ready for export")
        
        # Use default professional export if no config provided
        if not export_config:
            export_config = AssetExportConfiguration(
                export_format="PNG",
                export_quality="high",
                include_variations=True,
                include_brand_guidelines=True,
                include_color_palette=True,
                include_usage_guide=True
            )
        
        self.logger.info(f"Generating complete brand package for project {project.id}")
        
        package_components = {}
        
        # 1. Brand Guidelines Document
        if export_config.include_brand_guidelines:
            guidelines = self.create_brand_guidelines_document(project.brand_strategy)
            package_components["brand_guidelines"] = guidelines
        
        # 2. Logo Suite
        logo_assets = project.asset_collection.get_assets_by_type(AssetType.LOGO)
        if logo_assets:
            logo_suite = self.package_logo_suite(logo_assets, export_config)
            package_components["logo_suite"] = logo_suite
        
        # 3. Marketing Assets
        marketing_assets = [
            asset for asset in project.asset_collection.assets 
            if asset.asset_type != AssetType.LOGO
        ]
        if marketing_assets:
            marketing_package = self.package_marketing_assets(marketing_assets, export_config)
            package_components["marketing_assets"] = marketing_package
        
        # 4. Color Palette Files
        if export_config.include_color_palette:
            color_palette = self.create_color_palette_files(project.brand_strategy)
            package_components["color_palette"] = color_palette
        
        # 5. Usage Guide
        if export_config.include_usage_guide:
            usage_guide = self.create_usage_guide(project)
            package_components["usage_guide"] = usage_guide
        
        # 6. Brand Summary
        brand_summary = self.create_brand_summary(project)
        package_components["brand_summary"] = brand_summary
        
        # 7. Create downloadable package
        package_zip = self.create_downloadable_package(
            package_components, 
            project, 
            export_config
        )
        
        return {
            "package_id": f"brand_package_{project.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "project_name": project.business_input.business_name,
            "components": list(package_components.keys()),
            "total_assets": len(project.asset_collection.assets),
            "package_size": len(package_zip),
            "download_data": package_zip,
            "export_timestamp": datetime.now(timezone.utc),
            "export_config": export_config.dict()
        }
    
    def create_brand_guidelines_document(self, brand_strategy: BrandStrategy) -> Dict[str, Any]:
        """Create comprehensive brand guidelines document"""
        
        guidelines = {
            "document_type": "brand_guidelines",
            "brand_name": brand_strategy.business_name,
            "version": "1.0",
            "created_date": datetime.now(timezone.utc).isoformat(),
            
            "brand_overview": {
                "brand_essence": brand_strategy.brand_personality.brand_essence,
                "brand_archetype": brand_strategy.brand_personality.brand_archetype,
                "personality_traits": brand_strategy.brand_personality.primary_traits,
                "brand_promise": brand_strategy.messaging_framework.brand_promise,
                "tagline": brand_strategy.messaging_framework.brand_tagline
            },
            
            "visual_identity": {
                "design_style": brand_strategy.visual_direction.design_style,
                "visual_mood": brand_strategy.visual_direction.visual_mood,
                "color_palette": {
                    "primary_colors": brand_strategy.visual_direction.color_strategy.get("primary_colors", []),
                    "secondary_colors": brand_strategy.visual_direction.color_strategy.get("secondary_colors", []),
                    "color_psychology": brand_strategy.visual_direction.color_strategy.get("color_psychology", "")
                },
                "typography": brand_strategy.visual_direction.typography_direction,
                "imagery_style": brand_strategy.visual_direction.imagery_style
            },
            
            "logo_guidelines": {
                "logo_concept": brand_strategy.visual_direction.logo_direction.get("logo_concept", ""),
                "usage_rules": brand_strategy.consistency_rules.get("visual_consistency", {}).get("logo_usage", {}),
                "minimum_sizes": "Logo should not be smaller than 24px in digital or 0.5 inches in print",
                "clear_space": "Maintain clear space equal to the height of the logo symbol",
                "approved_variations": ["Primary", "Horizontal", "Vertical", "Icon Only", "Monochrome"]
            },
            
            "messaging_guidelines": {
                "tone_of_voice": brand_strategy.brand_personality.tone_of_voice,
                "key_messages": brand_strategy.messaging_framework.key_messages,
                "communication_style": brand_strategy.messaging_framework.communication_guidelines,
                "brand_story": brand_strategy.messaging_framework.storytelling_framework
            },
            
            "application_guidelines": {
                "do_use": [
                    "Use approved color palette",
                    "Maintain consistent spacing",
                    "Follow typography hierarchy",
                    "Ensure high contrast for readability"
                ],
                "dont_use": [
                    "Don't distort or stretch the logo",
                    "Don't use unauthorized colors",
                    "Don't place logo on busy backgrounds",
                    "Don't use low-resolution assets"
                ]
            },
            
            "consistency_rules": brand_strategy.consistency_rules
        }
        
        return guidelines
    
    def package_logo_suite(
        self, 
        logo_assets: List[GeneratedAsset], 
        export_config: AssetExportConfiguration
    ) -> Dict[str, Any]:
        """Package logo assets with proper organization"""
        
        logo_package = {
            "package_type": "logo_suite",
            "total_variations": len(logo_assets),
            "assets": {}
        }
        
        for asset in logo_assets:
            variant_name = asset.variant or "primary"
            
            # Organize by variant
            logo_package["assets"][variant_name] = {
                "asset_id": asset.id,
                "variant": asset.variant,
                "quality_score": asset.metadata.quality_score,
                "file_data": asset.asset_url,
                "recommended_usage": self._get_logo_usage_recommendation(asset.variant),
                "technical_specs": {
                    "format": "PNG",
                    "background": "Transparent",
                    "recommended_sizes": ["512x512", "256x256", "128x128", "64x64", "32x32"]
                }
            }
        
        return logo_package
    
    def package_marketing_assets(
        self, 
        marketing_assets: List[GeneratedAsset], 
        export_config: AssetExportConfiguration
    ) -> Dict[str, Any]:
        """Package marketing and collateral assets"""
        
        # Group assets by type
        assets_by_type = {}
        for asset in marketing_assets:
            asset_type = asset.asset_type.value
            if asset_type not in assets_by_type:
                assets_by_type[asset_type] = []
            assets_by_type[asset_type].append(asset)
        
        marketing_package = {
            "package_type": "marketing_assets",
            "asset_categories": list(assets_by_type.keys()),
            "total_assets": len(marketing_assets),
            "assets_by_category": {}
        }
        
        for asset_type, assets in assets_by_type.items():
            category_package = {
                "category": asset_type,
                "asset_count": len(assets),
                "assets": []
            }
            
            for asset in assets:
                asset_info = {
                    "asset_id": asset.id,
                    "variant": asset.variant,
                    "quality_score": asset.metadata.quality_score,
                    "file_data": asset.asset_url,
                    "usage_context": self._get_asset_usage_context(asset.asset_type),
                    "technical_specs": self._get_asset_technical_specs(asset.asset_type)
                }
                category_package["assets"].append(asset_info)
            
            marketing_package["assets_by_category"][asset_type] = category_package
        
        return marketing_package
    
    def create_color_palette_files(self, brand_strategy: BrandStrategy) -> Dict[str, Any]:
        """Create color palette files in multiple formats"""
        
        primary_colors = brand_strategy.visual_direction.color_strategy.get("primary_colors", [])
        secondary_colors = brand_strategy.visual_direction.color_strategy.get("secondary_colors", [])
        
        color_palette = {
            "palette_name": f"{brand_strategy.business_name} Brand Colors",
            "primary_colors": [],
            "secondary_colors": [],
            "formats": {}
        }
        
        # Process primary colors
        for i, color in enumerate(primary_colors):
            color_info = {
                "name": f"Primary {i+1}",
                "hex": color,
                "rgb": self._hex_to_rgb(color),
                "cmyk": self._hex_to_cmyk(color),
                "usage": "Primary brand applications"
            }
            color_palette["primary_colors"].append(color_info)
        
        # Process secondary colors
        for i, color in enumerate(secondary_colors):
            color_info = {
                "name": f"Secondary {i+1}",
                "hex": color,
                "rgb": self._hex_to_rgb(color),
                "cmyk": self._hex_to_cmyk(color),
                "usage": "Supporting brand applications"
            }
            color_palette["secondary_colors"].append(color_info)
        
        # Create different format exports
        color_palette["formats"] = {
            "css_variables": self._create_css_variables(primary_colors, secondary_colors),
            "json_palette": self._create_json_palette(primary_colors, secondary_colors),
            "adobe_swatches": self._create_adobe_swatch_info(primary_colors, secondary_colors)
        }
        
        return color_palette
    
    def create_usage_guide(self, project: BrandProject) -> Dict[str, Any]:
        """Create comprehensive usage guide"""
        
        usage_guide = {
            "guide_title": f"{project.business_input.business_name} Brand Usage Guide",
            "created_date": datetime.now(timezone.utc).isoformat(),
            
            "quick_start": {
                "logo_usage": "Use the primary logo for most applications. Switch to horizontal or vertical layouts as needed for space constraints.",
                "color_usage": "Primary colors should dominate brand applications. Use secondary colors for accents and supporting elements.",
                "typography": "Maintain consistent typography hierarchy across all materials.",
                "spacing": "Always maintain adequate white space around brand elements."
            },
            
            "asset_specific_guidance": {},
            
            "common_applications": {
                "business_cards": {
                    "recommended_logo": "primary or horizontal",
                    "color_approach": "primary colors with white background",
                    "typography": "clean, professional fonts"
                },
                "letterhead": {
                    "recommended_logo": "horizontal at top or primary in corner",
                    "color_approach": "minimal color usage, primary color accent",
                    "layout": "clean, professional layout with ample white space"
                },
                "social_media": {
                    "recommended_logo": "icon version for profile, primary for posts",
                    "color_approach": "bold use of primary colors",
                    "style": "consistent with brand personality"
                },
                "marketing_materials": {
                    "recommended_logo": "primary logo prominently displayed",
                    "color_approach": "full color palette utilization",
                    "messaging": "incorporate key brand messages"
                }
            },
            
            "technical_specifications": {
                "minimum_logo_sizes": {
                    "digital": "24px minimum height",
                    "print": "0.5 inches minimum height"
                },
                "file_formats": {
                    "web": "PNG with transparent background",
                    "print": "High-resolution PNG or vector formats",
                    "social_media": "PNG optimized for platform requirements"
                },
                "color_reproduction": {
                    "digital": "Use RGB color values",
                    "print": "Use CMYK color values",
                    "web": "Use hex color codes"
                }
            },
            
            "brand_maintenance": {
                "consistency_checklist": [
                    "Is the logo properly sized and positioned?",
                    "Are brand colors used correctly?",
                    "Does the messaging align with brand voice?",
                    "Is the overall design consistent with brand personality?"
                ],
                "quality_standards": [
                    "Use high-resolution assets for all applications",
                    "Ensure proper contrast for accessibility",
                    "Maintain brand color accuracy",
                    "Review all materials for consistency before use"
                ]
            }
        }
        
        # Add asset-specific guidance
        if project.asset_collection:
            for asset in project.asset_collection.assets:
                asset_type = asset.asset_type.value
                usage_guide["asset_specific_guidance"][asset_type] = {
                    "recommended_usage": self._get_asset_usage_context(asset.asset_type),
                    "quality_score": asset.metadata.quality_score,
                    "variant": asset.variant,
                    "best_practices": self._get_asset_best_practices(asset.asset_type)
                }
        
        return usage_guide
    
    def create_brand_summary(self, project: BrandProject) -> Dict[str, Any]:
        """Create executive brand summary"""
        
        summary = {
            "brand_name": project.business_input.business_name,
            "project_id": project.id,
            "created_date": project.created_at.isoformat(),
            "completion_date": datetime.now(timezone.utc).isoformat(),
            
            "brand_essence": {
                "core_message": project.brand_strategy.brand_personality.brand_essence,
                "brand_archetype": project.brand_strategy.brand_personality.brand_archetype,
                "key_traits": project.brand_strategy.brand_personality.primary_traits[:3],
                "tagline": project.brand_strategy.messaging_framework.brand_tagline
            },
            
            "visual_identity_summary": {
                "design_style": project.brand_strategy.visual_direction.design_style,
                "primary_colors": project.brand_strategy.get_color_palette()[:3],
                "visual_mood": project.brand_strategy.visual_direction.visual_mood
            },
            
            "deliverables_summary": {
                "total_assets": len(project.asset_collection.assets) if project.asset_collection else 0,
                "asset_types": list(set([a.asset_type.value for a in project.asset_collection.assets])) if project.asset_collection else [],
                "average_quality_score": project.asset_collection.average_quality_score if project.asset_collection else 0,
                "completion_percentage": project.metadata.completion_percentage
            },
            
            "next_steps": [
                "Review all brand assets for consistency",
                "Implement brand identity across all touchpoints",
                "Train team members on brand guidelines",
                "Monitor brand application for consistency",
                "Plan for future brand asset needs"
            ]
        }
        
        return summary
    
    def create_downloadable_package(
        self, 
        components: Dict[str, Any], 
        project: BrandProject,
        export_config: AssetExportConfiguration
    ) -> str:
        """Create downloadable ZIP package"""
        
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            
            # Create folder structure
            brand_name = project.business_input.business_name.replace(" ", "_")
            base_folder = f"{brand_name}_Brand_Package"
            
            # Add brand guidelines
            if "brand_guidelines" in components:
                guidelines_json = json.dumps(components["brand_guidelines"], indent=2)
                zip_file.writestr(f"{base_folder}/Brand_Guidelines.json", guidelines_json)
            
            # Add logo suite
            if "logo_suite" in components:
                logo_suite = components["logo_suite"]
                for variant, asset_info in logo_suite["assets"].items():
                    # Decode base64 image data
                    if asset_info["file_data"].startswith("data:image"):
                        image_data = asset_info["file_data"].split(",")[1]
                        image_binary = base64.b64decode(image_data)
                        filename = f"{base_folder}/Logo_Suite/{variant}_logo.png"
                        zip_file.writestr(filename, image_binary)
            
            # Add marketing assets
            if "marketing_assets" in components:
                marketing_assets = components["marketing_assets"]
                for category, category_data in marketing_assets["assets_by_category"].items():
                    for i, asset in enumerate(category_data["assets"]):
                        if asset["file_data"].startswith("data:image"):
                            image_data = asset["file_data"].split(",")[1]
                            image_binary = base64.b64decode(image_data)
                            filename = f"{base_folder}/Marketing_Assets/{category.title()}/{category}_{i+1}.png"
                            zip_file.writestr(filename, image_binary)
            
            # Add color palette
            if "color_palette" in components:
                palette_json = json.dumps(components["color_palette"], indent=2)
                zip_file.writestr(f"{base_folder}/Color_Palette.json", palette_json)
                
                # Add CSS variables
                css_content = self._generate_css_file(components["color_palette"])
                zip_file.writestr(f"{base_folder}/brand_colors.css", css_content)
            
            # Add usage guide
            if "usage_guide" in components:
                guide_json = json.dumps(components["usage_guide"], indent=2)
                zip_file.writestr(f"{base_folder}/Usage_Guide.json", guide_json)
            
            # Add brand summary
            if "brand_summary" in components:
                summary_json = json.dumps(components["brand_summary"], indent=2)
                zip_file.writestr(f"{base_folder}/Brand_Summary.json", summary_json)
            
            # Add README file
            readme_content = self._create_readme_content(project, components)
            zip_file.writestr(f"{base_folder}/README.txt", readme_content)
        
        zip_buffer.seek(0)
        zip_data = zip_buffer.getvalue()
        return base64.b64encode(zip_data).decode('utf-8')
    
    def _get_logo_usage_recommendation(self, variant: str) -> str:
        """Get usage recommendation for logo variant"""
        recommendations = {
            "primary": "Use for most brand applications, websites, and general marketing",
            "horizontal": "Use when horizontal space is limited, such as headers or banners",
            "vertical": "Use when vertical space is limited, such as sidebars or tall formats",
            "icon_only": "Use for favicons, social media profiles, or when space is very limited",
            "monochrome": "Use for single-color applications, stamps, or when color printing is not available"
        }
        return recommendations.get(variant, "General brand applications")
    
    def _get_asset_usage_context(self, asset_type: AssetType) -> str:
        """Get usage context for asset type"""
        contexts = {
            AssetType.BUSINESS_CARD: "Professional networking, trade shows, client meetings",
            AssetType.LETTERHEAD: "Official correspondence, contracts, formal communications",
            AssetType.SOCIAL_MEDIA_POST: "Instagram, Facebook, Twitter posts and marketing campaigns",
            AssetType.FLYER: "Event promotion, product launches, general marketing",
            AssetType.BANNER: "Website headers, trade show displays, online advertising",
            AssetType.POSTER: "Event promotion, office displays, marketing campaigns"
        }
        return contexts.get(asset_type, "General marketing and brand applications")
    
    def _get_asset_technical_specs(self, asset_type: AssetType) -> Dict[str, str]:
        """Get technical specifications for asset type"""
        specs = {
            AssetType.BUSINESS_CARD: {"format": "PNG", "dimensions": "3.5x2 inches at 300 DPI", "background": "White or transparent"},
            AssetType.LETTERHEAD: {"format": "PNG", "dimensions": "8.5x11 inches at 300 DPI", "background": "White"},
            AssetType.SOCIAL_MEDIA_POST: {"format": "PNG", "dimensions": "1080x1080 pixels", "background": "Various"},
            AssetType.FLYER: {"format": "PNG", "dimensions": "8.5x11 inches at 300 DPI", "background": "White or colored"},
            AssetType.BANNER: {"format": "PNG", "dimensions": "1200x400 pixels", "background": "Various"},
            AssetType.POSTER: {"format": "PNG", "dimensions": "18x24 inches at 300 DPI", "background": "Various"}
        }
        return specs.get(asset_type, {"format": "PNG", "dimensions": "Variable", "background": "Transparent"})
    
    def _get_asset_best_practices(self, asset_type: AssetType) -> List[str]:
        """Get best practices for asset type"""
        practices = {
            AssetType.BUSINESS_CARD: [
                "Ensure text is readable at actual size",
                "Use high-contrast colors for text",
                "Include essential contact information only",
                "Maintain consistent branding with other materials"
            ],
            AssetType.LETTERHEAD: [
                "Keep design minimal and professional",
                "Ensure adequate space for letter content",
                "Use consistent typography and spacing",
                "Include necessary contact information"
            ],
            AssetType.SOCIAL_MEDIA_POST: [
                "Optimize for platform-specific dimensions",
                "Use bold, eye-catching visuals",
                "Ensure brand consistency across platforms",
                "Consider mobile viewing experience"
            ]
        }
        return practices.get(asset_type, ["Maintain brand consistency", "Use high-quality images", "Follow brand guidelines"])
    
    def _hex_to_rgb(self, hex_color: str) -> str:
        """Convert hex color to RGB"""
        hex_color = hex_color.lstrip('#')
        try:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return f"rgb({r}, {g}, {b})"
        except:
            return "rgb(0, 0, 0)"
    
    def _hex_to_cmyk(self, hex_color: str) -> str:
        """Convert hex color to approximate CMYK (simplified conversion)"""
        # This is a simplified conversion - for production use a proper color library
        return "cmyk(0%, 0%, 0%, 100%)"  # Placeholder
    
    def _create_css_variables(self, primary_colors: List[str], secondary_colors: List[str]) -> str:
        """Create CSS variables for colors"""
        css_vars = ":root {\n"
        
        for i, color in enumerate(primary_colors):
            css_vars += f"  --brand-primary-{i+1}: {color};\n"
        
        for i, color in enumerate(secondary_colors):
            css_vars += f"  --brand-secondary-{i+1}: {color};\n"
        
        css_vars += "}"
        return css_vars
    
    def _create_json_palette(self, primary_colors: List[str], secondary_colors: List[str]) -> Dict[str, Any]:
        """Create JSON color palette"""
        return {
            "primary": primary_colors,
            "secondary": secondary_colors,
            "format": "hex"
        }
    
    def _create_adobe_swatch_info(self, primary_colors: List[str], secondary_colors: List[str]) -> Dict[str, Any]:
        """Create Adobe swatch information"""
        return {
            "format": "Adobe Swatch Exchange (.ase)",
            "colors": primary_colors + secondary_colors,
            "note": "Import these hex values into your Adobe Creative Suite applications"
        }
    
    def _generate_css_file(self, color_palette: Dict[str, Any]) -> str:
        """Generate CSS file with brand colors"""
        css_content = "/* Brand Color Palette */\n\n"
        css_content += color_palette["formats"]["css_variables"]
        css_content += "\n\n/* Usage Examples */\n"
        css_content += ".brand-primary { color: var(--brand-primary-1); }\n"
        css_content += ".brand-bg-primary { background-color: var(--brand-primary-1); }\n"
        return css_content
    
    def _create_readme_content(self, project: BrandProject, components: Dict[str, Any]) -> str:
        """Create README content for the package"""
        
        readme = f"""
{project.business_input.business_name} Brand Package
=====================================

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Project ID: {project.id}

Package Contents:
"""
        
        if "brand_guidelines" in components:
            readme += "- Brand_Guidelines.json: Complete brand strategy and guidelines\n"
        
        if "logo_suite" in components:
            readme += "- Logo_Suite/: All logo variations in PNG format\n"
        
        if "marketing_assets" in components:
            readme += "- Marketing_Assets/: Business cards, letterheads, and marketing materials\n"
        
        if "color_palette" in components:
            readme += "- Color_Palette.json: Brand colors in multiple formats\n"
            readme += "- brand_colors.css: CSS variables for web development\n"
        
        if "usage_guide" in components:
            readme += "- Usage_Guide.json: Comprehensive usage instructions\n"
        
        readme += "- Brand_Summary.json: Executive summary of the brand identity\n"
        
        readme += f"""

Quick Start:
1. Review the Brand_Guidelines.json for complete brand strategy
2. Use logo files from Logo_Suite/ for various applications
3. Reference Usage_Guide.json for implementation best practices
4. Import brand_colors.css for web development projects

Brand Colors:
"""
        
        if "color_palette" in components:
            for color in components["color_palette"]["primary_colors"]:
                readme += f"- {color['name']}: {color['hex']}\n"
        
        readme += """
For questions or additional brand assets, refer to the Brand_Guidelines.json file.

Generated by BrandForge AI - Professional Brand Identity Generator
"""
        
        return readme