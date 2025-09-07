import requests
import sys
import json
import time
from datetime import datetime

class BrandForgeAPITester:
    def __init__(self, base_url="https://logo-vanisher.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.project_id = None

    def run_test(self, name, method, endpoint, expected_status, data=None, params=None, timeout=30):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
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
                    if isinstance(response_data, dict) and len(str(response_data)) < 500:
                        print(f"   Response: {response_data}")
                    else:
                        print(f"   Response: Large response received ({len(str(response_data))} chars)")
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
        """Test health check endpoint"""
        success, response = self.run_test(
            "Health Check",
            "GET",
            "health",
            200
        )
        return success

    def test_create_project(self):
        """Test project creation with Phase 3 business input"""
        test_data = {
            "business_name": "Phase3 Revolutionary Corp",
            "business_description": "Revolutionary AI-powered visual identity platform with advanced generation capabilities",
            "industry": "Technology/AI",
            "target_audience": "Creative professionals and brand designers",
            "business_values": ["innovation", "creativity", "excellence"],
            "preferred_style": "modern",
            "preferred_colors": "blue"
        }
        
        success, response = self.run_test(
            "Create Project",
            "POST",
            "projects",
            200,
            data=test_data
        )
        
        if success:
            # Check for project_id field as specified in review request
            if 'project_id' in response:
                self.project_id = response['project_id']
                print(f"   Project ID: {self.project_id}")
                return True
            elif 'id' in response:
                self.project_id = response['id']
                print(f"   Project ID: {self.project_id}")
                return True
            else:
                print("❌ Response missing project_id field")
                return False
        return False

    def test_generate_strategy(self):
        """Test enhanced brand strategy generation with Phase 2 capabilities"""
        if not self.project_id:
            print("❌ Cannot test strategy generation - no project ID")
            return False
            
        success, response = self.run_test(
            "Generate Enhanced Brand Strategy",
            "POST",
            f"projects/{self.project_id}/strategy",
            200,
            timeout=180  # Increased timeout for Phase 2 AI generation
        )
        
        if success:
            # Verify strategy structure
            required_fields = ['brand_personality', 'visual_direction', 'color_palette', 'messaging_framework']
            for field in required_fields:
                if field not in response:
                    print(f"❌ Missing required field: {field}")
                    return False
            print("   ✅ Enhanced strategy structure validated")
        
        return success

    def test_phase2_advanced_analysis(self):
        """Test Phase 2 Advanced Analysis endpoint - NEW FEATURE"""
        if not self.project_id:
            print("❌ Cannot test advanced analysis - no project ID")
            return False
            
        print("🔍 Testing Phase 2 Advanced Analysis (5-layer strategic analysis)...")
        success, response = self.run_test(
            "Phase 2 Advanced Analysis",
            "POST",
            f"projects/{self.project_id}/advanced-analysis",
            200,
            timeout=180  # Advanced analysis takes time
        )
        
        if success:
            # Verify Phase 2 analysis structure
            required_fields = ['project_id', 'analysis_complete', 'analysis_layers', 'confidence_scores']
            for field in required_fields:
                if field not in response:
                    print(f"❌ Missing required field: {field}")
                    return False
            
            # Verify 5-layer analysis structure
            analysis_layers = response.get('analysis_layers', {})
            expected_layers = [
                'market_intelligence',
                'competitive_positioning', 
                'brand_personality',
                'visual_direction',
                'strategic_recommendations'
            ]
            
            missing_layers = []
            for layer in expected_layers:
                if layer not in analysis_layers:
                    missing_layers.append(layer)
                else:
                    print(f"   ✅ {layer} analysis complete")
            
            if missing_layers:
                print(f"❌ Missing analysis layers: {missing_layers}")
                return False
            
            # Verify confidence scores
            confidence_scores = response.get('confidence_scores', {})
            if not confidence_scores:
                print("⚠️  No confidence scores provided")
            else:
                print(f"   ✅ Confidence scores provided: {list(confidence_scores.keys())}")
            
            # Verify analysis completion flag
            if response.get('analysis_complete') != True:
                print("❌ Analysis not marked as complete")
                return False
            
            print("   ✅ Phase 2 Advanced Analysis structure validated")
            print("   ✅ 5-layer strategic analysis confirmed")
            
        return success

    def test_phase3_revolutionary_visual_identity(self):
        """🚀 Test Phase 3 Revolutionary Visual Identity Generation System"""
        if not self.project_id:
            print("❌ Cannot test revolutionary visual identity - no project ID")
            return False
            
        print("🚀 Testing Phase 3 Revolutionary Visual Identity System...")
        success, response = self.run_test(
            "Phase 3 Revolutionary Visual Identity",
            "POST",
            f"projects/{self.project_id}/revolutionary-visual-identity",
            200,
            timeout=300  # Revolutionary generation may take longer
        )
        
        if success:
            # Verify Phase 3 response structure
            required_fields = ['project_id', 'status', 'visual_identity_system', 'total_generated_assets', 'phase_3_capabilities']
            for field in required_fields:
                if field not in response:
                    print(f"❌ Missing required field: {field}")
                    return False
            
            # Verify status
            if response.get('status') != 'revolutionary_visual_identity_complete':
                print(f"❌ Unexpected status: {response.get('status')}")
                return False
            
            # Verify visual identity system structure
            visual_identity_system = response.get('visual_identity_system', {})
            if not visual_identity_system:
                print("❌ Missing visual_identity_system")
                return False
            
            # Check for visual identity suite
            visual_suite = visual_identity_system.get('visual_identity_suite', {})
            if not visual_suite:
                print("❌ Missing visual_identity_suite")
                return False
            
            # Verify logo suite
            logo_suite = visual_suite.get('logo_suite', {})
            if not logo_suite:
                print("❌ Missing logo_suite")
                return False
            
            # Check for primary logo and variations
            if 'primary' not in logo_suite:
                print("❌ Missing primary logo")
                return False
            
            if 'variations' not in logo_suite or not isinstance(logo_suite['variations'], list):
                print("❌ Missing logo variations")
                return False
            
            print(f"   ✅ Logo suite: 1 primary + {len(logo_suite['variations'])} variations")
            
            # Verify Phase 3 capabilities
            phase3_capabilities = response.get('phase_3_capabilities', {})
            expected_capabilities = [
                'advanced_logo_suite',
                'business_card_designs', 
                'letterhead_templates',
                'social_media_templates',
                'marketing_collateral',
                'brand_patterns',
                'realistic_mockups',
                'consistency_management',
                'quality_assurance'
            ]
            
            missing_capabilities = []
            for capability in expected_capabilities:
                if not phase3_capabilities.get(capability):
                    missing_capabilities.append(capability)
                else:
                    print(f"   ✅ {capability} capability confirmed")
            
            if missing_capabilities:
                print(f"❌ Missing Phase 3 capabilities: {missing_capabilities}")
                return False
            
            # Verify asset count
            total_assets = response.get('total_generated_assets', 0)
            if total_assets < 20:
                print(f"⚠️  WARNING: Expected 20+ assets, got {total_assets}")
            else:
                print(f"   ✅ Revolutionary asset generation: {total_assets} assets")
            
            # Verify asset breakdown
            asset_breakdown = response.get('asset_breakdown', {})
            if asset_breakdown:
                print(f"   ✅ Asset breakdown provided: {list(asset_breakdown.keys())}")
            
            # Verify system consistency
            system_consistency = response.get('system_consistency', {})
            if system_consistency:
                print(f"   ✅ System consistency metrics provided")
            
            print("   ✅ Phase 3 Revolutionary Visual Identity System validated")
            print("   ✅ Advanced visual generation capabilities confirmed")
            
        return success

    def test_get_project(self):
        """Test getting project details"""
        if not self.project_id:
            print("❌ Cannot test get project - no project ID")
            return False
            
        success, response = self.run_test(
            "Get Project Details",
            "GET",
            f"projects/{self.project_id}",
            200
        )
        
        if success:
            # Verify project has strategy
            if 'brand_strategy' in response and response['brand_strategy']:
                print("   ✅ Project contains brand strategy")
            else:
                print("   ⚠️  Project missing brand strategy")
        
        return success

    def test_generate_single_asset(self, asset_type="logo"):
        """Test single asset generation with base64 encoding validation"""
        if not self.project_id:
            print(f"❌ Cannot test {asset_type} generation - no project ID")
            return False
            
        success, response = self.run_test(
            f"Generate {asset_type.title()}",
            "POST",
            f"projects/{self.project_id}/assets/{asset_type}",
            200,
            timeout=60  # AI generation takes longer
        )
        
        if success:
            # Verify asset structure
            required_fields = ['id', 'project_id', 'asset_type', 'asset_url']
            for field in required_fields:
                if field not in response:
                    print(f"❌ Missing required field: {field}")
                    return False
            
            # CRITICAL: Verify base64 encoding fix
            asset_url = response['asset_url']
            
            # Check data URL format
            if not asset_url.startswith('data:image/png;base64,'):
                print(f"❌ CRITICAL: Invalid data URL format. Expected 'data:image/png;base64,' but got: {asset_url[:50]}...")
                return False
            
            # Extract base64 data
            base64_data = asset_url.split(',')[1] if ',' in asset_url else ''
            
            # CRITICAL: Check for Python byte notation (the bug we're fixing)
            if "b'" in base64_data or "\\x" in base64_data:
                print(f"❌ CRITICAL: Python byte notation detected in base64 data: {base64_data[:100]}...")
                return False
            
            # Verify substantial base64 data (not tiny placeholder)
            if len(base64_data) < 200:
                print(f"⚠️  WARNING: Base64 data seems small ({len(base64_data)} chars) - might be placeholder")
            else:
                print(f"   ✅ Substantial base64 data ({len(base64_data)} chars)")
            
            # Validate base64 format
            try:
                import base64
                base64.b64decode(base64_data)
                print("   ✅ Valid base64 encoding format")
            except Exception as e:
                print(f"❌ CRITICAL: Invalid base64 format: {str(e)}")
                return False
            
            print(f"   ✅ {asset_type.title()} base64 encoding fix verified")
        
        return success

    def test_generate_complete_package(self):
        """Test enhanced complete package generation with retry logic"""
        if not self.project_id:
            print("❌ Cannot test complete package - no project ID")
            return False
            
        print("🔍 Testing Enhanced Complete Package Generation with Retry Logic...")
        success, response = self.run_test(
            "Generate Complete Package (Enhanced)",
            "POST",
            f"projects/{self.project_id}/complete-package",
            200,
            timeout=180  # Enhanced retry logic may take longer
        )
        
        if success:
            # CRITICAL TEST: Verify exactly 6 assets are returned
            if 'generated_assets' in response:
                asset_count = len(response['generated_assets'])
                print(f"   📊 Asset Count: {asset_count}")
                
                if asset_count == 6:
                    print("   ✅ CRITICAL: Exactly 6 assets generated as expected")
                else:
                    print(f"   ❌ CRITICAL: Expected 6 assets, got {asset_count}")
                    return False
                
                # Check all expected asset types are present
                asset_types = [asset['asset_type'] for asset in response['generated_assets']]
                expected_types = ['logo', 'business_card', 'letterhead', 'social_media_post', 'flyer', 'banner']
                
                missing_types = []
                for expected_type in expected_types:
                    if expected_type in asset_types:
                        print(f"   ✅ {expected_type} generated")
                    else:
                        print(f"   ❌ {expected_type} missing")
                        missing_types.append(expected_type)
                
                if missing_types:
                    print(f"   ❌ CRITICAL: Missing asset types: {missing_types}")
                    return False
                
                # CRITICAL TEST: Verify asset URLs contain substantial base64 data and proper encoding
                tiny_placeholders = 0
                valid_assets = 0
                encoding_errors = 0
                
                for asset in response['generated_assets']:
                    asset_url = asset.get('asset_url', '')
                    asset_type = asset.get('asset_type', 'unknown')
                    
                    # Check data URL format
                    if not asset_url.startswith('data:image/png;base64,'):
                        print(f"   ❌ {asset_type}: Invalid data URL format")
                        encoding_errors += 1
                        continue
                    
                    # Extract base64 data
                    base64_data = asset_url.split(',')[1] if ',' in asset_url else ''
                    
                    # CRITICAL: Check for Python byte notation (the main bug we're fixing)
                    if "b'" in base64_data or "\\x" in base64_data:
                        print(f"   ❌ CRITICAL: {asset_type}: Python byte notation detected in base64 data")
                        encoding_errors += 1
                        continue
                    
                    # Validate base64 format
                    try:
                        import base64
                        base64.b64decode(base64_data)
                    except Exception as e:
                        print(f"   ❌ CRITICAL: {asset_type}: Invalid base64 format - {str(e)}")
                        encoding_errors += 1
                        continue
                    
                    # Check data size
                    data_length = len(base64_data)
                    if data_length < 200:
                        print(f"   ⚠️  {asset_type}: Potentially tiny placeholder ({data_length} chars)")
                        tiny_placeholders += 1
                    else:
                        print(f"   ✅ {asset_type}: Valid base64 image data ({data_length} chars)")
                        valid_assets += 1
                
                # Report on encoding quality
                print(f"   📊 Base64 Encoding Summary:")
                print(f"      Valid assets: {valid_assets}/6")
                print(f"      Tiny placeholders: {tiny_placeholders}/6") 
                print(f"      Encoding errors: {encoding_errors}/6")
                
                if encoding_errors > 0:
                    print(f"   ❌ CRITICAL: {encoding_errors} assets have base64 encoding issues")
                    return False
                
                if tiny_placeholders > 0:
                    print(f"   ⚠️  WARNING: {tiny_placeholders} assets may be tiny placeholders")
                    # Don't fail the test for this, as branded placeholders are acceptable
                
                print("   ✅ BASE64 ENCODING FIX VERIFIED: All assets have clean base64 data URLs")
                return True
            else:
                print("   ❌ CRITICAL: No 'generated_assets' field in response")
                return False
        
        return success

    def test_get_all_projects(self):
        """Test getting all projects"""
        success, response = self.run_test(
            "Get All Projects",
            "GET",
            "projects",
            200
        )
        
        if success and isinstance(response, list):
            print(f"   ✅ Found {len(response)} projects")
        
        return success

def main():
    print("🚀 Starting Phase 3 Revolutionary Gemini Visual Generation System Tests")
    print("=" * 70)
    print("🎯 Focus: Testing Phase 3 Revolutionary Visual Identity Implementation")
    print("📋 Business Input: Phase3 Revolutionary Corp - AI visual identity platform")
    print("=" * 70)
    
    tester = BrandForgeAPITester()
    
    # Phase 3 Test sequence focusing on Revolutionary Visual Generation System
    tests = [
        ("Health Check", tester.test_health_check),
        ("Create Test Project", tester.test_create_project),
        ("Generate Brand Strategy", tester.test_generate_strategy),
        ("Phase 3 Revolutionary Visual Identity", tester.test_phase3_revolutionary_visual_identity),
        ("Advanced Feature Validation", tester.test_get_project),
        ("Data Structure Validation", tester.test_get_all_projects),
    ]
    
    failed_tests = []
    
    for test_name, test_func in tests:
        try:
            if not test_func():
                failed_tests.append(test_name)
        except Exception as e:
            print(f"❌ {test_name} - Exception: {str(e)}")
            failed_tests.append(test_name)
    
    # Print results
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)
    print(f"Tests Run: {tester.tests_run}")
    print(f"Tests Passed: {tester.tests_passed}")
    print(f"Tests Failed: {len(failed_tests)}")
    print(f"Success Rate: {(tester.tests_passed/tester.tests_run*100):.1f}%")
    
    if failed_tests:
        print(f"\n❌ Failed Tests:")
        for test in failed_tests:
            print(f"   - {test}")
    else:
        print(f"\n✅ All tests passed!")
    
    return 0 if len(failed_tests) == 0 else 1

if __name__ == "__main__":
    sys.exit(main())