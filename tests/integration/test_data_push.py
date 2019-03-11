import unittest
from blackhole_data_gathering.data_push import DataPusher


class TestDataPush(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.data_dir = 'data/'
        self.subdir = 'test/'
        self.dir = self.data_dir + self.subdir
        self.data_pusher = DataPusher()

    def test_example(self):
        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()
