## BANK MANAGEMENT PROJECT
# OBJECTIVES:
### user must be able to-
            ##1. CREATE AN ACCOUNT
            ##2. DEPOSIT MONEY INTO ACCOUNT
            ##3. WITHDRAW MONEY FROM ACCOUNT
            ##4. GET ALL DETAILS OF HIS/HER ACCOUNT
            ##5. UPDATE DETAILS OF ACCOUNT
            ##6. DELETEM DETAILS OF ACCOUNT

## project  will make use of: File handling, oops concept, list comprehension, database mgmt, shallow and deepcopy
import json
import random
from pathlib import Path
import string


class Bank:

    ##making of dummy from original data.json
    data=[]
    database ='data.json'       ##giving datbase file path, we need to access this path again and again to update, delete etc using Path 
    
    try:
        if Path(database).exists():
            with open(database) as fs:  #use json.load--> it accepts a file object
                data = json.loads(fs.read())   # use of json.loads--> when the content is string as in fs.read()(pass the content of the file using read() function)
        else:
            print("No such file exists")                   
    except Exception as err:
        print(f"Exception occured as {err}")

    @staticmethod         ## we dont need to use self with decorator
    def __update():
        with open(Bank.database, 'w') as fs:
            json.dump(Bank.data, fs, indent=4)
            
    @classmethod   ## using a class method to point to our class
    def __accountgenerate(cls):   ##private- we dont WANt people to access our account numbers
        alpha=random.choices(string.ascii_letters,k=4)
        num=random.choices(string.digits,k=2)
        spchar=random.choices("!@#$%*",k=1)
        id=alpha+num+spchar
        random.shuffle(id)
        return "".join(id)

    
    def createaccount(self):
        info = {
            "name": input("Tell your name :- "),
            "age" : int(input("tell your age :- ")),
            "email": input("tell your email :- "),
            "pin": int(input("tell your 4 number pin :- ")),
            "accountNo." : Bank.__accountgenerate(),
            "balance" : 0
        }
        if info['age'] < 18  or len(str(info['pin'])) != 4:
            print("sorry you cannot create your account")
        else:
            print("account has been created successfully")
            for i in info:
                print(f"{i} : {info[i]}")
            print("please note down your account number")

            Bank.data.append(info)  ##adding the info data into our dummy

            Bank.__update()        # updating our dummy annd update function loading into our original json

    def depositmoney(self):
        acctno=input("Enter account no: ")
        pin=int(input("Enter your pin: "))

        userdata=[i for i in Bank.data if i['accountNo.']==acctno and i['pin']==pin]

        if userdata==False:
            print("WHoops no such account found!!")
        else:
            print("You have: ", userdata[0]["balance"], " currently")
            amount=int(input("Enter how much  you want to deposit(0-10000): "))
            if amount<0 or amount>10000:
                print("Sorry amount to deposit is invalid, enter between 0 and 10,000Rs")
            else:
                userdata[0]['balance'] += amount
                Bank.__update()
                print("Amount deposited successfully!! ")
        
    def withdraw(self):
        acctno=input("Enter account no: ")
        pin=int(input("Enter your pin: "))

        userdata=[i for i in Bank.data if  i['accountNo.']==acctno and i['pin']==pin]

        if userdata== False:
            print("No such account found")

        else:
            amount=int(input("Enter how much you want to withdraw: "))
            if userdata[0]['balance']<amount:
                print("Insufficient funds! ")
            elif amount>5000 or amount<0:
                print("Not a valid amount you can withdraw!")
            else:

                userdata[0]['balance']-=amount
                
            Bank.__update()
            print("Amount withdrawn successfully!! ")
            print(userdata)

    def getalldetails(self):
        acctno=input("Enter account no: ")
        pin=int(input("Enter your pin: "))

        userdata=[i for i in Bank.data if  i['accountNo.']==acctno and i['pin']==pin]

        if userdata==False:
            print("No such account found! ")
        else:
            print("Here are all your details-")
            for i in userdata[0]:
                print(f"{i}: {userdata[0][i]}")

    def updatedetails(self):
        print("You are allowed to edit three things: name,mail,pin") 
        acctno=input("Enter account no: ")
        pin=int(input("Enter your pin: "))

        userdata=[i for i in Bank.data if  i['accountNo.']==acctno and i['pin']==pin]
        print("Fill the details for change or leave it empty if no change")
        
        if userdata==False:
            print("No such data exists!")
        else:
            newdata={
                "name": input("Enter new name or press enter to skip changes: "),
                "email": input("Enter new mail or press enter to skip changes: "),
                "pin": input("Enter new pin or press enter to skip changes: ")
            }

            if newdata["name"]=="":
                newdata["name"]=userdata[0]["name"]
            if newdata["email"]=="":
                newdata["email"]=userdata[0]["email"]
            if newdata["pin"]=="":
                newdata["pin"]=userdata[0]["pin"]
            
            newdata["age"]=userdata[0]["age"]
            newdata["accountNo."]=userdata[0]["accountNo."]
            newdata["balance"]=userdata[0]["balance"]

            if type(newdata["pin"])==str:
                newdata["pin"]=int(newdata["pin"])
            
            for i in newdata:
                if newdata[i]==userdata[0][i]:
                    continue
                else:
                    userdata[0][i]=newdata[i]

            Bank.__update()
            print("Details update successfully!")
            print(userdata)

    def delete(self):
        acctno=input("Enter account no: ")
        pin=int(input("Enter your pin: "))

        userdata=[i for i in Bank.data if  i['accountNo.']==acctno and i['pin']==pin]
        if userdata==False:
            print("No such data exists!")
        else:
            check=input("Press Y to proceed with delete or Press N to cancel delete: ")
            if check =="N" or check=="n":
                print("No deletion executed")
            else:
                index=Bank.data.index(userdata[0])
                Bank.data.pop(index)
                print("Account deleted successfully! ")
                Bank.__update()

        

user=Bank()



print("PRESS 1 TO CREATE AN ACCOUNT")
print("PRESS 2 TO DEPOSIT MONEY INTO ACCOUNT")
print("PRESS 3 TO WITHDRAW MONEY FROM ACCOUNT")
print("PRESS 4 TO GET ALL DETAILS OF HIS/HER ACCOUNT")
print("PRESS 5 TO UPDATE DETAILS OF ACCOUNT")
print("PRESS 6 TO DELETE DETAILS OF ACCOUNT")

check= int(input("Enter your response:-  "))

if check ==1:
    user.createaccount()

if check==2:
    user.depositmoney()

if check ==3:
    user.withdraw()
if check ==4:
    user.getalldetails()

if check ==5:
    user.updatedetails()

if check==6:
    user.delete()