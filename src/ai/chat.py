import json
from openai import OpenAI
from ..utils.config import get_config
from .context_extractor import ContextExtractor
from ..data.diary_entry import DiaryEntry
from ..data.user_profile import UserProfile
import logging
import datetime

logging.basicConfig(level=logging.INFO)

class ChatBot:
    def __init__(self, user_data_folder):
        config = get_config()
        self.client = OpenAI(api_key=config['openai_api_key'])
        self.model = config['openai_gpt_model']
        self.conversation_history = []
        self.context_extractor = ContextExtractor()
        self.diary_entry = DiaryEntry(user_data_folder)
        self.user_profile = UserProfile(user_data_folder)
        self.user_context = self.load_user_context()

    def load_user_context(self):
        logging.info("Loading user context")
        contexts = {}
        for period in ['day', 'week', 'month', 'year']:
            if self.user_profile.context_needs_update(period):
                entries = self.diary_entry.get_entries_for_period(period)
                if entries:
                    context = self.context_extractor.extract_context(entries, period, contexts)
                    if context:
                        self.user_profile.store_context(context, period)
                        contexts[period] = context
                else:
                    logging.info(f"No entries found for period: {period}")
            else:
                context = self.user_profile.get_latest_context(period)
                if context:
                    contexts[period] = context
                    logging.info(f"Using cached context for period: {period}")
                else:
                    logging.info(f"No cached context found for period: {period}")
        
        return self.combine_contexts(contexts)

    def combine_contexts(self, contexts):
        combined_context = "User Context:\n"
        for period, context in contexts.items():
            combined_context += f"{period.capitalize()}: {context}\n\n"
        return combined_context.strip()

    def get_response(self, user_input):
        self.conversation_history.append({"role": "user", "content": user_input})
        logging.info(f"User input: {user_input}")
        
        # Get today's entries
        today = datetime.datetime.now().date()
        today_entries = self.diary_entry.get_entries_for_period('day')
        
        # Separate the latest entry from previous entries
        latest_entry = today_entries[0] if today_entries else None
        previous_entries = today_entries[1:] if len(today_entries) > 1 else []
        
        # Prepare context with focus on the latest entry
        focused_context = f"Latest entry: {latest_entry['content'] if latest_entry else 'No entry for today yet.'}\n\n"
        if previous_entries:
            focused_context += f"Summary of previous entries today: {self.context_extractor.extract_context(previous_entries, 'day', {})}\n\n"
        focused_context += self.user_context
        logging.info(f"User context: {focused_context}")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": focused_context},
                    {"role": "user", "content": "Please focus primarily on responding to my latest entry, while considering the context of previous entries and user information."},
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
                "new_user_info": [],
                "error": str(e)
            }

    def clear_conversation(self):
        self.conversation_history = []

    def get_conversation_summary(self):
        return self.conversation_history

    def refresh_user_context(self):
        self.user_context = self.load_user_context()