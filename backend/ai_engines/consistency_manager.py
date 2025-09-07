import logging
from typing import Dict, Any, List, Optional, Tuple
import json
from models.brand_strategy import BrandStrategy
from models.visual_assets import GeneratedAsset, AssetVariation

class ConsistencyManager:
    """Advanced consistency management for cross-asset visual coherence"""
    
    def __init__(self):
        self.consistency_rules = {}
        self.brand_guidelines = {}
        
    def initialize_brand_consistency(self, brand_strategy: BrandStrategy) -> Dict[str, Any]:
        """Initialize consistency rules based on brand strategy"""
        
        self.brand_guidelines = {
            "color_palette": brand_strategy.color_palette,
            "design_style": brand_strategy.visual_direction.get('design_style', 'modern'),
            "visual_mood": brand_strategy.visual_direction.get('visual_mood', 'professional'),
            "typography_style": brand_strategy.visual_direction.get('typography_style', 'clean'),
            "brand_personality": brand_strategy.brand_personality,
            "consistency_rules": brand_strategy.consistency_rules
        }
        
        # Extract visual DNA for consistency tracking
        visual_dna = self._extract_visual_dna(brand_strategy)
        
        # Define consistency rules
        self.consistency_rules = {
            "color_consistency": self._define_color_rules(brand_strategy.color_palette),
            "style_consistency": self._define_style_rules(brand_strategy.visual_direction),
            "personality_consistency": self._define_personality_rules(brand_strategy.brand_personality),
            "layout_consistency": self._define_layout_rules(brand_strategy.visual_direction)
        }
        
        return {
            "visual_dna": visual_dna,
            "consistency_rules": self.consistency_rules,
            "brand_guidelines": self.brand_guidelines
        }
    
    def maintain_visual_consistency(
        self,
        base_assets: List[GeneratedAsset],
        new_asset_type: str,
        brand_strategy: BrandStrategy
    ) -> Dict[str, Any]:
        """Generate consistency constraints for new assets"""
        
        if not base_assets:
            return self.initialize_brand_consistency(brand_strategy)
        
        # Analyze existing assets for consistency patterns
        visual_patterns = self._analyze_visual_patterns(base_assets)
        
        # Generate consistency constraints
        consistency_constraints = {
            "color_constraints": self._generate_color_constraints(visual_patterns, brand_strategy),
            "style_constraints": self._generate_style_constraints(visual_patterns, brand_strategy),
            "layout_constraints": self._generate_layout_constraints(visual_patterns, new_asset_type),
            "brand_alignment": self._ensure_brand_alignment(brand_strategy)
        }
        
        return consistency_constraints
    
    def validate_asset_consistency(
        self,
        new_asset: GeneratedAsset,
        existing_assets: List[GeneratedAsset],
        brand_strategy: BrandStrategy
    ) -> Tuple[float, Dict[str, Any]]:
        """Validate consistency of new asset against existing assets"""
        
        consistency_scores = {}
        
        # Color consistency check
        consistency_scores['color_consistency'] = self._check_color_consistency(
            new_asset, existing_assets, brand_strategy.color_palette
        )
        
        # Style consistency check
        consistency_scores['style_consistency'] = self._check_style_consistency(
            new_asset, existing_assets, brand_strategy.visual_direction
        )
        
        # Brand alignment check
        consistency_scores['brand_alignment'] = self._check_brand_alignment(
            new_asset, brand_strategy
        )
        
        # Overall consistency score
        overall_score = sum(consistency_scores.values()) / len(consistency_scores)
        
        # Generate recommendations if score is low
        recommendations = []
        if overall_score < 0.8:
            recommendations = self._generate_consistency_recommendations(
                consistency_scores, new_asset, brand_strategy
            )
        
        return overall_score, {
            "individual_scores": consistency_scores,
            "overall_score": overall_score,
            "recommendations": recommendations,
            "passes_threshold": overall_score >= 0.8
        }
    
    def refine_asset_consistency(
        self,
        asset: GeneratedAsset,
        visual_dna: Dict[str, Any],
        target_score: float = 0.9
    ) -> Dict[str, Any]:
        """Generate refinement instructions to improve asset consistency"""
        
        refinement_instructions = {
            "color_adjustments": self._suggest_color_adjustments(asset, visual_dna),
            "style_adjustments": self._suggest_style_adjustments(asset, visual_dna),
            "layout_adjustments": self._suggest_layout_adjustments(asset, visual_dna),
            "regeneration_prompt": self._build_refinement_prompt(asset, visual_dna)
        }
        
        return refinement_instructions
    
    def generate_brand_guidelines_document(self, brand_strategy: BrandStrategy, assets: List[GeneratedAsset]) -> Dict[str, Any]:
        """Generate comprehensive brand guidelines document"""
        
        guidelines = {
            "brand_overview": {
                "brand_name": brand_strategy.business_name,
                "brand_essence": brand_strategy.brand_personality.get('brand_essence', ''),
                "brand_personality": brand_strategy.brand_personality,
                "brand_values": brand_strategy.messaging_framework.get('key_messages', [])
            },
            "visual_identity": {
                "logo_usage": self._generate_logo_usage_guidelines(assets),
                "color_palette": self._generate_color_guidelines(brand_strategy.color_palette),
                "typography": self._generate_typography_guidelines(brand_strategy.visual_direction),
                "imagery_style": brand_strategy.visual_direction.get('imagery_style', '')
            },
            "brand_voice": {
                "tone_of_voice": brand_strategy.brand_personality.get('tone_of_voice', ''),
                "messaging_framework": brand_strategy.messaging_framework,
                "communication_guidelines": self._generate_communication_guidelines(brand_strategy)
            },
            "application_guidelines": {
                "do_and_donts": self._generate_usage_guidelines(brand_strategy),
                "asset_specifications": self._generate_asset_specifications(assets),
                "consistency_checklist": self._generate_consistency_checklist()
            }
        }
        
        return guidelines
    
    def _extract_visual_dna(self, brand_strategy: BrandStrategy) -> Dict[str, Any]:
        """Extract core visual DNA from brand strategy"""
        
        return {
            "primary_colors": brand_strategy.color_palette[:2],
            "secondary_colors": brand_strategy.color_palette[2:],
            "design_style_keywords": self._extract_style_keywords(brand_strategy.visual_direction),
            "personality_traits": brand_strategy.brand_personality.get('primary_traits', []),
            "visual_mood": brand_strategy.visual_direction.get('visual_mood', 'professional'),
            "consistency_seed": brand_strategy.id
        }
    
    def _define_color_rules(self, color_palette: List[str]) -> Dict[str, Any]:
        """Define color consistency rules"""
        
        return {
            "primary_colors": color_palette[:2],
            "accent_colors": color_palette[2:],
            "color_harmony": "maintain_palette_ratios",
            "contrast_requirements": "ensure_readability",
            "background_compatibility": "works_on_light_and_dark"
        }
    
    def _define_style_rules(self, visual_direction: Dict[str, Any]) -> Dict[str, Any]:
        """Define style consistency rules"""
        
        return {
            "design_style": visual_direction.get('design_style', 'modern'),
            "visual_elements": visual_direction.get('visual_mood', 'professional'),
            "typography_consistency": visual_direction.get('typography_style', 'clean'),
            "layout_principles": visual_direction.get('layout_principles', 'balanced')
        }
    
    def _define_personality_rules(self, brand_personality: Dict[str, Any]) -> Dict[str, Any]:
        """Define brand personality consistency rules"""
        
        return {
            "personality_traits": brand_personality.get('primary_traits', []),
            "brand_archetype": brand_personality.get('brand_archetype', 'Professional'),
            "emotional_tone": brand_personality.get('tone_of_voice', 'professional'),
            "brand_essence": brand_personality.get('brand_essence', '')
        }
    
    def _define_layout_rules(self, visual_direction: Dict[str, Any]) -> Dict[str, Any]:
        """Define layout consistency rules"""
        
        return {
            "composition_style": "balanced_and_clean",
            "spacing_consistency": "maintain_proportions",
            "element_hierarchy": "clear_visual_hierarchy",
            "alignment_rules": "consistent_alignment_system"
        }
    
    def _analyze_visual_patterns(self, assets: List[GeneratedAsset]) -> Dict[str, Any]:
        """Analyze visual patterns from existing assets"""
        
        patterns = {
            "color_usage": self._analyze_color_patterns(assets),
            "style_elements": self._analyze_style_patterns(assets),
            "layout_patterns": self._analyze_layout_patterns(assets),
            "consistency_score": self._calculate_consistency_score(assets)
        }
        
        return patterns
    
    def _generate_color_constraints(self, patterns: Dict[str, Any], brand_strategy: BrandStrategy) -> Dict[str, Any]:
        """Generate color constraints for new assets"""
        
        return {
            "required_colors": brand_strategy.color_palette[:3],
            "color_ratios": "maintain_brand_color_dominance",
            "contrast_requirements": "ensure_accessibility",
            "background_preferences": patterns.get('color_usage', {}).get('background_colors', [])
        }
    
    def _generate_style_constraints(self, patterns: Dict[str, Any], brand_strategy: BrandStrategy) -> Dict[str, Any]:
        """Generate style constraints for new assets"""
        
        return {
            "design_style": brand_strategy.visual_direction.get('design_style', 'modern'),
            "visual_elements": patterns.get('style_elements', {}),
            "consistency_requirements": "maintain_established_patterns"
        }
    
    def _generate_layout_constraints(self, patterns: Dict[str, Any], asset_type: str) -> Dict[str, Any]:
        """Generate layout constraints based on asset type"""
        
        layout_specs = {
            "logo": {"composition": "centered", "spacing": "generous", "scalability": "vector"},
            "business_card": {"layout": "professional", "hierarchy": "clear", "spacing": "optimal"},
            "letterhead": {"layout": "formal", "branding": "subtle", "functionality": "document"},
            "social_media": {"layout": "engaging", "visual_impact": "high", "text_space": "adequate"},
            "flyer": {"layout": "promotional", "hierarchy": "attention_grabbing", "balance": "dynamic"},
            "banner": {"layout": "horizontal", "visibility": "high", "scalability": "responsive"}
        }
        
        return layout_specs.get(asset_type, {"layout": "professional", "consistency": "maintain_patterns"})
    
    def _ensure_brand_alignment(self, brand_strategy: BrandStrategy) -> Dict[str, Any]:
        """Ensure alignment with brand strategy"""
        
        return {
            "personality_reflection": brand_strategy.brand_personality.get('primary_traits', []),
            "visual_mood_alignment": brand_strategy.visual_direction.get('visual_mood', 'professional'),
            "message_consistency": brand_strategy.messaging_framework.get('brand_promise', ''),
            "target_audience_appropriateness": "suitable_for_target_market"
        }
    
    def _check_color_consistency(
        self,
        asset: GeneratedAsset,
        existing_assets: List[GeneratedAsset],
        color_palette: List[str]
    ) -> float:
        """Check color consistency score"""
        
        # Simplified consistency check based on metadata
        # In a real implementation, this would analyze actual image colors
        metadata = asset.metadata
        
        if 'brand_alignment_score' in metadata:
            return metadata['brand_alignment_score']
        
        return 0.9  # Default high score for generated assets
    
    def _check_style_consistency(
        self,
        asset: GeneratedAsset,
        existing_assets: List[GeneratedAsset],
        visual_direction: Dict[str, Any]
    ) -> float:
        """Check style consistency score"""
        
        # Check if asset maintains consistent generation method and style
        if asset.metadata.get('generation_method') == 'gemini':
            return 0.95
        
        return 0.8
    
    def _check_brand_alignment(self, asset: GeneratedAsset, brand_strategy: BrandStrategy) -> float:
        """Check brand alignment score"""
        
        alignment_score = asset.metadata.get('brand_alignment_score', 0.9)
        
        # Bonus for consistency maintenance
        if asset.metadata.get('consistency_maintained'):
            alignment_score += 0.05
        
        return min(alignment_score, 1.0)
    
    def _generate_consistency_recommendations(
        self,
        scores: Dict[str, float],
        asset: GeneratedAsset,
        brand_strategy: BrandStrategy
    ) -> List[str]:
        """Generate recommendations to improve consistency"""
        
        recommendations = []
        
        if scores.get('color_consistency', 1.0) < 0.8:
            recommendations.append(f"Ensure primary brand colors {', '.join(brand_strategy.color_palette[:2])} are prominently featured")
        
        if scores.get('style_consistency', 1.0) < 0.8:
            recommendations.append(f"Maintain {brand_strategy.visual_direction.get('design_style', 'modern')} design style")
        
        if scores.get('brand_alignment', 1.0) < 0.8:
            recommendations.append(f"Better reflect brand personality traits: {', '.join(brand_strategy.brand_personality.get('primary_traits', []))}")
        
        return recommendations
    
    def _suggest_color_adjustments(self, asset: GeneratedAsset, visual_dna: Dict[str, Any]) -> List[str]:
        """Suggest color adjustments for better consistency"""
        
        return [
            f"Emphasize primary colors: {', '.join(visual_dna.get('primary_colors', []))}",
            "Ensure proper color balance and contrast",
            "Maintain color hierarchy established in other assets"
        ]
    
    def _suggest_style_adjustments(self, asset: GeneratedAsset, visual_dna: Dict[str, Any]) -> List[str]:
        """Suggest style adjustments for better consistency"""
        
        style_keywords = visual_dna.get('design_style_keywords', [])
        
        return [
            f"Strengthen {', '.join(style_keywords)} design elements",
            "Maintain consistent visual mood and personality",
            "Ensure alignment with established design patterns"
        ]
    
    def _suggest_layout_adjustments(self, asset: GeneratedAsset, visual_dna: Dict[str, Any]) -> List[str]:
        """Suggest layout adjustments for better consistency"""
        
        return [
            "Improve visual hierarchy and element spacing",
            "Ensure consistent composition and balance",
            "Maintain established layout patterns from other assets"
        ]
    
    def _build_refinement_prompt(self, asset: GeneratedAsset, visual_dna: Dict[str, Any]) -> str:
        """Build prompt for asset refinement"""
        
        return f"""
        Refine this {asset.asset_type} to better match the established brand visual identity:
        
        Brand Visual DNA:
        - Primary Colors: {', '.join(visual_dna.get('primary_colors', []))}
        - Design Style: {', '.join(visual_dna.get('design_style_keywords', []))}
        - Visual Mood: {visual_dna.get('visual_mood', 'professional')}
        - Personality Traits: {', '.join(visual_dna.get('personality_traits', []))}
        
        Refinement Goals:
        - Strengthen brand color usage and hierarchy
        - Enhance consistency with existing brand assets
        - Improve overall visual cohesion and professional quality
        - Maintain asset functionality while improving brand alignment
        
        Generate a refined version that better embodies the brand identity.
        """
    
    def _extract_style_keywords(self, visual_direction: Dict[str, Any]) -> List[str]:
        """Extract style keywords from visual direction"""
        
        keywords = []
        
        design_style = visual_direction.get('design_style', '')
        if design_style:
            keywords.extend(design_style.lower().split())
        
        visual_mood = visual_direction.get('visual_mood', '')
        if visual_mood:
            keywords.extend(visual_mood.lower().split())
        
        return list(set(keywords))[:5]  # Return top 5 unique keywords
    
    def _analyze_color_patterns(self, assets: List[GeneratedAsset]) -> Dict[str, Any]:
        """Analyze color patterns from existing assets"""
        
        # Simplified analysis based on metadata
        return {
            "dominant_colors": ["primary", "secondary"],
            "color_usage_frequency": {"primary": 0.8, "secondary": 0.6},
            "background_colors": ["light", "white"]
        }
    
    def _analyze_style_patterns(self, assets: List[GeneratedAsset]) -> Dict[str, Any]:
        """Analyze style patterns from existing assets"""
        
        return {
            "common_elements": ["clean", "professional", "modern"],
            "layout_preferences": "balanced",
            "typography_consistency": "clean_fonts"
        }
    
    def _analyze_layout_patterns(self, assets: List[GeneratedAsset]) -> Dict[str, Any]:
        """Analyze layout patterns from existing assets"""
        
        return {
            "composition_style": "centered",
            "spacing_patterns": "generous",
            "hierarchy_approach": "clear"
        }
    
    def _calculate_consistency_score(self, assets: List[GeneratedAsset]) -> float:
        """Calculate overall consistency score for existing assets"""
        
        if not assets:
            return 1.0
        
        # Average brand alignment scores from metadata
        scores = [asset.metadata.get('brand_alignment_score', 0.9) for asset in assets]
        return sum(scores) / len(scores)
    
    def _generate_logo_usage_guidelines(self, assets: List[GeneratedAsset]) -> Dict[str, Any]:
        """Generate logo usage guidelines"""
        
        logo_assets = [asset for asset in assets if 'logo' in asset.asset_type]
        
        return {
            "primary_logo": "Use for main brand representation",
            "variations": "Use horizontal for wide spaces, vertical for narrow spaces",
            "minimum_size": "Ensure readability at small sizes",
            "clear_space": "Maintain adequate spacing around logo",
            "color_variations": "Use monochrome version when color reproduction is limited"
        }
    
    def _generate_color_guidelines(self, color_palette: List[str]) -> Dict[str, Any]:
        """Generate comprehensive color guidelines"""
        
        return {
            "primary_color": {"hex": color_palette[0] if color_palette else "#000000", "usage": "Main brand color for headers and key elements"},
            "secondary_color": {"hex": color_palette[1] if len(color_palette) > 1 else "#666666", "usage": "Supporting color for accents and highlights"},
            "accent_colors": [{"hex": color, "usage": "Use sparingly for emphasis"} for color in color_palette[2:5]],
            "color_combinations": "Ensure sufficient contrast for accessibility",
            "usage_rules": "Primary color should dominate, use secondary and accents strategically"
        }
    
    def _generate_typography_guidelines(self, visual_direction: Dict[str, Any]) -> Dict[str, Any]:
        """Generate typography guidelines"""
        
        return {
            "primary_font": "Clean, professional typeface for headers",
            "secondary_font": "Readable font for body text",
            "font_hierarchy": "Consistent size and weight relationships",
            "usage_rules": visual_direction.get('typography_style', 'Clean and readable fonts'),
            "accessibility": "Ensure proper contrast and readability"
        }
    
    def _generate_communication_guidelines(self, brand_strategy: BrandStrategy) -> Dict[str, Any]:
        """Generate communication guidelines"""
        
        return {
            "tone_of_voice": brand_strategy.brand_personality.get('tone_of_voice', 'Professional'),
            "key_messages": brand_strategy.messaging_framework.get('key_messages', []),
            "brand_promise": brand_strategy.messaging_framework.get('brand_promise', ''),
            "communication_style": "Consistent with brand personality and values"
        }
    
    def _generate_usage_guidelines(self, brand_strategy: BrandStrategy) -> Dict[str, List[str]]:
        """Generate do's and don'ts for brand usage"""
        
        return {
            "dos": [
                "Maintain consistent color usage across all materials",
                "Use high-quality, professional imagery",
                "Ensure adequate white space and clean layouts",
                "Reflect brand personality in all communications",
                "Follow established visual hierarchy"
            ],
            "donts": [
                "Don't alter logo proportions or colors",
                "Don't use low-resolution or pixelated images",
                "Don't mix inconsistent design styles",
                "Don't overcrowd layouts with too many elements",
                "Don't deviate from established brand voice"
            ]
        }
    
    def _generate_asset_specifications(self, assets: List[GeneratedAsset]) -> Dict[str, Any]:
        """Generate technical specifications for assets"""
        
        specifications = {}
        
        for asset in assets:
            asset_type = asset.asset_type
            specifications[asset_type] = {
                "format": "PNG with transparency support",
                "quality": "High resolution for print and digital use",
                "usage": f"Professional {asset_type.replace('_', ' ')} for business applications",
                "technical_notes": asset.metadata.get('technical_notes', 'Standard professional quality')
            }
        
        return specifications
    
    def _generate_consistency_checklist(self) -> List[str]:
        """Generate consistency checklist for quality assurance"""
        
        return [
            "Colors match the established brand palette",
            "Design style is consistent with brand guidelines",
            "Typography follows established hierarchy",
            "Visual elements reflect brand personality",
            "Overall composition is balanced and professional",
            "Asset is appropriate for intended use case",
            "Quality is suitable for both print and digital applications",
            "Brand message and values are clearly communicated"
        ]