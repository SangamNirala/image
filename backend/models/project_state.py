"""
Project State Models
Advanced data models for project management and session state
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timezone
from enum import Enum
import uuid

from .brand_strategy import BrandStrategy, BusinessInput
from .visual_assets import AssetCollection, GeneratedAsset, AssetType

class ProjectStatus(Enum):
    """Project status enumeration"""
    CREATED = "created"
    STRATEGY_IN_PROGRESS = "strategy_in_progress"
    STRATEGY_COMPLETED = "strategy_completed"
    ASSETS_IN_PROGRESS = "assets_in_progress"
    ASSETS_COMPLETED = "assets_completed"
    REVIEW_IN_PROGRESS = "review_in_progress"
    EXPORT_READY = "export_ready"
    COMPLETED = "completed"
    PAUSED = "paused"
    CANCELLED = "cancelled"

class ProjectMetadata(BaseModel):
    """Comprehensive project metadata"""
    metadata_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Project tracking
    project_phase: str = Field(default="initialization", description="Current project phase")
    completion_percentage: float = Field(default=0.0, description="Overall completion percentage")
    estimated_completion_time: Optional[datetime] = Field(default=None, description="Estimated completion")
    
    # Performance metrics
    generation_time_strategy: Optional[float] = Field(default=None, description="Strategy generation time (seconds)")
    generation_time_assets: Optional[float] = Field(default=None, description="Asset generation time (seconds)")
    total_generation_time: Optional[float] = Field(default=None, description="Total generation time (seconds)")
    
    # Quality metrics
    strategy_quality_score: Optional[float] = Field(default=None, description="Strategy quality score")
    assets_quality_score: Optional[float] = Field(default=None, description="Average asset quality score")
    overall_quality_score: Optional[float] = Field(default=None, description="Overall project quality")
    
    # User interaction
    user_feedback_score: Optional[float] = Field(default=None, description="User feedback score")
    revision_count: int = Field(default=0, description="Number of revisions made")
    user_sessions: int = Field(default=1, description="Number of user sessions")
    
    # Technical metrics
    ai_model_versions: Dict[str, str] = Field(default_factory=dict, description="AI model versions used")
    generation_attempts: Dict[str, int] = Field(default_factory=dict, description="Generation attempts per component")
    
    # Collaboration
    collaborators: List[str] = Field(default_factory=list, description="Project collaborators")
    sharing_permissions: Dict[str, str] = Field(default_factory=dict, description="Sharing permissions")

class BrandProject(BaseModel):
    """Complete brand project with all components and state management"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Project identification
    project_name: str = Field(default="", description="Project name")
    project_description: str = Field(default="", description="Project description")
    
    # Business context
    business_input: BusinessInput = Field(..., description="Original business requirements")
    
    # Brand strategy
    brand_strategy: Optional[BrandStrategy] = Field(default=None, description="Generated brand strategy")
    strategy_alternatives: List[BrandStrategy] = Field(default_factory=list, description="Alternative strategies")
    
    # Visual assets
    asset_collection: Optional[AssetCollection] = Field(default=None, description="Generated assets collection")
    featured_assets: List[str] = Field(default_factory=list, description="Featured asset IDs")
    
    # Project state
    status: ProjectStatus = Field(default=ProjectStatus.CREATED, description="Current project status")
    metadata: ProjectMetadata = Field(default_factory=ProjectMetadata, description="Project metadata")
    
    # Project configuration
    generation_preferences: Dict[str, Any] = Field(default_factory=dict, description="Generation preferences")
    brand_guidelines: Dict[str, Any] = Field(default_factory=dict, description="Brand guidelines")
    export_configuration: Dict[str, Any] = Field(default_factory=dict, description="Export configuration")
    
    # Project timeline
    milestones: List[Dict[str, Any]] = Field(default_factory=list, description="Project milestones")
    timeline: Dict[str, datetime] = Field(default_factory=dict, description="Project timeline")
    
    # Collaboration and sharing
    owner_id: str = Field(default="anonymous", description="Project owner ID")
    access_permissions: Dict[str, str] = Field(default_factory=dict, description="Access permissions")
    shared_publicly: bool = Field(default=False, description="Whether project is public")
    
    # Version control
    version: str = Field(default="1.0", description="Project version")
    version_history: List[Dict[str, Any]] = Field(default_factory=list, description="Version history")
    
    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_accessed: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    def update_status(self, new_status: ProjectStatus, notes: str = ""):
        """Update project status with tracking"""
        old_status = self.status
        self.status = new_status
        self.updated_at = datetime.now(timezone.utc)
        
        # Add to timeline
        self.timeline[new_status.value] = self.updated_at
        
        # Add milestone
        milestone = {
            "status": new_status.value,
            "previous_status": old_status.value,
            "timestamp": self.updated_at,
            "notes": notes
        }
        self.milestones.append(milestone)
        
        # Update completion percentage
        self._update_completion_percentage()
    
    def _update_completion_percentage(self):
        """Update completion percentage based on current status"""
        status_completion = {
            ProjectStatus.CREATED: 10,
            ProjectStatus.STRATEGY_IN_PROGRESS: 25,
            ProjectStatus.STRATEGY_COMPLETED: 40,
            ProjectStatus.ASSETS_IN_PROGRESS: 60,
            ProjectStatus.ASSETS_COMPLETED: 80,
            ProjectStatus.REVIEW_IN_PROGRESS: 90,
            ProjectStatus.EXPORT_READY: 95,
            ProjectStatus.COMPLETED: 100
        }
        
        self.metadata.completion_percentage = status_completion.get(self.status, 0)
    
    def add_brand_strategy(self, strategy: BrandStrategy):
        """Add brand strategy to project"""
        self.brand_strategy = strategy
        self.update_status(ProjectStatus.STRATEGY_COMPLETED, "Brand strategy generated")
        
        # Update metadata
        self.metadata.strategy_quality_score = strategy.strategy_score
    
    def add_asset_collection(self, collection: AssetCollection):
        """Add asset collection to project"""
        self.asset_collection = collection
        
        if collection.completion_percentage >= 100:
            self.update_status(ProjectStatus.ASSETS_COMPLETED, "All assets generated")
        else:
            self.update_status(ProjectStatus.ASSETS_IN_PROGRESS, f"Assets {collection.completion_percentage}% complete")
        
        # Update metadata
        self.metadata.assets_quality_score = collection.average_quality_score
        self._update_overall_quality()
    
    def _update_overall_quality(self):
        """Update overall project quality score"""
        scores = []
        
        if self.metadata.strategy_quality_score:
            scores.append(self.metadata.strategy_quality_score)
        
        if self.metadata.assets_quality_score:
            scores.append(self.metadata.assets_quality_score)
        
        if scores:
            self.metadata.overall_quality_score = sum(scores) / len(scores)
    
    def get_required_assets(self) -> List[AssetType]:
        """Get list of required asset types based on business input"""
        # Basic required assets for all businesses
        required = [
            AssetType.LOGO,
            AssetType.BUSINESS_CARD,
            AssetType.LETTERHEAD
        ]
        
        # Additional assets based on industry/needs
        industry = self.business_input.industry.lower()
        
        if "retail" in industry or "ecommerce" in industry:
            required.extend([
                AssetType.SOCIAL_MEDIA_POST,
                AssetType.FLYER,
                AssetType.PACKAGING
            ])
        elif "tech" in industry or "software" in industry:
            required.extend([
                AssetType.WEBSITE_MOCKUP,
                AssetType.PRESENTATION_TEMPLATE,
                AssetType.EMAIL_TEMPLATE
            ])
        elif "food" in industry or "restaurant" in industry:
            required.extend([
                AssetType.SOCIAL_MEDIA_POST,
                AssetType.FLYER,
                AssetType.BANNER
            ])
        else:
            # Default additional assets
            required.extend([
                AssetType.SOCIAL_MEDIA_POST,
                AssetType.FLYER,
                AssetType.BANNER
            ])
        
        return required
    
    def is_ready_for_export(self) -> bool:
        """Check if project is ready for export"""
        return (
            self.brand_strategy is not None and
            self.asset_collection is not None and
            self.asset_collection.completion_percentage >= 80 and
            self.status in [ProjectStatus.ASSETS_COMPLETED, ProjectStatus.EXPORT_READY, ProjectStatus.COMPLETED]
        )
    
    def get_export_package(self) -> Dict[str, Any]:
        """Get complete export package"""
        if not self.is_ready_for_export():
            raise ValueError("Project not ready for export")
        
        return {
            "project_info": {
                "name": self.project_name or self.business_input.business_name,
                "description": self.business_input.business_description,
                "created_at": self.created_at,
                "version": self.version
            },
            "brand_strategy": self.brand_strategy.dict() if self.brand_strategy else None,
            "assets": [asset.dict() for asset in self.asset_collection.assets] if self.asset_collection else [],
            "brand_guidelines": self.brand_guidelines,
            "metadata": self.metadata.dict()
        }
    
    def update_last_accessed(self):
        """Update last accessed timestamp"""
        self.last_accessed = datetime.now(timezone.utc)

