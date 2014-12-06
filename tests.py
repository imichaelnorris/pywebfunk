import unittest
from main import *

class TestCss(unittest.TestCase):
    def testSingle(self):
        expected = '''p {
    text-align: center;
}'''
        c = css("p", text_align="center")
        self.assertEqual(c,expected)

if __name__ == '__main__':
    unittest.main()
