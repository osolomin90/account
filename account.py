class Transactions:

    def __init__(self):
        self.transactions = []

    def read_transactions(self, txt_file='transactions.txt'):
        for t in open(txt_file):
            self.transactions.append(t)
        return self

    def get_transactions_size(self):
        return self.transactions.__len__()

    def get_total_balance(self):
        total = 0
        for t in self.transactions:
            total += float(t.split('$')[1].rstrip())
        return total

    def get_first_transaction_with_negative_balance(self):
        for t in self.transactions:
            if '-' in t.split('$')[1].rstrip():
                return t


if __name__ == '__main__':
    transactions = Transactions().read_transactions()
    print "Total:", transactions.get_transactions_size()
    print "Total of balance:", transactions.get_total_balance()
    print "First transaction with negative balance: ", transactions.get_first_transaction_with_negative_balance()