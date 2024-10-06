import unittest
import json
from src.ai.chat import ResponseParser

class TestResponseParser(unittest.TestCase):
    def test_parse_with_all_tags(self):
        response = """
        <output>Your main response to the user's input.</output>
        <user_profile>{"goals": "improve fitness", "strengths": "discipline"}</user_profile>
        <tasks>["Go for a run", "Join a gym"]</tasks>
        """
        expected_output = {
            "output": "Your main response to the user's input.",
            "user_profile": {
                "goals": "improve fitness",
                "strengths": "discipline"
            },
            "tasks": ["Go for a run", "Join a gym"]
        }
        parsed_response = ResponseParser.parse(response)
        self.assertEqual(parsed_response, expected_output)

    def test_parse_with_missing_tags(self):
        response = """
        <output>Your main response to the user's input.</output>
        <tasks>["Go for a run", "Join a gym"]</tasks>
        """
        expected_output = {
            "output": "Your main response to the user's input.",
            "tasks": ["Go for a run", "Join a gym"]
        }
        parsed_response = ResponseParser.parse(response)
        self.assertEqual(parsed_response, expected_output)

    def test_parse_with_no_tags(self):
        response = "No tags here."
        expected_output = {}
        parsed_response = ResponseParser.parse(response)
        self.assertEqual(parsed_response, expected_output)

if __name__ == '__main__':
    unittest.main()