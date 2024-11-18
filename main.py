class bankAccount():
    def __init__(self, accountHolder, startingBalance = 0.0):
        self.accountHolder = accountHolder
        self.balance = startingBalance
    
    def __str__(self):
        return f"Account owned by {self.accountHolder} with ${self.balance} in it"
    
    def accountInfo(self):
        return str(self)
    
    def deposit(self, depositAmount):
        """
        Deposits an amount of money into a bank account
        depositAmount: Amount of money to be deposited. Must be at least $10, or it returns an error
        """
        if(depositAmount >= 10):
            self.balance += depositAmount
        else:
            print(f"Deposited amount must be at least $10 (tried to deposit ${depositAmount})")
    
    def withdraw(self, withdrawlAmount):
        """
        Withdrawls an amount of money from a bank account
        withdrawlAmount: Amount of money to be withdrawn. Must be between $0 and the account balance, or it returns an error
        """
        if(0 <= withdrawlAmount <= self.balance):
            self.balance -= withdrawlAmount
        else:
            print(f"Withdrawn amount bust be between $0 and the account balance (currently ${self.balance}, tried to withdraw ${withdrawlAmount})")

colin_account = bankAccount("Colin", 5000)
print(colin_account.accountInfo())

#No error
colin_account.deposit(40)
colin_account.withdraw(30)
#Creates error
colin_account.deposit(5)
colin_account.deposit(-30)
colin_account.withdraw(10000)
colin_account.withdraw(-50)