class ProjectSession(BaseModel):
    """Individual user session within a project"""
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    project_id: str = Field(..., description="Associated project ID")
    
    # Session details
    user_id: str = Field(default="anonymous", description="User identifier")
    session_start: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    session_end: Optional[datetime] = Field(default=None, description="Session end time")
    
    # Session activity
    actions_performed: List[Dict[str, Any]] = Field(default_factory=list, description="Actions in this session")
    pages_visited: List[str] = Field(default_factory=list, description="Pages visited")
    
    # Session state
    current_step: str = Field(default="business_input", description="Current workflow step")
    session_data: Dict[str, Any] = Field(default_factory=dict, description="Temporary session data")
    
    # Session metrics
    time_spent: Optional[float] = Field(default=None, description="Total time spent (seconds)")
    engagement_score: Optional[float] = Field(default=None, description="User engagement score")
    
    def add_action(self, action_type: str, details: Dict[str, Any]):
        """Add action to session history"""
        action = {
            "action_type": action_type,
            "timestamp": datetime.now(timezone.utc),
            "details": details
        }
        self.actions_performed.append(action)
    
    def end_session(self):
        """End the current session"""
        self.session_end = datetime.now(timezone.utc)
        if self.session_start:
            self.time_spent = (self.session_end - self.session_start).total_seconds()

