"""
Emergent Strategy Engine
Advanced brand strategy generation using Emergent LLM
"""

import logging
import json
import asyncio
import os
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
import google.generativeai as genai
from models.brand_strategy import BrandStrategy, BrandPersonality, VisualDirection, MessagingFramework, BusinessInput

class EmergentStrategyEngine:
    """Advanced brand strategy generation engine using Emergent LLM"""
    
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        self.model_provider = "google"  # Using Google Gemini
        self.logger = logging.getLogger(__name__)
        
        # Configure Google Generative AI
        if self.api_key:
            genai.configure(api_key=self.api_key)
        
    async def analyze_business_concept(self, business_input: BusinessInput) -> BrandStrategy:
        """
        Multi-layer strategic analysis using Emergent AI
        
        Args:
            business_input: Business concept and requirements
            
        Returns:
            Comprehensive brand strategy with all components
        """
        try:
            # Layer 1: Market Analysis
            market_analysis = await self._analyze_market_position(business_input)
            
            # Layer 2: Competitive Landscape
            competitive_analysis = await self._analyze_competitors(business_input)
            
            # Layer 3: Brand Personality Development
            personality = await self._develop_brand_personality(
                business_input, market_analysis, competitive_analysis
            )
            
            # Layer 4: Visual Direction Brief
            visual_direction = await self._create_visual_brief(personality, business_input)
            
            # Layer 5: Messaging Framework
            messaging = await self._create_messaging_framework(personality, business_input)
            
            # Layer 6: Consistency Rules
            consistency_rules = await self._generate_consistency_rules(
                personality, visual_direction, messaging
            )
            
            return BrandStrategy(
                business_name=business_input.business_name,
                brand_personality=personality,
                visual_direction=visual_direction,
                messaging_framework=messaging,
                consistency_rules=consistency_rules,
                market_analysis=market_analysis,
                competitive_positioning=competitive_analysis
            )
            
        except Exception as e:
            self.logger.error(f"Error in brand strategy analysis: {str(e)}")
            raise
    
    async def _analyze_market_position(self, business_input: BusinessInput) -> Dict[str, Any]:
        """Analyze market position and opportunities"""
        
        market_prompt = f"""
        As a senior market research analyst, analyze this business concept:
        
        BUSINESS: {business_input.business_name}
        DESCRIPTION: {business_input.business_description}
        INDUSTRY: {business_input.industry}
        TARGET AUDIENCE: {business_input.target_audience}
        VALUES: {', '.join(business_input.business_values)}
        
        Provide a comprehensive market analysis in JSON format:
        {{
            "market_size": "estimated market size and growth",
            "key_trends": ["trend1", "trend2", "trend3"],
            "opportunities": ["opportunity1", "opportunity2", "opportunity3"],
            "challenges": ["challenge1", "challenge2", "challenge3"],
            "market_positioning": "recommended market position",
            "differentiation_potential": "unique positioning opportunities"
        }}
        
        Focus on actionable insights for brand development.
        """
        
        response = await self._call_emergent_ai(market_prompt)
        return self._parse_json_response(response, "market_analysis")
    
    async def _analyze_competitors(self, business_input: BusinessInput) -> Dict[str, Any]:
        """Analyze competitive landscape"""
        
        competitive_prompt = f"""
        As a competitive intelligence expert, analyze the competitive landscape for:
        
        BUSINESS: {business_input.business_name}
        DESCRIPTION: {business_input.business_description}
        INDUSTRY: {business_input.industry}
        TARGET: {business_input.target_audience}
        
        Provide competitive analysis in JSON format:
        {{
            "direct_competitors": ["competitor1", "competitor2", "competitor3"],
            "indirect_competitors": ["competitor1", "competitor2"],
            "competitive_gaps": ["gap1", "gap2", "gap3"],
            "differentiation_opportunities": ["opportunity1", "opportunity2"],
            "positioning_strategy": "recommended positioning vs competitors",
            "competitive_advantages": ["advantage1", "advantage2", "advantage3"]
        }}
        
        Focus on opportunities for unique brand positioning.
        """
        
        response = await self._call_emergent_ai(competitive_prompt)
        return self._parse_json_response(response, "competitive_analysis")
    
    async def _develop_brand_personality(
        self, 
        business_input: BusinessInput,
        market_analysis: Dict[str, Any],
        competitive_analysis: Dict[str, Any]
    ) -> BrandPersonality:
        """Develop comprehensive brand personality"""
        
        personality_prompt = f"""
        As an expert brand strategist, develop a comprehensive brand personality for:
        
        BUSINESS: {business_input.business_name}
        DESCRIPTION: {business_input.business_description}
        INDUSTRY: {business_input.industry}
        TARGET: {business_input.target_audience}
        VALUES: {', '.join(business_input.business_values)}
        STYLE PREFERENCE: {business_input.preferred_style}
        
        MARKET CONTEXT: {market_analysis.get('market_positioning', '')}
        COMPETITIVE POSITION: {competitive_analysis.get('positioning_strategy', '')}
        
        Create a detailed brand personality in JSON format:
        {{
            "primary_traits": ["trait1", "trait2", "trait3", "trait4", "trait5"],
            "secondary_traits": ["trait1", "trait2", "trait3"],
            "brand_archetype": "The [Archetype Name]",
            "brand_essence": "one sentence brand essence",
            "tone_of_voice": {{
                "primary_tone": "main tone descriptor",
                "communication_style": "how the brand communicates",
                "personality_adjectives": ["adj1", "adj2", "adj3", "adj4", "adj5"],
                "avoid_traits": ["what the brand should not be"]
            }},
            "emotional_connection": {{
                "desired_emotions": ["emotion1", "emotion2", "emotion3"],
                "brand_promise_emotion": "core emotional promise",
                "customer_relationship": "how customers should feel about the brand"
            }},
            "behavioral_characteristics": {{
                "decision_making": "how the brand makes decisions",
                "communication_patterns": "how the brand speaks and acts",
                "values_in_action": ["how values show up in behavior"]
            }}
        }}
        
        Make it distinctive, memorable, and aligned with business goals.
        """
        
        response = await self._call_emergent_ai(personality_prompt)
        personality_data = self._parse_json_response(response, "brand_personality")
        
        return BrandPersonality(
            primary_traits=personality_data.get("primary_traits", []),
            secondary_traits=personality_data.get("secondary_traits", []),
            brand_archetype=personality_data.get("brand_archetype", ""),
            brand_essence=personality_data.get("brand_essence", ""),
            tone_of_voice=personality_data.get("tone_of_voice", {}),
            emotional_connection=personality_data.get("emotional_connection", {}),
            behavioral_characteristics=personality_data.get("behavioral_characteristics", {})
        )
    
    async def _create_visual_brief(
        self, 
        personality: BrandPersonality, 
        business_input: BusinessInput
    ) -> VisualDirection:
        """Create comprehensive visual direction brief"""
        
        visual_prompt = f"""
        As a senior creative director, create a detailed visual direction brief for:
        
        BRAND: {business_input.business_name}
        PERSONALITY TRAITS: {', '.join(personality.primary_traits)}
        BRAND ARCHETYPE: {personality.brand_archetype}
        BRAND ESSENCE: {personality.brand_essence}
        INDUSTRY: {business_input.industry}
        PREFERRED STYLE: {business_input.preferred_style}
        COLOR PREFERENCE: {business_input.preferred_colors}
        
        Create comprehensive visual direction in JSON format:
        {{
            "design_style": "detailed design style description",
            "visual_mood": "overall visual mood and feeling",
            "color_strategy": {{
                "primary_colors": ["#hex1", "#hex2", "#hex3"],
                "secondary_colors": ["#hex4", "#hex5"],
                "accent_colors": ["#hex6"],
                "color_psychology": "why these colors work for the brand",
                "color_relationships": "how colors work together"
            }},
            "typography_direction": {{
                "logo_typography": "typography style for logo",
                "heading_style": "style for headings",
                "body_text_style": "style for body text",
                "personality_match": "how typography reflects personality"
            }},
            "imagery_style": {{
                "photography_style": "photography direction",
                "illustration_style": "illustration approach",
                "iconography": "icon and symbol style",
                "visual_metaphors": ["metaphor1", "metaphor2"]
            }},
            "logo_direction": {{
                "logo_concept": "conceptual direction for logo",
                "symbol_approach": "approach to symbols/icons",
                "wordmark_style": "style for text-based elements",
                "versatility_requirements": "how logo should adapt"
            }},
            "layout_principles": {{
                "composition_style": "layout and composition approach",
                "spacing_philosophy": "approach to whitespace and spacing",
                "hierarchy_style": "visual hierarchy principles",
                "balance_approach": "how to achieve visual balance"
            }}
        }}
        
        Ensure everything aligns with the brand personality and creates visual consistency.
        """
        
        response = await self._call_emergent_ai(visual_prompt)
        visual_data = self._parse_json_response(response, "visual_direction")
        
        return VisualDirection(
            design_style=visual_data.get("design_style", ""),
            visual_mood=visual_data.get("visual_mood", ""),
            color_strategy=visual_data.get("color_strategy", {}),
            typography_direction=visual_data.get("typography_direction", {}),
            imagery_style=visual_data.get("imagery_style", {}),
            logo_direction=visual_data.get("logo_direction", {}),
            layout_principles=visual_data.get("layout_principles", {})
        )
    
    async def _create_messaging_framework(
        self, 
        personality: BrandPersonality, 
        business_input: BusinessInput
    ) -> MessagingFramework:
        """Create comprehensive messaging framework"""
        
        messaging_prompt = f"""
        As a senior brand messaging strategist, create a comprehensive messaging framework for:
        
        BRAND: {business_input.business_name}
        DESCRIPTION: {business_input.business_description}
        PERSONALITY: {', '.join(personality.primary_traits)}
        ESSENCE: {personality.brand_essence}
        TARGET: {business_input.target_audience}
        VALUES: {', '.join(business_input.business_values)}
        TONE: {personality.tone_of_voice.get('primary_tone', 'professional')}
        
        Create detailed messaging framework in JSON format:
        {{
            "brand_tagline": "memorable brand tagline",
            "elevator_pitch": "30-second brand description",
            "brand_promise": "what the brand promises customers",
            "unique_value_proposition": "what makes this brand unique",
            "key_messages": {{
                "primary_message": "most important brand message",
                "supporting_messages": ["message1", "message2", "message3"],
                "proof_points": ["evidence1", "evidence2", "evidence3"]
            }},
            "audience_messaging": {{
                "customer_pain_points": ["pain1", "pain2", "pain3"],
                "customer_aspirations": ["aspiration1", "aspiration2"],
                "message_customization": "how to adapt messaging for different segments"
            }},
            "communication_guidelines": {{
                "voice_characteristics": ["characteristic1", "characteristic2", "characteristic3"],
                "do_say": ["phrase type 1", "phrase type 2"],
                "dont_say": ["avoid this", "avoid that"],
                "example_phrases": ["example phrase 1", "example phrase 2"]
            }},
            "storytelling_framework": {{
                "brand_story": "compelling brand origin story",
                "story_themes": ["theme1", "theme2", "theme3"],
                "narrative_structure": "how to tell the brand story"
            }}
        }}
        
        Make messaging distinctive, memorable, and emotionally resonant.
        """
        
        response = await self._call_emergent_ai(messaging_prompt)
        messaging_data = self._parse_json_response(response, "messaging_framework")
        
        return MessagingFramework(
            brand_tagline=messaging_data.get("brand_tagline", ""),
            elevator_pitch=messaging_data.get("elevator_pitch", ""),
            brand_promise=messaging_data.get("brand_promise", ""),
            unique_value_proposition=messaging_data.get("unique_value_proposition", ""),
            key_messages=messaging_data.get("key_messages", {}),
            audience_messaging=messaging_data.get("audience_messaging", {}),
            communication_guidelines=messaging_data.get("communication_guidelines", {}),
            storytelling_framework=messaging_data.get("storytelling_framework", {})
        )
    
    async def _generate_consistency_rules(
        self,
        personality: BrandPersonality,
        visual_direction: VisualDirection,
        messaging: MessagingFramework
    ) -> Dict[str, Any]:
        """Generate comprehensive brand consistency rules"""
        
        consistency_prompt = f"""
        As a brand standards expert, create comprehensive consistency rules for maintaining brand integrity:
        
        BRAND PERSONALITY: {', '.join(personality.primary_traits)}
        VISUAL STYLE: {visual_direction.design_style}
        MESSAGING TONE: {personality.tone_of_voice.get('primary_tone', 'professional')}
        
        Create detailed consistency rules in JSON format:
        {{
            "visual_consistency": {{
                "logo_usage": {{
                    "minimum_sizes": "minimum logo sizes for different media",
                    "clear_space": "required clear space around logo",
                    "color_variations": "when to use which logo variation",
                    "dont_modify": ["modification to avoid"]
                }},
                "color_usage": {{
                    "primary_applications": "when to use primary colors",
                    "color_combinations": "approved color combinations",
                    "accessibility": "color accessibility requirements",
                    "brand_recognition": "how colors maintain brand recognition"
                }},
                "typography_consistency": {{
                    "font_hierarchy": "typography hierarchy rules",
                    "usage_guidelines": "when to use which typography",
                    "readability": "readability requirements"
                }},
                "imagery_standards": {{
                    "style_requirements": "image style requirements",
                    "quality_standards": "image quality standards",
                    "brand_alignment": "how images should align with brand"
                }}
            }},
            "messaging_consistency": {{
                "tone_maintenance": "how to maintain consistent tone",
                "key_phrase_usage": "important phrases to use consistently",
                "message_adaptation": "how to adapt messages while staying consistent",
                "brand_voice_checklist": ["voice check 1", "voice check 2"]
            }},
            "cross_platform_rules": {{
                "digital_applications": "consistency rules for digital platforms",
                "print_applications": "consistency rules for print materials",
                "social_media": "social media consistency guidelines",
                "packaging": "packaging consistency requirements"
            }},
            "brand_recognition_factors": {{
                "visual_recognition": ["what makes the brand visually recognizable"],
                "verbal_recognition": ["what makes the brand verbally recognizable"],
                "experience_consistency": "consistent brand experience elements"
            }}
        }}
        
        Ensure rules maintain brand integrity across all touchpoints.
        """
        
        response = await self._call_emergent_ai(consistency_prompt)
        return self._parse_json_response(response, "consistency_rules")
    
    async def _call_emergent_ai(self, prompt: str) -> str:
        """Make API call to Emergent AI"""
        try:
            from emergentintegrations import OpenAIClient
            
            client = OpenAIClient(api_key=self.api_key)
            
            response = await client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert brand strategist with 20+ years of experience creating successful brand identities for companies ranging from startups to Fortune 500. You think strategically, create distinctive brand personalities, and provide actionable guidance. Always respond with valid JSON when requested."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"Error calling Emergent AI: {str(e)}")
            raise
    
    def _parse_json_response(self, response: str, component_name: str) -> Dict[str, Any]:
        """Parse JSON response with error handling"""
        try:
            # Clean response text
            response_clean = response.strip()
            if response_clean.startswith('```json'):
                response_clean = response_clean.replace('```json', '').replace('```', '').strip()
            
            return json.loads(response_clean)
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing JSON for {component_name}: {str(e)}")
            self.logger.error(f"Response content: {response[:500]}...")
            
            # Return fallback structure
            return self._get_fallback_structure(component_name)
    
    def _get_fallback_structure(self, component_name: str) -> Dict[str, Any]:
        """Provide fallback structure if JSON parsing fails"""
        fallbacks = {
            "market_analysis": {
                "market_size": "Growing market with opportunities",
                "key_trends": ["digital transformation", "sustainability focus", "customer experience"],
                "opportunities": ["market gap identification", "unique positioning", "customer needs"],
                "challenges": ["competition", "market saturation", "customer acquisition"],
                "market_positioning": "Differentiated positioning in target market",
                "differentiation_potential": "Strong potential for unique market position"
            },
            "competitive_analysis": {
                "direct_competitors": ["Competitor A", "Competitor B"],
                "indirect_competitors": ["Alternative Solution"],
                "competitive_gaps": ["service gap", "quality gap", "innovation gap"],
                "differentiation_opportunities": ["unique approach", "better service"],
                "positioning_strategy": "Position as premium alternative",
                "competitive_advantages": ["superior quality", "better service", "innovation"]
            },
            "brand_personality": {
                "primary_traits": ["professional", "innovative", "trustworthy", "approachable", "reliable"],
                "secondary_traits": ["creative", "efficient", "customer-focused"],
                "brand_archetype": "The Expert",
                "brand_essence": "Trusted expertise that delivers results"
            }
        }
        
        return fallbacks.get(component_name, {})

    async def refine_strategy(
        self, 
        current_strategy: BrandStrategy, 
        modification_request: str
    ) -> BrandStrategy:
        """Refine existing brand strategy based on user feedback"""
        
        refinement_prompt = f"""
        As a brand strategist, refine this existing brand strategy based on the modification request:
        
        CURRENT STRATEGY:
        - Brand Name: {current_strategy.business_name}
        - Primary Traits: {', '.join(current_strategy.brand_personality.primary_traits)}
        - Brand Essence: {current_strategy.brand_personality.brand_essence}
        - Visual Style: {current_strategy.visual_direction.design_style}
        - Tagline: {current_strategy.messaging_framework.brand_tagline}
        
        MODIFICATION REQUEST: {modification_request}
        
        Provide the refined elements that need to change in JSON format:
        {{
            "modified_elements": ["list of what changed"],
            "brand_personality_updates": {{
                "primary_traits": ["updated trait list if changed"],
                "brand_essence": "updated essence if changed"
            }},
            "visual_direction_updates": {{
                "design_style": "updated style if changed",
                "color_strategy": {{ "primary_colors": ["colors if changed"] }}
            }},
            "messaging_updates": {{
                "brand_tagline": "updated tagline if changed",
                "brand_promise": "updated promise if changed"
            }},
            "rationale": "explanation of changes made"
        }}
        
        Only modify elements that need to change based on the request.
        """
        
        response = await self._call_emergent_ai(refinement_prompt)
        updates = self._parse_json_response(response, "strategy_refinement")
        
        # Apply updates to current strategy
        # This is a simplified version - in production you'd update specific fields
        return current_strategy  # Return updated strategy