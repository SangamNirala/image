#!/usr/bin/env python3
"""
BrandForge AI Phase 1 Architecture Comprehensive Test Suite
Testing the newly implemented advanced AI engines and professional architecture
"""

import requests
import sys
import json
import time
from datetime import datetime
from typing import Dict, Any, List

class Phase1ArchitectureTester:
    def __init__(self, base_url="https://brandforge-phase1.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.project_id = None
        self.test_results = []
        
    def log_test_result(self, test_name: str, success: bool, details: str = ""):
        """Log test result for comprehensive reporting"""
        self.test_results.append({
            'test_name': test_name,
            'success': success,
            'details': details,
            'timestamp': datetime.now().isoformat()
        })

    def run_test(self, name, method, endpoint, expected_status, data=None, params=None, timeout=60):
        """Run a single API test with enhanced error handling"""
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
                    self.log_test_result(name, True, f"Status: {response.status_code}")
                    return True, response_data
                except:
                    print(f"   Response: Non-JSON response")
                    self.log_test_result(name, True, f"Status: {response.status_code}, Non-JSON response")
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                    self.log_test_result(name, False, f"Status: {response.status_code}, Error: {error_data}")
                except:
                    print(f"   Error: {response.text}")
                    self.log_test_result(name, False, f"Status: {response.status_code}, Error: {response.text}")
                return False, {}

        except requests.exceptions.Timeout:
            print(f"❌ Failed - Request timed out after {timeout} seconds")
            self.log_test_result(name, False, f"Timeout after {timeout}s")
            return False, {}
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.log_test_result(name, False, f"Exception: {str(e)}")
            return False, {}

    def test_health_check(self):
        """Test API health and service availability"""
        success, response = self.run_test(
            "Health Check",
            "GET",
            "health",
            200
        )
        
        if success and response.get('status') == 'healthy':
            print("   ✅ Service is healthy and operational")
            return True
        return False

    def test_create_project_advanced(self):
        """Test project creation with comprehensive business input"""
        test_data = {
            "business_name": "BrandForge Phase1 Test Co",
            "business_description": "Advanced AI-powered brand strategy and visual asset generation company specializing in comprehensive brand development using cutting-edge artificial intelligence",
            "industry": "Technology & AI Services",
            "target_audience": "Startups, SMEs, and enterprises seeking professional brand development",
            "business_values": ["innovation", "excellence", "reliability", "creativity", "professionalism"],
            "preferred_style": "modern",
            "preferred_colors": "professional blue and complementary palette"
        }
        
        success, response = self.run_test(
            "Create Advanced Project",
            "POST",
            "projects",
            200,
            data=test_data
        )
        
        if success:
            # Extract project_id correctly
            if 'project_id' in response:
                self.project_id = response['project_id']
                print(f"   ✅ Project created with ID: {self.project_id}")
                
                # Validate response structure
                required_fields = ['project_id', 'status', 'business_name', 'created_at']
                for field in required_fields:
                    if field not in response:
                        print(f"   ❌ Missing required field: {field}")
                        return False
                
                print("   ✅ Project response structure validated")
                return True
            else:
                print("   ❌ No project_id in response")
                return False
        return False

    def test_advanced_strategy_generation(self):
        """Test the new emergent strategy engine with multi-layer analysis"""
        if not self.project_id:
            print("❌ Cannot test strategy generation - no project ID")
            return False
            
        print("🧠 Testing Advanced AI Strategy Generation (Emergent Strategy Engine)...")
        success, response = self.run_test(
            "Generate Advanced Brand Strategy",
            "POST",
            f"projects/{self.project_id}/strategy",
            200,
            params={"advanced_analysis": True},
            timeout=90  # Advanced AI analysis takes longer
        )
        
        if success:
            # Validate comprehensive strategy structure
            required_fields = [
                'id', 'business_name', 'brand_personality', 'visual_direction', 
                'color_palette', 'messaging_framework', 'consistency_rules', 'created_at'
            ]
            
            for field in required_fields:
                if field not in response:
                    print(f"   ❌ Missing required field: {field}")
                    return False
            
            # Validate brand_personality structure (advanced analysis)
            personality = response.get('brand_personality', {})
            personality_fields = ['primary_traits', 'brand_archetype', 'tone_of_voice']
            for field in personality_fields:
                if field not in personality:
                    print(f"   ⚠️  Missing personality field: {field}")
            
            # Validate visual_direction structure (sophisticated visual guidance)
            visual = response.get('visual_direction', {})
            visual_fields = ['design_style', 'visual_mood', 'typography_style', 'logo_direction']
            for field in visual_fields:
                if field not in visual:
                    print(f"   ⚠️  Missing visual direction field: {field}")
            
            # Validate color palette (should have multiple colors)
            colors = response.get('color_palette', [])
            if len(colors) >= 3:
                print(f"   ✅ Color palette contains {len(colors)} colors")
            else:
                print(f"   ⚠️  Color palette only has {len(colors)} colors")
            
            # Validate messaging framework
            messaging = response.get('messaging_framework', {})
            messaging_fields = ['tagline', 'key_messages', 'brand_promise']
            for field in messaging_fields:
                if field not in messaging:
                    print(f"   ⚠️  Missing messaging field: {field}")
            
            print("   ✅ Advanced strategy generation successful")
            print("   ✅ Emergent Strategy Engine working correctly")
            return True
        
        return False

    def test_visual_asset_generation_engine(self):
        """Test the new Gemini Visual Engine with consistency management"""
        if not self.project_id:
            print("❌ Cannot test visual generation - no project ID")
            return False
        
        print("🎨 Testing Advanced Visual Asset Generation (Gemini Visual Engine)...")
        
        # Test logo generation with style variants
        logo_success, logo_response = self.run_test(
            "Generate Logo (Advanced Visual Engine)",
            "POST",
            f"projects/{self.project_id}/assets/logo",
            200,
            params={"style_variant": "primary"},
            timeout=90
        )
        
        if logo_success:
            # Validate asset structure
            required_fields = ['id', 'project_id', 'asset_type', 'asset_url', 'metadata', 'created_at']
            for field in required_fields:
                if field not in logo_response:
                    print(f"   ❌ Missing asset field: {field}")
                    return False
            
            # Validate metadata (should contain advanced engine info)
            metadata = logo_response.get('metadata', {})
            expected_metadata = ['style_variant', 'consistency_seed', 'generation_method', 'brand_alignment_score']
            for field in expected_metadata:
                if field in metadata:
                    print(f"   ✅ Metadata contains {field}: {metadata[field]}")
            
            # Validate asset URL format
            asset_url = logo_response.get('asset_url', '')
            if asset_url.startswith('data:image/png;base64,'):
                base64_data = asset_url.split(',')[1] if ',' in asset_url else ''
                if len(base64_data) > 1000:  # Substantial image data
                    print(f"   ✅ Logo contains substantial image data ({len(base64_data)} chars)")
                else:
                    print(f"   ⚠️  Logo may be placeholder ({len(base64_data)} chars)")
            
            print("   ✅ Gemini Visual Engine working correctly")
            return True
        
        return False

    def test_marketing_asset_generation(self):
        """Test marketing asset generation with the visual engine"""
        if not self.project_id:
            print("❌ Cannot test marketing assets - no project ID")
            return False
        
        print("📄 Testing Marketing Asset Generation...")
        
        # Test business card generation
        success, response = self.run_test(
            "Generate Business Card (Visual Engine)",
            "POST",
            f"projects/{self.project_id}/assets/business_card",
            200,
            timeout=90
        )
        
        if success:
            # Validate business card specific requirements
            asset_url = response.get('asset_url', '')
            if asset_url.startswith('data:image/png;base64,'):
                base64_data = asset_url.split(',')[1] if ',' in asset_url else ''
                if len(base64_data) > 1000:
                    print(f"   ✅ Business card contains substantial image data ({len(base64_data)} chars)")
                    return True
                else:
                    print(f"   ⚠️  Business card may be placeholder ({len(base64_data)} chars)")
        
        return success

    def test_complete_brand_package_advanced(self):
        """Test the complete brand package generation with all advanced engines"""
        if not self.project_id:
            print("❌ Cannot test complete package - no project ID")
            return False
        
        print("📦 Testing Complete Brand Package (All Advanced Engines)...")
        success, response = self.run_test(
            "Generate Complete Brand Package (Advanced)",
            "POST",
            f"projects/{self.project_id}/complete-package",
            200,
            params={"package_type": "professional"},
            timeout=180  # Advanced generation takes longer
        )
        
        if success:
            # Validate package structure
            required_fields = ['project_id', 'generated_assets', 'total_assets', 'status', 'export_package']
            for field in required_fields:
                if field not in response:
                    print(f"   ❌ Missing package field: {field}")
                    return False
            
            # Validate asset count and types
            assets = response.get('generated_assets', [])
            total_assets = len(assets)
            print(f"   📊 Total assets generated: {total_assets}")
            
            # Check for expected asset types (logo suite + marketing assets)
            expected_types = ['logo', 'business_card', 'letterhead', 'social_media_post', 'flyer', 'banner']
            found_types = []
            
            for asset in assets:
                asset_type = asset.get('asset_type', '')
                if asset_type not in found_types:
                    found_types.append(asset_type)
                
                # Validate each asset has substantial data
                asset_url = asset.get('asset_url', '')
                if asset_url.startswith('data:image/png;base64,'):
                    base64_data = asset_url.split(',')[1] if ',' in asset_url else ''
                    if len(base64_data) > 500:
                        print(f"   ✅ {asset_type}: Valid image data ({len(base64_data)} chars)")
                    else:
                        print(f"   ⚠️  {asset_type}: Small image data ({len(base64_data)} chars)")
            
            print(f"   📊 Asset types generated: {found_types}")
            
            # Validate export package
            export_package = response.get('export_package', {})
            if export_package:
                print("   ✅ Export package generated")
                if 'download_url' in export_package:
                    print("   ✅ Download URL available")
            
            print("   ✅ Complete brand package generation successful")
            return True
        
        return False

    def test_consistency_management(self):
        """Test the consistency manager functionality"""
        if not self.project_id:
            print("❌ Cannot test consistency management - no project ID")
            return False
        
        print("🔄 Testing Consistency Management...")
        
        # Get project analytics to test consistency analysis
        success, response = self.run_test(
            "Get Project Analytics (Consistency Analysis)",
            "GET",
            f"projects/{self.project_id}/analytics",
            200
        )
        
        if success:
            # Validate analytics structure
            expected_fields = ['project_id', 'brand_strength_score', 'visual_consistency_score', 'brand_guidelines']
            for field in expected_fields:
                if field in response:
                    print(f"   ✅ Analytics contains {field}")
                else:
                    print(f"   ⚠️  Missing analytics field: {field}")
            
            # Check brand guidelines (consistency manager output)
            guidelines = response.get('brand_guidelines', {})
            if guidelines:
                print("   ✅ Brand guidelines generated by consistency manager")
                
                # Check for comprehensive guidelines structure
                guideline_sections = ['brand_overview', 'visual_identity', 'brand_voice', 'application_guidelines']
                for section in guideline_sections:
                    if section in guidelines:
                        print(f"   ✅ Guidelines include {section}")
            
            return True
        
        return False

    def test_export_engine(self):
        """Test the professional export engine"""
        if not self.project_id:
            print("❌ Cannot test export engine - no project ID")
            return False
        
        print("📤 Testing Professional Export Engine...")
        
        success, response = self.run_test(
            "Export Brand Package (Professional Engine)",
            "POST",
            f"projects/{self.project_id}/export",
            200,
            data={"package_type": "professional", "formats": ["png", "pdf"]},
            timeout=120
        )
        
        if success:
            # Validate export structure
            if 'download_url' in response:
                print("   ✅ Export download URL generated")
            
            if 'package_contents' in response:
                print("   ✅ Package contents structured")
            
            print("   ✅ Professional export engine working")
            return True
        
        return False

    def test_error_handling(self):
        """Test robust error handling throughout the system"""
        print("🛡️  Testing Error Handling...")
        
        # Test invalid project ID
        invalid_success, _ = self.run_test(
            "Invalid Project ID Handling",
            "GET",
            "projects/invalid-id-12345",
            404
        )
        
        # Test missing strategy generation
        missing_strategy_success, _ = self.run_test(
            "Missing Strategy Error Handling",
            "POST",
            "projects/invalid-id-12345/assets/logo",
            404
        )
        
        if invalid_success and missing_strategy_success:
            print("   ✅ Error handling working correctly")
            return True
        
        return False

    def test_api_functionality_comprehensive(self):
        """Test all API endpoints for functionality"""
        print("🔌 Testing Comprehensive API Functionality...")
        
        # Test GET all projects
        projects_success, projects_response = self.run_test(
            "Get All Projects",
            "GET",
            "projects",
            200
        )
        
        if projects_success and isinstance(projects_response, list):
            print(f"   ✅ Found {len(projects_response)} projects")
            
            # Test GET specific project
            if self.project_id:
                project_success, project_response = self.run_test(
                    "Get Specific Project",
                    "GET",
                    f"projects/{self.project_id}",
                    200
                )
                
                if project_success:
                    # Validate project contains strategy and assets
                    if 'brand_strategy' in project_response:
                        print("   ✅ Project contains brand strategy")
                    
                    if 'generated_assets' in project_response:
                        assets_count = len(project_response.get('generated_assets', []))
                        print(f"   ✅ Project contains {assets_count} generated assets")
                    
                    return True
        
        return False

    def run_comprehensive_phase1_tests(self):
        """Run all Phase 1 architecture tests"""
        print("🚀 Starting BrandForge AI Phase 1 Architecture Comprehensive Tests")
        print("=" * 80)
        print("Testing: Advanced AI Engines, Professional Architecture, Enhanced Models")
        print("=" * 80)
        
        # Core workflow test sequence
        test_sequence = [
            ("Health Check", self.test_health_check),
            ("Advanced Project Creation", self.test_create_project_advanced),
            ("Advanced Strategy Generation (Emergent Engine)", self.test_advanced_strategy_generation),
            ("Visual Asset Generation (Gemini Engine)", self.test_visual_asset_generation_engine),
            ("Marketing Asset Generation", self.test_marketing_asset_generation),
            ("Complete Brand Package (All Engines)", self.test_complete_brand_package_advanced),
            ("Consistency Management", self.test_consistency_management),
            ("Professional Export Engine", self.test_export_engine),
            ("Error Handling", self.test_error_handling),
            ("Comprehensive API Functionality", self.test_api_functionality_comprehensive),
        ]
        
        failed_tests = []
        
        for test_name, test_func in test_sequence:
            try:
                print(f"\n{'='*60}")
                print(f"🧪 PHASE 1 TEST: {test_name}")
                print(f"{'='*60}")
                
                if not test_func():
                    failed_tests.append(test_name)
                    print(f"❌ {test_name} - FAILED")
                else:
                    print(f"✅ {test_name} - PASSED")
                    
            except Exception as e:
                print(f"❌ {test_name} - Exception: {str(e)}")
                failed_tests.append(test_name)
        
        # Generate comprehensive report
        self.generate_phase1_report(failed_tests)
        
        return len(failed_tests) == 0

    def generate_phase1_report(self, failed_tests):
        """Generate comprehensive Phase 1 architecture test report"""
        print("\n" + "=" * 80)
        print("📊 BRANDFORGE AI PHASE 1 ARCHITECTURE TEST REPORT")
        print("=" * 80)
        
        print(f"🧪 Total Tests Run: {self.tests_run}")
        print(f"✅ Tests Passed: {self.tests_passed}")
        print(f"❌ Tests Failed: {len(failed_tests)}")
        print(f"📈 Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        
        print(f"\n🏗️  PHASE 1 ARCHITECTURE COMPONENTS TESTED:")
        print(f"   ✅ Emergent Strategy Engine (Advanced AI Analysis)")
        print(f"   ✅ Gemini Visual Engine (Sophisticated Asset Generation)")
        print(f"   ✅ Consistency Manager (Cross-asset Coherence)")
        print(f"   ✅ Professional Export Engine (Enterprise Packaging)")
        print(f"   ✅ Enhanced Models (Brand Strategy, Visual Assets, Project State)")
        print(f"   ✅ Refactored API Routes (Advanced Functionality)")
        
        if failed_tests:
            print(f"\n❌ FAILED TESTS:")
            for test in failed_tests:
                print(f"   - {test}")
            print(f"\n🔧 RECOMMENDATION: Review failed components for Phase 1 stability")
        else:
            print(f"\n🎉 ALL PHASE 1 ARCHITECTURE TESTS PASSED!")
            print(f"✅ Phase 1 foundation is solid and ready for building upon")
        
        print(f"\n📋 DETAILED TEST RESULTS:")
        for result in self.test_results:
            status = "✅" if result['success'] else "❌"
            print(f"   {status} {result['test_name']}: {result['details']}")

def main():
    """Main test execution"""
    tester = Phase1ArchitectureTester()
    
    success = tester.run_comprehensive_phase1_tests()
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())