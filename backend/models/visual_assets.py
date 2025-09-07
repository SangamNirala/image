"""
Visual Assets Models
Advanced data models for visual asset management and generation
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timezone
from enum import Enum
import uuid

class AssetType(Enum):
    """Enumeration of supported asset types"""
    LOGO = "logo"
    BUSINESS_CARD = "business_card"
    LETTERHEAD = "letterhead"
    SOCIAL_MEDIA_POST = "social_media_post"
    FLYER = "flyer"
    BANNER = "banner"
    POSTER = "poster"
    BROCHURE = "brochure"
    PACKAGING = "packaging"
    WEBSITE_MOCKUP = "website_mockup"
    PRESENTATION_TEMPLATE = "presentation_template"
    EMAIL_TEMPLATE = "email_template"

class AssetDimensions(BaseModel):
    """Asset dimensions and technical specifications"""
    width: int = Field(..., description="Asset width in pixels")
    height: int = Field(..., description="Asset height in pixels")
    aspect_ratio: str = Field(..., description="Aspect ratio (e.g., '16:9', '1:1')")
    dpi: Optional[int] = Field(default=300, description="Dots per inch for print")
    format: str = Field(default="PNG", description="File format")

class AssetMetadata(BaseModel):
    """Comprehensive metadata for generated assets"""
    metadata_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Generation details
    generation_prompt: str = Field(default="", description="Prompt used for generation")
    consistency_seed: str = Field(default="", description="Consistency seed for brand coherence")
    variant: str = Field(default="standard", description="Asset variant type")
    
    # Quality and performance metrics
    quality_score: float = Field(default=0.0, description="Assessed quality score (0-1)")
    generation_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    attempt_number: int = Field(default=1, description="Generation attempt number")
    
    # Technical specifications
    dimensions: Optional[AssetDimensions] = Field(default=None, description="Asset dimensions")
    file_size: Optional[int] = Field(default=None, description="File size in bytes")
    
    # Brand consistency tracking
    brand_consistency_score: Optional[float] = Field(default=None, description="Brand consistency score")
    consistency_reference_id: Optional[str] = Field(default=None, description="Reference asset for consistency")
    
    # Generation context
    ai_model_used: str = Field(default="gemini-2.5-flash-image-preview", description="AI model used")
    generation_parameters: Dict[str, Any] = Field(default_factory=dict, description="Generation parameters")
    
    # Asset status
    is_fallback: bool = Field(default=False, description="Whether this is a fallback asset")
    needs_revision: bool = Field(default=False, description="Whether asset needs revision")
    approval_status: str = Field(default="pending", description="Approval status")
    
    # User interaction
    user_rating: Optional[float] = Field(default=None, description="User rating (1-5)")
    user_feedback: Optional[str] = Field(default="", description="User feedback")
    usage_count: int = Field(default=0, description="Number of times used")

class GeneratedAsset(BaseModel):
    """Individual generated brand asset"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    project_id: Optional[str] = Field(default=None, description="Associated project ID")
    
    # Asset identification
    asset_type: AssetType = Field(..., description="Type of asset")
    variant: str = Field(default="standard", description="Asset variant")
    asset_name: Optional[str] = Field(default="", description="Human-readable asset name")
    
    # Asset content
    asset_url: str = Field(..., description="Asset URL or base64 data")
    thumbnail_url: Optional[str] = Field(default="", description="Thumbnail URL")
    
    # Asset metadata
    metadata: AssetMetadata = Field(default_factory=AssetMetadata, description="Comprehensive metadata")
    
    # Asset relationships
    parent_asset_id: Optional[str] = Field(default=None, description="Parent asset for variations")
    child_asset_ids: List[str] = Field(default_factory=list, description="Child asset variations")
    
    # Asset versioning
    version: str = Field(default="1.0", description="Asset version")
    version_history: List[str] = Field(default_factory=list, description="Version history")
    
    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    def update_timestamp(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.now(timezone.utc)
    
    def get_display_name(self) -> str:
        """Get display-friendly asset name"""
        if self.asset_name:
            return self.asset_name
        return f"{self.asset_type.value.replace('_', ' ').title()} - {self.variant}"
    
    def is_high_quality(self) -> bool:
        """Check if asset meets high quality standards"""
        return self.metadata.quality_score >= 0.8
    
    def needs_regeneration(self) -> bool:
        """Check if asset needs regeneration"""
        return (
            self.metadata.is_fallback or 
            self.metadata.needs_revision or 
            self.metadata.quality_score < 0.5
        )

class AssetCollection(BaseModel):
    """Collection of related brand assets"""
    collection_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    project_id: str = Field(..., description="Associated project ID")
    
    # Collection metadata
    collection_name: str = Field(default="Brand Assets", description="Collection name")
    description: str = Field(default="", description="Collection description")
    
    # Assets in collection
    assets: List[GeneratedAsset] = Field(default_factory=list, description="Assets in collection")
    
    # Collection statistics
    total_assets: int = Field(default=0, description="Total number of assets")
    high_quality_assets: int = Field(default=0, description="Number of high-quality assets")
    average_quality_score: float = Field(default=0.0, description="Average quality score")
    
    # Collection consistency
    consistency_score: Optional[float] = Field(default=None, description="Cross-asset consistency score")
    brand_coherence_score: Optional[float] = Field(default=None, description="Brand coherence score")
    
    # Completion tracking
    completion_percentage: float = Field(default=0.0, description="Collection completion percentage")
    required_asset_types: List[AssetType] = Field(default_factory=list, description="Required asset types")
    completed_asset_types: List[AssetType] = Field(default_factory=list, description="Completed asset types")
    
    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    def add_asset(self, asset: GeneratedAsset):
        """Add asset to collection and update statistics"""
        self.assets.append(asset)
        self.total_assets = len(self.assets)
        self.high_quality_assets = sum(1 for a in self.assets if a.is_high_quality())
        
        if self.assets:
            self.average_quality_score = sum(a.metadata.quality_score for a in self.assets) / len(self.assets)
        
        # Update completed asset types
        completed_types = set(asset.asset_type for asset in self.assets)
        self.completed_asset_types = list(completed_types)
        
        # Calculate completion percentage
        if self.required_asset_types:
            completed_required = len(set(self.completed_asset_types) & set(self.required_asset_types))
            self.completion_percentage = (completed_required / len(self.required_asset_types)) * 100
        
        self.update_timestamp()
    
    def get_assets_by_type(self, asset_type: AssetType) -> List[GeneratedAsset]:
        """Get all assets of a specific type"""
        return [asset for asset in self.assets if asset.asset_type == asset_type]
    
    def get_high_quality_assets(self) -> List[GeneratedAsset]:
        """Get all high-quality assets"""
        return [asset for asset in self.assets if asset.is_high_quality()]
    
    def update_timestamp(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.now(timezone.utc)

class AssetGenerationRequest(BaseModel):
    """Request for asset generation"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    project_id: str = Field(..., description="Project ID")
    
    # Generation parameters
    asset_types: List[AssetType] = Field(..., description="Asset types to generate")
    variants: List[str] = Field(default_factory=lambda: ["standard"], description="Asset variants")
    
    # Generation options
    maintain_consistency: bool = Field(default=True, description="Maintain visual consistency")
    quality_threshold: float = Field(default=0.7, description="Minimum quality threshold")
    max_retry_attempts: int = Field(default=3, description="Maximum retry attempts")
    
    # Additional context
    additional_context: str = Field(default="", description="Additional generation context")
    reference_assets: List[str] = Field(default_factory=list, description="Reference asset IDs")
    
    # Request metadata
    requested_by: str = Field(default="user", description="Who requested the generation")
    priority: str = Field(default="normal", description="Request priority")
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AssetTemplate(BaseModel):
    """Template for asset generation"""
    template_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    template_name: str = Field(..., description="Template name")
    
    # Template configuration
    asset_type: AssetType = Field(..., description="Asset type for this template")
    template_prompt: str = Field(..., description="Base prompt template")
    
    # Template parameters
    default_dimensions: AssetDimensions = Field(..., description="Default dimensions")
    style_parameters: Dict[str, Any] = Field(default_factory=dict, description="Style parameters")
    
    # Template performance
    usage_count: int = Field(default=0, description="Template usage count")
    success_rate: float = Field(default=0.0, description="Template success rate")
    average_quality: float = Field(default=0.0, description="Average quality of generated assets")
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AssetExportConfiguration(BaseModel):
    """Configuration for asset export"""
    export_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Export parameters
    export_format: str = Field(default="PNG", description="Export format")
    export_quality: str = Field(default="high", description="Export quality")
    include_variations: bool = Field(default=True, description="Include asset variations")
    
    # File organization
    folder_structure: str = Field(default="by_type", description="Folder organization method")
    naming_convention: str = Field(default="descriptive", description="File naming convention")
    
    # Additional files
    include_brand_guidelines: bool = Field(default=True, description="Include brand guidelines PDF")
    include_color_palette: bool = Field(default=True, description="Include color palette files")
    include_usage_guide: bool = Field(default=True, description="Include usage guide")
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))