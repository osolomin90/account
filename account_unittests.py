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

    def test_try_to_read_file_from_incorrect_path(self):
        assert Transactions().read_transactions("absent.txt")._transactions.__len__() == 0

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
            f.write("01-03-2017 Deposit $-1000.00\n")
            f.write("01-02-2017 Deposit $150.55\n")
            f.write("01-02-2017 Deposit $-2150.55")
        assert "-1000" and "01-03-2017" in Transactions().read_transactions(self.__test_file)\
                   .get_first_transaction_with_negative_balance()

    def test_if_get_total_balance_is_none_when_transaction_format_is_incorrect(self):
        with self.file as f:
            f.write("01-03-2019")
        assert Transactions().read_transactions(self.__test_file) \
            .get_total_balance() is None

    def test_if_get_transactions_size_is_none_when_transaction_format_is_incorrect(self):
        with self.file as f:
            f.write("")
        assert Transactions().read_transactions(self.__test_file) \
            .get_transactions_size() is None

    def test_if_get_first_transaction_with_negative_balance_is_none_when_transaction_format_is_incorrect(self):
        with self.file as f:
            f.write("$-4000.00\n")
        assert Transactions().read_transactions(self.__test_file) \
            .get_first_transaction_with_negative_balance() is None

    def tearDown(self):
        os.remove(self.__test_file)

if __name__ == '__main__':
    unittest.main()
