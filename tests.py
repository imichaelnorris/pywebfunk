import unittest
from wgui import *

class TestCss(unittest.TestCase):
    def testSingle(self):
        expected = '''p {
    text-align: center;
}'''
        c = css("p", text_align="center")
        self.assertEqual(c.__str__(),expected)

    def testDiv(self):
        expected='''<div>
<button></button>
</div>'''
        b = Button()
        div = Div(b)
        self.assertEqual(expected, div.__str__())

    def testForm(self):
        expected = '''<form method="post" onclick="action()">
<input type="text" name="fname">\n<br>
<input type="text" name="lname">\n<br>
</form>'''
        
        b1 = Text("",Input(type="text", name="fname"), Text("<br>"))
        b2 = Text("",Input(type="text", name="lname"), Text("<br>"))
        form = Form(b1, b2, method="post", onclick="action()")

        self.assertEqual(expected, form.__str__())

    def testText(self):
        text = Text("hello", Button(name="sally"))
        expected = 'hello<button name="sally"></button>'
        self.assertEqual(text.__str__(), expected)

if __name__ == '__main__':
    unittest.main()
