import os
import json
import logging
from typing import Dict, Any, List
import google.generativeai as genai
from models.brand_strategy import BusinessInput, BrandStrategy

class BrandStrategyEngine:
    """Advanced brand strategy generation using Gemini AI with sophisticated prompting"""
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
    async def analyze_business_concept(self, business_input: BusinessInput) -> Dict[str, Any]:
        """Multi-layer strategic analysis of business concept"""
        
        # Layer 1: Market Analysis
        market_analysis = await self._analyze_market_position(business_input)
        
        # Layer 2: Competitive Landscape
        competitive_analysis = await self._analyze_competitive_landscape(business_input)
        
        # Layer 3: Brand Personality Development
        personality_analysis = await self._develop_brand_personality(business_input, market_analysis, competitive_analysis)
        
        return {
            "market_analysis": market_analysis,
            "competitive_analysis": competitive_analysis,
            "personality_analysis": personality_analysis
        }
    
    async def generate_comprehensive_strategy(self, business_input: BusinessInput) -> BrandStrategy:
        """Generate comprehensive brand strategy using advanced analysis"""
        
        # Get multi-layer analysis
        analysis = await self.analyze_business_concept(business_input)
        
        # Create comprehensive strategy prompt
        strategy_prompt = self._build_advanced_strategy_prompt(business_input, analysis)
        
        try:
            response = await self.model.generate_content_async(strategy_prompt)
            
            # Extract and parse JSON response
            strategy_text = response.text.strip()
            if strategy_text.startswith('```json'):
                strategy_text = strategy_text.replace('```json', '').replace('```', '').strip()
            
            strategy_data = json.loads(strategy_text)
            
            # Create BrandStrategy object with enhanced data
            brand_strategy = BrandStrategy(
                business_name=business_input.business_name,
                brand_personality=strategy_data["brand_personality"],
                visual_direction=strategy_data["visual_direction"],
                color_palette=strategy_data["color_palette"],
                messaging_framework=strategy_data["messaging_framework"],
                consistency_rules=strategy_data["consistency_rules"]
            )
            
            return brand_strategy
            
        except Exception as e:
            logging.error(f"Error generating comprehensive brand strategy: {str(e)}")
            # Fallback to simplified strategy
            return await self._generate_fallback_strategy(business_input)
    
    async def _analyze_market_position(self, business_input: BusinessInput) -> Dict[str, Any]:
        """Analyze market position and opportunities"""
        
        market_prompt = f"""
        As a market research expert, analyze the market position for this business:
        
        Business: {business_input.business_name}
        Industry: {business_input.industry}
        Description: {business_input.business_description}
        Target Audience: {business_input.target_audience}
        
        Provide market analysis in JSON format:
        {{
            "market_size": "description",
            "market_trends": ["trend1", "trend2", "trend3"],
            "opportunities": ["opportunity1", "opportunity2"],
            "challenges": ["challenge1", "challenge2"],
            "positioning_recommendations": "recommendations"
        }}
        """
        
        try:
            response = await self.model.generate_content_async(market_prompt)
            return json.loads(response.text.strip().replace('```json', '').replace('```', '').strip())
        except:
            return {"market_size": "moderate", "market_trends": [], "opportunities": [], "challenges": []}
    
    async def _analyze_competitive_landscape(self, business_input: BusinessInput) -> Dict[str, Any]:
        """Analyze competitive landscape and differentiation opportunities"""
        
        competitive_prompt = f"""
        As a competitive intelligence expert, analyze the competitive landscape:
        
        Business: {business_input.business_name}
        Industry: {business_input.industry}
        Description: {business_input.business_description}
        
        Provide competitive analysis in JSON format:
        {{
            "key_competitors": ["competitor1", "competitor2", "competitor3"],
            "competitive_advantages": ["advantage1", "advantage2"],
            "differentiation_opportunities": ["opportunity1", "opportunity2"],
            "market_gaps": ["gap1", "gap2"],
            "positioning_strategy": "strategy_description"
        }}
        """
        
        try:
            response = await self.model.generate_content_async(competitive_prompt)
            return json.loads(response.text.strip().replace('```json', '').replace('```', '').strip())
        except:
            return {"key_competitors": [], "competitive_advantages": [], "differentiation_opportunities": []}
    
    async def _develop_brand_personality(self, business_input: BusinessInput, market_analysis: Dict, competitive_analysis: Dict) -> Dict[str, Any]:
        """Develop sophisticated brand personality based on analysis"""
        
        personality_prompt = f"""
        As a brand psychology expert, develop a sophisticated brand personality:
        
        Business Context:
        - Name: {business_input.business_name}
        - Industry: {business_input.industry}
        - Values: {', '.join(business_input.business_values)}
        
        Market Context: {market_analysis.get('positioning_recommendations', 'Standard positioning')}
        Competitive Context: {competitive_analysis.get('positioning_strategy', 'Standard strategy')}
        
        Develop brand personality in JSON format:
        {{
            "core_personality": {{
                "primary_traits": ["trait1", "trait2", "trait3", "trait4", "trait5"],
                "brand_archetype": "archetype_name",
                "personality_description": "detailed_description"
            }},
            "emotional_drivers": ["driver1", "driver2", "driver3"],
            "brand_voice_attributes": ["attribute1", "attribute2", "attribute3"],
            "relationship_style": "how_brand_relates_to_customers"
        }}
        """
        
        try:
            response = await self.model.generate_content_async(personality_prompt)
            return json.loads(response.text.strip().replace('```json', '').replace('```', '').strip())
        except:
            return {"core_personality": {"primary_traits": ["professional", "reliable", "innovative"]}}
    
    def _build_advanced_strategy_prompt(self, business_input: BusinessInput, analysis: Dict[str, Any]) -> str:
        """Build comprehensive strategy generation prompt"""
        
        return f"""
        You are an expert brand strategist with 20+ years of experience. Create a comprehensive brand strategy.
        
        BUSINESS INFORMATION:
        - Name: {business_input.business_name}
        - Description: {business_input.business_description}
        - Industry: {business_input.industry}
        - Target Audience: {business_input.target_audience}
        - Values: {', '.join(business_input.business_values)}
        - Style Preference: {business_input.preferred_style}
        - Color Preference: {business_input.preferred_colors}
        
        STRATEGIC ANALYSIS:
        Market Position: {analysis.get('market_analysis', {}).get('positioning_recommendations', 'Standard')}
        Competitive Strategy: {analysis.get('competitive_analysis', {}).get('positioning_strategy', 'Standard')}
        Brand Personality: {analysis.get('personality_analysis', {}).get('core_personality', {})}
        
        Generate a detailed brand strategy with this exact JSON structure:
        {{
            "brand_personality": {{
                "primary_traits": ["trait1", "trait2", "trait3", "trait4", "trait5"],
                "brand_archetype": "archetype_name",
                "tone_of_voice": "detailed_tone_description",
                "brand_essence": "one_sentence_brand_essence",
                "emotional_drivers": ["driver1", "driver2", "driver3"]
            }},
            "visual_direction": {{
                "design_style": "detailed_style_description",
                "visual_mood": "mood_and_feeling_description",
                "typography_style": "typography_recommendations",
                "imagery_style": "imagery_and_photography_style",
                "logo_direction": "detailed_logo_design_guidance",
                "layout_principles": "layout_and_composition_guidelines"
            }},
            "color_palette": ["#primary_color", "#secondary_color", "#accent1", "#accent2", "#neutral"],
            "messaging_framework": {{
                "tagline": "compelling_memorable_tagline",
                "key_messages": ["message1", "message2", "message3"],
                "brand_promise": "clear_brand_promise",
                "unique_value_proposition": "distinctive_uvp",
                "brand_story": "compelling_brand_narrative"
            }},
            "consistency_rules": {{
                "logo_usage": "detailed_logo_usage_guidelines",
                "color_usage": "color_application_and_combination_rules",
                "typography_rules": "typography_hierarchy_and_usage",
                "visual_consistency": "visual_consistency_requirements",
                "brand_voice_consistency": "voice_and_tone_consistency_rules"
            }}
        }}
        
        Make the strategy sophisticated, cohesive, and perfectly aligned with the business goals and market position.
        """
    
    async def _generate_fallback_strategy(self, business_input: BusinessInput) -> BrandStrategy:
        """Generate a simplified strategy as fallback"""
        
        return BrandStrategy(
            business_name=business_input.business_name,
            brand_personality={
                "primary_traits": ["professional", "reliable", "innovative", "trustworthy", "modern"],
                "brand_archetype": "The Innovator",
                "tone_of_voice": "Professional yet approachable",
                "brand_essence": f"Delivering excellence in {business_input.industry}"
            },
            visual_direction={
                "design_style": "Modern and clean",
                "visual_mood": "Professional and trustworthy",
                "typography_style": "Clean, readable fonts",
                "imagery_style": "Professional and high-quality",
                "logo_direction": "Simple, memorable, and scalable"
            },
            color_palette=["#2563eb", "#1e40af", "#3b82f6", "#60a5fa", "#f8fafc"],
            messaging_framework={
                "tagline": f"Excellence in {business_input.industry}",
                "key_messages": ["Quality", "Innovation", "Trust"],
                "brand_promise": "Delivering exceptional value",
                "unique_value_proposition": "Your trusted partner for success"
            },
            consistency_rules={
                "logo_usage": "Use primary logo on light backgrounds",
                "color_usage": "Primary blue for main elements, neutrals for text",
                "typography_rules": "Consistent font hierarchy",
                "visual_consistency": "Maintain clean, professional appearance"
            }
        )