class ProjectAnalytics(BaseModel):
    """Analytics and insights for brand projects"""
    analytics_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    project_id: str = Field(..., description="Associated project ID")
    
    # Performance analytics
    generation_performance: Dict[str, Any] = Field(default_factory=dict, description="Generation performance metrics")
    quality_analytics: Dict[str, Any] = Field(default_factory=dict, description="Quality analytics")
    user_behavior: Dict[str, Any] = Field(default_factory=dict, description="User behavior analytics")
    
    # Comparative analytics
    industry_benchmarks: Dict[str, Any] = Field(default_factory=dict, description="Industry benchmark comparison")
    similar_projects: List[str] = Field(default_factory=list, description="Similar project IDs")
    
    # Insights and recommendations
    insights: List[str] = Field(default_factory=list, description="Generated insights")
    recommendations: List[str] = Field(default_factory=list, description="Improvement recommendations")
    
    # Analytics metadata
    last_updated: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    analytics_version: str = Field(default="1.0", description="Analytics version")

class ProjectTemplate(BaseModel):
    """Template for creating similar projects"""
    template_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    template_name: str = Field(..., description="Template name")
    
    # Template source
    source_project_id: str = Field(..., description="Source project ID")
    industry: str = Field(..., description="Target industry")
    business_type: str = Field(..., description="Business type")
    
    # Template components
    business_input_template: Dict[str, Any] = Field(default_factory=dict, description="Business input template")
    strategy_template: Dict[str, Any] = Field(default_factory=dict, description="Strategy template")
    asset_requirements: List[AssetType] = Field(default_factory=list, description="Required assets")
    
    # Template metadata
    usage_count: int = Field(default=0, description="Template usage count")
    success_rate: float = Field(default=0.0, description="Template success rate")
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))