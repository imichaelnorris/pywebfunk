class Warnings(object):
    exceptions = True
    accept_unimplemented_validation = True

class Ids(dict):
    def __init__(self):
        dict.__init__(self)

    def add_id_if_unique(self,a,b):
        if a in self:
            if Warnings.exceptions:
                raise Exception("elem with id {} exists! use a unique name".format(a))
            else:
                print "div with id {} exists.  Bad things may happen if you ignore me.".format(a) 
        self[a] = b

class Component(object):
    tag = ''
    '''

    Components that are defined with "close" in their attributes will be written like <property />, instead of normal tags that are <property></property>
    '''
    def __init__(self, **attributes):
        #now I'm starting to feel that every component should be a Container as
        #well and should be __init__(self, *children, **attributes)
        self.attributes = {}
        for i in attributes:
            if attributes[i] != None:
                self.attributes[i] = attributes[i]

        '''
        A new idea I want to try.  An applicator applies a rule on a Component.
        For instance, center(btn) will apply a center rule on that button in css.
        it will apply itself inside a stylesheet or apply that property
        directly to the object.
        '''
        self.applicators = []

    def __str__(self):
        if self.tag != '':
            temp =  "<{}".format(self.tag)
            for i in self.attributes:
                if i not in ['tag', 'close', 'text']:
                    temp = temp + ' {}="{}"'.format(i,self.attributes[i])
            temp = temp + (">" if 'close' in self.attributes else ">")
            if 'close' in self.attributes:
                return temp
            elif 'text' in self.attributes:
                temp = temp + "{}</{}>".format(self.attributes['text'], self.tag)
            else:
                return temp + "</{}>".format(self.tag)
            return temp
        else:
            temp = self.attributes['text'] if 'text' in self.attributes else ''
            if type(temp) != str:
                temp = temp.__str__()

            if type(self) in Container.__subclasses__():
                temp += '\n'.join([i.__str__() for i in self])
            return temp

            
class document(list):
    def __init__(self, *lst):
        list.__init__(self, lst)
        self.ids = Ids()
        for i in lst:
            self.append(i)

    def append(self, x):
        if type(x) in ([Component] + Component.__subclasses__()):
            if 'id' in x.attributes: #stylesheet doesn't have id
                if x.attributes['id'] in self.ids:
                    s = "there's a name collision in the document {}".format(x.attributes['id'])
                    if Warnings.exceptions:
                        raise Exception(s)
                    else:
                        print s
                else:
                    self.ids.add_id_if_unique(x.attributes['id'], x)
        list.append(self, x)

    def write(self):
        return '\n'.join([item.__str__() for item in self])
            
class cssdict(dict):
    '''allows us to validate the properties in a given css rule. this can store them and then validate keys and values to ensure that they are correct.'''
    def __init__(self, d=None):
        for key in d:
            val = d[key] 
            if self.validate(key, val):
                self[key] = val

    def validate(self, key, val):
        if key == 'opacity':
            f = float(val)
            if f >= 0.0 and f <= 1.0:
                return True
            elif Warnings.exceptions:
                raise Exception("Invalid value for {}: {}".format(key,val))
        if Warnings.accept_unimplemented_validation:
            return True
        else:
            return False

class Container(list):
    '''A container contains 0+ elements with a __str__ method'''
    def __init__(self, *x):
        list.__init__(self, x)

    def __str__(self):
        return "\n".join([i.__str__() for i in self])

class css(str):
    #minification -- adjust this
    spaces = ' '*4
    def __init__(self, selector, **properties):
        '''selector applied to and properties where the key's _ is replaced as -'''
        self.selector = selector
        self.properties = cssdict(properties)

    def __new__(self, a, **properties):
        return str.__new__(self, "css obj")

    def __str__(self):
        t = self.selector + " {\n"
        for i in self.properties:
            t += "{0}{1}: {2};\n".format(self.spaces, i.replace('_','-'), self.properties[i])
        return t +'}'

    def __add__(self, other):
        if type(other) == css:
            #merge
            if self.selector == other.selector:
                c = css(self.selector, self.properties)
                c.properties.update(other.properties)
                return c
            #combine
            else:
                return self + '\n\n' + other
        
class Stylesheet(Container, Component):
    tag = "style"
    def __init__(self, *x, **args):
        for i in x:
            if type(i) == css:
                pass
            elif Warnings.exceptions:
                raise Exception("Stylesheet may only contain css")
            else:
                print "warning: stylesheet may only contain css"
        Container.__init__(self, *x)
        Component.__init__(self, **args)

    def __str__(self):
        self.attributes['text'] = "\n" + Container.__str__(self) + "\n"
        return Component.__str__(self)
        
        

class Button(Component):
    tag = "button"

    def __init__(self, **args):
        Component.__init__(self, **args)
        if id == None:
            self.attributes['id'] = "btn" + text.title()

class Div(Container, Component):
    '''NB: Div is a container of components.  self.attributes['text'] is overwritten any time a Div is written out, so watch out for losing a text attribute.  Basically don't set one and add a Text Component to it instead of setting this attribute on the Div'''
    tag = "div"
    def __init__(self, *elements, **attributes):
        Component.__init__(self, **attributes)
        Container.__init__(self, *elements)

    def __str__(self):
        if 'text' not in self.attributes: self.attributes['text'] = ''
        self.attributes['text'] += '\n'+'\n'.join([i.__str__() for i in self])+'\n'
        
        #return super(Div, self).__str__()
        return Component.__str__(self)

class Text(Component, Container):
    def __init__(self, text, *children, **kwargs):
        Container.__init__(self, *children)
        Component.__init__(self, **kwargs)
        self.attributes['text'] = text

class A(Container):
    tag = "a"

class Input(Component):
    def __init__(self, **args):
        Component.__init__(self, **args)
        self.attributes['close'] = True
    tag = "input"

class Img(Component):
    tag = "img"

class Form(Div):
    tag = 'form'

#class Applicator(object):
#    def __init__(self, *x, **args):
#        '''An Applicator applies itself on a list of unnamed objects x, and can be given properties "args" like a Component'''
#        for i in x:
#            if x in Components.__subclasses__():
#                x.applicators.append(

class Center(object):
    def __init__(self, *args, **args2):
        pass
        #raise Exception("error, 1999 called, and they want their website back.\n{}".format('http://html5hub.com/centering-all-the-directions'))
#center = Center

if __name__ == '__main__':
    #Warnings.exceptions = False
    stylesheet = Stylesheet(
        css("button", color='red'),
        css("#div1", background_color='red'),
        css("div", opacity=1.0,
                    text_align='center',
                    width="200px",
                    background_color="yellow",
                    margin_left= "auto",
                    margin_right= "auto")
    )
    doc = document()
    doc.append(stylesheet)
    b = Button(text="submit") 

    btn1 = Button(text="submit2")
    btn2 = Button(text="logout")
    div1 = Div(btn1, btn2, id="div1", name="divName")
    div2 = Div(b, id="div2", name="divName")

    doc.append(div1)
    doc.append(div2)
    print doc.write()
