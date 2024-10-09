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
        self.user_context = self.load_user_context()

    def load_user_context(self):
       return "Mikhail, a Russian-speaking software developer working on the 'Personal Coach' project. Provide guidance and support for personal development, project management, financial planning, communication skills, and spiritual growth. Remember that Mikhail is a devout Christian with a family (wife Natasha, children Lisa, Naomi, and Daniel) and is actively involved in his church community. He values productivity, technology, and balancing professional responsibilities with personal growth. Tailor your advice to include both technical aspects of his work and spiritual components of his life. Be prepared to discuss software development concepts, AI integration, and religious topics. Use a mix of Russian and English terms as appropriate, reflecting Mikhail's bilingual nature. Your goal is to help Mikhail improve in all areas of his life while respecting his faith and family commitments."


    def get_response(self, user_input):
        self.conversation_history.append({"role": "user", "content": user_input})
        logging.info(f"User input: {user_input}")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.user_context},
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
                                "description": "New insights about the user's personality, behaviors, strengths, challenges, and growth areas, derived from the current conversation."
                            },
                            "tasks": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Actionable and meaningful tasks or goals for the user, designed to promote growth and progress in relevant areas of their life."
                            },
                            "new_user_info": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Array of strings containing new factual information about the user gathered from the current conversation, excluding information already present in the context."
                            }
                        },
                        "required": ["output", "user_profile", "tasks", "new_user_info"]
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