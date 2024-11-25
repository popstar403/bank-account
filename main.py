import base64
import os #Salt generation
import getpass #Hidden password/pin input
import cryptography
from cryptography.fernet import *
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import gc #Garbage collection

class bankAccount():
    reservedNames = ["exit", "Exit", "or exit", "Or exit", "or Exit", "Or Exit"] #Names people can't use

    def __init__(self, accountHolder: str, password, startingBalance = 0.0) -> None:
        if accountHolder in bankAccount.reservedNames:
            raise ValueError(f"Name {accountHolder} in reserved names list")
        self.accountHolder = accountHolder

        self.encryptBalance(password, startingBalance)
    
    def __str__(self) -> str:
        return f"Account owned by {self.accountHolder}"
    
    def accountInfo(self, includeBalance = False, password = None) -> str:
        if includeBalance:
            return str(self) + f" with ${self.decryptBalance(password)} in it"
        else:
            return str(self)
    
    def passwordBytes(self, password) -> bytes:
        return password.encode("utf-8")

    def encryptBalance(self, password, balance) -> None:
        # generates 16 cryptographicaly safe random bytes for salting password/pin
        self.passwordSalt = os.urandom(16)

        # derives key
        kdf = PBKDF2HMAC(
            algorithm = hashes.SHA256(),
            length = 32,
            salt = self.passwordSalt,
            iterations = 480000,
        )

        try:
            encryptedBalance = Fernet(base64.urlsafe_b64encode(kdf.derive(self.passwordBytes(password)))).encrypt(str(balance).encode("utf-8"))
        except Exception as exception:
            print(f"Other exception: {exception}")
        self.encryptedBalance = encryptedBalance
        gc.collect() #garbage collect to rid memory of secrets when possible

    def decryptBalance(self, password) -> float:
        # derives key
        kdf = PBKDF2HMAC(
            algorithm = hashes.SHA256(),
            length = 32,
            salt = self.passwordSalt,
            iterations = 480000,
        )
        returnDecryptedBalance = None
        try:
            returnDecryptedBalance = Fernet(base64.urlsafe_b64encode(kdf.derive(self.passwordBytes(password)))).decrypt(self.encryptedBalance)
            returnDecryptedBalance = float(returnDecryptedBalance)
        except cryptography.fernet.InvalidToken:
            print("Incorrect Pin or Password")
        except Exception as exception:
            print(f"Other Exception: {exception}")
        gc.collect() #garbage collect to rid memory of secrets when possible
        return returnDecryptedBalance
        
    
    def deposit(self, password, depositAmount: float) -> bool:
        """
        Deposits an amount of money into a bank account\n
        password: Password to decrypt bank balance\n
        depositAmount: Amount of money to be deposited. Must be at least $10, or it returns an error\n
        returns: a bool indicating success
        """
        if (depositAmount < 10):
            print(f"Must deposit at least $10 (tried to deposit ${depositAmount})")
            return False
        else:
            tempBalance = self.decryptBalance(password)
            tempBalance += depositAmount
            self.encryptBalance(password, tempBalance)
            del tempBalance
            gc.collect() #garbage collect to rid memory of secrets when possible
            return True

    
    def withdraw(self, password, withdrawlAmount: float) -> bool:
        """
        Withdrawls an amount of money from a bank account\n
        password: Password to decrypt bank balance\n
        withdrawlAmount: Amount of money to be withdrawn. Must be between $0 and the account balance, or it returns an error\n
        returns: a bool indicating success
        """
        if(0 > withdrawlAmount):
            print(f"Can't withdrawl less than $0 (tried to withdrawl ${withdrawlAmount})")
            return False
        else:
            tempBalance = self.decryptBalance(password)
            if(withdrawlAmount > tempBalance):
                del tempBalance
                gc.collect() #garbage collect to rid memory of secrets when possible
                print(f"Can't withdrawl more than what is in the account (tried to withdrawl ${withdrawlAmount})")
                return False
            else:
                tempBalance -= withdrawlAmount
                self.encryptBalance(password, tempBalance)
                del tempBalance
                gc.collect() #garbage collect to rid memory of secrets when possible
                return True

bankAccounts = {
    "alice": bankAccount("alice", "1000"),
    "bob":   bankAccount("bob",   "1001"),
    "john":  bankAccount("john",  "1002"),
    "sam":   bankAccount("sam",   "1003"),
}

users = ["alice", "bob", "john", "sam"]
exitList = ["exit", "Exit", "or exit", "Or exit", "or Exit", "Or Exit"]

while True:
    print("Choose a user, or exit")
    for accountName in bankAccounts:
        print(bankAccounts[accountName].accountHolder)
    print("Or exit")

    inputString = input("Choice: ")

    if inputString in exitList:
        break

    elif inputString in users:
        activeAccount = bankAccounts[inputString]

        while True:
            print(f"What will you do? (account: {activeAccount.accountHolder})",
                  "Deposit",
                  "Withdraw",
                  "Check balance",
                  "Or exit",
                  sep="\n")
            
            inputString = input("Choice: ").lower()

            if inputString in exitList:
                break

            elif inputString == "deposit":
                try:
                    depositAmount = int(input("Deposit amount: "))
                    password = getpass.getpass("Passsword/Pin: ")
                    couldDeposit = activeAccount.deposit(password, depositAmount)
                    if couldDeposit:
                        print("Deposited sucessfully")
                    else:
                        print("Could not deposit")
                except Exception as exception:
                    print(f"Exception: {exception}")
                del password
                del depositAmount
                gc.collect() #garbage collect to rid memory of secrets when possible
            
            elif inputString == "withdraw":
                try:
                    withdrawAmount = int(input("Withdrawl amount: "))
                    password = getpass.getpass("Passsword/Pin: ")
                    couldWithdraw = activeAccount.withdraw(password, withdrawAmount)
                    if couldWithdraw:
                        print("Withdrawn sucessfully")
                    else:
                        print("Could not withdraw")
                except Exception as exception:
                    print(f"Exception: {exception}")
                del password
                del withdrawAmount
                gc.collect() #garbage collect to rid memory of secrets when possible
            
            elif inputString == "check balance":
                try:
                    password = getpass.getpass("Passsword/Pin: ")
                    print(f"Current Balance: ${activeAccount.decryptBalance(password)}")
                except Exception as exception:
                    print(f"Exception: {exception}")
                del password
                gc.collect() #garbage collect to rid memory of secrets when possible
    