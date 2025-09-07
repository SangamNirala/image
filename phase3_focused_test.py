#!/usr/bin/env python3
"""
Phase 3 Revolutionary Visual Generation System - Focused Testing
Tests the core Phase 3 functionality with proper timeouts and error handling
"""

import requests
import json
import time
import sys

class Phase3Tester:
    def __init__(self):
        self.base_url = "https://asset-harmony.preview.emergentagent.com/api"
        self.project_id = None
        self.test_results = []
        
    def log_test(self, name, success, details=""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {name}")
        if details:
            print(f"    {details}")
        self.test_results.append({"name": name, "success": success, "details": details})
        
    def test_health_check(self):
        """Test backend health"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            if success:
                data = response.json()
                details += f", Service: {data.get('service', 'Unknown')}"
            self.log_test("Health Check", success, details)
            return success
        except Exception as e:
            self.log_test("Health Check", False, f"Error: {str(e)}")
            return False
    
    def test_create_project(self):
        """Create test project for Phase 3"""
        try:
            project_data = {
                "business_name": "Phase3 Revolutionary Corp",
                "business_description": "Revolutionary AI-powered visual identity platform",
                "industry": "Technology/AI", 
                "target_audience": "Creative professionals and brand designers",
                "business_values": ["innovation", "creativity", "excellence"],
                "preferred_style": "modern",
                "preferred_colors": "blue"
            }
            
            response = requests.post(f"{self.base_url}/projects", json=project_data, timeout=30)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                self.project_id = data.get('project_id')
                details = f"Project ID: {self.project_id}"
            else:
                details = f"Status: {response.status_code}, Error: {response.text[:100]}"
                
            self.log_test("Create Project", success, details)
            return success
            
        except Exception as e:
            self.log_test("Create Project", False, f"Error: {str(e)}")
            return False
    
    def test_generate_strategy(self):
        """Generate brand strategy (required for Phase 3)"""
        if not self.project_id:
            self.log_test("Generate Strategy", False, "No project ID available")
            return False
            
        try:
            print("    Generating brand strategy (this may take up to 3 minutes)...")
            response = requests.post(
                f"{self.base_url}/projects/{self.project_id}/strategy",
                timeout=180  # 3 minute timeout
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                business_name = data.get('business_name', 'Unknown')
                details = f"Strategy generated for: {business_name}"
            else:
                details = f"Status: {response.status_code}, Error: {response.text[:100]}"
                
            self.log_test("Generate Strategy", success, details)
            return success
            
        except requests.exceptions.Timeout:
            self.log_test("Generate Strategy", False, "Request timed out after 3 minutes")
            return False
        except Exception as e:
            self.log_test("Generate Strategy", False, f"Error: {str(e)}")
            return False
    
    def test_phase3_revolutionary_visual_identity(self):
        """🚀 Test Phase 3 Revolutionary Visual Identity System"""
        if not self.project_id:
            self.log_test("Phase 3 Revolutionary Visual Identity", False, "No project ID available")
            return False
            
        try:
            print("    🚀 Testing Phase 3 Revolutionary Visual Identity System...")
            print("    This may take up to 5 minutes for complete visual identity generation...")
            
            response = requests.post(
                f"{self.base_url}/projects/{self.project_id}/revolutionary-visual-identity",
                timeout=300  # 5 minute timeout for comprehensive generation
            )
            
            success = response.status_code == 200
            
            if success:
                data = response.json()
                
                # Validate Phase 3 response structure
                required_fields = ['project_id', 'status', 'visual_identity_system', 'total_generated_assets', 'phase_3_capabilities']
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    details = f"Missing required fields: {missing_fields}"
                    success = False
                else:
                    # Extract key metrics
                    total_assets = data.get('total_generated_assets', 0)
                    status = data.get('status', 'unknown')
                    capabilities = data.get('phase_3_capabilities', {})
                    
                    # Validate Phase 3 capabilities
                    expected_capabilities = [
                        'advanced_logo_suite', 'business_card_designs', 'letterhead_templates',
                        'social_media_templates', 'marketing_collateral', 'brand_patterns',
                        'realistic_mockups', 'consistency_management', 'quality_assurance'
                    ]
                    
                    missing_capabilities = [cap for cap in expected_capabilities if not capabilities.get(cap)]
                    
                    if missing_capabilities:
                        details = f"Missing Phase 3 capabilities: {missing_capabilities}"
                        success = False
                    else:
                        details = f"Status: {status}, Assets: {total_assets}, All Phase 3 capabilities confirmed"
                        
                        # Additional validation
                        if total_assets < 20:
                            details += f" (WARNING: Expected 20+ assets, got {total_assets})"
                        
                        # Check visual identity system structure
                        visual_system = data.get('visual_identity_system', {})
                        if 'visual_identity_suite' in visual_system:
                            suite = visual_system['visual_identity_suite']
                            if 'logo_suite' in suite:
                                logo_suite = suite['logo_suite']
                                if 'primary' in logo_suite and 'variations' in logo_suite:
                                    logo_count = 1 + len(logo_suite['variations'])
                                    details += f", Logo suite: {logo_count} assets"
                                    
                        print(f"    ✅ Phase 3 Revolutionary Visual Identity System validated")
                        print(f"    📊 Total Assets Generated: {total_assets}")
                        print(f"    🎯 Status: {status}")
                        print(f"    🚀 All Phase 3 capabilities confirmed")
            else:
                details = f"Status: {response.status_code}, Error: {response.text[:200]}"
                
            self.log_test("Phase 3 Revolutionary Visual Identity", success, details)
            return success
            
        except requests.exceptions.Timeout:
            self.log_test("Phase 3 Revolutionary Visual Identity", False, "Request timed out after 5 minutes")
            return False
        except Exception as e:
            self.log_test("Phase 3 Revolutionary Visual Identity", False, f"Error: {str(e)}")
            return False
    
    def test_validate_project_data(self):
        """Validate project data after Phase 3 generation"""
        if not self.project_id:
            self.log_test("Validate Project Data", False, "No project ID available")
            return False
            
        try:
            response = requests.get(f"{self.base_url}/projects/{self.project_id}", timeout=30)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                has_strategy = 'brand_strategy' in data and data['brand_strategy']
                phase3_complete = data.get('phase_3_complete', False)
                revolutionary_generated = data.get('revolutionary_identity_generated', False)
                
                details = f"Strategy: {'✓' if has_strategy else '✗'}, Phase 3: {'✓' if phase3_complete else '✗'}, Revolutionary: {'✓' if revolutionary_generated else '✗'}"
                
                if not (has_strategy and phase3_complete and revolutionary_generated):
                    success = False
                    details += " - Missing expected Phase 3 completion markers"
            else:
                details = f"Status: {response.status_code}, Error: {response.text[:100]}"
                
            self.log_test("Validate Project Data", success, details)
            return success
            
        except Exception as e:
            self.log_test("Validate Project Data", False, f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run complete Phase 3 test suite"""
        print("🚀 PHASE 3 REVOLUTIONARY GEMINI VISUAL GENERATION SYSTEM TESTING")
        print("=" * 70)
        print("🎯 Focus: Testing Phase 3 Revolutionary Visual Identity Implementation")
        print("📋 Business: Phase3 Revolutionary Corp - AI visual identity platform")
        print("=" * 70)
        
        # Test sequence
        tests = [
            ("Health Check", self.test_health_check),
            ("Create Test Project", self.test_create_project),
            ("Generate Brand Strategy", self.test_generate_strategy),
            ("Phase 3 Revolutionary Visual Identity", self.test_phase3_revolutionary_visual_identity),
            ("Validate Project Data", self.test_validate_project_data),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n🔍 Running: {test_name}")
            if test_func():
                passed += 1
            else:
                # If a critical test fails, we might want to continue for diagnostic purposes
                if test_name in ["Create Test Project", "Generate Brand Strategy"]:
                    print(f"⚠️  Critical test failed: {test_name} - continuing for diagnostics")
        
        # Results summary
        print("\n" + "=" * 70)
        print("📊 PHASE 3 TEST RESULTS")
        print("=" * 70)
        print(f"Tests Passed: {passed}/{total}")
        print(f"Success Rate: {(passed/total*100):.1f}%")
        
        if passed == total:
            print("🎉 ALL PHASE 3 TESTS PASSED - Revolutionary Visual Generation System is operational!")
        else:
            print("⚠️  Some tests failed - see details above")
            
        return passed == total

def main():
    tester = Phase3Tester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())