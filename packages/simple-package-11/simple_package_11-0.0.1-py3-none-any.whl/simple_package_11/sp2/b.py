def func_b():
    print("I am a function from module b")



from ..sp1.a import func_a

def func_b1():
    print("Inside b1")
    func_a()
