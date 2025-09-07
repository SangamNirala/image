"""
Brand Strategy Models
Advanced data models for comprehensive brand strategy management
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
from enum import Enum
import uuid

class BusinessInput(BaseModel):
    """Business input requirements for brand strategy generation"""
    business_name: str = Field(..., description="Name of the business")
    business_description: str = Field(..., description="Detailed business description")
    industry: str = Field(..., description="Industry sector")
    target_audience: str = Field(..., description="Target audience description")
    business_values: List[str] = Field(default_factory=list, description="Core business values")
    preferred_style: Optional[str] = Field(default="modern", description="Preferred design style")
    preferred_colors: Optional[str] = Field(default="flexible", description="Color preferences")
    
    # Advanced business context
    business_stage: Optional[str] = Field(default="startup", description="Business maturity stage")
    budget_range: Optional[str] = Field(default="medium", description="Budget considerations")
    timeline: Optional[str] = Field(default="standard", description="Project timeline")
    special_requirements: Optional[str] = Field(default="", description="Special requirements")

class BrandPersonality(BaseModel):
    """Comprehensive brand personality definition"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Core personality traits
    primary_traits: List[str] = Field(default_factory=list, description="5 primary brand traits")
    secondary_traits: List[str] = Field(default_factory=list, description="Supporting traits")
    brand_archetype: str = Field(default="", description="Brand archetype (The Hero, The Sage, etc.)")
    brand_essence: str = Field(default="", description="One-sentence brand essence")
    
    # Communication personality
    tone_of_voice: Dict[str, Any] = Field(default_factory=dict, description="Tone and voice characteristics")
    emotional_connection: Dict[str, Any] = Field(default_factory=dict, description="Emotional positioning")
    behavioral_characteristics: Dict[str, Any] = Field(default_factory=dict, description="Brand behavior patterns")
    
    # Personality validation
    personality_score: Optional[float] = Field(default=None, description="Personality coherence score")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class VisualDirection(BaseModel):
    """Comprehensive visual direction and design system"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Core visual elements
    design_style: str = Field(default="", description="Primary design style")
    visual_mood: str = Field(default="", description="Overall visual mood")
    
    # Advanced color system
    color_strategy: Dict[str, Any] = Field(default_factory=dict, description="Comprehensive color strategy")
    color_palette: List[str] = Field(default_factory=list, description="Brand color palette (hex codes)")
    color_psychology: Optional[str] = Field(default="", description="Color psychology rationale")
    
    # Typography system
    typography_direction: Dict[str, Any] = Field(default_factory=dict, description="Typography guidelines")
    
    # Visual style elements
    imagery_style: Dict[str, Any] = Field(default_factory=dict, description="Imagery and photography style")
    logo_direction: Dict[str, Any] = Field(default_factory=dict, description="Logo design direction")
    layout_principles: Dict[str, Any] = Field(default_factory=dict, description="Layout and composition rules")
    
    # Technical specifications
    design_system: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Complete design system")
    brand_guidelines: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Usage guidelines")
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class MessagingFramework(BaseModel):
    """Comprehensive brand messaging and communication framework"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Core messaging
    brand_tagline: str = Field(default="", description="Main brand tagline")
    elevator_pitch: str = Field(default="", description="30-second brand description")
    brand_promise: str = Field(default="", description="Brand promise to customers")
    unique_value_proposition: str = Field(default="", description="Unique value proposition")
    
    # Messaging hierarchy
    key_messages: Dict[str, Any] = Field(default_factory=dict, description="Structured key messages")
    audience_messaging: Dict[str, Any] = Field(default_factory=dict, description="Audience-specific messaging")
    
    # Communication guidelines
    communication_guidelines: Dict[str, Any] = Field(default_factory=dict, description="Communication standards")
    storytelling_framework: Dict[str, Any] = Field(default_factory=dict, description="Brand storytelling approach")
    
    # Message validation
    message_consistency_score: Optional[float] = Field(default=None, description="Message consistency score")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class BrandStrategy(BaseModel):
    """Complete brand strategy combining all elements"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Business context
    business_name: str = Field(..., description="Business name")
    business_input: Optional[BusinessInput] = Field(default=None, description="Original business input")
    
    # Core strategy components
    brand_personality: BrandPersonality = Field(..., description="Brand personality definition")
    visual_direction: VisualDirection = Field(..., description="Visual direction and design system")
    messaging_framework: MessagingFramework = Field(..., description="Messaging and communication framework")
    
    # Strategic analysis
    market_analysis: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Market analysis results")
    competitive_positioning: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Competitive analysis")
    
    # Implementation guidance
    consistency_rules: Dict[str, Any] = Field(default_factory=dict, description="Brand consistency rules")
    implementation_roadmap: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Implementation guidance")
    
    # Strategy metadata
    strategy_version: str = Field(default="1.0", description="Strategy version")
    strategy_score: Optional[float] = Field(default=None, description="Overall strategy strength score")
    
    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    def update_timestamp(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.now(timezone.utc)
    
    def get_color_palette(self) -> List[str]:
        """Get the primary color palette"""
        return self.visual_direction.color_strategy.get("primary_colors", [])
    
    def get_brand_traits(self) -> List[str]:
        """Get primary brand personality traits"""
        return self.brand_personality.primary_traits
    
    def get_design_style(self) -> str:
        """Get the primary design style"""
        return self.visual_direction.design_style
    
    def get_brand_essence(self) -> str:
        """Get the brand essence statement"""
        return self.brand_personality.brand_essence
    
    def get_consistency_seed(self) -> str:
        """Generate consistency seed for visual generation"""
        import hashlib
        import json
        
        consistency_data = {
            "business_name": self.business_name,
            "primary_traits": self.brand_personality.primary_traits,
            "design_style": self.visual_direction.design_style,
            "primary_colors": self.get_color_palette()
        }
        
        seed_string = json.dumps(consistency_data, sort_keys=True)
        return hashlib.md5(seed_string.encode()).hexdigest()[:8]

class StrategyTemplate(BaseModel):
    """Template for brand strategy generation"""
    template_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    template_name: str = Field(..., description="Template name")
    industry_focus: str = Field(..., description="Target industry")
    
    # Template components
    personality_template: Dict[str, Any] = Field(default_factory=dict)
    visual_template: Dict[str, Any] = Field(default_factory=dict)
    messaging_template: Dict[str, Any] = Field(default_factory=dict)
    
    # Template metadata
    usage_count: int = Field(default=0, description="Number of times used")
    success_score: Optional[float] = Field(default=None, description="Template success rate")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StrategyEvolution(BaseModel):
    """Track strategy evolution and refinements"""
    evolution_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    strategy_id: str = Field(..., description="Associated strategy ID")
    
    # Evolution tracking
    version: str = Field(..., description="Strategy version")
    changes_made: List[str] = Field(default_factory=list, description="List of changes")
    change_rationale: str = Field(default="", description="Reason for changes")
    
    # Performance tracking
    performance_impact: Optional[Dict[str, Any]] = Field(default_factory=dict)
    user_feedback: Optional[str] = Field(default="")
    
    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: str = Field(default="system", description="Who made the changes")