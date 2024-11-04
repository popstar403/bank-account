class bankAccount():
    def __init__(self, accountHolder, startingBalance = 0.0):
        self.accountHolder = accountHolder
        self.balance = startingBalance
    
    def __str__(self):
        return f"Account owned by {self.accountHolder} with ${self.balance} in it"
    
    def accountInfo(self):
        return str(self)

guestArf_account = bankAccount("Guest Arf","1234567890")
print(guestArf_account.accountInfo())
