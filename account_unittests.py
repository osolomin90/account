import unittest
import os
from account import Transactions


class AccountUnittests(unittest.TestCase):

    __test_file = "test.txt"

    def setUp(self):
         self.file = open(self.__test_file, "w")

    def test_read_transactions_from_transactions_txt(self):
        with self.file as f:
            f.write("01-02-2017 Deposit $4000.00")
        assert Transactions().read_transactions(self.__test_file)._transactions.__len__() > 0,\
            "File is empty or system can not read 'transaction.txt'"

    def test_is_transaction_count_correct(self):
        with self.file as f:
            f.write("01-02-2017 Deposit $4000.00\n")
            f.write("01-02-2017 Deposit $-1000.00")
        assert Transactions().read_transactions(self.__test_file).get_transactions_size() == 2

    def test_total_balance(self):
        with self.file as f:
            f.write("01-02-2017 Deposit $4000.00\n")
            f.write("01-02-2017 Deposit $-1000.00\n")
            f.write("01-02-2017 Deposit $150.55")
        assert Transactions().read_transactions(self.__test_file).get_total_balance() == 3150.55

    def test_first_transaction_with_negative_balance(self):
        with self.file as f:
            f.write("01-02-2017 Deposit $4000.00\n")
            f.write("01-02-2017 Deposit $-1000.00\n")
            f.write("01-02-2017 Deposit $150.55\n")
            f.write("01-02-2017 Deposit $-2150.55")
        assert "-1000" and "01-02-2017" in Transactions().read_transactions(self.__test_file)\
                   .get_first_transaction_with_negative_balance()

    def test_if_transaction_format_incorrect(self):
        with self.file as f:
            f.write("$-4000.00\n")
        assert Transactions().read_transactions(self.__test_file) \
            .get_first_transaction_with_negative_balance() is None

    def tearDown(self):
        os.remove(self.__test_file)

if __name__ == '__main__':
    unittest.main()
