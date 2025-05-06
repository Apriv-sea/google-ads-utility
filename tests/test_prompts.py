import unittest
from utils.prompts import get_title_prompt

class TestPrompts(unittest.TestCase):
    def test_title_prompt_contains_inputs(self):
        result = get_title_prompt("global", "camp", "ag", "kw1,kw2")
        self.assertIn("global", result)
        self.assertIn("camp", result)
        self.assertIn("ag", result)
        self.assertIn("kw1,kw2", result)

if __name__ == "__main__":
    unittest.main()
