def some_function(*args):
    if type(args[0])== list:
        print(args[0][1])

def some_function2(*args,**kwargs):
    print("ARGS", args)
    print("KWARGS", kwargs)
    print("Type:", type(kwargs))
    b=kwargs
    for i in b:
        if type(b[i])==dict:
            print(b[i])


    

#test1=some_function2(1,2,3,a=1,b=2,c=3,d=4,e=5)
#test2=some_function2(a=["one","two"],b=123)

#test3=some_function2(a={"key": "val", "hello": 55, "Penis":10})
a = [51,27,13,56]         #given list
d={x:i for i,x in enumerate(a)}
print(d)

