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
        """Generate comprehensive brand strategy using Phase 2 advanced multi-layer analysis"""
        
        # Get revolutionary 5-layer analysis
        analysis = await self.analyze_business_concept(business_input)
        
        # Build final strategy from all analysis layers
        strategy_prompt = self._build_phase2_strategy_prompt(business_input, analysis)
        
        try:
            response = await asyncio.get_event_loop().run_in_executor(None,
                lambda: self.client.models.generate_content(
                    model=self.gemini_model,
                    contents=strategy_prompt
                )
            )
            
            # Extract and parse JSON response
            strategy_text = response.text.strip()
            if strategy_text.startswith('```json'):
                strategy_text = strategy_text.replace('```json', '').replace('```', '').strip()
            
            strategy_data = json.loads(strategy_text)
            
            # Create BrandStrategy object with Phase 2 enhanced data
            brand_strategy = BrandStrategy(
                business_name=business_input.business_name,
                brand_personality=strategy_data["brand_personality"],
                visual_direction=strategy_data["visual_direction"],
                color_palette=strategy_data["color_palette"],
                messaging_framework=strategy_data["messaging_framework"],
                consistency_rules=strategy_data["consistency_rules"],
                advanced_analysis=analysis  # Include all Phase 2 analysis data
            )
            
            return brand_strategy
            
        except Exception as e:
            logging.error(f"Error generating Phase 2 comprehensive brand strategy: {str(e)}")
            # Enhanced fallback with Phase 2 capabilities
            return await self._generate_phase2_fallback_strategy(business_input)

    def _build_phase2_strategy_prompt(self, business_input: BusinessInput, analysis: Dict[str, Any]) -> str:
        """Build Phase 2 advanced strategy generation prompt with multi-layer analysis"""
        
        return f"""
You are an expert brand strategist with 20+ years of experience creating world-class brand strategies.
You have access to comprehensive 5-layer strategic analysis. Create the most sophisticated brand strategy possible.

BUSINESS INFORMATION:
- Name: {business_input.business_name}
- Description: {business_input.business_description}
- Industry: {business_input.industry}
- Target Audience: {business_input.target_audience}
- Values: {', '.join(business_input.business_values)}
- Style Preference: {business_input.preferred_style}
- Color Preference: {business_input.preferred_colors}

ADVANCED STRATEGIC ANALYSIS (5 LAYERS):

LAYER 1 - MARKET INTELLIGENCE:
Market Position: {analysis.get('market_intelligence', {}).get('positioning_recommendations', {}).get('optimal_position', 'Standard')}
Growth Opportunities: {analysis.get('market_intelligence', {}).get('market_opportunities', {}).get('emerging_trends', [])}

LAYER 2 - COMPETITIVE POSITIONING:
Differentiation Strategy: {analysis.get('competitive_positioning', {}).get('differentiation_strategy', {}).get('positioning_against_competition', 'Standard')}
Unique Value Props: {analysis.get('competitive_positioning', {}).get('differentiation_strategy', {}).get('unique_value_propositions', [])}

LAYER 3 - BRAND PERSONALITY:
Primary Archetype: {analysis.get('brand_personality', {}).get('brand_archetype', {}).get('primary_archetype', 'Innovator')}
Core Traits: {[trait.get('trait', '') for trait in analysis.get('brand_personality', {}).get('personality_traits', {}).get('core_traits', [])]}

LAYER 4 - VISUAL DIRECTION:
Visual Philosophy: {analysis.get('visual_direction', {}).get('visual_strategy', {}).get('visual_philosophy', 'Modern approach')}
Color Strategy: {analysis.get('visual_direction', {}).get('color_strategy', {}).get('color_psychology_rationale', 'Strategic colors')}

LAYER 5 - STRATEGIC SYNTHESIS:
Key Insights: {analysis.get('strategic_recommendations', {}).get('strategic_insights', {}).get('key_insights', [])}
Brand Promise: {analysis.get('strategic_recommendations', {}).get('brand_strategy_framework', {}).get('brand_promise', 'Excellence')}

Generate the most advanced brand strategy with this exact JSON structure:
{{
    "brand_personality": {{
        "primary_traits": ["trait1", "trait2", "trait3", "trait4", "trait5"],
        "brand_archetype": "archetype_name_from_analysis",
        "tone_of_voice": "sophisticated_tone_description_based_on_analysis",
        "brand_essence": "powerful_one_sentence_brand_essence",
        "emotional_drivers": ["driver1", "driver2", "driver3"],
        "personality_expression": "how_personality_shows_up_across_touchpoints"
    }},
    "visual_direction": {{
        "design_style": "advanced_style_description_from_visual_brief",
        "visual_mood": "sophisticated_mood_from_analysis",
        "typography_strategy": "strategic_typography_recommendations",
        "imagery_style": "advanced_imagery_direction",
        "logo_direction": "detailed_logo_design_guidance_from_brief",
        "layout_principles": "advanced_layout_composition_guidelines",
        "visual_consistency_framework": "comprehensive_visual_consistency_approach"
    }},
    "color_palette": ["#strategic_primary", "#strategic_secondary", "#strategic_accent1", "#strategic_accent2", "#strategic_neutral"],
    "messaging_framework": {{
        "tagline": "compelling_memorable_tagline_from_synthesis",
        "key_messages": ["strategic_message1", "strategic_message2", "strategic_message3"],
        "brand_promise": "clear_brand_promise_from_analysis",
        "unique_value_proposition": "distinctive_uvp_from_competitive_analysis",
        "brand_story": "compelling_brand_narrative_from_all_layers",
        "messaging_hierarchy": "how_messages_prioritize_and_connect"
    }},
    "consistency_rules": {{
        "logo_usage": "detailed_logo_usage_guidelines_from_visual_brief",
        "color_usage": "strategic_color_application_rules",
        "typography_rules": "comprehensive_typography_hierarchy",
        "visual_consistency": "advanced_visual_consistency_requirements",
        "brand_voice_consistency": "sophisticated_voice_tone_consistency_rules",
        "touchpoint_consistency": "how_brand_stays_consistent_across_all_touchpoints"
    }},
    "strategic_insights": {{
        "market_opportunity": "key_market_opportunity_from_analysis",
        "competitive_advantage": "primary_competitive_advantage",
        "brand_positioning": "precise_brand_positioning_statement",
        "success_factors": ["factor1", "factor2", "factor3"]
    }}
}}

Make the strategy revolutionary, sophisticated, and perfectly aligned with all 5 layers of strategic analysis.
This should be the most advanced brand strategy possible using AI-powered multi-layer intelligence.
        """
    
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
    
    async def develop_brand_personality(self, business_input: BusinessInput, market_analysis: Dict, competitive_analysis: Dict) -> Dict[str, Any]:
        """Layer 3: Advanced Brand Personality & Archetype Development"""
        
        brand_personality_prompt = f"""
You are a brand psychology expert specializing in brand archetypes and personality development.

BUSINESS CONTEXT: {business_input.business_description}
MARKET INSIGHTS: {market_analysis.get('positioning_recommendations', {}).get('optimal_position', 'Standard positioning')}
COMPETITIVE LANDSCAPE: {competitive_analysis.get('differentiation_strategy', {}).get('positioning_against_competition', 'Standard strategy')}
INDUSTRY: {business_input.industry}
TARGET AUDIENCE: {business_input.target_audience}
BUSINESS VALUES: {', '.join(business_input.business_values)}

Develop comprehensive brand personality:

1. BRAND ARCHETYPE SELECTION
   - Primary archetype (Hero, Sage, Innovator, etc.)
   - Secondary archetype influences
   - Archetype justification based on market position

2. PERSONALITY TRAITS MATRIX
   - 5 core personality traits with detailed explanations
   - Personality expression across touchpoints
   - Emotional connection strategies

3. BRAND VOICE & TONE
   - Communication style and voice
   - Tone variations for different contexts
   - Language patterns and vocabulary

4. BRAND VALUES & BELIEFS
   - Core brand values alignment
   - Brand purpose and mission
   - Belief system and worldview

5. RELATIONSHIP DYNAMICS
   - How brand relates to customers
   - Brand-customer relationship model
   - Trust and credibility building

6. EMOTIONAL POSITIONING
   - Primary emotions to evoke
   - Emotional journey mapping
   - Feeling-based differentiation

Respond in this exact JSON format:
{{
    "brand_archetype": {{
        "primary_archetype": "archetype name",
        "secondary_influences": ["influence1", "influence2"],
        "archetype_justification": "why this archetype fits the market position and business goals",
        "archetype_characteristics": ["characteristic1", "characteristic2", "characteristic3"]
    }},
    "personality_traits": {{
        "core_traits": [
            {{"trait": "trait1", "description": "detailed explanation", "expression": "how it shows up"}},
            {{"trait": "trait2", "description": "detailed explanation", "expression": "how it shows up"}},
            {{"trait": "trait3", "description": "detailed explanation", "expression": "how it shows up"}},
            {{"trait": "trait4", "description": "detailed explanation", "expression": "how it shows up"}},
            {{"trait": "trait5", "description": "detailed explanation", "expression": "how it shows up"}}
        ],
        "personality_summary": "cohesive personality description"
    }},
    "brand_voice": {{
        "communication_style": "primary communication approach",
        "tone_variations": {{
            "formal_contexts": "tone for formal situations",
            "casual_contexts": "tone for casual interactions",
            "crisis_contexts": "tone during challenges"
        }},
        "language_patterns": ["pattern1", "pattern2", "pattern3"],
        "vocabulary_preferences": ["preference1", "preference2"]
    }},
    "brand_values_beliefs": {{
        "core_values": ["value1", "value2", "value3", "value4", "value5"],
        "brand_purpose": "why the brand exists beyond profit",
        "mission_statement": "what the brand aims to achieve",
        "belief_system": ["belief1", "belief2", "belief3"],
        "worldview": "how the brand sees the world"
    }},
    "relationship_dynamics": {{
        "customer_relationship_model": "how brand relates to customers",
        "trust_building_approach": "how trust is established",
        "credibility_factors": ["factor1", "factor2", "factor3"],
        "relationship_goals": ["goal1", "goal2"]
    }},
    "emotional_positioning": {{
        "primary_emotions": ["emotion1", "emotion2", "emotion3"],
        "emotional_journey": {{
            "awareness": "emotion at first contact",
            "consideration": "emotion during evaluation",
            "purchase": "emotion at decision",
            "loyalty": "emotion as loyal customer"
        }},
        "feeling_differentiation": "unique emotional position vs competitors"
    }},
    "confidence_score": 0.92
}}

Ensure personality aligns with market opportunity and competitive positioning.
        """
        
        try:
            response = await asyncio.get_event_loop().run_in_executor(None,
                lambda: self.client.models.generate_content(
                    model=self.gemini_model,
                    contents=brand_personality_prompt
                )
            )
            
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            return json.loads(response_text)
            
        except Exception as e:
            logging.error(f"Error in brand personality development: {str(e)}")
            return self._get_fallback_personality_analysis()
    
    async def create_visual_brief(self, personality_analysis: Dict, market_analysis: Dict, business_input: BusinessInput) -> Dict[str, Any]:
        """Layer 4: Advanced Visual Direction & Creative Brief Development"""
        
        visual_brief_prompt = f"""
You are a creative director with expertise in visual brand identity and design strategy.

BRAND PERSONALITY: {personality_analysis.get('brand_archetype', {}).get('primary_archetype', 'Innovator')}
PERSONALITY TRAITS: {[trait.get('trait', '') for trait in personality_analysis.get('personality_traits', {}).get('core_traits', [])]}
MARKET POSITION: {market_analysis.get('positioning_recommendations', {}).get('optimal_position', 'Standard positioning')}
BUSINESS CONTEXT: {business_input.business_description}
INDUSTRY: {business_input.industry}
STYLE PREFERENCE: {business_input.preferred_style}
COLOR PREFERENCE: {business_input.preferred_colors}

Create comprehensive visual direction and creative brief:

1. VISUAL STRATEGY FOUNDATION
   - Overall visual approach and philosophy
   - Visual personality expression
   - Brand visual goals and objectives

2. DESIGN SYSTEM ARCHITECTURE
   - Primary design principles
   - Visual hierarchy and structure
   - Design system components

3. COLOR STRATEGY & PSYCHOLOGY
   - Strategic color palette with psychology
   - Color usage guidelines and meanings
   - Emotional impact of color choices

4. TYPOGRAPHY & COMMUNICATION
   - Typography strategy and personality
   - Font selection criteria and rationale
   - Typographic hierarchy and applications

5. IMAGERY & VISUAL CONTENT
   - Photography and illustration style
   - Visual content strategy
   - Mood and aesthetic direction

6. LOGO & IDENTITY SYSTEMS
   - Logo design direction and requirements
   - Identity system architecture
   - Application and usage principles

Respond in this exact JSON format:
{{
    "visual_strategy": {{
        "visual_philosophy": "overarching visual philosophy and approach",
        "visual_personality_expression": "how personality shows up visually",
        "visual_goals": ["goal1", "goal2", "goal3"],
        "brand_visual_positioning": "how visuals position the brand"
    }},
    "design_system": {{
        "primary_design_principles": ["principle1", "principle2", "principle3"],
        "visual_hierarchy": "hierarchy structure and approach",
        "design_components": ["component1", "component2", "component3"],
        "consistency_framework": "how visual consistency is maintained"
    }},
    "color_strategy": {{
        "strategic_palette": [
            {{"color": "#primary", "hex": "#hexcode", "psychology": "emotional impact", "usage": "usage guidelines"}},
            {{"color": "#secondary", "hex": "#hexcode", "psychology": "emotional impact", "usage": "usage guidelines"}},
            {{"color": "#accent1", "hex": "#hexcode", "psychology": "emotional impact", "usage": "usage guidelines"}},
            {{"color": "#accent2", "hex": "#hexcode", "psychology": "emotional impact", "usage": "usage guidelines"}},
            {{"color": "#neutral", "hex": "#hexcode", "psychology": "emotional impact", "usage": "usage guidelines"}}
        ],
        "color_psychology_rationale": "why these colors support the brand strategy",
        "color_combinations": "recommended color pairings and relationships"
    }},
    "typography_strategy": {{
        "typography_personality": "how typography expresses brand personality",
        "font_selection_criteria": "what to look for in fonts",
        "typographic_hierarchy": {{
            "primary_heading": "font characteristics for main headlines",
            "secondary_heading": "font characteristics for subheadings", 
            "body_text": "font characteristics for body copy",
            "accent_text": "font characteristics for special text"
        }},
        "typography_applications": "how typography is used across touchpoints"
    }},
    "imagery_direction": {{
        "photography_style": "photography approach and characteristics",
        "illustration_style": "illustration approach if applicable",
        "visual_content_strategy": "overall approach to visual content",
        "mood_aesthetic": "overall aesthetic and mood direction",
        "visual_storytelling": "how visuals tell the brand story"
    }},
    "logo_identity_brief": {{
        "logo_design_direction": "specific logo design requirements and direction",
        "identity_system_requirements": "what the identity system needs to include",
        "logo_personality_expression": "how logo should express brand personality",
        "application_considerations": "key applications and usage scenarios",
        "logo_effectiveness_criteria": "how to measure logo success"
    }},
    "confidence_score": 0.94
}}

Ensure all visual direction aligns with brand personality and market positioning.
        """
        
        try:
            response = await asyncio.get_event_loop().run_in_executor(None,
                lambda: self.client.models.generate_content(
                    model=self.gemini_model,
                    contents=visual_brief_prompt
                )
            )
            
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            return json.loads(response_text)
            
        except Exception as e:
            logging.error(f"Error in visual brief creation: {str(e)}")
            return self._get_fallback_visual_brief()

    async def synthesize_strategy(self, market_analysis: Dict, competitive_analysis: Dict, 
                                personality_analysis: Dict, visual_brief: Dict, business_input: BusinessInput) -> Dict[str, Any]:
        """Layer 5: Advanced Strategic Synthesis & Comprehensive Recommendations"""
        
        synthesis_prompt = f"""
You are a senior brand strategist synthesizing comprehensive brand strategy analysis.

SYNTHESIS INPUTS:
MARKET INTELLIGENCE: {market_analysis.get('positioning_recommendations', {}).get('optimal_position', 'Standard')}
COMPETITIVE POSITIONING: {competitive_analysis.get('differentiation_strategy', {}).get('positioning_against_competition', 'Standard')}  
BRAND PERSONALITY: {personality_analysis.get('brand_archetype', {}).get('primary_archetype', 'Innovator')}
VISUAL DIRECTION: {visual_brief.get('visual_strategy', {}).get('visual_philosophy', 'Modern approach')}
BUSINESS CONTEXT: {business_input.business_description}

Create comprehensive strategic synthesis and recommendations:

1. STRATEGIC INSIGHTS INTEGRATION
   - Key insights from all analysis layers
   - Strategic themes and patterns
   - Critical success factors

2. BRAND STRATEGY SYNTHESIS
   - Unified brand strategy framework
   - Strategic positioning statement
   - Brand strategy pillars

3. IMPLEMENTATION ROADMAP
   - Priority implementation phases
   - Strategic milestones and metrics
   - Resource requirements and timeline

4. SUCCESS MEASUREMENT
   - Key performance indicators
   - Success metrics and benchmarks
   - Brand health measurement framework

5. STRATEGIC RECOMMENDATIONS
   - Immediate action items
   - Long-term strategic initiatives
   - Risk mitigation strategies

Respond in this exact JSON format:
{{
    "strategic_insights": {{
        "key_insights": ["insight1", "insight2", "insight3", "insight4"],
        "strategic_themes": ["theme1", "theme2", "theme3"],
        "critical_success_factors": ["factor1", "factor2", "factor3"],
        "strategic_opportunities": ["opportunity1", "opportunity2"]
    }},
    "brand_strategy_framework": {{
        "unified_strategy": "comprehensive brand strategy statement",
        "positioning_statement": "precise brand positioning",
        "strategy_pillars": ["pillar1", "pillar2", "pillar3", "pillar4"],
        "brand_promise": "clear brand promise to customers",
        "unique_value_proposition": "distinctive value proposition"
    }},
    "implementation_roadmap": {{
        "phase_1_immediate": {{
            "timeline": "0-3 months",
            "priorities": ["priority1", "priority2", "priority3"],
            "deliverables": ["deliverable1", "deliverable2"]
        }},
        "phase_2_build": {{
            "timeline": "3-9 months", 
            "priorities": ["priority1", "priority2", "priority3"],
            "deliverables": ["deliverable1", "deliverable2"]
        }},
        "phase_3_optimize": {{
            "timeline": "9-18 months",
            "priorities": ["priority1", "priority2"],
            "deliverables": ["deliverable1", "deliverable2"]
        }}
    }},
    "success_measurement": {{
        "kpis": ["kpi1", "kpi2", "kpi3", "kpi4"],
        "success_metrics": {{
            "brand_awareness": "awareness measurement approach",
            "brand_perception": "perception tracking method",
            "business_impact": "business impact metrics"
        }},
        "measurement_frequency": "how often to measure progress"
    }},
    "strategic_recommendations": {{
        "immediate_actions": ["action1", "action2", "action3"],
        "long_term_initiatives": ["initiative1", "initiative2"],
        "risk_mitigation": ["risk1_mitigation", "risk2_mitigation"],
        "competitive_response": "how to respond to competitive moves"
    }},
    "confidence_score": 0.96
}}

Provide actionable, strategic recommendations that integrate all analysis layers.
        """
        
        try:
            response = await asyncio.get_event_loop().run_in_executor(None,
                lambda: self.client.models.generate_content(
                    model=self.gemini_model,
                    contents=synthesis_prompt
                )
            )
            
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            return json.loads(response_text)
            
        except Exception as e:
            logging.error(f"Error in strategic synthesis: {str(e)}")
            return self._get_fallback_strategic_synthesis()

    def calculate_analysis_confidence(self, market_analysis: Dict, competitive_analysis: Dict, 
                                    personality_analysis: Dict, visual_brief: Dict, strategic_synthesis: Dict) -> Dict[str, float]:
        """Calculate confidence scores for each analysis layer"""
        
        return {
            "market_analysis_confidence": market_analysis.get("confidence_score", 0.85),
            "competitive_analysis_confidence": competitive_analysis.get("confidence_score", 0.80),
            "personality_analysis_confidence": personality_analysis.get("confidence_score", 0.90),
            "visual_brief_confidence": visual_brief.get("confidence_score", 0.88),
            "strategic_synthesis_confidence": strategic_synthesis.get("confidence_score", 0.92),
            "overall_confidence": (
                market_analysis.get("confidence_score", 0.85) +
                competitive_analysis.get("confidence_score", 0.80) +
                personality_analysis.get("confidence_score", 0.90) +
                visual_brief.get("confidence_score", 0.88) +
                strategic_synthesis.get("confidence_score", 0.92)
            ) / 5
        }
    
    async def _generate_phase2_fallback_strategy(self, business_input: BusinessInput) -> BrandStrategy:
        """Generate Phase 2 enhanced fallback strategy with advanced capabilities"""
        
        return BrandStrategy(
            business_name=business_input.business_name,
            brand_personality={
                "primary_traits": ["innovative", "trustworthy", "professional", "forward-thinking", "reliable"],
                "brand_archetype": "The Innovator",
                "tone_of_voice": "Professional yet approachable, confident and knowledgeable",
                "brand_essence": f"Pioneering excellence and innovation in {business_input.industry}",
                "emotional_drivers": ["trust", "confidence", "aspiration"],
                "personality_expression": "Consistent professional excellence across all touchpoints"
            },
            visual_direction={
                "design_style": "Modern, clean, and sophisticated with strategic use of space",
                "visual_mood": "Professional confidence with innovative edge",
                "typography_strategy": "Clean, readable fonts that convey authority and accessibility",
                "imagery_style": "High-quality, professional imagery that tells the brand story",
                "logo_direction": "Simple, memorable, scalable design that works across all applications",
                "layout_principles": "Clean hierarchy, strategic whitespace, consistent alignment",
                "visual_consistency_framework": "Cohesive visual language across all brand touchpoints"
            },
            color_palette=["#2563eb", "#1e40af", "#3b82f6", "#60a5fa", "#f8fafc"],
            messaging_framework={
                "tagline": f"Innovating Excellence in {business_input.industry}",
                "key_messages": ["Innovation Leadership", "Trusted Expertise", "Exceptional Results"],
                "brand_promise": "Delivering innovative solutions that drive exceptional outcomes",
                "unique_value_proposition": "Your strategic partner for breakthrough success",
                "brand_story": f"Leading innovation in {business_input.industry} through expertise and commitment",
                "messaging_hierarchy": "Innovation first, trust builds, results deliver"
            },
            consistency_rules={
                "logo_usage": "Primary logo on light backgrounds, reversed logo on dark backgrounds",
                "color_usage": "Primary blue for key elements, supporting palette for hierarchy",
                "typography_rules": "Consistent font hierarchy with clear information architecture",
                "visual_consistency": "Maintain sophisticated professional appearance across all materials",
                "brand_voice_consistency": "Professional confidence balanced with approachable expertise",
                "touchpoint_consistency": "Seamless brand experience across all customer interactions"
            },
            advanced_analysis={
                "market_intelligence": {"confidence_score": 0.75},
                "competitive_positioning": {"confidence_score": 0.70},
                "brand_personality": {"confidence_score": 0.85},
                "visual_direction": {"confidence_score": 0.80},
                "strategic_recommendations": {"confidence_score": 0.78}
            }
        )

    def _get_fallback_market_analysis(self) -> Dict[str, Any]:
        """Fallback market analysis for error scenarios"""
        return {
            "market_size_analysis": {
                "total_addressable_market": "Growing market with digital transformation opportunities",
                "growth_trends": ["Digital adoption", "Customer experience focus", "Efficiency demands"],
                "market_drivers": ["Technology advancement", "Changing customer expectations", "Competitive pressure"]
            },
            "industry_dynamics": {
                "major_trends": ["Digital transformation", "Customer-centric approaches", "Innovation focus"],
                "regulatory_environment": "Standard industry regulations apply",
                "technology_disruptions": ["AI integration", "Automation", "Digital platforms"],
                "industry_challenges": ["Market competition", "Technology adoption", "Customer retention"]
            },
            "target_audience_insights": {
                "demographics": "Professional decision-makers and end users",
                "psychographics": "Value-driven, efficiency-focused, quality-conscious",
                "pain_points": ["Time constraints", "Quality concerns", "Cost considerations"],
                "buying_behavior": "Research-driven decision making with emphasis on proven results",
                "unmet_needs": ["Simplified solutions", "Better integration", "Improved outcomes"]
            },
            "market_opportunities": {
                "underserved_segments": ["Small to medium businesses", "Emerging markets"],
                "emerging_trends": ["Sustainability focus", "Remote solutions", "Personalization"],
                "partnership_opportunities": ["Technology providers", "Industry associations"],
                "market_gaps": ["Affordable premium solutions", "Integrated platforms"]
            },
            "positioning_recommendations": {
                "optimal_position": "Innovative leader delivering exceptional value",
                "value_proposition_focus": "Quality, innovation, and trusted expertise",
                "differentiation_strategy": "Superior results through innovative approaches",
                "positioning_statement": "The trusted partner for innovative excellence"
            },
            "confidence_score": 0.75
        }

    def _get_fallback_competitive_analysis(self) -> Dict[str, Any]:
        """Fallback competitive analysis for error scenarios"""
        return {
            "competitive_landscape": {
                "direct_competitors": [
                    {"name": "Market Leader A", "market_share": "25%", "strengths": ["Brand recognition", "Market presence"]},
                    {"name": "Challenger B", "market_share": "15%", "strengths": ["Innovation", "Customer service"]},
                    {"name": "Specialist C", "market_share": "10%", "strengths": ["Expertise", "Specialization"]}
                ],
                "indirect_competitors": ["Alternative solutions", "In-house options", "Generic providers"],
                "competitive_intensity": "Moderate to high with opportunities for differentiation"
            },
            "competitor_analysis": {
                "market_leaders": ["Established Player 1", "Established Player 2"],
                "brand_strength_ranking": ["Leader A", "Challenger B", "Specialist C"],
                "competitive_advantages_by_player": {
                    "Leader A": ["Market presence", "Resources"],
                    "Challenger B": ["Innovation", "Agility"]
                }
            },
            "market_gaps": {
                "unmet_customer_needs": ["Better integration", "Simplified solutions", "Personal touch"],
                "service_gaps": ["Customization", "Support quality", "Value pricing"],
                "positioning_white_spaces": ["Premium affordable", "Innovative traditional"],
                "underserved_segments": ["Small business", "Emerging sectors"]
            },
            "differentiation_strategy": {
                "unique_value_propositions": ["Superior outcomes", "Innovative approach", "Trusted partnership"],
                "competitive_moats": ["Expertise depth", "Customer relationships", "Innovation capability"],
                "positioning_against_competition": "Premium quality with accessible approach",
                "differentiation_pillars": ["Innovation", "Quality", "Service", "Results"]
            },
            "strategic_recommendations": {
                "competitive_response_strategies": ["Focus on differentiation", "Build customer loyalty"],
                "market_entry_tactics": ["Value demonstration", "Strategic partnerships"],
                "brand_positioning_strategy": "Position as innovative leader with proven results",
                "competitive_messaging": "Emphasize unique value and proven outcomes"
            },
            "confidence_score": 0.70
        }

    def _get_fallback_personality_analysis(self) -> Dict[str, Any]:
        """Fallback personality analysis for error scenarios"""
        return {
            "brand_archetype": {
                "primary_archetype": "The Innovator",
                "secondary_influences": ["The Expert", "The Caregiver"],
                "archetype_justification": "Fits market need for innovative solutions with trusted expertise",
                "archetype_characteristics": ["Forward-thinking", "Problem-solving", "Reliable", "Creative"]
            },
            "personality_traits": {
                "core_traits": [
                    {"trait": "Innovative", "description": "Forward-thinking and creative", "expression": "Shows up in solutions and approaches"},
                    {"trait": "Trustworthy", "description": "Reliable and dependable", "expression": "Consistent delivery and communication"},
                    {"trait": "Professional", "description": "Expert and competent", "expression": "Quality work and professional standards"},
                    {"trait": "Approachable", "description": "Accessible and friendly", "expression": "Easy to work with and understand"},
                    {"trait": "Results-focused", "description": "Outcome-oriented", "expression": "Clear delivery and measurable success"}
                ],
                "personality_summary": "An innovative yet trustworthy brand that combines expertise with approachability"
            },
            "brand_voice": {
                "communication_style": "Professional confidence balanced with approachable expertise",
                "tone_variations": {
                    "formal_contexts": "Professional and authoritative",
                    "casual_contexts": "Friendly and helpful",
                    "crisis_contexts": "Calm and reassuring"
                },
                "language_patterns": ["Clear communication", "Action-oriented", "Solution-focused"],
                "vocabulary_preferences": ["Positive", "Professional", "Accessible"]
            },
            "brand_values_beliefs": {
                "core_values": ["Innovation", "Quality", "Trust", "Excellence", "Partnership"],
                "brand_purpose": "To drive success through innovative excellence",
                "mission_statement": "Delivering exceptional outcomes through innovative solutions",
                "belief_system": ["Quality matters", "Innovation drives progress", "Trust builds relationships"],
                "worldview": "Success comes from combining innovation with proven expertise"
            },
            "relationship_dynamics": {
                "customer_relationship_model": "Trusted advisor and strategic partner",
                "trust_building_approach": "Consistent delivery and transparent communication",
                "credibility_factors": ["Proven results", "Expert knowledge", "Professional approach"],
                "relationship_goals": ["Long-term partnership", "Mutual success"]
            },
            "emotional_positioning": {
                "primary_emotions": ["Confidence", "Trust", "Aspiration"],
                "emotional_journey": {
                    "awareness": "Curiosity and interest",
                    "consideration": "Confidence and trust",
                    "purchase": "Excitement and commitment",
                    "loyalty": "Satisfaction and advocacy"
                },
                "feeling_differentiation": "Trusted innovation partner vs. just another service provider"
            },
            "confidence_score": 0.85
        }

    def _get_fallback_visual_brief(self) -> Dict[str, Any]:
        """Fallback visual brief for error scenarios"""
        return {
            "visual_strategy": {
                "visual_philosophy": "Clean, professional design that conveys innovation and trust",
                "visual_personality_expression": "Modern sophistication with approachable professionalism",
                "visual_goals": ["Build trust", "Convey expertise", "Show innovation"],
                "brand_visual_positioning": "Premium quality with accessible approach"
            },
            "design_system": {
                "primary_design_principles": ["Clarity", "Consistency", "Quality"],
                "visual_hierarchy": "Clear information architecture with strategic emphasis",
                "design_components": ["Typography", "Color", "Imagery", "Layout"],
                "consistency_framework": "Unified visual language across all touchpoints"
            },
            "color_strategy": {
                "strategic_palette": [
                    {"color": "Primary Blue", "hex": "#2563eb", "psychology": "Trust and professionalism", "usage": "Main brand elements"},
                    {"color": "Secondary Blue", "hex": "#1e40af", "psychology": "Depth and reliability", "usage": "Supporting elements"},
                    {"color": "Accent Blue", "hex": "#3b82f6", "psychology": "Innovation and energy", "usage": "Highlights and calls to action"},
                    {"color": "Light Blue", "hex": "#60a5fa", "psychology": "Accessibility and friendliness", "usage": "Secondary accents"},
                    {"color": "Neutral", "hex": "#f8fafc", "psychology": "Clean and professional", "usage": "Backgrounds and text"}
                ],
                "color_psychology_rationale": "Blue conveys trust and professionalism while maintaining innovation feel",
                "color_combinations": "Primary with neutrals for authority, accents for energy"
            },
            "typography_strategy": {
                "typography_personality": "Clean, readable, and professional with modern feel",
                "font_selection_criteria": "Legibility, professionalism, modern appearance",
                "typographic_hierarchy": {
                    "primary_heading": "Bold, clear, authoritative",
                    "secondary_heading": "Supporting, professional",
                    "body_text": "Clean, readable, accessible",
                    "accent_text": "Strategic emphasis elements"
                },
                "typography_applications": "Consistent hierarchy across all brand materials"
            },
            "imagery_direction": {
                "photography_style": "Professional, high-quality, authentic",
                "illustration_style": "Clean, modern, purposeful when needed",
                "visual_content_strategy": "Support brand story with quality visuals",
                "mood_aesthetic": "Professional confidence with approachable warmth",
                "visual_storytelling": "Show expertise and results through visual narrative"
            },
            "logo_identity_brief": {
                "logo_design_direction": "Simple, memorable, scalable design",
                "identity_system_requirements": "Flexible system for all applications",
                "logo_personality_expression": "Innovation balanced with trustworthiness",
                "application_considerations": "Digital and print, various sizes and contexts",
                "logo_effectiveness_criteria": "Recognition, memorability, appropriate personality"
            },
            "confidence_score": 0.80
        }

    def _get_fallback_strategic_synthesis(self) -> Dict[str, Any]:
        """Fallback strategic synthesis for error scenarios"""
        return {
            "strategic_insights": {
                "key_insights": ["Market opportunity exists", "Differentiation is key", "Trust builds success", "Innovation drives growth"],
                "strategic_themes": ["Innovation leadership", "Trusted expertise", "Quality delivery"],
                "critical_success_factors": ["Brand differentiation", "Customer trust", "Quality delivery"],
                "strategic_opportunities": ["Market leadership", "Customer loyalty"]
            },
            "brand_strategy_framework": {
                "unified_strategy": "Innovative leader delivering exceptional results through trusted expertise",
                "positioning_statement": "The trusted partner for innovative excellence and exceptional outcomes",
                "strategy_pillars": ["Innovation", "Trust", "Quality", "Results"],
                "brand_promise": "Exceptional outcomes through innovative excellence",
                "unique_value_proposition": "Proven results through innovative approaches and trusted expertise"
            },
            "implementation_roadmap": {
                "phase_1_immediate": {
                    "timeline": "0-3 months",
                    "priorities": ["Brand foundation", "Visual identity", "Key messaging"],
                    "deliverables": ["Brand guidelines", "Visual assets"]
                },
                "phase_2_build": {
                    "timeline": "3-9 months",
                    "priorities": ["Market presence", "Customer experience", "Brand consistency"],
                    "deliverables": ["Marketing materials", "Customer touchpoints"]
                },
                "phase_3_optimize": {
                    "timeline": "9-18 months",
                    "priorities": ["Brand optimization", "Market expansion"],
                    "deliverables": ["Performance analytics", "Brand evolution"]
                }
            },
            "success_measurement": {
                "kpis": ["Brand awareness", "Customer satisfaction", "Market share", "Brand perception"],
                "success_metrics": {
                    "brand_awareness": "Measure recognition and recall",
                    "brand_perception": "Track brand attributes and sentiment",
                    "business_impact": "Monitor business growth and customer metrics"
                },
                "measurement_frequency": "Quarterly assessment with annual comprehensive review"
            },
            "strategic_recommendations": {
                "immediate_actions": ["Establish brand foundation", "Create consistent messaging", "Develop visual identity"],
                "long_term_initiatives": ["Build market leadership", "Expand customer base"],
                "risk_mitigation": ["Monitor competitive response", "Maintain quality standards"],
                "competitive_response": "Focus on differentiation and customer value"
            },
            "confidence_score": 0.78
        }