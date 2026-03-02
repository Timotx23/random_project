def some_function(*args):
    if type(args[0])== list:
        print(args[0][1])

def some_function2(*args,**kwargs):
    print("Type:", type(kwargs))
    for i in kwargs:
        if type(kwargs[i]) == list:
            print(kwargs[i][0])
        if type(kwargs[i])==dict:
            print(kwargs[i].values())


    

test1=some_function2(1,2,3,a=1,b=2,c=3,d=4,e=5)
test2=some_function2(a=["one","two"],b=123)
test3=some_function2(a={"key": "val"})




