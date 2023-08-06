import unittest
from winotify import Notification

toast = Notification("app test", "test title")


class MyTestCase(unittest.TestCase):
    def test_show(self):
        self.
        toast.build().show()


if __name__ == '__main__':
    unittest.main()
