import os
import json
import logging
import asyncio
from typing import Dict, Any, List
from google import genai
from models.brand_strategy import BusinessInput, BrandStrategy

class AdvancedBrandStrategyEngine:
    """Phase 2: Advanced Multi-Layer AI Strategy Engine using Gemini AI with sophisticated strategic reasoning"""
    
    def __init__(self):
        self.client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))
        self.gemini_model = "gemini-2.5-flash"
        self.analysis_layers = 5
        
    async def analyze_business_concept(self, business_input: BusinessInput) -> Dict[str, Any]:
        """Revolutionary 5-Layer Strategic Analysis System"""
        
        # Layer 1: Market Analysis & Industry Intelligence
        market_analysis = await self.analyze_market_position(business_input)
        
        # Layer 2: Competitive Landscape & Differentiation
        competitive_analysis = await self.analyze_competitive_landscape(business_input, market_analysis)
        
        # Layer 3: Brand Personality & Archetype Development
        personality_analysis = await self.develop_brand_personality(
            business_input, market_analysis, competitive_analysis
        )
        
        # Layer 4: Visual Direction & Creative Brief
        visual_brief = await self.create_visual_brief(
            personality_analysis, market_analysis, business_input
        )
        
        # Layer 5: Strategic Synthesis & Recommendations
        strategic_synthesis = await self.synthesize_strategy(
            market_analysis, competitive_analysis, personality_analysis, visual_brief, business_input
        )
        
        return {
            "market_intelligence": market_analysis,
            "competitive_positioning": competitive_analysis,
            "brand_personality": personality_analysis,
            "visual_direction": visual_brief,
            "strategic_recommendations": strategic_synthesis,
            "confidence_scores": self.calculate_analysis_confidence(
                market_analysis, competitive_analysis, personality_analysis, visual_brief, strategic_synthesis
            )
        }
        
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
            response = await asyncio.get_event_loop().run_in_executor(None,
                lambda: self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=strategy_prompt
                )
            )
            
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
    
    async def analyze_market_position(self, business_input: BusinessInput) -> Dict[str, Any]:
        """Layer 1: Advanced Market Analysis & Industry Intelligence"""
        
        market_analysis_prompt = f"""
You are a senior market research analyst with 15+ years experience. Analyze this business:

BUSINESS: {business_input.business_description}
INDUSTRY: {business_input.industry}
TARGET AUDIENCE: {business_input.target_audience}
BUSINESS VALUES: {', '.join(business_input.business_values)}

Provide comprehensive market analysis:

1. MARKET SIZE & GROWTH POTENTIAL
   - Total Addressable Market (TAM)
   - Market growth trends and drivers
   - Key market segments

2. INDUSTRY DYNAMICS
   - Major industry trends affecting this business
   - Regulatory environment and challenges
   - Technology disruptions and opportunities

3. TARGET AUDIENCE INSIGHTS
   - Demographics and psychographics
   - Pain points and unmet needs
   - Buying behavior and decision factors

4. MARKET OPPORTUNITIES
   - Underserved segments
   - Emerging trends to capitalize on
   - Strategic partnerships potential

5. MARKET POSITIONING RECOMMENDATIONS
   - Optimal market position
   - Value proposition positioning
   - Differentiation strategies

Respond in this exact JSON format:
{{
    "market_size_analysis": {{
        "total_addressable_market": "TAM description and size estimation",
        "growth_trends": ["trend1", "trend2", "trend3"],
        "market_drivers": ["driver1", "driver2", "driver3"]
    }},
    "industry_dynamics": {{
        "major_trends": ["trend1", "trend2", "trend3"],
        "regulatory_environment": "regulatory landscape description",
        "technology_disruptions": ["disruption1", "disruption2"],
        "industry_challenges": ["challenge1", "challenge2"]
    }},
    "target_audience_insights": {{
        "demographics": "demographic profile",
        "psychographics": "psychological and behavioral traits",
        "pain_points": ["pain1", "pain2", "pain3"],
        "buying_behavior": "buying patterns and decision making process",
        "unmet_needs": ["need1", "need2", "need3"]
    }},
    "market_opportunities": {{
        "underserved_segments": ["segment1", "segment2"],
        "emerging_trends": ["trend1", "trend2", "trend3"],
        "partnership_opportunities": ["opportunity1", "opportunity2"],
        "market_gaps": ["gap1", "gap2"]
    }},
    "positioning_recommendations": {{
        "optimal_position": "recommended market position",
        "value_proposition_focus": "key value proposition elements",
        "differentiation_strategy": "how to differentiate from competition",
        "positioning_statement": "concise positioning statement"
    }},
    "confidence_score": 0.95
}}

Be specific, data-driven, and actionable. Focus on insights that inform brand strategy.
        """
        
        try:
            response = await asyncio.get_event_loop().run_in_executor(None,
                lambda: self.client.models.generate_content(
                    model=self.gemini_model,
                    contents=market_analysis_prompt
                )
            )
            
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            return json.loads(response_text)
            
        except Exception as e:
            logging.error(f"Error in market analysis: {str(e)}")
            return self._get_fallback_market_analysis()
    
    async def analyze_competitive_landscape(self, business_input: BusinessInput, market_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Layer 2: Advanced Competitive Landscape & Differentiation Analysis"""
        
        competitive_analysis_prompt = f"""
You are a competitive intelligence expert. Analyze the competitive landscape:

BUSINESS CONTEXT: {business_input.business_description}
INDUSTRY: {business_input.industry}
TARGET MARKET: {business_input.target_audience}
MARKET ANALYSIS: {market_analysis.get('positioning_recommendations', {}).get('optimal_position', 'Standard positioning')}

Provide detailed competitive analysis:

1. COMPETITIVE LANDSCAPE MAPPING
   - Direct competitors (3-5 main players)
   - Indirect competitors and substitutes
   - Competitive intensity assessment

2. COMPETITOR STRENGTH ANALYSIS
   - Market share and positioning
   - Brand strength and recognition
   - Competitive advantages

3. COMPETITIVE GAPS & OPPORTUNITIES
   - Unmet customer needs
   - Service/product gaps in market
   - Positioning white spaces

4. DIFFERENTIATION STRATEGY
   - Unique value propositions
   - Competitive moats to build
   - Positioning against competitors

5. STRATEGIC RECOMMENDATIONS
   - Competitive response strategies
   - Market entry/expansion tactics
   - Brand positioning vs. competition

Respond in this exact JSON format:
{{
    "competitive_landscape": {{
        "direct_competitors": [
            {{"name": "competitor1", "market_share": "percentage", "strengths": ["strength1", "strength2"]}},
            {{"name": "competitor2", "market_share": "percentage", "strengths": ["strength1", "strength2"]}},
            {{"name": "competitor3", "market_share": "percentage", "strengths": ["strength1", "strength2"]}}
        ],
        "indirect_competitors": ["substitute1", "substitute2", "substitute3"],
        "competitive_intensity": "high/medium/low with explanation"
    }},
    "competitor_analysis": {{
        "market_leaders": ["leader1", "leader2"],
        "brand_strength_ranking": ["brand1", "brand2", "brand3"],
        "competitive_advantages_by_player": {{
            "competitor1": ["advantage1", "advantage2"],
            "competitor2": ["advantage1", "advantage2"]
        }}
    }},
    "market_gaps": {{
        "unmet_customer_needs": ["need1", "need2", "need3"],
        "service_gaps": ["gap1", "gap2"],
        "positioning_white_spaces": ["space1", "space2"],
        "underserved_segments": ["segment1", "segment2"]
    }},
    "differentiation_strategy": {{
        "unique_value_propositions": ["uvp1", "uvp2", "uvp3"],
        "competitive_moats": ["moat1", "moat2"],
        "positioning_against_competition": "how to position vs competitors",
        "differentiation_pillars": ["pillar1", "pillar2", "pillar3"]
    }},
    "strategic_recommendations": {{
        "competitive_response_strategies": ["strategy1", "strategy2"],
        "market_entry_tactics": ["tactic1", "tactic2"],
        "brand_positioning_strategy": "recommended positioning vs competition",
        "competitive_messaging": "how to message against competition"
    }},
    "confidence_score": 0.90
}}

Focus on actionable insights for brand differentiation and positioning.
        """
        
        try:
            response = await asyncio.get_event_loop().run_in_executor(None,
                lambda: self.client.models.generate_content(
                    model=self.gemini_model,
                    contents=competitive_analysis_prompt
                )
            )
            
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            return json.loads(response_text)
            
        except Exception as e:
            logging.error(f"Error in competitive analysis: {str(e)}")
            return self._get_fallback_competitive_analysis()
    
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
            response = await asyncio.get_event_loop().run_in_executor(None,
                lambda: self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=personality_prompt
                )
            )
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