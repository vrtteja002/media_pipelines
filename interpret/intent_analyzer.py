import json
from typing import Dict, Any
from openai import OpenAI
from config import Config

class IntentAnalyzer:
    """
    REQUIREMENT: Infer intent and parameters from text
    Uses GPT-4o to analyze intent and extract parameters
    """
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        print("✅ Intent Analysis: IntentAnalyzer initialized")
    
    def analyze_intent(self, text: str) -> Dict[str, Any]:
        """Analyze intent and extract parameters from text"""
        try:
            print(f"🧠 Analyzing intent for: '{text[:30]}...'")
            
            prompt = f"""
            You are an expert Natural Language Understanding (NLU) system. Analyze the user's input comprehensively and extract actionable insights.

            **ANALYSIS FRAMEWORK:**
            
            1. **INTENT CLASSIFICATION** - Determine the primary action/goal:
               - information_request (seeking data/facts)
               - task_execution (wanting something done)
               - conversation (social/casual interaction)
               - problem_solving (need help with issue)
               - transaction (buying/selling/booking)
               - navigation (finding/going somewhere)
               - configuration (settings/preferences)
               - complaint (expressing dissatisfaction)
               - compliment (expressing satisfaction)
               - emergency (urgent assistance needed)

            2. **ENTITY EXTRACTION** - Identify key components:
               - Named entities (people, places, organizations)
               - Temporal expressions (dates, times, durations)
               - Numerical values (quantities, measurements, prices)
               - Products/services mentioned
               - Actions/verbs indicating desired operations

            3. **PARAMETER MAPPING** - Extract actionable parameters:
               - Required parameters (must-have for intent fulfillment)
               - Optional parameters (enhance the experience)
               - Context parameters (background information)

            4. **SENTIMENT & URGENCY ANALYSIS**:
               - Sentiment: positive/negative/neutral/mixed
               - Urgency: low/medium/high/critical
               - Emotion indicators: frustrated/excited/confused/satisfied

            5. **CONFIDENCE ASSESSMENT**:
               - high: Intent is clear and unambiguous
               - medium: Intent is likely but has some uncertainty
               - low: Multiple possible interpretations exist

            6. **SPOKEN RESPONSE OPTIMIZATION**:
               - Use natural, conversational language
               - Include contractions (I'll, you'll, can't, won't)
               - Add natural pauses with commas
               - Avoid complex punctuation or symbols
               - Use spoken language patterns and flow
               - Keep sentences moderate length for natural speech rhythm
               - Include empathetic and friendly tone markers

            **USER INPUT:** "{text}"

            **RESPONSE FORMAT (Valid JSON only):**
            {{
                "intent": "primary_intent_category",
                "intent_description": "Natural language description of what user wants",
                "entities": {{
                    "named_entities": ["person", "place", "organization"],
                    "temporal": ["date", "time", "duration"],
                    "numerical": ["quantity", "price", "measurement"],
                    "products_services": ["item1", "item2"],
                    "actions": ["verb1", "verb2"]
                }},
                "parameters": {{
                    "required": {{"param1": "value1"}},
                    "optional": {{"param2": "value2"}},
                    "context": {{"background_info": "value3"}}
                }},
                "sentiment": "positive/negative/neutral/mixed",
                "urgency": "low/medium/high/critical",
                "confidence": "high/medium/low",
                "confidence_reasoning": "Why this confidence level",
                "suggested_response": "Natural, spoken-friendly response optimized for TTS (conversational, with contractions, natural flow)",
                "next_steps": ["action1", "action2", "action3"],
                "category": "broad_classification",
                "subcategory": "specific_classification",
                "requires_clarification": false,
                "clarification_questions": ["question1", "question2"],
                "extracted_keywords": ["keyword1", "keyword2", "keyword3"]
            }}

            **EXAMPLES:**

            Input: "Book me a flight to Paris next Friday"
            Output: {{
                "intent": "transaction",
                "intent_description": "User wants to book airline travel",
                "entities": {{
                    "named_entities": ["Paris"],
                    "temporal": ["next Friday"],
                    "numerical": [],
                    "products_services": ["flight"],
                    "actions": ["book"]
                }},
                "parameters": {{
                    "required": {{"destination": "Paris", "travel_date": "next Friday", "service_type": "flight"}},
                    "optional": {{}},
                    "context": {{}}
                }},
                "sentiment": "neutral",
                "urgency": "medium",
                "confidence": "high",
                "confidence_reasoning": "Clear intent with specific destination and timeframe",
                "suggested_response": "I'd love to help you book a flight to Paris for next Friday! To find you the best options, I'll just need to know which city you're flying from, and what time of day works best for you.",
                "next_steps": ["collect_departure_location", "get_time_preferences", "search_flights", "present_options"],
                "category": "travel",
                "subcategory": "flight_booking",
                "requires_clarification": true,
                "clarification_questions": ["What city will you be departing from?", "Do you have a preferred departure time?"],
                "extracted_keywords": ["book", "flight", "Paris", "Friday", "travel"]
            }}

            Input: "I'm frustrated with this slow service"
            Output: {{
                "intent": "complaint",
                "intent_description": "User is expressing dissatisfaction with service quality",
                "entities": {{
                    "named_entities": [],
                    "temporal": [],
                    "numerical": [],
                    "products_services": ["service"],
                    "actions": []
                }},
                "parameters": {{
                    "required": {{"issue_type": "slow_service"}},
                    "optional": {{}},
                    "context": {{"emotion": "frustrated"}}
                }},
                "sentiment": "negative",
                "urgency": "medium",
                "confidence": "high",
                "confidence_reasoning": "Clear expression of dissatisfaction with specific issue mentioned",
                "suggested_response": "I totally understand your frustration with the slow service, and I'm really sorry you're experiencing this. Let me help you get this sorted out right away.",
                "next_steps": ["acknowledge_frustration", "gather_details", "escalate_if_needed", "provide_solution"],
                "category": "customer_service",
                "subcategory": "service_complaint",
                "requires_clarification": true,
                "clarification_questions": ["Can you tell me more about which specific service is running slowly?", "How long have you been experiencing this issue?"],
                "extracted_keywords": ["frustrated", "slow", "service", "complaint"]
            }}

            Input: "What's the weather like today?"
            Output: {{
                "intent": "information_request",
                "intent_description": "User wants current weather information",
                "entities": {{
                    "named_entities": [],
                    "temporal": ["today"],
                    "numerical": [],
                    "products_services": ["weather"],
                    "actions": ["check", "get"]
                }},
                "parameters": {{
                    "required": {{"time_frame": "today", "info_type": "weather"}},
                    "optional": {{"location": "current_location"}},
                    "context": {{}}
                }},
                "sentiment": "neutral",
                "urgency": "low",
                "confidence": "high",
                "confidence_reasoning": "Simple, direct request for weather information",
                "suggested_response": "I'll check today's weather for you right now! Just to make sure I get the right forecast, are you looking for the weather where you are currently, or somewhere else?",
                "next_steps": ["get_location", "fetch_weather_data", "provide_forecast"],
                "category": "information",
                "subcategory": "weather_inquiry",
                "requires_clarification": true,
                "clarification_questions": ["What location should I check the weather for?"],
                "extracted_keywords": ["weather", "today", "check"]
            }}

            **IMPORTANT GUIDELINES:**
            - Always return valid JSON
            - Be specific but not overly granular
            - Consider context and implied meaning
            - Prioritize user experience in suggested responses
            - Extract all relevant information, even if not explicitly stated
            - Handle ambiguity gracefully with appropriate confidence levels
            
            **SPOKEN RESPONSE REQUIREMENTS:**
            - Write responses that sound natural when spoken aloud
            - Use contractions: "I'll" not "I will", "you're" not "you are"
            - Include natural conversation markers: "Great!", "Absolutely!", "Of course!"
            - Add empathetic phrases: "I understand", "That makes sense", "I hear you"
            - Use moderate sentence length (10-20 words) for natural speech flow
            - Include strategic pauses with commas for TTS rhythm
            - Avoid symbols, brackets, or complex punctuation
            - Use friendly, helpful tone that translates well to voice
            - End with clear next steps or questions that invite response
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert NLU system. Always respond with valid JSON that follows the exact schema provided. Be thorough, accurate, and user-focused."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,  # Lower temperature for more consistent responses
                max_tokens=1500   # Ensure enough tokens for detailed analysis
            )
            
            # Parse JSON response
            try:
                analysis = json.loads(response.choices[0].message.content)
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                analysis = {
                    "intent": "general_request",
                    "intent_description": "Unable to parse specific intent",
                    "entities": {
                        "named_entities": [],
                        "temporal": [],
                        "numerical": [],
                        "products_services": [text],
                        "actions": []
                    },
                    "parameters": {
                        "required": {"original_text": text},
                        "optional": {},
                        "context": {}
                    },
                    "sentiment": "neutral",
                    "urgency": "low",
                    "confidence": "low",
                    "confidence_reasoning": "JSON parsing failed, using fallback analysis",
                    "suggested_response": f"I heard you say: {text}. Could you help me understand what you'd like me to help you with?",
                    "next_steps": ["request_clarification", "provide_general_help"],
                    "category": "general",
                    "subcategory": "unclear_request",
                    "requires_clarification": True,
                    "clarification_questions": ["Could you please rephrase your request?", "What specific help do you need?"],
                    "extracted_keywords": text.split()[:5]
                }
            
            result = {
                "status": "success",
                "original_text": text,
                "analysis": analysis,
                "metadata": {
                    "model": "gpt-4o",
                    "processor": "intent_analyzer",
                    "step": "2_intent_analysis",
                    "prompt_version": "v2.0_enhanced"
                }
            }
            
            intent_desc = analysis.get('intent_description', analysis.get('intent', 'unknown'))
            print(f"✅ Intent detected: {intent_desc}")
            return result
            
        except Exception as e:
            print(f"❌ Intent analysis failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "original_text": text,
                "analysis": {
                    "intent": "error",
                    "intent_description": "System error occurred during analysis",
                    "entities": {
                        "named_entities": [],
                        "temporal": [],
                        "numerical": [],
                        "products_services": [],
                        "actions": []
                    },
                    "parameters": {
                        "required": {},
                        "optional": {},
                        "context": {"error": str(e)}
                    },
                    "sentiment": "neutral",
                    "urgency": "low",
                    "confidence": "low",
                    "confidence_reasoning": "Analysis failed due to system error",
                    "suggested_response": "Sorry about that! I ran into a technical issue processing your request. Could you try asking me again?",
                    "next_steps": ["retry_request", "contact_support"],
                    "category": "system_error",
                    "subcategory": "processing_error",
                    "requires_clarification": False,
                    "clarification_questions": [],
                    "extracted_keywords": []
                },
                "metadata": {
                    "model": "gpt-4o", 
                    "processor": "intent_analyzer", 
                    "step": "2_intent_analysis",
                    "prompt_version": "v2.0_enhanced"
                }
            }