import unittest
import json
from parser import Parser
import test_literals
import test_statements

parser = Parser()

class Test(unittest.TestCase):

    def test_literals(self):
        for test in test_literals.tests:
            result = parser.parse(test[0])
            self.assertEqual(
                json.dumps(result),
                json.dumps(test[1])
            )
    
    def test_statements(self):
        for test in test_statements.tests:
            result = parser.parse(test[0])
            self.assertEqual(
                json.dumps(result),
                json.dumps(test[1])
            )

if __name__ == "__main__":
    unittest.main()
