from openai import OpenAI
from ..utils.config import get_config

class ChatBot:
    def __init__(self):
        config = get_config()
        self.client = OpenAI(api_key=config['openai_api_key'])
        self.model = config['openai_gpt_model']
        self.conversation_history = []

    def get_response(self, user_input):
        """
        Get AI response for user input.
        """
        self.conversation_history.append({"role": "user", "content": user_input})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful personal coach assistant."},
                    *self.conversation_history
                ],
                temperature=0.7,
                max_tokens=150,
                n=1,
            )
            ai_response = response.choices[0].message.content.strip()
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            return ai_response
        except Exception as e:
            print(f"Error in getting AI response: {e}")
            return "I'm sorry, I encountered an error while processing your request."

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