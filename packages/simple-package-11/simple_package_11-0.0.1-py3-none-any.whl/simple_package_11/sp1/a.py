def func_a():
    print("Hello I am calling from function a")




from ..sp2.b import func_b

def func_a1():
    func_b()
