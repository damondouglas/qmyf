import unittest
import os, sys, json
currentdir = os.path.abspath(os.path.dirname(__file__))
rootpath = os.path.join(currentdir, '..')
sys.path.append(rootpath)
sys.path.append(os.path.join(rootpath, 'lib'))


class BaseTest(unittest.TestCase):
    def get_mock_data_from_relative_path(self, mock_file_path):
        f = open(os.path.join(currentdir, mock_file_path), 'r')
        data = f.read()
        f.close()
        return json.loads(data)

if __name__ == '__main__':
    unittest.main()
