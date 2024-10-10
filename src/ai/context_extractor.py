import logging
from openai import OpenAI
from ..utils.config import get_config

class ContextExtractor:
    def __init__(self):
        config = get_config()
        self.client = OpenAI(api_key=config['openai_api_key'])
        self.model = config['openai_gpt_model']

    def extract_context(self, entries, period, previous_contexts):
        if not entries:
            logging.info(f"No entries to extract context for period: {period}")
            return None

        logging.info(f"Extracting context for period: {period}")
        
        # Prepare the prompt based on the period and previous contexts
        prompt = self._prepare_prompt(period, previous_contexts)
        
        # Prepare the entries text
        entries_text = "\n\n".join([f"{entry['timestamp']}: {entry['content']}" for entry in entries])
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": f"Here are the diary entries for the {period}:\n\n{entries_text}"}
                ]
            )
            context = response.choices[0].message.content.strip()
            logging.info(f"Successfully extracted context for period: {period}")
            return context
        except Exception as e:
            logging.error(f"Error extracting context for period {period}: {str(e)}")
            return None

    def _prepare_prompt(self, period, previous_contexts):
        base_prompt = "You are an AI assistant tasked with summarizing and extracting key information from a user's diary entries. "
        
        if period == 'day':
            prompt = base_prompt + "Focus on the user's immediate mood, daily activities, and short-term goals. "
        elif period == 'week':
            prompt = base_prompt + "Identify weekly patterns, progress on short-term goals, and highlight any upcoming events or deadlines. "
        elif period == 'month':
            prompt = base_prompt + "Analyze monthly trends, progress on medium-term goals, and identify any recurring themes or challenges. "
        elif period == 'year':
            prompt = base_prompt + "Evaluate progress on long-term goals, personal growth, and highlight major life events and overall changes in the user's life. "
        else:
            prompt = base_prompt + "Provide a general summary of the user's activities and state of mind. "

        prompt += "Ensure your summary doesn't repeat information from previous contexts. "
        
        if previous_contexts:
            prompt += "Here are the previous contexts to avoid repetition:\n"
            for prev_period, prev_context in previous_contexts.items():
                prompt += f"\n{prev_period.capitalize()} context: {prev_context}\n"

        prompt += "\nBased on the diary entries provided, generate a concise and insightful summary that complements the existing information."

        return prompt