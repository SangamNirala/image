import requests
import json

def test_phase2_advanced_analysis_detailed():
    """Detailed test of Phase 2 Advanced Analysis response structure"""
    base_url = "https://logo-vanisher.preview.emergentagent.com/api"
    
    # Create test project
    test_data = {
        "business_name": "Phase2 TestCorp",
        "business_description": "AI-powered productivity platform for remote teams",
        "industry": "Technology/SaaS",
        "target_audience": "Remote teams and project managers",
        "business_values": ["innovation", "efficiency", "collaboration"],
        "preferred_style": "modern",
        "preferred_colors": "blue"
    }
    
    print("🔍 Creating test project...")
    response = requests.post(f"{base_url}/projects", json=test_data)
    if response.status_code != 200:
        print(f"❌ Failed to create project: {response.status_code}")
        return False
    
    project_id = response.json()['project_id']
    print(f"✅ Project created: {project_id}")
    
    # Test advanced analysis
    print("🔍 Testing Phase 2 Advanced Analysis...")
    response = requests.post(f"{base_url}/projects/{project_id}/advanced-analysis", timeout=180)
    
    if response.status_code != 200:
        print(f"❌ Advanced analysis failed: {response.status_code}")
        print(f"Error: {response.text}")
        return False
    
    analysis_data = response.json()
    
    # Detailed validation
    print("📋 DETAILED ANALYSIS VALIDATION:")
    print("=" * 50)
    
    # Check required fields
    required_fields = ['project_id', 'analysis_complete', 'analysis_layers', 'confidence_scores']
    for field in required_fields:
        if field in analysis_data:
            print(f"✅ {field}: Present")
        else:
            print(f"❌ {field}: Missing")
            return False
    
    # Check analysis layers structure
    analysis_layers = analysis_data.get('analysis_layers', {})
    expected_layers = {
        'market_intelligence': ['market_size', 'growth_trends', 'key_opportunities'],
        'competitive_positioning': ['direct_competitors', 'competitive_advantages', 'market_positioning'],
        'brand_personality': ['brand_archetype', 'personality_traits', 'brand_voice'],
        'visual_direction': ['design_principles', 'visual_style', 'color_strategy'],
        'strategic_recommendations': ['brand_strategy', 'marketing_approach', 'implementation_roadmap']
    }
    
    print("\n📊 ANALYSIS LAYERS VALIDATION:")
    for layer_name, expected_keys in expected_layers.items():
        if layer_name in analysis_layers:
            layer_data = analysis_layers[layer_name]
            print(f"✅ {layer_name}: Present")
            
            # Check if it has meaningful content
            if isinstance(layer_data, dict) and len(str(layer_data)) > 100:
                print(f"   ✅ Contains substantial analysis data ({len(str(layer_data))} chars)")
            else:
                print(f"   ⚠️  Limited data: {len(str(layer_data))} chars")
        else:
            print(f"❌ {layer_name}: Missing")
            return False
    
    # Check confidence scores
    confidence_scores = analysis_data.get('confidence_scores', {})
    print(f"\n🎯 CONFIDENCE SCORES:")
    expected_confidence_keys = [
        'market_analysis_confidence',
        'competitive_analysis_confidence', 
        'personality_analysis_confidence',
        'visual_brief_confidence',
        'strategic_synthesis_confidence',
        'overall_confidence'
    ]
    
    for key in expected_confidence_keys:
        if key in confidence_scores:
            score = confidence_scores[key]
            print(f"✅ {key}: {score}")
            
            # Validate score is reasonable (0.0 to 1.0)
            if isinstance(score, (int, float)) and 0.0 <= score <= 1.0:
                print(f"   ✅ Valid confidence score: {score}")
            else:
                print(f"   ⚠️  Unusual confidence score: {score}")
        else:
            print(f"❌ {key}: Missing")
    
    print(f"\n📈 OVERALL ANALYSIS:")
    print(f"   Analysis Complete: {analysis_data.get('analysis_complete')}")
    print(f"   Total Response Size: {len(str(analysis_data))} characters")
    print(f"   Project ID Match: {analysis_data.get('project_id') == project_id}")
    
    return True

if __name__ == "__main__":
    print("🚀 Phase 2 Advanced Analysis - Detailed Structure Test")
    print("=" * 60)
    
    success = test_phase2_advanced_analysis_detailed()
    
    if success:
        print("\n✅ Phase 2 Advanced Analysis structure validation PASSED")
    else:
        print("\n❌ Phase 2 Advanced Analysis structure validation FAILED")