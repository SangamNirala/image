from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid

class GeneratedAsset(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    project_id: str
    asset_type: str  # logo, business_card, social_media, etc.
    asset_url: str
    metadata: Dict[str, Any]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AssetGenerationRequest(BaseModel):
    asset_type: str
    style_variant: Optional[str] = "primary"
    custom_requirements: Optional[str] = None
    consistency_level: Optional[str] = "high"  # high, medium, low

class AssetVariation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    base_asset_id: str
    variation_type: str  # horizontal, vertical, icon_only, monochrome
    asset_url: str
    consistency_score: float
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))