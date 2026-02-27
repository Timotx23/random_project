mydict = {0 : "Apple", 1 : "Orange"}
x = all(mydict.values())
txt = "Hello Sam!"
mytable = str.maketrans("S", "P", "Mm")

words = ['apple', 'banana', 'cherry', 'date', 'fig']

## Your solution to HW-3.2 goes here:
def beeautify_font_c(text, style1, style2, style3):
    return style1(style2(style3(text)))


###########################
## Your solution to HW-3 goes here:

###########################
def make_underline(func):
    def wrapper():
        return "<u>"+ func() + "</u>"
    return wrapper

def make_bold(func):
    def wrapper():
        return "<b>" + func() + "</b>"
    return wrapper

def make_italic(func):
    def wrapper():
        return "<i>" + func() + "</i>"
    return wrapper

@make_underline
def hello():
    return "Hello, world!"
print(hello()) ## returns "<u>Hello, world!</u>"

@make_bold
def hello():
    return "Hello, world!"
print(hello()) ## returns "<b>Hello, world!</b>"

@make_italic
def hello():
    return "Hello, world!"
print(hello()) ## returns "<i>Hello, world!</i>"

def beeautify_font_c(text):
    def beeautify_inner1(style1):
        def beeautify_inner2(style2):
            def beeautify_inner3(style3):
                 print("Printing style", (style3))
                 return text(style1((style2(style3))))
            return beeautify_inner3
        return beeautify_inner2
    return beeautify_inner1
    


result_hey_there = beeautify_font_c(make_underline)(make_italic)(make_bold)
print(result_hey_there("I love prolog!")) # => <u><i><b>I love prolog!</b></i></u>