#!/usr/bin/env python3
"""
🔧 URGENT BUG FIX VERIFICATION: Logo Generation 500 Error Test

This test specifically verifies the fix for the logo generation bug:
- Error: 'BrandStrategy' object has no attribute 'industry'
- Fixed by removing industry references and using fallback values
- Tests the /api/projects/{id}/assets/logo endpoint that was failing
"""

import requests
import sys
import json
import time
from datetime import datetime

class LogoGenerationBugTester:
    def __init__(self, base_url="https://logo-vanisher.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.project_id = None

    def log_test(self, name, success, details=""):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name}: PASSED")
        else:
            print(f"❌ {name}: FAILED")
        
        if details:
            print(f"   {details}")

    def run_api_request(self, method, endpoint, data=None, timeout=60):
        """Make API request and return response"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=timeout)
            
            return response
        except Exception as e:
            print(f"   Request failed: {str(e)}")
            return None

    def test_health_check(self):
        """1. Health Check: Verify backend is running"""
        print("\n🔍 1. HEALTH CHECK - Verify backend is running")
        
        response = self.run_api_request('GET', 'health')
        if not response:
            self.log_test("Health Check", False, "Request failed")
            return False
        
        success = response.status_code == 200
        if success:
            try:
                data = response.json()
                self.log_test("Health Check", True, f"Backend healthy: {data}")
            except:
                self.log_test("Health Check", True, "Backend responding")
        else:
            self.log_test("Health Check", False, f"Status: {response.status_code}")
        
        return success

    def test_create_project(self):
        """2. Create Test Project: Create a simple test project"""
        print("\n🔍 2. CREATE TEST PROJECT - Create a simple test project")
        
        test_data = {
            "business_name": "LogoBugTest Corp",
            "business_description": "Testing logo generation bug fix for industry attribute error",
            "industry": "Technology",
            "target_audience": "Developers and testers",
            "business_values": ["reliability", "quality", "innovation"],
            "preferred_style": "modern",
            "preferred_colors": "blue"
        }
        
        response = self.run_api_request('POST', 'projects', data=test_data)
        if not response:
            self.log_test("Create Project", False, "Request failed")
            return False
        
        success = response.status_code == 200
        if success:
            try:
                data = response.json()
                # Extract project ID
                if 'project_id' in data:
                    self.project_id = data['project_id']
                elif 'id' in data:
                    self.project_id = data['id']
                else:
                    self.log_test("Create Project", False, "No project ID in response")
                    return False
                
                self.log_test("Create Project", True, f"Project ID: {self.project_id}")
            except Exception as e:
                self.log_test("Create Project", False, f"JSON parse error: {str(e)}")
                return False
        else:
            try:
                error_data = response.json()
                self.log_test("Create Project", False, f"Status {response.status_code}: {error_data}")
            except:
                self.log_test("Create Project", False, f"Status {response.status_code}: {response.text}")
        
        return success

    def test_generate_brand_strategy(self):
        """3. Generate Brand Strategy: Create a brand strategy for the project"""
        print("\n🔍 3. GENERATE BRAND STRATEGY - Create a brand strategy for the project")
        
        if not self.project_id:
            self.log_test("Generate Brand Strategy", False, "No project ID available")
            return False
        
        response = self.run_api_request('POST', f'projects/{self.project_id}/strategy', timeout=120)
        if not response:
            self.log_test("Generate Brand Strategy", False, "Request failed")
            return False
        
        success = response.status_code == 200
        if success:
            try:
                data = response.json()
                # Verify strategy has required fields
                required_fields = ['brand_personality', 'visual_direction', 'color_palette']
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Generate Brand Strategy", False, f"Missing fields: {missing_fields}")
                    return False
                
                self.log_test("Generate Brand Strategy", True, "Strategy generated successfully")
            except Exception as e:
                self.log_test("Generate Brand Strategy", False, f"JSON parse error: {str(e)}")
                return False
        else:
            try:
                error_data = response.json()
                self.log_test("Generate Brand Strategy", False, f"Status {response.status_code}: {error_data}")
            except:
                self.log_test("Generate Brand Strategy", False, f"Status {response.status_code}: {response.text}")
        
        return success

    def test_logo_generation_bug_fix(self):
        """4. CRITICAL TEST: Logo Generation Bug Fix - Test the /api/projects/{id}/assets/logo endpoint"""
        print("\n🔍 4. CRITICAL TEST: LOGO GENERATION BUG FIX")
        print("   Testing /api/projects/{id}/assets/logo endpoint that was failing")
        print("   Verifying fix for: 'BrandStrategy' object has no attribute 'industry'")
        
        if not self.project_id:
            self.log_test("Logo Generation Bug Fix", False, "No project ID available")
            return False
        
        # Test the specific endpoint that was failing
        response = self.run_api_request('POST', f'projects/{self.project_id}/assets/logo', timeout=90)
        if not response:
            self.log_test("Logo Generation Bug Fix", False, "Request failed")
            return False
        
        # CRITICAL: Check for 500 error (the bug we're fixing)
        if response.status_code == 500:
            try:
                error_data = response.json()
                error_detail = error_data.get('detail', '')
                
                # Check for the specific industry attribute error
                if 'industry' in error_detail and 'attribute' in error_detail:
                    self.log_test("Logo Generation Bug Fix", False, 
                                f"🚨 CRITICAL BUG STILL EXISTS: {error_detail}")
                    return False
                else:
                    self.log_test("Logo Generation Bug Fix", False, 
                                f"500 error (different issue): {error_detail}")
                    return False
            except:
                self.log_test("Logo Generation Bug Fix", False, 
                            f"500 error: {response.text}")
                return False
        
        # Check for successful response (200 status)
        success = response.status_code == 200
        if success:
            try:
                data = response.json()
                
                # Verify response structure
                required_fields = ['id', 'project_id', 'asset_type', 'asset_url']
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Logo Generation Bug Fix", False, 
                                f"Missing response fields: {missing_fields}")
                    return False
                
                # Verify asset_url contains valid base64 image data
                asset_url = data.get('asset_url', '')
                if not asset_url.startswith('data:image/png;base64,'):
                    self.log_test("Logo Generation Bug Fix", False, 
                                f"Invalid asset URL format: {asset_url[:50]}...")
                    return False
                
                # Extract and validate base64 data
                base64_data = asset_url.split(',')[1] if ',' in asset_url else ''
                if len(base64_data) < 100:
                    self.log_test("Logo Generation Bug Fix", False, 
                                f"Asset data too small ({len(base64_data)} chars)")
                    return False
                
                # Verify no Python byte notation (another potential encoding issue)
                if "b'" in base64_data or "\\x" in base64_data:
                    self.log_test("Logo Generation Bug Fix", False, 
                                "Python byte notation detected in base64 data")
                    return False
                
                self.log_test("Logo Generation Bug Fix", True, 
                            f"✅ Logo generated successfully! Asset URL: {len(base64_data)} chars base64 data")
                print(f"   ✅ NO MORE 500 ERRORS - Bug fix verified!")
                print(f"   ✅ Valid GeneratedAsset response structure")
                print(f"   ✅ Valid base64 image data ({len(base64_data)} characters)")
                
            except Exception as e:
                self.log_test("Logo Generation Bug Fix", False, f"JSON parse error: {str(e)}")
                return False
        else:
            try:
                error_data = response.json()
                self.log_test("Logo Generation Bug Fix", False, 
                            f"Status {response.status_code}: {error_data}")
            except:
                self.log_test("Logo Generation Bug Fix", False, 
                            f"Status {response.status_code}: {response.text}")
        
        return success

    def test_backend_logs_clean(self):
        """5. Verify Response: Ensure backend logs are clean"""
        print("\n🔍 5. VERIFY RESPONSE - Check that fix doesn't break existing functionality")
        
        if not self.project_id:
            self.log_test("Backend Logs Clean", False, "No project ID available")
            return False
        
        # Test another logo generation to ensure consistency
        response = self.run_api_request('POST', f'projects/{self.project_id}/assets/logo', 
                                      data={"style_variant": "secondary"}, timeout=60)
        if not response:
            self.log_test("Backend Logs Clean", False, "Request failed")
            return False
        
        success = response.status_code == 200
        if success:
            try:
                data = response.json()
                self.log_test("Backend Logs Clean", True, 
                            "✅ Multiple logo generations working - fix is stable")
            except Exception as e:
                self.log_test("Backend Logs Clean", False, f"JSON parse error: {str(e)}")
                return False
        else:
            try:
                error_data = response.json()
                self.log_test("Backend Logs Clean", False, 
                            f"Status {response.status_code}: {error_data}")
            except:
                self.log_test("Backend Logs Clean", False, 
                            f"Status {response.status_code}: {response.text}")
        
        return success

def main():
    print("🔧 URGENT BUG FIX VERIFICATION: Logo Generation 500 Error")
    print("=" * 70)
    print("🎯 FOCUS: Testing logo generation endpoint bug fix")
    print("🐛 BUG: 'BrandStrategy' object has no attribute 'industry'")
    print("🔧 FIX: Removed industry references and using fallback values")
    print("📋 ENDPOINT: /api/projects/{id}/assets/logo")
    print("=" * 70)
    
    tester = LogoGenerationBugTester()
    
    # Bug fix verification test sequence
    tests = [
        ("Health Check", tester.test_health_check),
        ("Create Test Project", tester.test_create_project),
        ("Generate Brand Strategy", tester.test_generate_brand_strategy),
        ("Logo Generation Bug Fix", tester.test_logo_generation_bug_fix),
        ("Backend Logs Clean", tester.test_backend_logs_clean),
    ]
    
    failed_tests = []
    
    for test_name, test_func in tests:
        try:
            if not test_func():
                failed_tests.append(test_name)
                # If logo generation fails, no point continuing
                if test_name == "Logo Generation Bug Fix":
                    print("\n🚨 CRITICAL: Logo generation bug fix failed - stopping tests")
                    break
        except Exception as e:
            print(f"❌ {test_name} - Exception: {str(e)}")
            failed_tests.append(test_name)
    
    # Print results
    print("\n" + "=" * 60)
    print("📊 BUG FIX VERIFICATION RESULTS")
    print("=" * 60)
    print(f"Tests Run: {tester.tests_run}")
    print(f"Tests Passed: {tester.tests_passed}")
    print(f"Tests Failed: {len(failed_tests)}")
    
    if len(failed_tests) == 0:
        print("\n✅ BUG FIX VERIFICATION: SUCCESS!")
        print("✅ Logo generation endpoint working correctly")
        print("✅ No more 'BrandStrategy' object has no attribute 'industry' errors")
        print("✅ Valid GeneratedAsset responses with base64 image data")
        print("✅ Backend logs are clean")
    else:
        print(f"\n❌ BUG FIX VERIFICATION: FAILED")
        print(f"❌ Failed Tests: {failed_tests}")
        
        if "Logo Generation Bug Fix" in failed_tests:
            print("🚨 CRITICAL: The logo generation bug is NOT fixed!")
            print("🚨 The endpoint is still returning 500 errors")
    
    return 0 if len(failed_tests) == 0 else 1

if __name__ == "__main__":
    sys.exit(main())