# 什么是代理模式
# 1.代理英文名　proxy，经常出现在网络中，比如代理服务器,同时也出现在现实生活中
# 比如　代理机构　代理人,
# 主要的特点是 只代理一方，区别于中介者模式(或者mvc中的control)
# 那么代理的意义是什么？
# 一般来说用户要找代理是因为雇主或者主体无法简单处理某件事情，而需要一个专业人或者
# 专业做某事的代理机构来间接处理这些事情，因此在程序方面，也是这样子的，也就是
# 专门做一些非常特殊的事情或者消耗非常大的操作的时候
# 1.特殊的事情（保护／防护代理）
# 判断是否拥有访问敏感信息的权限（安全问题）
# 2.异步处理（远程代理）
# 比如在访问网络资源uri的时候，本身访问其他网络地址的数据是一个比较耗时的操作，
# 往往应用中用代理方式处理uri，而又不能影响现有应用当前的正常运行．在web中这种
# 操作经常是以异步处理的方式进行的
# ３．延时加载占用资源比较大的对象（虚拟代理）
# 应用本身需要轻量级的，毕竟越轻松用户用起来就越流畅，越开心对吧，只有在进行特殊
# 情况下，才会调用耗资源较大的情况，此时就是事先加载的是个假的虚拟的不存在的对象
# 只有达到某个条件的情况下才会出现
# ４．其他的，当然代理模式可以根据作用或者职责分了其他类型，但是归根到底，代码
# 都是类似的，只是在这套代码的一些地方更改一下，就分割了以上不同类型的代理

# 核心代理结构
# ＃＃＃＃＃＃＃＃＃＃＃＃＃＃保护私有信息　＃＃＃＃＃＃＃＃＃＃＃
class SensitiveInfo:
    def __init__(self):
        self.users = ["li1","zhangl2","jin3"]
    def read(self):
        return self.users
    def add(self,user):
        self.users.append(user)
class InfoProxy:
    def __init__(self):
        self.info = SensitiveInfo()
        self.password = "aaaa"
    def read(self):
        return self.info.read()
    def add(self,user):
        password = input("your password")
        self.info.add(user) if password == self.password else print("worry password")
client = InfoProxy()
print(client.read())
client.add("new")
print(client.read())

################## 3.加载未来数据比较大的时候＃＃＃＃＃＃＃＃＃＃＃＃＃＃
class LazyProperty:
    def __init__(self,method):
        self.method = method
        self.methodname = method.__name__

    def __get__(self,obj,objtype):
        if not obj:
            return None
        print("赋值给素组对象")
        value = self.method(obj)
        # 在第一次调用的时候会给宿主实例对象添加一个__dict__对象，
        #　在非数据描述符级别上，调用__dict__优先于非数据描述符的__get__方法
        #1.这个是赋值给宿主对象的，只有在宿主实例对象上才能看到
        setattr(obj,self.methodname,value)
        #２.这个是赋值给宿主类的，只有也就是所以类上都有数据
        # setattr(objtype,self.methodname,value)
        return value

class Rect:
    def __init__(self):
        self.x = 100
        self.y = 200
        self._source = None# 此时数据比较大
    @LazyProperty
    def source(self):
        self._source = tuple(range(50))
        return self._source
if __name__ == "__main__":
    # LazyProperty("1")
    rect = Rect()
    print(rect.source)
    print(rect.source)
    rect2 = Rect()
    print(rect2.source)
    # print(Rect.__dict__)