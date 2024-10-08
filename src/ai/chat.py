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
                    "description": "Provide a coaching response with main output, user profile insights, and tasks",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "output": {
                                "type": "string",
                                "description": "Main response to the user's input"
                            },
                            "user_profile": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Insights about the user's profile"
                            },
                            "tasks": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of tasks or action items for the user"
                            }
                        },
                        "required": ["output", "user_profile", "tasks"]
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