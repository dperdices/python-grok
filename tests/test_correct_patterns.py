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

class TestCommonPatterns(unittest.TestCase):
    def subtest_correct_match(self):
        for key, val in correct_examples:
            with self.subTest(msg=f"Checking pattern {key}", key=key, val=val):
                pat = grok.GrokPattern(f"^{key}$")
                self.assertIsNotNone(pat.match(val), f"{key} should match {val}")
    def subtest_incorrect_match(self):
        for key, val in correct_examples:
            with self.subTest(msg=f"Checking pattern {key}", key=key, val=val):
                pat = grok.GrokPattern(f"^{key}$")
                self.assertIsNotNone(pat.match(val), f"{key} should match {val}")


def build_assert_not_none(key, val):
    def tmp(self):
        pat = grok.GrokPattern(f"^{key}$")
        self.assertIsNotNone(pat.match(val), f"{key} should match {val}")
    return tmp

def build_assert_none(key, val):
    def tmp(self):
        pat = grok.GrokPattern(f"^{key}$")
        self.assertIsNone(pat.match(val), f"{key} should not match {val}")
    return tmp

counter = {}

for key, val in correct_examples:
    if key not in counter:
        counter[key] = 0
    counter[key] += 1
    
    setattr(TestCommonPatterns, f"test_correct_match_{key}_{counter[key]}", build_assert_not_none(key, val))

counter = {}
for key, val in incorrect_examples:
    if key not in counter:
        counter[key] = 0
    counter[key] += 1
    setattr(TestCommonPatterns, f"test_incorrect_match_{key}_{counter[key]}", build_assert_none(key, val))

    
if __name__ == '__main__':
    unittest.main()