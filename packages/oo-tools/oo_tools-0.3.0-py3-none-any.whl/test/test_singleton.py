import unittest

from oo_tools.singleton import Singleton

class TestSingleton(unittest.TestCase):
    def test_singleton_creates_singleton(self):
        class MyClass(Singleton):
            def __init__(self):
                self.value = 1

        c = MyClass()

        b = MyClass()

        c.value = 2
        assert b.value == 2, 'Singleton not created'