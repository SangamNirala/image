import requests
import json
import time

def test_critical_asset_generation():
    """Test the critical fix for asset generation"""
    
    base_url = "https://asset-harmony.preview.emergentagent.com/api"
    
    print("🚨 CRITICAL ASSET GENERATION TEST")
    print("=" * 50)
    
    # Step 1: Create project
    print("1. Creating test project...")
    project_data = {
        "business_name": "CriticalTest Corp",
        "business_description": "Testing critical asset generation fix",
        "industry": "Technology",
        "target_audience": "Test users",
        "business_values": ["reliability", "quality"],
        "preferred_style": "modern",
        "preferred_colors": "blue"
    }
    
    response = requests.post(f"{base_url}/projects", json=project_data, timeout=30)
    if response.status_code != 200:
        print(f"❌ Project creation failed: {response.status_code}")
        return False
    
    project_id = response.json().get('project_id') or response.json().get('id')
    print(f"✅ Project created: {project_id}")
    
    # Step 2: Generate strategy
    print("2. Generating brand strategy...")
    response = requests.post(f"{base_url}/projects/{project_id}/strategy", timeout=120)
    if response.status_code != 200:
        print(f"❌ Strategy generation failed: {response.status_code}")
        return False
    print("✅ Brand strategy generated")
    
    # Step 3: Test individual asset generation (the critical ones that were broken)
    critical_assets = ["letterhead", "social_media_post", "flyer", "banner"]
    working_assets = ["logo", "business_card"]
    
    results = {}
    
    print("3. Testing CRITICAL asset generation (previously broken)...")
    for asset_type in critical_assets:
        print(f"   Testing {asset_type}...")
        response = requests.post(f"{base_url}/projects/{project_id}/assets/{asset_type}", timeout=90)
        
        if response.status_code == 200:
            data = response.json()
            asset_url = data.get('asset_url', '')
            
            if asset_url.startswith('data:image/png;base64,'):
                base64_data = asset_url.split(',')[1] if ',' in asset_url else ''
                data_length = len(base64_data)
                
                # Check if it's a substantial image (not a colored block)
                if data_length > 1000:  # Substantial data
                    print(f"   ✅ {asset_type}: SUCCESS - {data_length} chars (real image)")
                    results[asset_type] = "SUCCESS"
                else:
                    print(f"   ⚠️  {asset_type}: SMALL DATA - {data_length} chars (possible colored block)")
                    results[asset_type] = "SMALL_DATA"
            else:
                print(f"   ❌ {asset_type}: INVALID URL FORMAT")
                results[asset_type] = "INVALID_URL"
        else:
            print(f"   ❌ {asset_type}: API ERROR - {response.status_code}")
            results[asset_type] = "API_ERROR"
    
    print("4. Testing WORKING asset generation (should still work)...")
    for asset_type in working_assets:
        print(f"   Testing {asset_type}...")
        response = requests.post(f"{base_url}/projects/{project_id}/assets/{asset_type}", timeout=90)
        
        if response.status_code == 200:
            data = response.json()
            asset_url = data.get('asset_url', '')
            
            if asset_url.startswith('data:image/png;base64,'):
                base64_data = asset_url.split(',')[1] if ',' in asset_url else ''
                data_length = len(base64_data)
                
                if data_length > 1000:
                    print(f"   ✅ {asset_type}: SUCCESS - {data_length} chars")
                    results[asset_type] = "SUCCESS"
                else:
                    print(f"   ⚠️  {asset_type}: SMALL DATA - {data_length} chars")
                    results[asset_type] = "SMALL_DATA"
            else:
                print(f"   ❌ {asset_type}: INVALID URL FORMAT")
                results[asset_type] = "INVALID_URL"
        else:
            print(f"   ❌ {asset_type}: API ERROR - {response.status_code}")
            results[asset_type] = "API_ERROR"
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 CRITICAL FIX TEST RESULTS")
    print("=" * 50)
    
    success_count = sum(1 for result in results.values() if result == "SUCCESS")
    total_count = len(results)
    
    print(f"Overall Success Rate: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    
    print("\nDetailed Results:")
    for asset_type, result in results.items():
        status_icon = "✅" if result == "SUCCESS" else "⚠️" if result == "SMALL_DATA" else "❌"
        print(f"  {status_icon} {asset_type}: {result}")
    
    # Critical assessment
    critical_success = sum(1 for asset in critical_assets if results.get(asset) == "SUCCESS")
    working_success = sum(1 for asset in working_assets if results.get(asset) == "SUCCESS")
    
    print(f"\n🎯 CRITICAL FIX ASSESSMENT:")
    print(f"   Previously Broken Assets: {critical_success}/{len(critical_assets)} working")
    print(f"   Previously Working Assets: {working_success}/{len(working_assets)} still working")
    
    if critical_success >= 3:  # At least 3 out of 4 critical assets working
        print("   ✅ CRITICAL FIX APPEARS TO BE WORKING!")
        print("   ✅ Most previously broken assets now generating real images")
        return True
    elif critical_success >= 1:
        print("   ⚠️  PARTIAL SUCCESS - Some critical assets working")
        print("   ⚠️  Fix is partially effective but needs improvement")
        return False
    else:
        print("   ❌ CRITICAL FIX NOT WORKING")
        print("   ❌ Previously broken assets still not generating properly")
        return False

if __name__ == "__main__":
    success = test_critical_asset_generation()
    exit(0 if success else 1)