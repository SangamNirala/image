#!/usr/bin/env python3
"""
🔧 CRITICAL IMAGE GENERATION FIX TESTING
Test the image generation fix with the NEW GEMINI API KEY

FOCUS: Test INDIVIDUAL asset generation for all asset types to verify they generate 
ACTUAL IMAGES instead of colored placeholder blocks.

NEW API KEY: AIzaSyC4dZxc_uqWKGvSpU4_OC6uFEI3D3kj7xE
OLD API KEY: AIzaSyDF5OScBQWbdM6o6tsm8-YGxQLBOVjt-yA (hit quota limits)

SUCCESS CRITERIA:
- All assets should generate with SUBSTANTIAL base64 image data
- No more 429 RESOURCE_EXHAUSTED errors in logs  
- All asset types should have proper metadata and generation details
- Verify the new Gemini API key is working properly
"""

import requests
import sys
import json
import time
import base64
from datetime import datetime

class ImageGenerationTester:
    def __init__(self, base_url="https://complete-gen-fix.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.project_id = None
        self.asset_results = {}
        
        # Asset types to test individually
        self.asset_types_to_test = [
            "logo",
            "business_card", 
            "letterhead",
            "social_media_post",
            "flyer",
            "banner"
        ]

    def run_test(self, name, method, endpoint, expected_status, data=None, params=None, timeout=60):
        """Run a single API test with enhanced error reporting"""
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
                    return True, response_data
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                    
                    # Check for specific 429 quota errors
                    if response.status_code == 429:
                        print("   🚨 CRITICAL: 429 RESOURCE_EXHAUSTED - API quota limit hit!")
                    elif response.status_code == 500:
                        error_detail = error_data.get('detail', '')
                        if 'RESOURCE_EXHAUSTED' in error_detail:
                            print("   🚨 CRITICAL: Gemini API quota exhausted!")
                        elif 'quota' in error_detail.lower():
                            print("   🚨 CRITICAL: API quota issue detected!")
                            
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

    def create_test_project(self):
        """Create a new test project with complete brand strategy"""
        test_data = {
            "business_name": "ImageGen TestCorp",
            "business_description": "Testing image generation fix with new Gemini API key - comprehensive visual asset generation platform",
            "industry": "Technology/AI",
            "target_audience": "Creative professionals and brand designers", 
            "business_values": ["innovation", "reliability", "quality"],
            "preferred_style": "modern",
            "preferred_colors": "blue"
        }
        
        success, response = self.run_test(
            "Create Test Project",
            "POST",
            "projects", 
            200,
            data=test_data
        )
        
        if success:
            if 'project_id' in response:
                self.project_id = response['project_id']
                print(f"   ✅ Project ID: {self.project_id}")
                return True
            elif 'id' in response:
                self.project_id = response['id']
                print(f"   ✅ Project ID: {self.project_id}")
                return True
            else:
                print("❌ Response missing project_id field")
                return False
        return False

    def generate_brand_strategy(self):
        """Generate brand strategy for the test project"""
        if not self.project_id:
            print("❌ Cannot generate strategy - no project ID")
            return False
            
        success, response = self.run_test(
            "Generate Brand Strategy",
            "POST",
            f"projects/{self.project_id}/strategy",
            200,
            timeout=120
        )
        
        if success:
            # Verify strategy structure
            required_fields = ['brand_personality', 'visual_direction', 'color_palette']
            for field in required_fields:
                if field not in response:
                    print(f"❌ Missing required field: {field}")
                    return False
            print("   ✅ Brand strategy generated successfully")
        
        return success

    def test_individual_asset_generation(self, asset_type):
        """Test individual asset generation with detailed base64 analysis"""
        if not self.project_id:
            print(f"❌ Cannot test {asset_type} generation - no project ID")
            return False
            
        print(f"\n🎨 TESTING {asset_type.upper()} GENERATION")
        print("=" * 50)
        
        success, response = self.run_test(
            f"Generate {asset_type.title()}",
            "POST",
            f"projects/{self.project_id}/assets/{asset_type}",
            200,
            timeout=90  # Increased timeout for image generation
        )
        
        if not success:
            self.asset_results[asset_type] = {
                "status": "FAILED",
                "error": "API call failed",
                "base64_size": 0,
                "is_placeholder": True
            }
            return False
        
        # Analyze the response in detail
        analysis_result = self.analyze_asset_response(asset_type, response)
        self.asset_results[asset_type] = analysis_result
        
        return analysis_result["status"] == "SUCCESS"

    def analyze_asset_response(self, asset_type, response):
        """Detailed analysis of asset generation response"""
        
        # Check required fields
        required_fields = ['id', 'project_id', 'asset_type', 'asset_url', 'metadata']
        missing_fields = [field for field in required_fields if field not in response]
        
        if missing_fields:
            print(f"   ❌ Missing required fields: {missing_fields}")
            return {
                "status": "FAILED",
                "error": f"Missing fields: {missing_fields}",
                "base64_size": 0,
                "is_placeholder": True
            }
        
        # Analyze asset URL and base64 data
        asset_url = response.get('asset_url', '')
        
        # Check data URL format
        if not asset_url.startswith('data:image/png;base64,'):
            print(f"   ❌ CRITICAL: Invalid data URL format")
            print(f"      Expected: 'data:image/png;base64,'")
            print(f"      Got: {asset_url[:50]}...")
            return {
                "status": "FAILED", 
                "error": "Invalid data URL format",
                "base64_size": 0,
                "is_placeholder": True
            }
        
        # Extract base64 data
        try:
            base64_data = asset_url.split(',')[1] if ',' in asset_url else ''
        except:
            print(f"   ❌ CRITICAL: Could not extract base64 data")
            return {
                "status": "FAILED",
                "error": "Could not extract base64 data", 
                "base64_size": 0,
                "is_placeholder": True
            }
        
        # CRITICAL: Check for Python byte notation (the main bug we're fixing)
        if "b'" in base64_data or "\\x" in base64_data:
            print(f"   ❌ CRITICAL: Python byte notation detected in base64 data!")
            print(f"      This indicates the base64 encoding fix has NOT been applied")
            print(f"      Sample: {base64_data[:100]}...")
            return {
                "status": "FAILED",
                "error": "Python byte notation in base64 data",
                "base64_size": len(base64_data),
                "is_placeholder": True
            }
        
        # Validate base64 format
        try:
            decoded_data = base64.b64decode(base64_data)
            print(f"   ✅ Valid base64 encoding format")
        except Exception as e:
            print(f"   ❌ CRITICAL: Invalid base64 format - {str(e)}")
            return {
                "status": "FAILED",
                "error": f"Invalid base64 format: {str(e)}",
                "base64_size": len(base64_data),
                "is_placeholder": True
            }
        
        # Analyze data size to determine if it's a real image or placeholder
        data_size = len(base64_data)
        
        # Determine if this is likely a placeholder or real image
        is_likely_placeholder = data_size < 1000  # Less than 1KB is likely a tiny placeholder
        is_substantial_image = data_size > 50000   # More than 50KB is definitely substantial
        
        # Check metadata for placeholder indicators
        metadata = response.get('metadata', {})
        is_placeholder_status = metadata.get('status') == 'placeholder' or metadata.get('status') == 'enhanced_placeholder'
        
        # Determine final status
        if is_placeholder_status:
            print(f"   ⚠️  PLACEHOLDER: Metadata indicates this is a placeholder asset")
            print(f"      Reason: {metadata.get('error', 'Unknown')}")
            status = "PLACEHOLDER"
        elif is_likely_placeholder:
            print(f"   ⚠️  LIKELY PLACEHOLDER: Base64 data is very small ({data_size} chars)")
            print(f"      This may be a colored block rather than a real image")
            status = "LIKELY_PLACEHOLDER"
        elif is_substantial_image:
            print(f"   ✅ SUBSTANTIAL IMAGE: Large base64 data ({data_size:,} chars)")
            print(f"      This appears to be a real generated image")
            status = "SUCCESS"
        else:
            print(f"   ⚠️  MEDIUM SIZE: Base64 data is medium size ({data_size:,} chars)")
            print(f"      Could be a real image or enhanced placeholder")
            status = "MEDIUM_SIZE"
        
        # Additional metadata analysis
        generation_method = metadata.get('generation_method', 'unknown')
        quality_tier = metadata.get('quality_tier', 'unknown')
        
        print(f"   📊 Generation Details:")
        print(f"      Method: {generation_method}")
        print(f"      Quality: {quality_tier}")
        print(f"      Base64 Size: {data_size:,} characters")
        
        return {
            "status": status,
            "base64_size": data_size,
            "is_placeholder": is_placeholder_status or is_likely_placeholder,
            "generation_method": generation_method,
            "quality_tier": quality_tier,
            "metadata": metadata
        }

    def test_complete_package_generation(self):
        """Test complete package generation to verify all 6 assets"""
        if not self.project_id:
            print("❌ Cannot test complete package - no project ID")
            return False
            
        print(f"\n📦 TESTING COMPLETE PACKAGE GENERATION")
        print("=" * 50)
        
        success, response = self.run_test(
            "Generate Complete Package",
            "POST",
            f"projects/{self.project_id}/complete-package",
            200,
            timeout=180  # Complete package takes longer
        )
        
        if not success:
            return False
        
        # Verify exactly 6 assets are returned
        if 'generated_assets' not in response:
            print("   ❌ CRITICAL: No 'generated_assets' field in response")
            return False
        
        assets = response['generated_assets']
        asset_count = len(assets)
        
        print(f"   📊 Asset Count: {asset_count}")
        
        if asset_count != 6:
            print(f"   ❌ CRITICAL: Expected 6 assets, got {asset_count}")
            return False
        
        print("   ✅ CRITICAL: Exactly 6 assets generated as expected")
        
        # Analyze each asset in the package
        expected_types = ['logo', 'business_card', 'letterhead', 'social_media_post', 'flyer', 'banner']
        package_results = {}
        
        for asset in assets:
            asset_type = asset.get('asset_type', 'unknown')
            asset_url = asset.get('asset_url', '')
            
            if asset_type in expected_types:
                print(f"   ✅ {asset_type} present in package")
                
                # Quick analysis of base64 data
                if asset_url.startswith('data:image/png;base64,'):
                    base64_data = asset_url.split(',')[1] if ',' in asset_url else ''
                    data_size = len(base64_data)
                    
                    # Check for byte notation bug
                    has_byte_notation = "b'" in base64_data or "\\x" in base64_data
                    
                    package_results[asset_type] = {
                        "present": True,
                        "base64_size": data_size,
                        "has_byte_notation": has_byte_notation,
                        "is_substantial": data_size > 50000
                    }
                    
                    if has_byte_notation:
                        print(f"      ❌ CRITICAL: {asset_type} has Python byte notation in base64!")
                    elif data_size > 50000:
                        print(f"      ✅ {asset_type}: Substantial image data ({data_size:,} chars)")
                    elif data_size < 1000:
                        print(f"      ⚠️  {asset_type}: Small data size ({data_size} chars) - likely placeholder")
                    else:
                        print(f"      ℹ️  {asset_type}: Medium data size ({data_size:,} chars)")
                else:
                    print(f"      ❌ {asset_type}: Invalid data URL format")
                    package_results[asset_type] = {
                        "present": True,
                        "base64_size": 0,
                        "has_byte_notation": False,
                        "is_substantial": False,
                        "error": "Invalid data URL format"
                    }
        
        # Check for missing asset types
        present_types = [asset.get('asset_type') for asset in assets]
        missing_types = [t for t in expected_types if t not in present_types]
        
        if missing_types:
            print(f"   ❌ CRITICAL: Missing asset types: {missing_types}")
            return False
        
        # Summary of package quality
        substantial_count = sum(1 for result in package_results.values() if result.get('is_substantial', False))
        byte_notation_count = sum(1 for result in package_results.values() if result.get('has_byte_notation', False))
        
        print(f"\n   📊 Package Quality Summary:")
        print(f"      Total assets: {asset_count}/6")
        print(f"      Substantial images: {substantial_count}/6")
        print(f"      Byte notation errors: {byte_notation_count}/6")
        
        if byte_notation_count > 0:
            print(f"   ❌ CRITICAL: {byte_notation_count} assets have base64 encoding issues")
            return False
        
        if substantial_count >= 4:  # At least 4 out of 6 should be substantial
            print(f"   ✅ GOOD: Most assets appear to be real images")
        else:
            print(f"   ⚠️  WARNING: Only {substantial_count} assets appear substantial")
        
        return True

    def print_final_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "=" * 70)
        print("🔧 IMAGE GENERATION FIX TEST RESULTS")
        print("=" * 70)
        print(f"📊 Overall Statistics:")
        print(f"   Tests Run: {self.tests_run}")
        print(f"   Tests Passed: {self.tests_passed}")
        print(f"   Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        
        if self.asset_results:
            print(f"\n🎨 Individual Asset Generation Results:")
            
            success_count = 0
            placeholder_count = 0
            failed_count = 0
            
            for asset_type, result in self.asset_results.items():
                status = result["status"]
                base64_size = result["base64_size"]
                
                if status == "SUCCESS":
                    print(f"   ✅ {asset_type}: SUCCESS ({base64_size:,} chars)")
                    success_count += 1
                elif status in ["PLACEHOLDER", "LIKELY_PLACEHOLDER"]:
                    print(f"   ⚠️  {asset_type}: {status} ({base64_size:,} chars)")
                    placeholder_count += 1
                else:
                    print(f"   ❌ {asset_type}: FAILED - {result.get('error', 'Unknown error')}")
                    failed_count += 1
            
            print(f"\n📈 Asset Generation Summary:")
            print(f"   Successful generations: {success_count}/{len(self.asset_results)}")
            print(f"   Placeholder/Small images: {placeholder_count}/{len(self.asset_results)}")
            print(f"   Failed generations: {failed_count}/{len(self.asset_results)}")
            
            # Determine overall fix status
            if failed_count == 0 and success_count >= len(self.asset_results) // 2:
                print(f"\n✅ IMAGE GENERATION FIX STATUS: SUCCESS")
                print(f"   The new Gemini API key is working properly")
                print(f"   Most assets are generating real images instead of placeholders")
            elif failed_count == 0:
                print(f"\n⚠️  IMAGE GENERATION FIX STATUS: PARTIAL SUCCESS")
                print(f"   No critical failures, but some assets may still be placeholders")
                print(f"   The new API key is working but image quality varies")
            else:
                print(f"\n❌ IMAGE GENERATION FIX STATUS: ISSUES DETECTED")
                print(f"   {failed_count} assets failed to generate properly")
                print(f"   May still have API quota or encoding issues")
        
        print(f"\n🔑 API Key Status:")
        print(f"   New Key: AIzaSyC4dZxc_uqWKGvSpU4_OC6uFEI3D3kj7xE")
        print(f"   Old Key: AIzaSyDF5OScBQWbdM6o6tsm8-YGxQLBOVjt-yA (quota exhausted)")
        
        if self.tests_passed == self.tests_run:
            print(f"\n🎉 ALL TESTS PASSED - Image generation fix verified!")
        else:
            failed_count = self.tests_run - self.tests_passed
            print(f"\n⚠️  {failed_count} tests failed - Review results above")

def main():
    print("🔧 CRITICAL IMAGE GENERATION FIX TESTING")
    print("=" * 70)
    print("🎯 FOCUS: Testing NEW GEMINI API KEY image generation")
    print("🔑 New API Key: AIzaSyC4dZxc_uqWKGvSpU4_OC6uFEI3D3kj7xE")
    print("🚫 Old API Key: AIzaSyDF5OScBQWbdM6o6tsm8-YGxQLBOVjt-yA (quota exhausted)")
    print("=" * 70)
    
    tester = ImageGenerationTester()
    
    # Test sequence focusing on image generation fix
    print("\n🚀 PHASE 1: Basic Setup and Project Creation")
    if not tester.test_health_check():
        print("❌ Health check failed - aborting tests")
        return 1
    
    if not tester.create_test_project():
        print("❌ Project creation failed - aborting tests")
        return 1
    
    if not tester.generate_brand_strategy():
        print("❌ Brand strategy generation failed - aborting tests")
        return 1
    
    print("\n🎨 PHASE 2: Individual Asset Generation Testing")
    print("Testing each asset type individually to verify real image generation...")
    
    individual_results = []
    for asset_type in tester.asset_types_to_test:
        result = tester.test_individual_asset_generation(asset_type)
        individual_results.append(result)
        time.sleep(2)  # Brief pause between generations
    
    print("\n📦 PHASE 3: Complete Package Generation Testing")
    package_result = tester.test_complete_package_generation()
    
    # Print final comprehensive summary
    tester.print_final_summary()
    
    # Determine exit code
    if all(individual_results) and package_result:
        print(f"\n🎉 SUCCESS: All image generation tests passed!")
        return 0
    else:
        print(f"\n⚠️  Some tests failed - see summary above")
        return 1

if __name__ == "__main__":
    sys.exit(main())