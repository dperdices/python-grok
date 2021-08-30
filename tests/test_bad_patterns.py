import unittest
import sys, os, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

import grok

correct_examples = [
    ("%{NUMBER}", "1"),
    ("%{NUMBER}", "-1"),
    ("%{NUMBER}", "1.0"),
    ("%{NUMBER}", "-2.0"),
    ("%{NUMBER}", "+2.0"),
    ("%{NUMBER}", "11"),
    ("%{NUMBER}", "-11"),
    ("%{NUMBER}", "11.0"),
    ("%{NUMBER}", "-22.0"),
    ("%{NUMBER}", "+22.0")
]

incorrect_examples = [
    ("%{NUMBER}", "1,0"),
    ("%{NUMBER}", "2-2"),
    ("%{NUMBER}", "asdpoasdk"),
    ("%{NUMBER}", "*2"),
]

class TestMalformedPatterns(unittest.TestCase):
    def test_not_closed_grok(self):
        val = "%{NUMBER"
        pat = grok.GrokPattern("%{NUMBER")
        self.assertEqual(pat.regex.pattern, val, "An unclosed Grok expression is a literal")

    def test_not_existing_grok(self):
        with self.assertRaises(ValueError):
            pat = grok.GrokPattern("%{sdjasdlkajdas}")

if __name__ == '__main__':
    unittest.main()