import unittest
from account import Transactions


class AccountUnittests(unittest.TestCase):

    def setUp(self):
        pass

    def test_read_transactions_from_transactions_txt(self):
        assert Transactions().read_transactions('transactions.txt').transactions.__len__() > 0

if __name__ == '__main__':
    unittest.main()
