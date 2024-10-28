class bankAccount():
    def __init__(self, accountHolder, startingBalance = 0.0):
        self.accountHolder = accountHolder
        self.balance = startingBalance
    
    def __str__(self):
        return f"Account owned by {self.accountHolder} with ${self.balance} in it"
    
    def accountInfo(self):
        return str(self)

faruk_account = bankAccount("Faruk",5000)
print(faruk_account.accountInfo())
