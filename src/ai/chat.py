import json
from openai import OpenAI
from ..utils.config import get_config
import logging

logging.basicConfig(level=logging.INFO)

class ChatBot:
    def __init__(self):
        config = get_config()
        self.client = OpenAI(api_key=config['openai_api_key'])
        self.model = config['openai_gpt_model']
        self.conversation_history = []

    def get_response(self, user_input):
        self.conversation_history.append({"role": "user", "content": user_input})
        logging.info(f"User input: {user_input}")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an AI personal coach assistant. Provide guidance and support for personal development, project management, financial planning, communication skills, and spiritual growth."},
                    *self.conversation_history
                ],
                functions=[{
                    "name": "provide_coaching_response",
                    "description": "Act as a comprehensive AI personal coach to empower the user's holistic growth and well-being. Provide insightful, empathetic, and actionable guidance across various life domains including personal development, professional growth, emotional well-being, physical health, spiritual growth, financial management, and interpersonal relationships. Analyze the user's input, current profile, and historical data to offer tailored advice, set meaningful goals, suggest practical tasks, and track progress. Your role is to inspire, motivate, and support the user in realizing their full potential and achieving a balanced, fulfilling life.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "output": {
                                "type": "string",
                                "description": "Main response to the user, including personalized advice, encouragement, and reflections based on their input and overall context."
                            },
                            "user_profile": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Insights about the user's personality, behaviors, strengths, challenges, and growth areas, derived from the conversation and historical data."
                            },
                            "tasks": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Actionable and meaningful tasks or goals for the user, designed to promote growth and progress in relevant areas of their life."
                            },
                            "user_info": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Array of strings containing factual information about the user. This may include, but is not limited to, personal details, physical characteristics, lifestyle information, and any other relevant objective facts about the user gathered from the conversation."
                            }
                        },
                        "required": ["output", "user_profile", "tasks", "user_info"]
                    }
                }],
                function_call={"name": "provide_coaching_response"}
            )
            
            function_call = response.choices[0].message.function_call
            
            if function_call and function_call.name == "provide_coaching_response":
                parsed_response = json.loads(function_call.arguments)
                logging.info(f"Parsed response:\n{json.dumps(parsed_response, indent=2, ensure_ascii=False)}")
                return parsed_response
            else:
                raise ValueError("Unexpected response format from OpenAI API")
        
        except Exception as e:
            logging.error(f"Unexpected error in getting AI response: {e}")
            return {
                "output": "I apologize, but I've encountered an unexpected issue. Let's try that again.",
                "user_profile": [],
                "tasks": [],
                "error": str(e)
            }

    def clear_conversation(self):
        self.conversation_history = []

    def get_conversation_summary(self):
        return self.conversation_history