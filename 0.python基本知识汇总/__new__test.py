# python中的 我们知道一般初始化一个实例,必然会走__init__ 方法
#　其实在　__init__ 方法之前还有一步要走,就是__new__方法
# 官方说明 https://docs.python.org/3.3/reference/datamodel.html?highlight=__new__#object.__new__
# object.__new__(cls[, ...])
# Called to create a new instance of class cls. __new__() is a static method (special-cased so you need not declare it as such) that takes the class of which an instance was requested as its first argument. The remaining arguments are those passed to the object constructor expression (the call to the class). The return value of __new__() should be the new object instance (usually an instance of cls).
# Typical implementations create a new instance of the class by invoking the superclass’s __new__() method using super(currentclass, cls).__new__(cls[, ...]) with appropriate arguments and then modifying the newly-created instance as necessary before returning it.
# If __new__() returns an instance of cls, then the new instance’s __init__() method will be invoked like __init__(self[, ...]), where self is the new instance and the remaining arguments are the same as were passed to __new__().
# If __new__() does not return an instance of cls, then the new instance’s __init__() method will not be invoked.
# __new__() is intended mainly to allow subclasses of immutable types (like int, str, or tuple) to customize instance creation. It is also commonly overridden in custom metaclasses in order to customize class creation.

class Test(object):
    def __new__(cls,a):###1. 默认cls是本类(Test)
        print("cls:",cls) 
        print("a:",a)
        # cls.__init__(cls,a)
        # cls.name = a
    
        return object.__new__(cls) #一旦调用某个实例就会调用该实例的__init__方法,

    def __init__(self,a):
        print("self",self,"a:",a)
        self.name = a
print("teststst")
Test("a")
print("teststst")
class Foo(object):
    def __new__(cls,*args,**kwargs):
        obj = object.__new__(cls,*args,**kwargs)
        #这里的object.__new__(cls,*args,**kwargs)等价于
        # super(Foo,cls).__new__(cls,*args,**kwargs)
        # object.__new__(Foo,*args,**kwargs)
        # Bar.__new__(cls,*args,**kwargs)
        # Student.__new__(cls,*args,**kwargs),即使Student和
        # Foo没有关系也是允许的，因为Student是由object派生的新类
        # 在任何新式类中，不能调用自身的__new__来创建实例，因为这会
        # 造成死循环，所以要避免出现这样的语法 Foo.__new__(cls,*args,**kwargs)
        # 或者 cls.__new__(cls,*args,**kwargs)
        print("Calling __new__ for %s"% obj.__class__)
        return obj

class Bar(Foo):
    def __new__(cls,*args,**kwargs):
        obj = object.__new__(cls,*args,**kwargs)
        print("Calling __new__ for %s"% obj.__class__)
        return obj
    def __init__(self):
        print("Bar...")

class Student(object):
    #Student没有__new__方法，那么会自动调用父类的__new__方法来
    #创建实例，即会自动调用object.__new__(cls)
    pass

class Car(object):
    def __new__(cls,*args,**kwargs):
        obj = object.__new__(Bar,*args,**kwargs)
        print("Calling __new__ for %s"% obj.__class__)
        return obj
    def __init__(self):
        print("Car..")


# 从这里可以看出 __new__方法是静态方法,B.__new__
class B:
    def __new__(cls):
        cls.name = "ccc"
        return object.__new__(cls)
    def __init__(self):
        print("a")
        self.name = "B"
    def say(self):
        print("bbbb")
class A:
    def __new__(cls):
        return B.__new__(B)# 调用B中的实例方法
    def __init__(self):
        print("aaas")
        self.name = "a"
    def __call__(self,*args):
        print(args)
    def say(self):
        print("aaaaaa")
def main():
    # test = Test("bb")
    # print(test.name)
    foo = Foo()
    bar = Bar()
    car = Car()
    print("##########") 
    a = A()# 因为A中的new方法返回的是B实例
    a.say() # 只能调用B实例的方法bbbbb

if __name__ == '__main__':
    main()