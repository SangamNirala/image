from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid
from .brand_strategy import BusinessInput, BrandStrategy
from .visual_assets import GeneratedAsset

class BrandProject(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    business_input: BusinessInput
    brand_strategy: Optional[BrandStrategy] = None
    generated_assets: List[GeneratedAsset] = []
    advanced_analysis: Optional[Dict[str, Any]] = None  # Phase 2: Advanced multi-layer analysis
    status: str = "created"  # created, strategy_generated, advanced_analysis_complete, assets_generated, completed
    consistency_seed: Optional[str] = None  # For maintaining visual consistency
    export_ready: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ProjectProgress(BaseModel):
    project_id: str
    current_step: str  # business_input, strategy_generation, visual_creation, asset_generation, export
    completed_steps: List[str]
    next_steps: List[str]
    estimated_completion_time: int  # in minutes
    
class ProjectAnalytics(BaseModel):
    project_id: str
    brand_strength_score: float
    visual_consistency_score: float
    market_positioning_score: float
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))