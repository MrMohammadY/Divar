class Singleton(type):
    _instance = None

    def __call__(self, *args, **kwargs):
        if self._instance:
            self._instance = super().__call__(*args, **kwargs)
        return self._instance


class Db(metaclass=Singleton):
    pass


d1 = Db()
d2 = Db()

print(id(d1))
print(id(d2))
