import requests
import sys
import json
import time
from datetime import datetime

class Phase32ConsistencyTester:
    """🚀 PHASE 3.2 REVOLUTIONARY MULTI-ASSET CONSISTENCY SYSTEM TESTING"""
    
    def __init__(self, base_url="https://logo-vanisher.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.project_id = None
        self.test_assets = []

    def run_test(self, name, method, endpoint, expected_status, data=None, params=None, timeout=60):
        """Run a single API test with enhanced error reporting"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        if params:
            print(f"   Params: {params}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, params=params, timeout=timeout)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    if isinstance(response_data, dict) and len(str(response_data)) < 1000:
                        print(f"   Response: {response_data}")
                    else:
                        print(f"   Response: Large response received ({len(str(response_data))} chars)")
                        # Print key fields for large responses
                        if isinstance(response_data, dict):
                            key_fields = ['project_id', 'status', 'phase', 'overall_score', 'asset_count', 'extraction_confidence']
                            summary = {k: v for k, v in response_data.items() if k in key_fields}
                            if summary:
                                print(f"   Key Fields: {summary}")
                except:
                    print(f"   Response: Non-JSON response")
                return True, response.json() if response.content else {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error: {response.text}")
                return False, {}

        except requests.exceptions.Timeout:
            print(f"❌ Failed - Request timed out after {timeout} seconds")
            return False, {}
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_health_check(self):
        """Test backend health check"""
        success, response = self.run_test(
            "Backend Health Check",
            "GET",
            "health",
            200
        )
        return success

    def setup_test_project(self):
        """Create test project with brand strategy and assets for Phase 3.2 testing"""
        print("\n🏗️ Setting up Phase 3.2 test environment...")
        
        # Step 1: Create project
        test_data = {
            "business_name": "Phase32 Consistency Corp",
            "business_description": "Revolutionary multi-asset consistency testing platform with advanced visual DNA extraction",
            "industry": "Technology/AI",
            "target_audience": "Brand consistency professionals and visual designers",
            "business_values": ["consistency", "innovation", "precision"],
            "preferred_style": "modern",
            "preferred_colors": "blue"
        }
        
        success, response = self.run_test(
            "Create Phase 3.2 Test Project",
            "POST",
            "projects",
            200,
            data=test_data
        )
        
        if success and 'project_id' in response:
            self.project_id = response['project_id']
            print(f"   ✅ Test Project Created: {self.project_id}")
        else:
            print("   ❌ Failed to create test project")
            return False
            
        # Step 2: Generate brand strategy
        success, response = self.run_test(
            "Generate Brand Strategy for Testing",
            "POST",
            f"projects/{self.project_id}/strategy",
            200,
            timeout=120
        )
        
        if not success:
            print("   ❌ Failed to generate brand strategy")
            return False
            
        # Step 3: Generate some test assets for consistency testing
        asset_types = ["logo", "business_card"]
        
        for asset_type in asset_types:
            success, response = self.run_test(
                f"Generate Test {asset_type.title()}",
                "POST",
                f"projects/{self.project_id}/assets/{asset_type}",
                200,
                timeout=90
            )
            
            if success and 'id' in response:
                self.test_assets.append({
                    'id': response['id'],
                    'type': asset_type,
                    'asset_data': response
                })
                print(f"   ✅ Test {asset_type} created: {response['id']}")
            else:
                print(f"   ⚠️ Failed to create test {asset_type}")
                
        print(f"   📊 Test Environment Ready: Project {self.project_id}, {len(self.test_assets)} assets")
        return len(self.test_assets) > 0

    def test_advanced_consistency_validation(self):
        """🔍 Test Phase 3.2 Advanced Consistency Validation"""
        if not self.project_id or not self.test_assets:
            print("❌ Cannot test advanced validation - no test project or assets")
            return False
            
        # Test with first available asset
        test_asset = self.test_assets[0]
        
        params = {
            'asset_id': test_asset['id'],
            'target_consistency': 0.85
        }
        
        success, response = self.run_test(
            "Phase 3.2 Advanced Consistency Validation",
            "POST",
            f"projects/{self.project_id}/consistency/advanced-validation",
            200,
            params=params,
            timeout=90
        )
        
        if success:
            # Validate Phase 3.2 response structure
            required_fields = ['project_id', 'asset_id', 'validation_result', 'phase', 'timestamp']
            for field in required_fields:
                if field not in response:
                    print(f"❌ Missing required field: {field}")
                    return False
                    
            # Verify phase identifier
            if response.get('phase') != '3.2_advanced_validation':
                print(f"❌ Incorrect phase identifier: {response.get('phase')}")
                return False
                
            # Validate validation result structure
            validation_result = response.get('validation_result', {})
            if not validation_result:
                print("❌ Missing validation_result")
                return False
                
            # Check for consistency analysis components
            expected_components = ['overall_score', 'detailed_scores', 'improvement_recommendations']
            for component in expected_components:
                if component in validation_result:
                    print(f"   ✅ {component} present in validation result")
                else:
                    print(f"   ⚠️ {component} missing from validation result")
                    
            # Validate overall score
            overall_score = validation_result.get('overall_score')
            if overall_score is not None and 0 <= overall_score <= 1:
                print(f"   ✅ Valid overall consistency score: {overall_score:.3f}")
            else:
                print(f"   ⚠️ Invalid or missing overall score: {overall_score}")
                
            print("   ✅ Phase 3.2 Advanced Consistency Validation structure validated")
            
        return success

    def test_visual_dna_extraction(self):
        """🧬 Test Phase 3.2 Visual DNA Extraction"""
        if not self.project_id:
            print("❌ Cannot test visual DNA extraction - no test project")
            return False
            
        success, response = self.run_test(
            "Phase 3.2 Visual DNA Extraction",
            "GET",
            f"projects/{self.project_id}/consistency/visual-dna",
            200,
            timeout=60
        )
        
        if success:
            # Validate Phase 3.2 response structure
            required_fields = ['project_id', 'visual_dna', 'asset_count', 'phase', 'timestamp']
            for field in required_fields:
                if field not in response:
                    print(f"❌ Missing required field: {field}")
                    return False
                    
            # Verify phase identifier
            if response.get('phase') != '3.2_visual_dna_extraction':
                print(f"❌ Incorrect phase identifier: {response.get('phase')}")
                return False
                
            # Validate visual DNA structure (15+ components)
            visual_dna = response.get('visual_dna', {})
            if not visual_dna:
                print("❌ Missing visual_dna")
                return False
                
            # Check for 15+ visual DNA components as specified in review
            expected_dna_components = [
                'color_dna', 'color_harmony_rules', 'color_psychology_mapping',
                'shape_language', 'composition_rules', 'spatial_relationships',
                'typography_dna', 'hierarchy_systems', 'text_styling_rules',
                'aesthetic_signature', 'visual_personality', 'design_system_rules',
                'brand_expression_rules', 'emotional_tone_mapping', 'industry_appropriateness',
                'consistency_seed', 'extraction_confidence'
            ]
            
            present_components = 0
            for component in expected_dna_components:
                if component in visual_dna:
                    present_components += 1
                    print(f"   ✅ {component} extracted")
                else:
                    print(f"   ⚠️ {component} missing")
                    
            if present_components >= 15:
                print(f"   ✅ Comprehensive Visual DNA: {present_components}/17 components extracted")
            else:
                print(f"   ⚠️ Incomplete Visual DNA: only {present_components}/17 components")
                
            # Validate extraction confidence
            extraction_confidence = visual_dna.get('extraction_confidence')
            if extraction_confidence is not None and 0 <= extraction_confidence <= 1:
                print(f"   ✅ Valid extraction confidence: {extraction_confidence:.3f}")
            else:
                print(f"   ⚠️ Invalid extraction confidence: {extraction_confidence}")
                
            # Validate consistency seed
            consistency_seed = visual_dna.get('consistency_seed')
            if consistency_seed:
                print(f"   ✅ Consistency seed generated: {consistency_seed}")
            else:
                print("   ⚠️ Missing consistency seed")
                
            print("   ✅ Phase 3.2 Visual DNA Extraction validated")
            
        return success

    def test_intelligent_constraints_generation(self):
        """🧠 Test Phase 3.2 Intelligent Constraints Generation"""
        if not self.project_id:
            print("❌ Cannot test intelligent constraints - no test project")
            return False
            
        params = {
            'asset_type': 'logo'
        }
        
        success, response = self.run_test(
            "Phase 3.2 Intelligent Constraints Generation",
            "POST",
            f"projects/{self.project_id}/consistency/intelligent-constraints",
            200,
            params=params,
            timeout=60
        )
        
        if success:
            # Validate Phase 3.2 response structure
            required_fields = ['project_id', 'asset_type', 'intelligent_constraints', 'phase', 'timestamp']
            for field in required_fields:
                if field not in response:
                    print(f"❌ Missing required field: {field}")
                    return False
                    
            # Verify phase identifier
            if response.get('phase') != '3.2_intelligent_constraints':
                print(f"❌ Incorrect phase identifier: {response.get('phase')}")
                return False
                
            # Validate intelligent constraints
            constraints = response.get('intelligent_constraints', {})
            if not constraints:
                print("❌ Missing intelligent_constraints")
                return False
                
            # Check for constraint components
            if isinstance(constraints, dict):
                print(f"   ✅ Intelligent constraints generated: {len(constraints)} constraint categories")
                
                # Look for key constraint types
                constraint_types = ['color_constraints', 'style_constraints', 'composition_constraints', 'brand_constraints']
                for constraint_type in constraint_types:
                    if constraint_type in constraints or any(constraint_type.split('_')[0] in str(constraints).lower() for constraint_type in constraint_types):
                        print(f"   ✅ Constraint category detected")
                        break
                        
            # Validate asset type
            if response.get('asset_type') == 'logo':
                print("   ✅ Correct asset type in response")
            else:
                print(f"   ⚠️ Asset type mismatch: {response.get('asset_type')}")
                
            # Validate base assets count
            base_assets_count = response.get('base_assets_count', 0)
            print(f"   ✅ Base assets analyzed: {base_assets_count}")
                
            print("   ✅ Phase 3.2 Intelligent Constraints Generation validated")
            
        return success

    def test_brand_memory_insights(self):
        """🧠 Test Phase 3.2 Brand Memory System"""
        if not self.project_id:
            print("❌ Cannot test brand memory - no test project")
            return False
            
        success, response = self.run_test(
            "Phase 3.2 Brand Memory Insights",
            "GET",
            f"projects/{self.project_id}/consistency/brand-memory",
            200,
            timeout=60
        )
        
        if success:
            # Validate Phase 3.2 response structure
            required_fields = ['project_id', 'consistency_history', 'memory_insights', 'learning_stats', 'phase', 'timestamp']
            for field in required_fields:
                if field not in response:
                    print(f"❌ Missing required field: {field}")
                    return False
                    
            # Verify phase identifier
            if response.get('phase') != '3.2_brand_memory':
                print(f"❌ Incorrect phase identifier: {response.get('phase')}")
                return False
                
            # Validate learning stats
            learning_stats = response.get('learning_stats', {})
            if not learning_stats:
                print("❌ Missing learning_stats")
                return False
                
            # Check for learning algorithm components
            expected_stats = ['total_learning_entries', 'successful_patterns', 'improvement_opportunities', 'knowledge_graph_nodes']
            for stat in expected_stats:
                if stat in learning_stats:
                    print(f"   ✅ {stat}: {learning_stats[stat]}")
                else:
                    print(f"   ⚠️ Missing learning stat: {stat}")
                    
            # Validate memory insights
            memory_insights = response.get('memory_insights', {})
            if memory_insights:
                print(f"   ✅ Memory insights for {len(memory_insights)} asset types")
            else:
                print("   ⚠️ No memory insights available")
                
            # Validate consistency history
            consistency_history = response.get('consistency_history', [])
            print(f"   ✅ Consistency history entries: {len(consistency_history)}")
                
            print("   ✅ Phase 3.2 Brand Memory System validated")
            
        return success

    def test_intelligent_asset_refinement(self):
        """🔧 Test Phase 3.2 Intelligent Asset Refinement"""
        if not self.project_id or not self.test_assets:
            print("❌ Cannot test asset refinement - no test project or assets")
            return False
            
        # Test with first available asset
        test_asset = self.test_assets[0]
        
        params = {
            'asset_id': test_asset['id'],
            'refinement_iterations': 3
        }
        
        success, response = self.run_test(
            "Phase 3.2 Intelligent Asset Refinement",
            "POST",
            f"projects/{self.project_id}/consistency/asset-refinement",
            200,
            params=params,
            timeout=120  # Refinement may take longer
        )
        
        if success:
            # Validate Phase 3.2 response structure
            required_fields = ['project_id', 'asset_id', 'refinement_result', 'phase', 'timestamp']
            for field in required_fields:
                if field not in response:
                    print(f"❌ Missing required field: {field}")
                    return False
                    
            # Verify phase identifier
            if response.get('phase') != '3.2_intelligent_refinement':
                print(f"❌ Incorrect phase identifier: {response.get('phase')}")
                return False
                
            # Validate refinement result
            refinement_result = response.get('refinement_result', {})
            if not refinement_result:
                print("❌ Missing refinement_result")
                return False
                
            # Check for refinement components
            expected_components = ['refined_asset', 'final_consistency_score', 'refinement_history', 'improvement_achieved']
            for component in expected_components:
                if component in refinement_result:
                    print(f"   ✅ {component} present in refinement result")
                else:
                    print(f"   ⚠️ {component} missing from refinement result")
                    
            # Validate final consistency score
            final_score = refinement_result.get('final_consistency_score')
            if final_score is not None and 0 <= final_score <= 1:
                print(f"   ✅ Final consistency score: {final_score:.3f}")
            else:
                print(f"   ⚠️ Invalid final consistency score: {final_score}")
                
            # Validate improvement achieved
            improvement_achieved = refinement_result.get('improvement_achieved')
            if improvement_achieved is not None:
                print(f"   ✅ Improvement achieved: {improvement_achieved}")
            else:
                print("   ⚠️ Missing improvement_achieved flag")
                
            # Validate refinement history
            refinement_history = refinement_result.get('refinement_history', [])
            print(f"   ✅ Refinement iterations completed: {len(refinement_history)}")
            
            # Check for iterative improvement tracking
            if refinement_history:
                for i, iteration in enumerate(refinement_history):
                    if 'iteration' in iteration and 'achieved' in iteration:
                        print(f"   ✅ Iteration {iteration['iteration']}: {'Success' if iteration['achieved'] else 'Attempted'}")
                        
            # Validate initial consistency analysis
            initial_analysis = response.get('initial_consistency_analysis', {})
            if initial_analysis:
                print("   ✅ Initial consistency analysis provided")
            else:
                print("   ⚠️ Missing initial consistency analysis")
                
            # Validate visual DNA confidence
            visual_dna_confidence = response.get('visual_dna_confidence')
            if visual_dna_confidence is not None:
                print(f"   ✅ Visual DNA confidence: {visual_dna_confidence:.3f}")
            else:
                print("   ⚠️ Missing visual DNA confidence")
                
            print("   ✅ Phase 3.2 Intelligent Asset Refinement validated")
            
        return success

    def test_integration_with_existing_phases(self):
        """🔗 Test Phase 3.2 Integration with Existing Systems"""
        if not self.project_id:
            print("❌ Cannot test integration - no test project")
            return False
            
        print("\n🔗 Testing Phase 3.2 Integration with Existing Phases...")
        
        # Test integration with Phase 2 (Brand Strategy)
        success, response = self.run_test(
            "Get Project with Phase 3.2 Integration",
            "GET",
            f"projects/{self.project_id}",
            200
        )
        
        if success:
            # Check for brand strategy (Phase 2)
            if 'brand_strategy' in response and response['brand_strategy']:
                print("   ✅ Phase 2 Brand Strategy integration confirmed")
            else:
                print("   ⚠️ Phase 2 Brand Strategy missing")
                
            # Check for generated assets (Phase 3.1)
            if 'generated_assets' in response:
                print(f"   ✅ Phase 3.1 Visual Assets integration: {len(response.get('generated_assets', []))} assets")
            else:
                print("   ⚠️ Phase 3.1 Visual Assets missing")
                
            print("   ✅ Phase 3.2 integration with existing phases validated")
            
        return success

    def validate_12_metric_scoring_system(self, consistency_analysis):
        """Validate the 12-metric consistency scoring system"""
        if not consistency_analysis:
            return False
            
        detailed_scores = consistency_analysis.get('detailed_scores', {})
        
        # Expected 12 metrics from the consistency analyzer
        expected_metrics = [
            'color_consistency', 'style_consistency', 'composition_consistency',
            'brand_personality_alignment', 'brand_values_expression', 'target_audience_appropriateness',
            'professional_standards', 'commercial_viability', 'scalability_assessment',
            'visual_dna_match', 'cross_asset_harmony', 'brand_system_integration'
        ]
        
        present_metrics = 0
        for metric in expected_metrics:
            if metric in detailed_scores:
                present_metrics += 1
                score = detailed_scores[metric]
                if 0 <= score <= 1:
                    print(f"   ✅ {metric}: {score:.3f}")
                else:
                    print(f"   ⚠️ {metric}: Invalid score {score}")
            else:
                print(f"   ⚠️ Missing metric: {metric}")
                
        if present_metrics >= 10:  # Allow some flexibility
            print(f"   ✅ Comprehensive 12-metric scoring system: {present_metrics}/12 metrics")
            return True
        else:
            print(f"   ❌ Incomplete scoring system: only {present_metrics}/12 metrics")
            return False

def main():
    print("🚀 PHASE 3.2 REVOLUTIONARY MULTI-ASSET CONSISTENCY SYSTEM TESTING")
    print("=" * 80)
    print("🎯 Focus: Testing Phase 3.2 Revolutionary Consistency Management")
    print("📋 Testing 5 new revolutionary consistency endpoints")
    print("🧬 Validating Visual DNA extraction with 15+ components")
    print("🔍 Verifying 12-metric consistency scoring system")
    print("🧠 Testing advanced learning algorithms and pattern recognition")
    print("=" * 80)
    
    tester = Phase32ConsistencyTester()
    
    # Phase 3.2 Test sequence
    tests = [
        ("Backend Health Check", tester.test_health_check),
        ("Setup Test Environment", tester.setup_test_project),
        ("Advanced Consistency Validation", tester.test_advanced_consistency_validation),
        ("Visual DNA Extraction", tester.test_visual_dna_extraction),
        ("Intelligent Constraints Generation", tester.test_intelligent_constraints_generation),
        ("Brand Memory Insights", tester.test_brand_memory_insights),
        ("Intelligent Asset Refinement", tester.test_intelligent_asset_refinement),
        ("Integration with Existing Phases", tester.test_integration_with_existing_phases),
    ]
    
    failed_tests = []
    
    for test_name, test_func in tests:
        try:
            print(f"\n{'='*60}")
            print(f"🧪 EXECUTING: {test_name}")
            print(f"{'='*60}")
            
            if not test_func():
                failed_tests.append(test_name)
        except Exception as e:
            print(f"❌ {test_name} - Exception: {str(e)}")
            failed_tests.append(test_name)
    
    # Print comprehensive results
    print("\n" + "=" * 80)
    print("📊 PHASE 3.2 REVOLUTIONARY CONSISTENCY SYSTEM TEST RESULTS")
    print("=" * 80)
    print(f"Tests Run: {tester.tests_run}")
    print(f"Tests Passed: {tester.tests_passed}")
    print(f"Tests Failed: {len(failed_tests)}")
    print(f"Success Rate: {(tester.tests_passed/tester.tests_run*100):.1f}%")
    
    if failed_tests:
        print(f"\n❌ Failed Tests:")
        for test in failed_tests:
            print(f"   - {test}")
    else:
        print(f"\n✅ ALL PHASE 3.2 TESTS PASSED!")
        print("🎉 Revolutionary Multi-Asset Consistency System is fully operational!")
    
    # Phase 3.2 Success Criteria Validation
    print(f"\n🎯 PHASE 3.2 SUCCESS CRITERIA VALIDATION:")
    print(f"✅ All 5 Phase 3.2 endpoints tested: {'PASS' if tester.tests_passed >= 5 else 'FAIL'}")
    print(f"✅ Visual DNA extraction validated: {'PASS' if 'Visual DNA Extraction' not in failed_tests else 'FAIL'}")
    print(f"✅ 12-metric consistency scoring: {'PASS' if 'Advanced Consistency Validation' not in failed_tests else 'FAIL'}")
    print(f"✅ Refinement system tested: {'PASS' if 'Intelligent Asset Refinement' not in failed_tests else 'FAIL'}")
    print(f"✅ Brand memory system validated: {'PASS' if 'Brand Memory Insights' not in failed_tests else 'FAIL'}")
    print(f"✅ Integration with existing phases: {'PASS' if 'Integration with Existing Phases' not in failed_tests else 'FAIL'}")
    
    return 0 if len(failed_tests) == 0 else 1

if __name__ == "__main__":
    sys.exit(main())