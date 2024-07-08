

class Interface:
    def __init__(self):
        print("Interface Call")
        self.name = "Ahn"
        self.a.append(100)
        self.b += 1

    @classmethod
    def MethodFunc(cls):
        print("MerhodFunc Call")

    a = []
    b = 0






Test = Interface()
Test.a.append(1)
Test.b += 1000


Test2 = Interface()
Test2.a.append(2)


print(Test2.a)
print(Test.b)
print(Test2.b)


print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")