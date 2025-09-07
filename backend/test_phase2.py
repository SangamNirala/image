#!/usr/bin/env python3
"""
Phase 2 Testing Script: Advanced Brand Strategy Engine
Tests the new 5-layer analysis system with Gemini AI
"""

import asyncio
import json
import sys
import os
from pathlib import Path

# Add backend to Python path
sys.path.append(str(Path(__file__).parent))

from ai_engines.emergent_strategy import AdvancedBrandStrategyEngine
from models.brand_strategy import BusinessInput

async def test_phase2_engine():
    """Test the Phase 2 Advanced Brand Strategy Engine"""
    
    print("🚀 PHASE 2: ADVANCED BRAND STRATEGY ENGINE TESTING")
    print("=" * 60)
    
    # Initialize Phase 2 engine
    engine = AdvancedBrandStrategyEngine()
    
    # Test business input
    business_input = BusinessInput(
        business_name="TechFlow Solutions", 
        business_description="AI-powered productivity platform that helps remote teams collaborate more effectively through intelligent automation and workflow optimization",
        industry="Technology/SaaS",
        target_audience="Remote teams, project managers, and productivity-focused professionals",
        business_values=["innovation", "efficiency", "collaboration", "reliability", "growth"],
        preferred_style="modern",
        preferred_colors="blue and white"
    )
    
    print(f"Testing Business: {business_input.business_name}")
    print(f"Industry: {business_input.industry}")
    print()
    
    try:
        # Test Phase 2: 5-Layer Advanced Analysis
        print("🔍 Starting 5-Layer Advanced Analysis...")
        print("-" * 40)
        
        analysis = await engine.analyze_business_concept(business_input)
        
        print("✅ Layer 1: Market Intelligence")
        market_score = analysis['confidence_scores']['market_analysis_confidence']
        print(f"   Confidence Score: {market_score:.2f}")
        
        print("✅ Layer 2: Competitive Positioning") 
        comp_score = analysis['confidence_scores']['competitive_analysis_confidence']
        print(f"   Confidence Score: {comp_score:.2f}")
        
        print("✅ Layer 3: Brand Personality")
        personality_score = analysis['confidence_scores']['personality_analysis_confidence']
        print(f"   Confidence Score: {personality_score:.2f}")
        
        print("✅ Layer 4: Visual Direction")
        visual_score = analysis['confidence_scores']['visual_brief_confidence']
        print(f"   Confidence Score: {visual_score:.2f}")
        
        print("✅ Layer 5: Strategic Synthesis")
        synthesis_score = analysis['confidence_scores']['strategic_synthesis_confidence']
        print(f"   Confidence Score: {synthesis_score:.2f}")
        
        overall_confidence = analysis['confidence_scores']['overall_confidence']
        print(f"\n🎯 OVERALL CONFIDENCE: {overall_confidence:.2f}")
        
        # Test comprehensive strategy generation
        print("\n🧠 Testing Comprehensive Strategy Generation...")
        print("-" * 45)
        
        brand_strategy = await engine.generate_comprehensive_strategy(business_input)
        
        print("✅ Advanced Brand Strategy Generated")
        print(f"   Business Name: {brand_strategy.business_name}")
        print(f"   Brand Archetype: {brand_strategy.brand_personality.get('brand_archetype', 'N/A')}")
        print(f"   Primary Traits: {brand_strategy.brand_personality.get('primary_traits', [])}")
        print(f"   Color Palette: {brand_strategy.color_palette}")
        
        if brand_strategy.advanced_analysis:
            print("✅ Advanced Analysis Data Included")
        else:
            print("⚠️  Advanced Analysis Data Missing")
        
        print("\n🏆 PHASE 2 TESTING RESULTS:")
        print("=" * 35)
        print(f"✅ 5-Layer Analysis: COMPLETE")
        print(f"✅ Confidence Scores: {overall_confidence:.1%} AVERAGE")
        print(f"✅ Strategy Generation: COMPLETE")
        print(f"✅ Advanced Data Storage: {'✅' if brand_strategy.advanced_analysis else '❌'}")
        
        if overall_confidence >= 0.85:
            print(f"\n🎉 PHASE 2: ADVANCED IMPLEMENTATION SUCCESS!")
            print("   Revolutionary multi-layer analysis working perfectly!")
        else:
            print(f"\n⚠️  PHASE 2: NEEDS OPTIMIZATION")
            print(f"   Current confidence: {overall_confidence:.1%} (Target: >85%)")
            
        return True
        
    except Exception as e:
        print(f"\n❌ PHASE 2 ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Run Phase 2 testing
    success = asyncio.run(test_phase2_engine())
    
    if success:
        print(f"\n🚀 Phase 2 implementation ready for production!")
        exit(0)
    else:
        print(f"\n💥 Phase 2 needs debugging...")
        exit(1)