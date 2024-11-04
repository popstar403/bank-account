class bankAccount():
    def __init__(self, accountHolder, startingBalance = 0.0):
        self.accountHolder = accountHolder
        self.balance = startingBalance
    
    def __str__(self):
        return f"Account owned by {self.accountHolder} with ${self.balance} in it"
    
    def accountInfo(self):
        return str(self)

    def addInterest(self, percentage, isDecimal = False):
        if(isDecimal):
            self.balance *= 1 + (percentage)
        else:
            self.balance *= 1 + (percentage / 100)