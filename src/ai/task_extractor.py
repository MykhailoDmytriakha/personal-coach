from openai import OpenAI
from ..utils.config import get_config
import json

class TaskExtractor:
    def __init__(self):
        config = get_config()
        self.client = OpenAI(api_key=config['openai_api_key'])
        self.model = config['openai_gpt_model_small']

    def extract_tasks(self, text):
        """
        Extract tasks from the given text using AI with a specified output format.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": """You are a task extraction assistant. Identify and list tasks or todo items from the given text.
                    Output the tasks in the following JSON format:
                    {"tasks": ["task1", "task2", "task3"]}
                    If no tasks are found, return an empty list: {"tasks": []}"""},
                    {"role": "user", "content": f"Extract tasks from this text: {text}"}
                ],
                temperature=0.3,
                max_tokens=150,
                n=1,
            )
            tasks_json = response.choices[0].message.content.strip()
            return self._parse_tasks(tasks_json)
        except Exception as e:
            print(f"Error in extracting tasks: {e}")
            return []

    def _parse_tasks(self, tasks_json):
        """
        Parse the JSON response to extract individual tasks.
        """
        try:
            tasks_data = json.loads(tasks_json)
            return tasks_data.get("tasks", [])
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return []

    def print_extracted_tasks(self, text):
        """
        Извлекает задачи из текста и печатает их для отладки.
        """
        print("Извлеченные задачи:")
        tasks = self.extract_tasks(text)
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}")