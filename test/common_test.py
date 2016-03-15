import base_test
import unittest
import getpass
from qmyf import common

class TestCommon(base_test.BaseTest):
    def test_get_password(self):
        test_password = getpass.getpass("test password: ")
        common.cache_password(test_password)
        password = common.get_password()
        common.clear_password_cache()
        self.assertEqual(test_password, password)

    def test_pretty_print_column_names(self):
        data = self.get_mock_data_from_relative_path('mock/connect_mock.json')
        transactions = data['transactions']
        columns = common.pretty_print_column_names(transactions)
        self.assertIn('category', columns)
        self.assertIn('score.detail.city', columns)
        self.assertIn('category_id', columns)
        self.assertIn('_account', columns)
        self.assertIn('name', columns)
        self.assertIn('score.detail.address', columns)
        self.assertIn('meta.location.coordinates.lon', columns)
        self.assertIn('meta.location.state', columns)
        self.assertIn('type.primary', columns)
        self.assertIn('meta.location.address', columns)
        self.assertIn('amount', columns)
        self.assertIn('meta.location.city', columns)
        self.assertIn('date', columns)
        self.assertIn('meta.location.coordinates.lat', columns)
        self.assertIn('score.detail.state', columns)
        self.assertIn('_id', columns)
        self.assertIn('score.master', columns)
        self.assertIn('pending', columns)
        self.assertIn('score.detail.name', columns)

    def test_pretty_print_rows(self):
        data = self.get_mock_data_from_relative_path('mock/connect_mock.json')
        transactions = data['transactions']
        rows = common.pretty_print_rows(transactions)
        self.assertIn('YzzrzBrO9OSzo6BXwAvVuL5dmMKMqkhOoEqeo', rows)
        self.assertIn('Morimoto', rows)

if __name__ == '__main__':
    unittest.main()
