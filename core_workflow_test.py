#!/usr/bin/env python3
"""
BrandForge AI Core Workflow Test
Testing the essential Phase 1 workflow: Create → Strategy → Assets → Export
"""

import requests
import sys
import json
import time

class CoreWorkflowTester:
    def __init__(self, base_url="https://brandforge-phase1.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.project_id = None

    def test_core_workflow(self):
        """Test the complete core workflow"""
        print("🚀 Testing BrandForge AI Core Workflow")
        print("=" * 60)
        
        # Step 1: Create Project
        print("\n📝 Step 1: Creating Project...")
        project_data = {
            "business_name": "CoreFlow Test Inc",
            "business_description": "Testing core workflow functionality",
            "industry": "Technology",
            "target_audience": "Business professionals",
            "business_values": ["innovation", "quality"],
            "preferred_style": "modern",
            "preferred_colors": "blue and white"
        }
        
        response = requests.post(f"{self.base_url}/projects", json=project_data)
        if response.status_code == 200:
            data = response.json()
            self.project_id = data.get('project_id')
            print(f"✅ Project created: {self.project_id}")
        else:
            print(f"❌ Project creation failed: {response.status_code}")
            return False
        
        # Step 2: Generate Strategy
        print("\n🧠 Step 2: Generating Brand Strategy...")
        response = requests.post(f"{self.base_url}/projects/{self.project_id}/strategy")
        if response.status_code == 200:
            strategy = response.json()
            print("✅ Brand strategy generated successfully")
            print(f"   - Brand personality: {len(strategy.get('brand_personality', {}))} fields")
            print(f"   - Color palette: {len(strategy.get('color_palette', []))} colors")
            print(f"   - Visual direction: {len(strategy.get('visual_direction', {}))} fields")
        else:
            print(f"❌ Strategy generation failed: {response.status_code}")
            return False
        
        # Step 3: Generate Individual Assets
        print("\n🎨 Step 3: Generating Individual Assets...")
        
        # Generate Logo
        response = requests.post(f"{self.base_url}/projects/{self.project_id}/assets/logo")
        if response.status_code == 200:
            logo = response.json()
            print("✅ Logo generated successfully")
            asset_url = logo.get('asset_url', '')
            if asset_url.startswith('data:image/png;base64,'):
                base64_data = asset_url.split(',')[1] if ',' in asset_url else ''
                print(f"   - Logo data size: {len(base64_data)} chars")
        else:
            print(f"❌ Logo generation failed: {response.status_code}")
        
        # Generate Business Card
        response = requests.post(f"{self.base_url}/projects/{self.project_id}/assets/business_card")
        if response.status_code == 200:
            business_card = response.json()
            print("✅ Business card generated successfully")
            asset_url = business_card.get('asset_url', '')
            if asset_url.startswith('data:image/png;base64,'):
                base64_data = asset_url.split(',')[1] if ',' in asset_url else ''
                print(f"   - Business card data size: {len(base64_data)} chars")
        else:
            print(f"❌ Business card generation failed: {response.status_code}")
        
        # Step 4: Test Analytics
        print("\n📊 Step 4: Testing Analytics...")
        response = requests.get(f"{self.base_url}/projects/{self.project_id}/analytics")
        if response.status_code == 200:
            analytics = response.json()
            print("✅ Analytics generated successfully")
            print(f"   - Brand strength score: {analytics.get('brand_strength_score', 'N/A')}")
            print(f"   - Visual consistency score: {analytics.get('visual_consistency_score', 'N/A')}")
            print(f"   - Total assets: {analytics.get('total_assets', 0)}")
        else:
            print(f"❌ Analytics failed: {response.status_code}")
        
        # Step 5: Test Export (with correct format)
        print("\n📤 Step 5: Testing Export...")
        export_data = ["png", "pdf"]  # Send as list directly
        response = requests.post(f"{self.base_url}/projects/{self.project_id}/export", json=export_data)
        if response.status_code == 200:
            export_result = response.json()
            print("✅ Export successful")
            if 'download_url' in export_result:
                print("   - Download URL generated")
        else:
            print(f"❌ Export failed: {response.status_code} - {response.text}")
        
        print("\n" + "=" * 60)
        print("✅ Core Workflow Test Completed")
        return True

def main():
    tester = CoreWorkflowTester()
    success = tester.test_core_workflow()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())