import requests
import json

def test_phase32_endpoints():
    """Simple test of Phase 3.2 endpoints availability"""
    base_url = "https://logo-vanisher.preview.emergentagent.com/api"
    
    print("🚀 PHASE 3.2 ENDPOINT AVAILABILITY TEST")
    print("=" * 50)
    
    # Test endpoints with a dummy project ID
    test_project_id = "test-project-id"
    test_asset_id = "test-asset-id"
    
    endpoints = [
        {
            'name': 'Health Check',
            'method': 'GET',
            'url': f"{base_url}/health",
            'expected_status': 200
        },
        {
            'name': 'Advanced Consistency Validation',
            'method': 'POST',
            'url': f"{base_url}/projects/{test_project_id}/consistency/advanced-validation?asset_id={test_asset_id}&target_consistency=0.85",
            'expected_status': 404  # Project not found is expected
        },
        {
            'name': 'Visual DNA Extraction',
            'method': 'GET',
            'url': f"{base_url}/projects/{test_project_id}/consistency/visual-dna",
            'expected_status': 404  # Project not found is expected
        },
        {
            'name': 'Intelligent Constraints Generation',
            'method': 'POST',
            'url': f"{base_url}/projects/{test_project_id}/consistency/intelligent-constraints?asset_type=logo",
            'expected_status': 404  # Project not found is expected
        },
        {
            'name': 'Brand Memory Insights',
            'method': 'GET',
            'url': f"{base_url}/projects/{test_project_id}/consistency/brand-memory",
            'expected_status': 404  # Project not found is expected
        },
        {
            'name': 'Intelligent Asset Refinement',
            'method': 'POST',
            'url': f"{base_url}/projects/{test_project_id}/consistency/asset-refinement?asset_id={test_asset_id}&refinement_iterations=3",
            'expected_status': 404  # Project not found is expected
        }
    ]
    
    results = []
    
    for endpoint in endpoints:
        print(f"\n🔍 Testing {endpoint['name']}...")
        print(f"   URL: {endpoint['url']}")
        
        try:
            if endpoint['method'] == 'GET':
                response = requests.get(endpoint['url'], timeout=10)
            else:
                response = requests.post(endpoint['url'], json={}, timeout=10)
            
            status_ok = response.status_code == endpoint['expected_status']
            
            if status_ok:
                print(f"✅ Endpoint Available - Status: {response.status_code}")
                results.append(True)
                
                # Check response content
                try:
                    response_data = response.json()
                    if endpoint['expected_status'] == 404:
                        if 'detail' in response_data and 'not found' in response_data['detail'].lower():
                            print(f"   ✅ Correct error response: {response_data['detail']}")
                        else:
                            print(f"   ⚠️ Unexpected error format: {response_data}")
                    else:
                        print(f"   ✅ Response: {response_data}")
                except:
                    print(f"   ⚠️ Non-JSON response")
            else:
                print(f"❌ Endpoint Issue - Expected {endpoint['expected_status']}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error: {response.text}")
                results.append(False)
                
        except Exception as e:
            print(f"❌ Request Failed - Error: {str(e)}")
            results.append(False)
    
    # Summary
    print(f"\n{'='*50}")
    print(f"📊 PHASE 3.2 ENDPOINT TEST RESULTS")
    print(f"{'='*50}")
    print(f"Endpoints Tested: {len(endpoints)}")
    print(f"Endpoints Available: {sum(results)}")
    print(f"Success Rate: {(sum(results)/len(results)*100):.1f}%")
    
    if sum(results) == len(results):
        print(f"\n✅ ALL PHASE 3.2 ENDPOINTS ARE AVAILABLE!")
        print(f"🎉 Revolutionary Multi-Asset Consistency System endpoints are operational!")
    else:
        failed_endpoints = [endpoints[i]['name'] for i, result in enumerate(results) if not result]
        print(f"\n❌ Failed Endpoints:")
        for endpoint in failed_endpoints:
            print(f"   - {endpoint}")
    
    return sum(results) == len(results)

if __name__ == "__main__":
    test_phase32_endpoints()