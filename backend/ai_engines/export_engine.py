import os
import json
import logging
import zipfile
import io
import base64
from typing import Dict, Any, List, Optional
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as ReportLabImage, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib import colors
from PIL import Image
from models.brand_strategy import BrandStrategy
from models.visual_assets import GeneratedAsset
from models.project_state import BrandProject

class ProfessionalExportEngine:
    """Enterprise-grade asset packaging and export system"""
    
    def __init__(self):
        self.export_formats = ['png', 'jpg', 'svg', 'pdf']
        self.package_types = ['basic', 'professional', 'enterprise']
        
    async def generate_complete_brand_package(
        self,
        project: BrandProject,
        package_type: str = 'professional',
        custom_requirements: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate complete professional brand package"""
        
        try:
            # Create package structure
            package_structure = self._create_package_structure(project, package_type)
            
            # Generate brand guidelines document
            brand_guidelines = await self._create_brand_guidelines_pdf(project)
            
            # Package logo suite with multiple formats
            logo_suite = self._package_logo_suite(project.generated_assets)
            
            # Create color palette files
            color_palette_files = self._create_color_palette_files(project.brand_strategy)
            
            # Generate marketing templates
            marketing_templates = self._package_marketing_assets(project.generated_assets)
            
            # Create usage examples and mockups
            usage_examples = await self._generate_usage_examples(project)
            
            # Generate asset inventory
            asset_inventory = self._create_asset_inventory(project.generated_assets)
            
            # Create downloadable ZIP package
            zip_package = await self._create_downloadable_package({
                'brand_guidelines': brand_guidelines,
                'logo_suite': logo_suite,
                'color_palette': color_palette_files,
                'marketing_assets': marketing_templates,
                'usage_examples': usage_examples,
                'asset_inventory': asset_inventory
            }, project.business_input.business_name)
            
            package_info = {
                'package_type': package_type,
                'total_assets': len(project.generated_assets),
                'package_size': len(zip_package),
                'created_at': datetime.now().isoformat(),
                'business_name': project.business_input.business_name,
                'package_contents': package_structure,
                'download_url': f"data:application/zip;base64,{zip_package}"
            }
            
            return package_info
            
        except Exception as e:
            logging.error(f"Error generating brand package: {str(e)}")
            return await self._create_fallback_package(project)
    
    async def create_brand_guidelines_pdf(self, project: BrandProject) -> str:
        """Create comprehensive brand guidelines PDF document"""
        
        return await self._create_brand_guidelines_pdf(project)
    
    async def export_assets_in_formats(
        self,
        assets: List[GeneratedAsset],
        formats: List[str],
        quality_settings: Optional[Dict[str, Any]] = None
    ) -> Dict[str, List[str]]:
        """Export assets in multiple formats with quality settings"""
        
        exported_assets = {}
        
        for format_type in formats:
            exported_assets[format_type] = []
            
            for asset in assets:
                try:
                    converted_asset = await self._convert_asset_format(asset, format_type, quality_settings)
                    exported_assets[format_type].append(converted_asset)
                except Exception as e:
                    logging.warning(f"Failed to convert {asset.asset_type} to {format_type}: {str(e)}")
        
        return exported_assets
    
    def create_asset_usage_guide(self, assets: List[GeneratedAsset], brand_strategy: BrandStrategy) -> Dict[str, Any]:
        """Create comprehensive asset usage guide"""
        
        usage_guide = {
            'overview': {
                'brand_name': brand_strategy.business_name,
                'total_assets': len(assets),
                'asset_categories': list(set([asset.asset_type for asset in assets]))
            },
            'logo_usage': self._create_logo_usage_guide(assets),
            'marketing_assets': self._create_marketing_usage_guide(assets),
            'technical_specifications': self._create_technical_specifications(assets),
            'best_practices': self._create_usage_best_practices(brand_strategy),
            'troubleshooting': self._create_usage_troubleshooting()
        }
        
        return usage_guide
    
    async def generate_mockup_presentations(
        self,
        assets: List[GeneratedAsset],
        brand_strategy: BrandStrategy,
        mockup_types: List[str] = None
    ) -> List[str]:
        """Generate realistic mockup presentations of brand assets"""
        
        if not mockup_types:
            mockup_types = ['business_card', 'letterhead', 'digital_presentation']
        
        mockups = []
        
        for mockup_type in mockup_types:
            try:
                mockup = await self._create_asset_mockup(assets, brand_strategy, mockup_type)
                mockups.append(mockup)
            except Exception as e:
                logging.warning(f"Failed to create {mockup_type} mockup: {str(e)}")
        
        return mockups
    
    def _create_package_structure(self, project: BrandProject, package_type: str) -> Dict[str, Any]:
        """Define package structure based on type"""
        
        structures = {
            'basic': {
                'folders': ['logos', 'colors', 'guidelines'],
                'included_assets': ['primary_logo', 'color_palette', 'basic_guidelines'],
                'formats': ['png', 'pdf']
            },
            'professional': {
                'folders': ['logos', 'marketing_assets', 'colors', 'guidelines', 'templates'],
                'included_assets': ['logo_suite', 'marketing_assets', 'color_system', 'comprehensive_guidelines', 'templates'],
                'formats': ['png', 'jpg', 'pdf', 'svg']
            },
            'enterprise': {
                'folders': ['logos', 'marketing_assets', 'colors', 'guidelines', 'templates', 'mockups', 'usage_examples'],
                'included_assets': ['complete_logo_suite', 'full_marketing_suite', 'color_system', 'detailed_guidelines', 'template_library', 'mockup_presentations'],
                'formats': ['png', 'jpg', 'pdf', 'svg', 'eps']
            }
        }
        
        return structures.get(package_type, structures['professional'])
    
    async def _create_brand_guidelines_pdf(self, project: BrandProject) -> str:
        """Create comprehensive brand guidelines PDF"""
        
        try:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
            
            # Get styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=HexColor(project.brand_strategy.color_palette[0] if project.brand_strategy.color_palette else '#000000'),
                spaceAfter=30
            )
            
            story = []
            
            # Title Page
            story.append(Paragraph(f"{project.business_input.business_name}", title_style))
            story.append(Paragraph("Brand Guidelines", styles['Heading2']))
            story.append(Spacer(1, 0.5*inch))
            
            # Brand Overview
            story.append(Paragraph("Brand Overview", styles['Heading2']))
            story.append(Paragraph(f"Business: {project.business_input.business_description}", styles['Normal']))
            story.append(Paragraph(f"Industry: {project.business_input.industry}", styles['Normal']))
            story.append(Paragraph(f"Target Audience: {project.business_input.target_audience}", styles['Normal']))
            story.append(Spacer(1, 0.3*inch))
            
            # Brand Personality
            if project.brand_strategy:
                story.append(Paragraph("Brand Personality", styles['Heading2']))
                
                personality = project.brand_strategy.brand_personality
                if 'primary_traits' in personality:
                    traits_text = ", ".join(personality['primary_traits'])
                    story.append(Paragraph(f"Primary Traits: {traits_text}", styles['Normal']))
                
                if 'brand_archetype' in personality:
                    story.append(Paragraph(f"Brand Archetype: {personality['brand_archetype']}", styles['Normal']))
                
                if 'tone_of_voice' in personality:
                    story.append(Paragraph(f"Tone of Voice: {personality['tone_of_voice']}", styles['Normal']))
                
                story.append(Spacer(1, 0.3*inch))
                
                # Color Palette
                story.append(Paragraph("Color Palette", styles['Heading2']))
                for i, color in enumerate(project.brand_strategy.color_palette):
                    color_name = ['Primary', 'Secondary', 'Accent 1', 'Accent 2', 'Neutral'][i] if i < 5 else f'Color {i+1}'
                    story.append(Paragraph(f"{color_name}: {color}", styles['Normal']))
                
                story.append(Spacer(1, 0.3*inch))
                
                # Visual Direction
                if project.brand_strategy.visual_direction:
                    story.append(Paragraph("Visual Direction", styles['Heading2']))
                    for key, value in project.brand_strategy.visual_direction.items():
                        if isinstance(value, str):
                            formatted_key = key.replace('_', ' ').title()
                            story.append(Paragraph(f"{formatted_key}: {value}", styles['Normal']))
                
                story.append(Spacer(1, 0.3*inch))
                
                # Messaging Framework
                if project.brand_strategy.messaging_framework:
                    story.append(Paragraph("Messaging Framework", styles['Heading2']))
                    messaging = project.brand_strategy.messaging_framework
                    
                    if 'tagline' in messaging:
                        story.append(Paragraph(f"Tagline: {messaging['tagline']}", styles['Normal']))
                    
                    if 'brand_promise' in messaging:
                        story.append(Paragraph(f"Brand Promise: {messaging['brand_promise']}", styles['Normal']))
                    
                    if 'unique_value_proposition' in messaging:
                        story.append(Paragraph(f"Unique Value Proposition: {messaging['unique_value_proposition']}", styles['Normal']))
                
                story.append(Spacer(1, 0.3*inch))
            
            # Asset Inventory
            story.append(Paragraph("Asset Inventory", styles['Heading2']))
            asset_data = []
            asset_data.append(['Asset Type', 'Usage', 'Format'])
            
            for asset in project.generated_assets:
                asset_type = asset.asset_type.replace('_', ' ').title()
                usage = self._get_asset_usage_description(asset.asset_type)
                format_info = "PNG (Digital/Print Ready)"
                asset_data.append([asset_type, usage, format_info])
            
            if len(asset_data) > 1:
                asset_table = Table(asset_data)
                asset_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(asset_table)
            
            # Usage Guidelines
            story.append(Spacer(1, 0.3*inch))
            story.append(Paragraph("Usage Guidelines", styles['Heading2']))
            story.append(Paragraph("• Maintain consistent use of brand colors across all materials", styles['Normal']))
            story.append(Paragraph("• Ensure adequate white space around logo and key elements", styles['Normal']))
            story.append(Paragraph("• Use high-quality versions of assets for professional applications", styles['Normal']))
            story.append(Paragraph("• Maintain brand personality and tone across all communications", styles['Normal']))
            
            # Build PDF
            doc.build(story)
            buffer.seek(0)
            
            # Convert to base64
            pdf_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()
            
            return pdf_data
            
        except Exception as e:
            logging.error(f"Error creating brand guidelines PDF: {str(e)}")
            return self._create_fallback_pdf(project)
    
    def _package_logo_suite(self, assets: List[GeneratedAsset]) -> Dict[str, Any]:
        """Package logo suite with proper organization"""
        
        logo_assets = [asset for asset in assets if 'logo' in asset.asset_type]
        
        logo_suite = {
            'primary_logo': None,
            'variations': [],
            'formats': ['PNG'],
            'usage_notes': {
                'primary': 'Use for main brand representation',
                'horizontal': 'Use in wide layouts and headers',
                'vertical': 'Use in narrow spaces and mobile',
                'icon_only': 'Use when space is very limited',
                'monochrome': 'Use when color reproduction is limited'
            }
        }
        
        for asset in logo_assets:
            if 'primary' in asset.asset_type:
                logo_suite['primary_logo'] = {
                    'url': asset.asset_url,
                    'metadata': asset.metadata
                }
            else:
                logo_suite['variations'].append({
                    'type': asset.asset_type,
                    'url': asset.asset_url,
                    'metadata': asset.metadata
                })
        
        return logo_suite
    
    def _create_color_palette_files(self, brand_strategy: BrandStrategy) -> Dict[str, Any]:
        """Create comprehensive color palette files"""
        
        if not brand_strategy or not brand_strategy.color_palette:
            return {}
        
        color_info = {
            'palette': [],
            'usage_guidelines': {},
            'accessibility_notes': 'Ensure sufficient contrast ratios for text readability'
        }
        
        color_names = ['Primary', 'Secondary', 'Accent 1', 'Accent 2', 'Neutral']
        
        for i, color_hex in enumerate(brand_strategy.color_palette):
            color_name = color_names[i] if i < len(color_names) else f'Color {i+1}'
            
            color_info['palette'].append({
                'name': color_name,
                'hex': color_hex,
                'rgb': self._hex_to_rgb(color_hex),
                'usage': self._get_color_usage(color_name.lower())
            })
        
        return color_info
    
    def _package_marketing_assets(self, assets: List[GeneratedAsset]) -> Dict[str, Any]:
        """Package marketing assets with organization"""
        
        marketing_assets = [asset for asset in assets if 'logo' not in asset.asset_type]
        
        packaged = {
            'business_materials': [],
            'digital_assets': [],
            'promotional_materials': [],
            'usage_guidelines': {}
        }
        
        business_types = ['business_card', 'letterhead']
        digital_types = ['social_media', 'banner']
        promotional_types = ['flyer']
        
        for asset in marketing_assets:
            asset_data = {
                'type': asset.asset_type,
                'url': asset.asset_url,
                'metadata': asset.metadata,
                'usage': self._get_asset_usage_description(asset.asset_type)
            }
            
            if asset.asset_type in business_types:
                packaged['business_materials'].append(asset_data)
            elif asset.asset_type in digital_types:
                packaged['digital_assets'].append(asset_data)
            elif asset.asset_type in promotional_types:
                packaged['promotional_materials'].append(asset_data)
        
        return packaged
    
    async def _generate_usage_examples(self, project: BrandProject) -> Dict[str, Any]:
        """Generate usage examples and applications"""
        
        examples = {
            'digital_applications': [
                'Website headers and branding',
                'Social media profiles and posts',
                'Email signatures and templates',
                'Digital presentations'
            ],
            'print_applications': [
                'Business cards and stationery',
                'Brochures and marketing materials',
                'Signage and displays',
                'Product packaging'
            ],
            'best_practices': [
                'Maintain consistent brand colors across all materials',
                'Ensure logo has adequate clear space',
                'Use appropriate logo variation for each context',
                'Maintain brand personality in all communications'
            ]
        }
        
        return examples
    
    def _create_asset_inventory(self, assets: List[GeneratedAsset]) -> Dict[str, Any]:
        """Create comprehensive asset inventory"""
        
        inventory = {
            'total_assets': len(assets),
            'asset_breakdown': {},
            'creation_date': datetime.now().isoformat(),
            'assets': []
        }
        
        # Count asset types
        for asset in assets:
            asset_type = asset.asset_type
            if asset_type not in inventory['asset_breakdown']:
                inventory['asset_breakdown'][asset_type] = 0
            inventory['asset_breakdown'][asset_type] += 1
            
            # Add asset details
            inventory['assets'].append({
                'id': asset.id,
                'type': asset_type,
                'created_at': asset.created_at.isoformat() if hasattr(asset.created_at, 'isoformat') else str(asset.created_at),
                'metadata': asset.metadata,
                'usage': self._get_asset_usage_description(asset_type)
            })
        
        return inventory
    
    async def _create_downloadable_package(self, package_contents: Dict[str, Any], business_name: str) -> str:
        """Create downloadable ZIP package"""
        
        try:
            zip_buffer = io.BytesIO()
            
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                # Add brand guidelines PDF
                if package_contents.get('brand_guidelines'):
                    pdf_data = base64.b64decode(package_contents['brand_guidelines'])
                    zip_file.writestr(f"{business_name}_Brand_Guidelines.pdf", pdf_data)
                
                # Add logo suite
                logo_suite = package_contents.get('logo_suite', {})
                if logo_suite.get('primary_logo'):
                    logo_data = self._extract_base64_data(logo_suite['primary_logo']['url'])
                    if logo_data:
                        zip_file.writestr(f"logos/{business_name}_Primary_Logo.png", logo_data)
                
                for i, variation in enumerate(logo_suite.get('variations', [])):
                    logo_data = self._extract_base64_data(variation['url'])
                    if logo_data:
                        variant_name = variation['type'].replace('logo_', '').title()
                        zip_file.writestr(f"logos/{business_name}_{variant_name}_Logo.png", logo_data)
                
                # Add marketing assets
                marketing_assets = package_contents.get('marketing_assets', {})
                for category, assets in marketing_assets.items():
                    if isinstance(assets, list):
                        for asset in assets:
                            asset_data = self._extract_base64_data(asset['url'])
                            if asset_data:
                                asset_name = asset['type'].replace('_', ' ').title()
                                zip_file.writestr(f"marketing_assets/{asset_name}.png", asset_data)
                
                # Add color palette information
                color_palette = package_contents.get('color_palette', {})
                if color_palette:
                    color_json = json.dumps(color_palette, indent=2)
                    zip_file.writestr(f"colors/{business_name}_Color_Palette.json", color_json)
                
                # Add asset inventory
                inventory = package_contents.get('asset_inventory', {})
                if inventory:
                    inventory_json = json.dumps(inventory, indent=2)
                    zip_file.writestr(f"{business_name}_Asset_Inventory.json", inventory_json)
                
                # Add usage examples
                usage_examples = package_contents.get('usage_examples', {})
                if usage_examples:
                    usage_json = json.dumps(usage_examples, indent=2)
                    zip_file.writestr(f"{business_name}_Usage_Guide.json", usage_json)
            
            zip_buffer.seek(0)
            zip_data = base64.b64encode(zip_buffer.getvalue()).decode('utf-8')
            zip_buffer.close()
            
            return zip_data
            
        except Exception as e:
            logging.error(f"Error creating ZIP package: {str(e)}")
            return ""
    
    async def _create_fallback_package(self, project: BrandProject) -> Dict[str, Any]:
        """Create fallback package when main generation fails"""
        
        return {
            'package_type': 'basic',
            'total_assets': len(project.generated_assets),
            'package_size': 0,
            'created_at': datetime.now().isoformat(),
            'business_name': project.business_input.business_name,
            'error': 'Package generation encountered issues',
            'available_assets': [asset.asset_type for asset in project.generated_assets]
        }
    
    def _create_fallback_pdf(self, project: BrandProject) -> str:
        """Create simple fallback PDF"""
        
        try:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            
            styles = getSampleStyleSheet()
            story = []
            
            story.append(Paragraph(f"{project.business_input.business_name} Brand Guidelines", styles['Title']))
            story.append(Spacer(1, 0.5*inch))
            story.append(Paragraph("Basic brand information and guidelines", styles['Normal']))
            
            doc.build(story)
            buffer.seek(0)
            
            pdf_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()
            
            return pdf_data
            
        except Exception:
            return ""
    
    def _extract_base64_data(self, data_url: str) -> bytes:
        """Extract binary data from base64 data URL"""
        
        try:
            if data_url.startswith('data:'):
                # Remove the data URL prefix
                base64_data = data_url.split(',')[1]
                return base64.b64decode(base64_data)
            return b""
        except Exception:
            return b""
    
    def _hex_to_rgb(self, hex_color: str) -> Dict[str, int]:
        """Convert hex color to RGB"""
        
        try:
            hex_color = hex_color.lstrip('#')
            return {
                'r': int(hex_color[0:2], 16),
                'g': int(hex_color[2:4], 16),
                'b': int(hex_color[4:6], 16)
            }
        except:
            return {'r': 0, 'g': 0, 'b': 0}
    
    def _get_color_usage(self, color_name: str) -> str:
        """Get usage description for color"""
        
        usage_map = {
            'primary': 'Main brand color for headers, logos, and key elements',
            'secondary': 'Supporting color for accents and highlights',
            'accent 1': 'First accent color for emphasis and call-to-action elements',
            'accent 2': 'Second accent color for variety and visual interest',
            'neutral': 'Neutral color for text, backgrounds, and subtle elements'
        }
        
        return usage_map.get(color_name, 'General purpose brand color')
    
    def _get_asset_usage_description(self, asset_type: str) -> str:
        """Get usage description for asset type"""
        
        usage_map = {
            'logo_primary': 'Primary logo for main brand representation',
            'logo_horizontal': 'Horizontal logo for wide layouts',
            'logo_vertical': 'Vertical logo for narrow spaces',
            'logo_icon_only': 'Icon-only logo for small spaces',
            'logo_monochrome': 'Single-color logo for limited color reproduction',
            'business_card': 'Professional business card design',
            'letterhead': 'Business letterhead for official correspondence',
            'social_media_post': 'Social media post template',
            'flyer': 'Promotional flyer for marketing',
            'banner': 'Web banner for digital marketing'
        }
        
        return usage_map.get(asset_type, f'Professional {asset_type.replace("_", " ")} for business use')
    
    def _create_logo_usage_guide(self, assets: List[GeneratedAsset]) -> Dict[str, Any]:
        """Create detailed logo usage guide"""
        
        logo_assets = [asset for asset in assets if 'logo' in asset.asset_type]
        
        guide = {
            'available_variations': [asset.asset_type for asset in logo_assets],
            'usage_scenarios': {
                'primary_logo': 'Main brand representation, websites, business cards',
                'horizontal_logo': 'Website headers, email signatures, wide layouts',
                'vertical_logo': 'Mobile interfaces, narrow columns, vertical designs',
                'icon_only': 'Social media profiles, favicons, app icons',
                'monochrome': 'Newspaper ads, single-color printing, embossing'
            },
            'technical_requirements': {
                'minimum_size': '1 inch width for print, 150px width for digital',
                'clear_space': 'Minimum clear space equal to logo height',
                'background': 'Ensure adequate contrast on all backgrounds'
            }
        }
        
        return guide
    
    def _create_marketing_usage_guide(self, assets: List[GeneratedAsset]) -> Dict[str, Any]:
        """Create marketing assets usage guide"""
        
        marketing_assets = [asset for asset in assets if 'logo' not in asset.asset_type]
        
        guide = {
            'available_assets': [asset.asset_type for asset in marketing_assets],
            'usage_scenarios': {},
            'customization_notes': 'All templates can be customized with specific content while maintaining brand consistency'
        }
        
        for asset in marketing_assets:
            guide['usage_scenarios'][asset.asset_type] = self._get_asset_usage_description(asset.asset_type)
        
        return guide
    
    def _create_technical_specifications(self, assets: List[GeneratedAsset]) -> Dict[str, Any]:
        """Create technical specifications for all assets"""
        
        specs = {
            'file_formats': 'PNG with transparency support',
            'resolution': 'High resolution suitable for both print and digital use',
            'color_space': 'RGB for digital, CMYK conversion recommended for print',
            'quality_settings': 'Maximum quality preservation',
            'compatibility': 'Compatible with all major design and office software'
        }
        
        return specs
    
    def _create_usage_best_practices(self, brand_strategy: BrandStrategy) -> List[str]:
        """Create usage best practices"""
        
        practices = [
            'Always use the provided logo files - do not recreate or modify',
            'Maintain consistent color usage across all brand materials',
            'Ensure adequate white space around logos and key elements',
            f'Reflect the brand personality ({", ".join(brand_strategy.brand_personality.get("primary_traits", []))}) in all communications',
            'Use high-resolution versions for professional printing',
            'Maintain brand voice and messaging consistency',
            'Test designs on both light and dark backgrounds',
            'Follow accessibility guidelines for color contrast'
        ]
        
        return practices
    
    def _create_usage_troubleshooting(self) -> Dict[str, str]:
        """Create usage troubleshooting guide"""
        
        return {
            'blurry_logo': 'Ensure you are using high-resolution PNG files, not web-optimized versions',
            'wrong_colors': 'Use the exact hex color codes provided in the color palette',
            'logo_distortion': 'Do not stretch or skew logo files - maintain original proportions',
            'poor_contrast': 'Test logo visibility on various backgrounds and adjust as needed',
            'file_compatibility': 'PNG files are universally compatible - use these for best results'
        }
    
    async def _convert_asset_format(
        self,
        asset: GeneratedAsset,
        target_format: str,
        quality_settings: Optional[Dict[str, Any]] = None
    ) -> str:
        """Convert asset to different format"""
        
        # For now, return the original asset since we're working with base64 PNG data
        # In a full implementation, this would handle actual format conversion
        return asset.asset_url
    
    async def _create_asset_mockup(
        self,
        assets: List[GeneratedAsset],
        brand_strategy: BrandStrategy,
        mockup_type: str
    ) -> str:
        """Create realistic mockup of assets in use"""
        
        # This would create mockup presentations showing assets in realistic contexts
        # For now, return a placeholder
        mockup_data = self._generate_placeholder_mockup(mockup_type)
        return f"data:image/png;base64,{mockup_data}"
    
    def _generate_placeholder_mockup(self, mockup_type: str) -> str:
        """Generate placeholder mockup image"""
        
        try:
            # Create a simple mockup placeholder
            img = Image.new('RGB', (800, 600), color='#f0f0f0')
            
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            
            return base64.b64encode(buffer.getvalue()).decode('utf-8')
            
        except Exception:
            # Return minimal 1x1 pixel image
            return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="