from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid

class BusinessInput(BaseModel):
    business_name: str
    business_description: str
    industry: str
    target_audience: str
    business_values: List[str]
    preferred_style: Optional[str] = "modern"
    preferred_colors: Optional[str] = "flexible"

class BrandStrategy(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    business_name: str
    brand_personality: Dict[str, Any]
    visual_direction: Dict[str, Any]
    color_palette: List[str]
    messaging_framework: Dict[str, Any]
    consistency_rules: Dict[str, Any]
    advanced_analysis: Optional[Dict[str, Any]] = None  # Phase 2: Advanced multi-layer analysis data
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))