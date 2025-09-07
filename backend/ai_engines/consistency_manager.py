"""
Consistency Manager
Advanced visual consistency management across brand assets
"""

import logging
import json
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timezone

from models.brand_strategy import BrandStrategy
from models.visual_assets import GeneratedAsset, AssetType, AssetCollection

class ConsistencyManager:
    """Advanced consistency management for brand visual assets"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.consistency_rules = {}
        self.brand_dna_cache = {}
        
    def establish_brand_consistency_rules(self, brand_strategy: BrandStrategy) -> Dict[str, Any]:
        """Establish comprehensive consistency rules based on brand strategy"""
        
        consistency_rules = {
            "visual_consistency": {
                "primary_colors": brand_strategy.get_color_palette(),
                "design_style": brand_strategy.get_design_style(),
                "brand_essence": brand_strategy.get_brand_essence(),
                "personality_traits": brand_strategy.get_brand_traits()
            },
            "consistency_seed": brand_strategy.get_consistency_seed(),
            "validation_criteria": {
                "color_consistency_threshold": 0.8,
                "style_consistency_threshold": 0.75,
                "brand_recognition_threshold": 0.7
            },
            "mandatory_elements": {
                "brand_name": brand_strategy.business_name,
                "brand_colors": brand_strategy.get_color_palette()[:3],  # Top 3 colors
                "style_keywords": [
                    brand_strategy.get_design_style(),
                    brand_strategy.brand_personality.brand_archetype,
                    brand_strategy.get_brand_essence()
                ]
            },
            "avoid_elements": [
                "conflicting color schemes",
                "inconsistent typography",
                "off-brand personality elements",
                "competing visual styles"
            ]
        }
        
        # Store rules for this brand
        project_id = brand_strategy.id
        self.consistency_rules[project_id] = consistency_rules
        
        self.logger.info(f"Established consistency rules for project {project_id}")
        return consistency_rules
    
    def extract_visual_dna(self, assets: List[GeneratedAsset]) -> Dict[str, Any]:
        """Extract visual DNA patterns from existing assets"""
        
        if not assets:
            return {}
        
        # Aggregate visual patterns from assets
        consistency_seeds = []
        variants = []
        quality_scores = []
        asset_types = []
        
        for asset in assets:
            if asset.metadata.consistency_seed:
                consistency_seeds.append(asset.metadata.consistency_seed)
            variants.append(asset.variant)
            quality_scores.append(asset.metadata.quality_score)
            asset_types.append(asset.asset_type.value)
        
        # Calculate visual DNA fingerprint
        visual_dna = {
            "dominant_consistency_seed": self._get_most_common(consistency_seeds),
            "asset_count": len(assets),
            "asset_types": list(set(asset_types)),
            "variant_patterns": list(set(variants)),
            "average_quality": sum(quality_scores) / len(quality_scores) if quality_scores else 0,
            "consistency_patterns": self._analyze_consistency_patterns(assets),
            "visual_signature": self._generate_visual_signature(assets)
        }
        
        return visual_dna
    
    def _analyze_consistency_patterns(self, assets: List[GeneratedAsset]) -> Dict[str, Any]:
        """Analyze consistency patterns across assets"""
        
        patterns = {
            "consistent_seeds": 0,
            "seed_variations": set(),
            "quality_distribution": {
                "high": 0,  # > 0.8
                "medium": 0,  # 0.5 - 0.8
                "low": 0   # < 0.5
            },
            "generation_attempts": [],
            "fallback_usage": 0
        }
        
        for asset in assets:
            # Consistency seed analysis
            if asset.metadata.consistency_seed:
                patterns["seed_variations"].add(asset.metadata.consistency_seed)
            
            # Quality distribution
            quality = asset.metadata.quality_score
            if quality > 0.8:
                patterns["quality_distribution"]["high"] += 1
            elif quality > 0.5:
                patterns["quality_distribution"]["medium"] += 1
            else:
                patterns["quality_distribution"]["low"] += 1
            
            # Generation attempts
            patterns["generation_attempts"].append(asset.metadata.attempt_number)
            
            # Fallback usage
            if asset.metadata.is_fallback:
                patterns["fallback_usage"] += 1
        
        # Calculate consistency score
        if len(patterns["seed_variations"]) <= 1:
            patterns["consistent_seeds"] = 1.0
        else:
            patterns["consistent_seeds"] = 1.0 / len(patterns["seed_variations"])
        
        return patterns
    
    def _generate_visual_signature(self, assets: List[GeneratedAsset]) -> str:
        """Generate visual signature from assets"""
        
        signature_elements = []
        
        for asset in assets:
            elements = [
                asset.asset_type.value,
                asset.variant,
                asset.metadata.consistency_seed,
                str(int(asset.metadata.quality_score * 10))
            ]
            signature_elements.append("|".join(elements))
        
        combined_signature = "::".join(sorted(signature_elements))
        return hashlib.md5(combined_signature.encode()).hexdigest()[:12]
    
    def validate_asset_consistency(
        self, 
        new_asset: GeneratedAsset, 
        existing_assets: List[GeneratedAsset],
        brand_strategy: BrandStrategy
    ) -> Dict[str, Any]:
        """Validate consistency of new asset against existing assets and brand strategy"""
        
        if not existing_assets:
            return {
                "consistency_score": 1.0,
                "validation_status": "baseline",
                "issues": [],
                "recommendations": []
            }
        
        issues = []
        recommendations = []
        scores = {}
        
        # Extract visual DNA from existing assets
        visual_dna = self.extract_visual_dna(existing_assets)
        
        # 1. Consistency Seed Validation
        seed_score = self._validate_consistency_seed(new_asset, visual_dna)
        scores["seed_consistency"] = seed_score
        
        if seed_score < 0.8:
            issues.append("Consistency seed mismatch with existing assets")
            recommendations.append("Regenerate with matching consistency seed")
        
        # 2. Quality Consistency Validation
        quality_score = self._validate_quality_consistency(new_asset, visual_dna)
        scores["quality_consistency"] = quality_score
        
        if quality_score < 0.6:
            issues.append("Quality significantly below existing assets")
            recommendations.append("Improve generation quality or regenerate")
        
        # 3. Brand Strategy Alignment
        strategy_score = self._validate_strategy_alignment(new_asset, brand_strategy)
        scores["strategy_alignment"] = strategy_score
        
        if strategy_score < 0.7:
            issues.append("Asset may not align with brand strategy")
            recommendations.append("Review brand guidelines and regenerate")
        
        # 4. Visual Harmony
        harmony_score = self._assess_visual_harmony(new_asset, existing_assets)
        scores["visual_harmony"] = harmony_score
        
        if harmony_score < 0.7:
            issues.append("Visual harmony concerns with existing assets")
            recommendations.append("Adjust visual elements for better harmony")
        
        # Calculate overall consistency score
        overall_score = sum(scores.values()) / len(scores)
        
        # Determine validation status
        if overall_score >= 0.85:
            status = "excellent"
        elif overall_score >= 0.7:
            status = "good"
        elif overall_score >= 0.5:
            status = "acceptable"
        else:
            status = "needs_improvement"
        
        return {
            "consistency_score": overall_score,
            "validation_status": status,
            "detailed_scores": scores,
            "issues": issues,
            "recommendations": recommendations,
            "visual_dna_match": visual_dna["visual_signature"] if visual_dna else None
        }
    
    def _validate_consistency_seed(self, asset: GeneratedAsset, visual_dna: Dict[str, Any]) -> float:
        """Validate consistency seed alignment"""
        
        if not visual_dna.get("dominant_consistency_seed"):
            return 1.0  # No baseline to compare
        
        if asset.metadata.consistency_seed == visual_dna["dominant_consistency_seed"]:
            return 1.0
        elif asset.metadata.consistency_seed in visual_dna.get("seed_variations", set()):
            return 0.8
        else:
            return 0.4
    
    def _validate_quality_consistency(self, asset: GeneratedAsset, visual_dna: Dict[str, Any]) -> float:
        """Validate quality consistency with existing assets"""
        
        avg_quality = visual_dna.get("average_quality", 0.5)
        asset_quality = asset.metadata.quality_score
        
        quality_diff = abs(asset_quality - avg_quality)
        
        if quality_diff <= 0.1:
            return 1.0
        elif quality_diff <= 0.2:
            return 0.8
        elif quality_diff <= 0.3:
            return 0.6
        else:
            return 0.4
    
    def _validate_strategy_alignment(self, asset: GeneratedAsset, brand_strategy: BrandStrategy) -> float:
        """Validate asset alignment with brand strategy"""
        
        # Get brand consistency rules
        rules = self.consistency_rules.get(brand_strategy.id, {})
        
        if not rules:
            return 0.8  # Default score if no rules established
        
        alignment_score = 0.8  # Base score
        
        # Check consistency seed alignment
        expected_seed = rules.get("consistency_seed")
        if expected_seed and asset.metadata.consistency_seed == expected_seed:
            alignment_score += 0.2
        
        return min(alignment_score, 1.0)
    
    def _assess_visual_harmony(self, new_asset: GeneratedAsset, existing_assets: List[GeneratedAsset]) -> float:
        """Assess visual harmony with existing assets"""
        
        # Simplified visual harmony assessment
        # In production, this could involve actual image analysis
        
        harmony_factors = []
        
        # Quality harmony
        qualities = [a.metadata.quality_score for a in existing_assets]
        avg_quality = sum(qualities) / len(qualities)
        quality_harmony = 1 - abs(new_asset.metadata.quality_score - avg_quality)
        harmony_factors.append(quality_harmony)
        
        # Generation method harmony
        fallback_ratio = sum(1 for a in existing_assets if a.metadata.is_fallback) / len(existing_assets)
        if new_asset.metadata.is_fallback and fallback_ratio > 0.5:
            method_harmony = 0.8
        elif not new_asset.metadata.is_fallback and fallback_ratio < 0.3:
            method_harmony = 1.0
        else:
            method_harmony = 0.6
        harmony_factors.append(method_harmony)
        
        return sum(harmony_factors) / len(harmony_factors)
    
    def maintain_visual_consistency(
        self, 
        asset_collection: AssetCollection, 
        brand_strategy: BrandStrategy
    ) -> Dict[str, Any]:
        """Maintain and improve visual consistency across asset collection"""
        
        if not asset_collection.assets:
            return {"status": "no_assets", "actions": []}
        
        # Establish or update consistency rules
        rules = self.establish_brand_consistency_rules(brand_strategy)
        
        # Analyze current consistency
        visual_dna = self.extract_visual_dna(asset_collection.assets)
        
        # Identify consistency issues
        issues = []
        recommendations = []
        actions_needed = []
        
        # Check for consistency seed fragmentation
        seed_variations = visual_dna.get("seed_variations", set())
        if len(seed_variations) > 1:
            issues.append(f"Multiple consistency seeds detected: {len(seed_variations)}")
            recommendations.append("Standardize on single consistency seed")
            actions_needed.append("regenerate_inconsistent_assets")
        
        # Check quality distribution
        quality_dist = visual_dna.get("consistency_patterns", {}).get("quality_distribution", {})
        low_quality_count = quality_dist.get("low", 0)
        
        if low_quality_count > len(asset_collection.assets) * 0.3:
            issues.append(f"High number of low-quality assets: {low_quality_count}")
            recommendations.append("Regenerate low-quality assets")
            actions_needed.append("improve_asset_quality")
        
        # Check fallback usage
        fallback_count = visual_dna.get("consistency_patterns", {}).get("fallback_usage", 0)
        if fallback_count > len(asset_collection.assets) * 0.2:
            issues.append(f"High fallback usage: {fallback_count}")
            recommendations.append("Improve generation success rate")
            actions_needed.append("reduce_fallback_usage")
        
        # Calculate overall consistency score
        consistency_metrics = self._calculate_collection_consistency(asset_collection, rules)
        
        return {
            "status": "analyzed",
            "consistency_score": consistency_metrics["overall_score"],
            "visual_dna": visual_dna,
            "issues": issues,
            "recommendations": recommendations,
            "actions_needed": actions_needed,
            "consistency_metrics": consistency_metrics,
            "improvement_potential": self._identify_improvement_opportunities(asset_collection, rules)
        }
    
    def _calculate_collection_consistency(
        self, 
        collection: AssetCollection, 
        rules: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate comprehensive consistency metrics for asset collection"""
        
        if not collection.assets:
            return {"overall_score": 0.0}
        
        # Extract consistency seeds
        seeds = [a.metadata.consistency_seed for a in collection.assets if a.metadata.consistency_seed]
        seed_consistency = len(set(seeds)) <= 1 if seeds else 0.5
        
        # Quality consistency
        qualities = [a.metadata.quality_score for a in collection.assets]
        quality_variance = self._calculate_variance(qualities)
        quality_consistency = max(0, 1 - quality_variance)
        
        # Brand alignment
        expected_seed = rules.get("consistency_seed", "")
        brand_alignment = sum(1 for s in seeds if s == expected_seed) / len(seeds) if seeds else 0.5
        
        # Asset type coverage
        required_types = set([AssetType.LOGO, AssetType.BUSINESS_CARD, AssetType.LETTERHEAD])
        actual_types = set([a.asset_type for a in collection.assets])
        type_coverage = len(actual_types & required_types) / len(required_types)
        
        metrics = {
            "seed_consistency": seed_consistency,
            "quality_consistency": quality_consistency,
            "brand_alignment": brand_alignment,
            "type_coverage": type_coverage
        }
        
        # Calculate weighted overall score
        weights = {
            "seed_consistency": 0.3,
            "quality_consistency": 0.25,
            "brand_alignment": 0.3,
            "type_coverage": 0.15
        }
        
        overall_score = sum(metrics[key] * weights[key] for key in metrics)
        metrics["overall_score"] = overall_score
        
        return metrics
    
    def _identify_improvement_opportunities(
        self, 
        collection: AssetCollection, 
        rules: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Identify specific opportunities to improve consistency"""
        
        opportunities = []
        
        # Identify assets that need regeneration
        for asset in collection.assets:
            if asset.metadata.is_fallback:
                opportunities.append({
                    "type": "regenerate_fallback",
                    "asset_id": asset.id,
                    "asset_type": asset.asset_type.value,
                    "priority": "high",
                    "reason": "Replace fallback with AI-generated asset"
                })
            
            elif asset.metadata.quality_score < 0.6:
                opportunities.append({
                    "type": "improve_quality",
                    "asset_id": asset.id,
                    "asset_type": asset.asset_type.value,
                    "priority": "medium",
                    "reason": f"Low quality score: {asset.metadata.quality_score:.2f}"
                })
            
            elif asset.metadata.consistency_seed != rules.get("consistency_seed"):
                opportunities.append({
                    "type": "align_consistency",
                    "asset_id": asset.id,
                    "asset_type": asset.asset_type.value,
                    "priority": "medium",
                    "reason": "Consistency seed mismatch"
                })
        
        return opportunities
    
    def suggest_consistency_improvements(
        self, 
        collection: AssetCollection, 
        brand_strategy: BrandStrategy
    ) -> Dict[str, Any]:
        """Suggest specific improvements for better consistency"""
        
        analysis = self.maintain_visual_consistency(collection, brand_strategy)
        
        suggestions = {
            "priority_actions": [],
            "optional_improvements": [],
            "consistency_tips": []
        }
        
        # Priority actions based on issues
        for issue in analysis.get("issues", []):
            if "low-quality" in issue.lower():
                suggestions["priority_actions"].append({
                    "action": "regenerate_low_quality_assets",
                    "description": "Regenerate assets with quality scores below 0.6",
                    "impact": "high"
                })
            
            elif "consistency seed" in issue.lower():
                suggestions["priority_actions"].append({
                    "action": "standardize_consistency_seed",
                    "description": "Regenerate assets with mismatched consistency seeds",
                    "impact": "high"
                })
        
        # Optional improvements
        opportunities = analysis.get("improvement_potential", [])
        for opp in opportunities:
            if opp.get("priority") == "medium":
                suggestions["optional_improvements"].append({
                    "action": opp["type"],
                    "description": opp["reason"],
                    "asset_type": opp["asset_type"]
                })
        
        # General consistency tips
        suggestions["consistency_tips"] = [
            "Maintain consistent color palette across all assets",
            "Use the same consistency seed for visual harmony",
            "Ensure quality scores are above 0.7 for professional results",
            "Review brand guidelines before generating new assets"
        ]
        
        return suggestions
    
    def _get_most_common(self, items: List[str]) -> Optional[str]:
        """Get most common item from list"""
        if not items:
            return None
        
        from collections import Counter
        counter = Counter(items)
        return counter.most_common(1)[0][0]
    
    def _calculate_variance(self, values: List[float]) -> float:
        """Calculate variance of values"""
        if len(values) < 2:
            return 0.0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance