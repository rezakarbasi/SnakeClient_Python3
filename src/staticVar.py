class Test(object):

    _i = 3

    @property
    def i(self):
        return type(self)._i

    @i.setter
    def i(self, val):
        type(self)._i = val


a = Test()
b = Test()

print(a.i)
a.i=7
print(b.i)
