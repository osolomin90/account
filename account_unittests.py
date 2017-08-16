import unittest
import os
import StringIO
from account import AccountTransactions
from ddt import ddt, data


@ddt
class AccountUnittests(unittest.TestCase):

    __test_file = "test.txt"

    def setUp(self):
         self.file = open(self.__test_file, "w")

    """This test verify if function 'read_transaction' get transactions from txt file and put their to the list."""
    def test_read_transactions_from_transactions_txt(self):
        with self.file as f:
            f.write("01-02-2017 Deposit $4000.00")
        assert AccountTransactions().read_transactions(self.__test_file)._transactions.__len__() > 0,\
            "File is empty or system can not read 'transaction.txt'"

    """This test verify if function 'read_transaction' raise correct error when path to txt file is wrong."""
    def test_try_to_read_file_from_incorrect_path(self):
        try:
            AccountTransactions().read_transactions("absent.txt")
            assert False
        except OSError as e:
            assert "No such file or directory: 'absent.txt'" in str(e)

    """This test verify if function 'read_transaction' raise correct error when txt file is empty."""
    def test_if_txt_file_empty(self):
        try:
            AccountTransactions().read_transactions(self.__test_file)
            assert False
        except ValueError as e:
            assert "transaction.txt is empty." in str(e)

    """This test verify if function 'get_transactions_size' return correct transactions size."""
    def test_is_transaction_count_correct(self):
        with self.file as f:
            f.write("01-02-2017 Deposit $4000.00\n")
            f.write("01-02-2017 Deposit $-1000.00")
        assert AccountTransactions().read_transactions(self.__test_file).get_transactions_size() == 2

    """This test verify if function 'get_total_balance' return correct total balance."""
    @data({"test data": ("4000.00", "-1000.00", "150.55"), "expected result": 3150.55},
          {"test data": ("4000.00", "-4000.00"), "expected result": 00.00},
           {"test data": ("4000.00", "-5300.00"), "expected result": -1300.00},
          {"test data": ("4000.00", "5300.00"), "expected result": 9300.00})
    def test_total_balance(self, dic):
        with self.file as f:
            for i in dic["test data"]:
                f.write("01-02-2017 Deposit $"+i+"\n")
        assert AccountTransactions().read_transactions(self.__test_file).get_total_balance() == dic["expected result"]

    """This test verify if 'get_total_balance' return correct error when format of transaction is wrong."""
    def test_if_total_balance_work_with_invalid_format(self):
        with self.file as f:
            f.write("01-02-2017 Deposit $4000.00\n")
            f.write("01-02-2017 Deposit $-1000.00\n")
            f.write("01-02-2017 Deposit 150.55")
        try:
            AccountTransactions().read_transactions(self.__test_file).get_total_balance()
            assert False
        except ValueError as e:
            assert str(e).__eq__("Transaction format is incorrect for line: '01-02-2017 Deposit 150.55'")

    """This test verify if function 'get_first_transaction_with_negative_balance' return date and balance from
     firs transaction with negative balance."""
    def test_first_transaction_with_negative_balance(self):
        with self.file as f:
            f.write("01-02-2017 Deposit $4000.00\n")
            f.write("01-03-2017 Deposit $-1000.00\n")
            f.write("01-02-2017 Deposit $150.55\n")
            f.write("01-02-2017 Deposit $-2150.55")
        assert "-1000" and "01-03-2017" in AccountTransactions().read_transactions(self.__test_file)\
                   .get_first_transaction_with_negative_balance()

    """This test verify if function 'read_transactions' returns correct error."""
    @data("test", "Deposit $4000.00", "$4000.00", "01-02-2017 $-2150.55", "01-02-2017 Deposit 150.55")
    def test_if_read_transactions_returns_correct_error(self, value):
        with self.file as f:
            f.write(value)
        try:
            AccountTransactions().read_transactions(self.__test_file)
            assert False
        except ValueError as e:
            assert str(e).__eq__("Transaction format is incorrect for line: '"+value+"'")

    """This test verify if function 'get_total_balance' returns None"""
    @data("test", "Deposit $4000.00", "$4000.00", "01-02-2017 $-2150.55", "01-02-2017 Deposit 150.55")
    def test_if_get_total_balance_is_none_when_transaction_format_is_incorrect(self, value):
        with self.file as f:
            f.write(value)
            accountTransactions = AccountTransactions()
        try:
            accountTransactions.read_transactions(self.__test_file)
        except ValueError:
            pass
        assert accountTransactions.get_total_balance() is None

    """This test verify if function 'get_transactions_size' returns None."""
    @data("test", "Deposit $4000.00", "$4000.00", "01-02-2017 $-2150.55", "01-02-2017 Deposit 150.55")
    def test_if_get_transactions_size_is_none_when_transaction_format_is_incorrect(self, value):
        with self.file as f:
            f.write(value)
        accountTransactions = AccountTransactions()
        try:
            accountTransactions.read_transactions(self.__test_file)
        except ValueError:
            pass
        assert accountTransactions.get_transactions_size() is None

    """This test verify if function 'get_first_transaction_with_negative_balance' returns None."""
    @data("test", "Deposit $4000.00", "$4000.00", "01-02-2017 $-2150.55", "01-02-2017 Deposit 150.55")
    def test_if_get_first_transaction_with_negative_balance_is_none_when_transaction_format_is_incorrect(self, value):
        with self.file as f:
            f.write(value)
        accountTransactions = AccountTransactions()
        try:
            accountTransactions.read_transactions(self.__test_file)
        except ValueError:
            pass
        assert accountTransactions.get_first_transaction_with_negative_balance() is None

    def tearDown(self):
        os.remove(self.__test_file)

if __name__ == '__main__':
    unittest.main()
