import os
import sys


class Transactions:

    def __init__(self):
        self._transactions = []
        self._file_read = False

    def _print_message(self):
        print "Pleas create file 'transactions.txt' in format 'mm-dd-yyyy Type $xx.xx' and try again."

    def read_transactions(self, txt_file='transactions.txt'):
        try:
            if os.stat(txt_file).st_size == 0:
                return self
            for t in open(txt_file):
                if "$" and "-" in str(t) and str(t).split(" ").__len__() == 3:
                    self._transactions.append(t)
                else:
                    return self
            self._file_read = True
        except IOError:
            pass
        finally:
            return self

    def get_transactions_size(self):
        if self._file_read:
            return self._transactions.__len__()

    def get_total_balance(self):
        if self._file_read:
            total = 0
            for t in self._transactions:
                total += float(t.split('$')[1].rstrip())
            return total

    def get_first_transaction_with_negative_balance(self):
        if self._file_read:
                for t in self._transactions:
                    if '-' in t.split(' ')[2].rstrip():
                        return t.split(' ')[0].rstrip()+" "+t.split(' ')[2].rstrip()

if __name__ == '__main__':
    if sys.argv.__len__() > 1:
        transactions = Transactions().read_transactions(str(sys.argv)[1])
    else:
        transactions = Transactions().read_transactions()

    if transactions._file_read:
        print "Total:", transactions.get_transactions_size()
        print "Total of balance:", transactions.get_total_balance()
        print "First transaction with negative balance: ", transactions.get_first_transaction_with_negative_balance()
    else:
        transactions._print_message()