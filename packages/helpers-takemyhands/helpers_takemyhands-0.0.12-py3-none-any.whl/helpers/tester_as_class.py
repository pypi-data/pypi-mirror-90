class Tester:
    
    def __init__(self, *args, **kwargs):
        print(args, kwargs)
        # self.user = kwargs["user"]
    
    def test(self):
        print(f"Hello~!")

t = Tester("user", user="user")
t.test()
