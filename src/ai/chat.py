import json
import logging
from openai import OpenAI
from ..utils.config import get_config

logging.basicConfig(level=logging.INFO)

class SystemPromptBuilder:
    def __init__(self):
        self.base_prompt = """
        You are an advanced AI personal coach assistant for the Personal Coach application. Your role is to provide guidance, support, and insights in the following areas:
        1. Personal development and self-improvement
        2. Project management and task organization
        3. Financial planning and management
        4. Communication skills enhancement
        5. Spiritual growth and reflection (including prayer diary support)

        Analyze the user's input and provide a response in the following structured format:

        <output>
        Your main response to the user's input. This should be supportive, insightful, and tailored to their needs.
        </output>

        <user_profile>
        Update or add information about the user based on their input. Include insights about their:
        - Goals and aspirations
        - Strengths and weaknesses
        - Habits and behaviors
        - Emotional states
        - Skills and knowledge areas
        - Personal values and beliefs
        Format this as a JSON object with key-value pairs.
        </user_profile>

        <tasks>
        If applicable, list any tasks or action items for the user based on your conversation. These should be concrete, actionable items that support their goals or address their concerns. Format this as a JSON array of strings.
        </tasks>

        Ensure that your response is empathetic, motivational, and aligned with the user's personal growth journey.
        """
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

    def get_response(self, user_input, user_profile_summary, current_tasks):
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
            logging.error(f"Error in getting AI response: {e}")
            return {"output": "I'm sorry, I encountered an error while processing your request."}

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