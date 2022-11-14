class Account:

    amount = 0
    def __init__(self):
        pass

    def deposit(self):
        self.amount = self.amount + input('''Please enter the amount you would like to deposit: \n''')
        return 'Your current amount is: '+ str(self.amount)

    def withdraw(self):
        withdraw_amount = input('''Please enter the amount you would like to withdraw: \n''')
        if withdraw_amount >= self.amount:
            self.amount = self.amount - withdraw_amount
        else:
            return "You can't withdraw that much money because you don't have it."
        return 'Your current amount is: ' + str(self.amount)

    def get_amount(self):
        return 'Your current amount is: ' + str(self.amount)

class BasicAccount(Account):

    acc_name = 'BasicPremiumAccount'

    def __init__(self, amount):
        self.amount = amount

    def calculate_yearly_gains(self):
        if self.amount < 100000:
            return 'Your yearly gains are: ' + str(self.amount * 0.02)
        else:
            return "Your yearly gains are: " + str(2000 + ((self.amount - 100000) * 0.01))

    def get_acc_name(self):
        return self.acc_name


class PremiumAccount(Account):

    acc_name = 'PremiumAccount'

    def __init__(self, amount):
        self.amount = amount

    def calculate_yearly_gains(self):
        if self.amount < 50000:
            return 'Your yearly gains are: ' + str(self.amount * 0.01)
        elif self.amount < 100000:
            return "Your yearly gains are: " + str(1000 + ((self.amount - 50000) * 0.03))
        else:
            return "Your yearly gains are: " + str(1000 + 1500 + ((self.amount - 100000) * 0.02))

    def get_acc_name(self):
        return self.acc_name

class UltraSuperPremiumAccount(Account):

    acc_name = 'UltraSuperPremiumAccount'
    def __init__(self, amount):
        self.amount = amount

    def calculate_yearly_gains(self):
        if self.amount < 1000000:
            return 'Your yearly gains are: ' + str(self.amount * 0.06)
        else:
            return "Your yearly gains are: " + str(60000 + ((self.amount - 1000000) * 0.02))

    def get_acc_name(self):
        return self.acc_name

class AccountConsumer:
    def __init__(self):
        pass

    def projected_gains(self, acc_name, acc_balance):
        acc = acc_name(acc_balance)    # hoping acc_name is a correct class name
        return acc.calculate_yearly_gains()

# b1 = AccountConsumer()

# print(b1.projected_gains(PremiumAccount, 300))

test1 = 30000
test2 = 140000
test3 = 420000
test4 = 690000
test5 = 3000000

tests = [test1, test2, test3, test4, test5]
types_of_accounts = [BasicAccount, PremiumAccount, UltraSuperPremiumAccount]

obj = AccountConsumer()

for test in tests:
    max_yearly_gain = 0
    max_test_acc = ''
    for toa in types_of_accounts:
        gains_msg = obj.projected_gains(toa, test)
        l = gains_msg.split(':')     # getting the number from messagge
        yearly_gains = l[1]

        if yearly_gains > max_yearly_gain:
            max_yearly_gain = yearly_gains
            obj2 = toa(0)
            max_test_acc = obj2.get_acc_name()

    print(' For ' + str(test) + ' amount of money, the ' + str(max_test_acc) + ' type of account is more worth it.')
