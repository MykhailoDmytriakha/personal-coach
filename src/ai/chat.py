import json
import logging
from openai import OpenAI
from ..utils.config import get_config
from .prompts import BASE_PROMPT

logging.basicConfig(level=logging.INFO)

class SystemPromptBuilder:
    def __init__(self):
        self.base_prompt = BASE_PROMPT
        self.user_profile_summary = {}
        self.current_tasks = []
    
    def add_user_profile(self, profile):
        self.user_profile_summary = profile

    def add_current_tasks(self, tasks):
        self.current_tasks = tasks

    def build(self):
        prompt = self.base_prompt

        if self.user_profile_summary:
            prompt += f"\n\nCurrent User Profile:\n{json.dumps(self.user_profile_summary, indent=2)}"

        if self.current_tasks:
            prompt += f"\n\nCurrent User Tasks:\n{json.dumps(self.current_tasks, indent=2)}"

        prompt += "\n\nUse the provided user profile and current tasks to personalize your response and recommendations."

        return prompt

class ResponseParser:
    @staticmethod
    def parse(response):
        parsed = {}
        tags = ['output', 'user_profile', 'tasks']
        
        for tag in tags:
            start_tag = f"<{tag}>"
            end_tag = f"</{tag}>"
            start = response.find(start_tag)
            end = response.find(end_tag)
            
            if start != -1 and end != -1:
                content = response[start + len(start_tag):end].strip()
                if tag in ['user_profile', 'tasks']:
                    try:
                        parsed[tag] = json.loads(content)
                    except json.JSONDecodeError:
                        parsed[tag] = []  # Return an empty list if parsing fails
                else:
                    parsed[tag] = content
        
        return parsed

class ChatBot:
    def __init__(self):
        config = get_config()
        self.client = OpenAI(api_key=config['openai_api_key'])
        self.model = config['openai_gpt_model']
        self.prompt_builder = SystemPromptBuilder()
        self.response_parser = ResponseParser()
        self.conversation_history = []

    def get_response(self, user_input):
        user_profile_summary = None
        current_tasks = None
        self.prompt_builder.add_user_profile(user_profile_summary)
        self.prompt_builder.add_current_tasks(current_tasks)
        system_prompt = self.prompt_builder.build()

        self.conversation_history.append({"role": "user", "content": user_input})
        logging.info(f"User input: {user_input}")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    *self.conversation_history
                ],
                temperature=0.7,
                max_tokens=500,
                n=1,
            )
            ai_response = response.choices[0].message.content.strip()
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            logging.info(f"AI response: \n{ai_response}")
            
            parsed_response = self.response_parser.parse(ai_response)
            logging.info(f"parsed response: {parsed_response}")
            return parsed_response
        except Exception as e:
            logging.error(f"Unexpected error in getting AI response: {e}")
            return {
                "output": "I apologize, but I've encountered an unexpected issue. Let's try that again.",
                "error": str(e)
            }

    def clear_conversation(self):
        """
        Clear the conversation history.
        """
        self.conversation_history = []

    def get_conversation_summary(self):
        """
        Get a summary of the conversation.
        """
        return self.conversation_history