import userdata
import pickle
import RSA

userd={}
groupd={}

def doNothing(*args):
    pass

def hazh(x):
    sume=sumo=suma=pr4=pr3=0
    ods=evs=prall=1
    for i in range(0,len(x),2):
        sume += ord(x[i])
    for i in range(1,len(x),2):
        sumo += ord(x[i])
    for i in range(len(x)):
        prall *= ord(x[i])+i
    for i in range(0,len(x),4):
        pr4 += (ord(x[i]) * ord(x[i-1]) * ord(x[i-2]) * ord(x[i-3]))
    for i in range(0,len(x),3):
        pr3 += (ord(x[i]) * ord(x[i-1]) * ord(x[i-2]))
    for i in range(1,len(x),2):
        ods *= ord(x[i])
    for i in range(0,len(x),2):
        evs *= ord(x[i])
    #for i in range(0,len(x),2):
    prs = hex(sume*sumo)[-1:-3:-1]
    suma = (sume+sumo)*len(x) - sume
    suma = hex(suma)[-1:-3:-1]
    if ods>evs: oediff = ods-evs
    else: oediff = ods + evs
    while not oediff%16: oediff//=16
    oediff = hex(oediff)[-1:-3:-1]
    while not prall%16: prall//=16
    prall = hex(prall)[-1:-5:-1]
    pr43 = hex(pr4%pr3)[-1:-3:-1]
    result = prall+suma+oediff+prs+pr43

    return result


def create_account():
    username=input("Enter your username: ")
    if username in userdata.userDict:
        print("Username already exists, enter a new one\n\n")
        create_account()
    else:
        password=input("Enter your password: ")
        password=hazh(password)
        with open("userdata.py",'a') as f:
            write_text="\nuserDict['"+username+"'] = '"+password+"'"
            f.write(write_text)
        userd[username] = password
        inbox_filename="./UserfilesInbox/"+username+".dat"
        outbox_filename="./UserfilesOutbox/"+username+".dat"
        inbox_userfile=open(inbox_filename,'w')
        inbox_userfile.close()
        outbox_userfile=open(outbox_filename,'w')
        outbox_userfile.close()
    login(username,password,True)



def send(username):
    receiver=input("To(Group's name/individual's name): ")
    if receiver in userdata.userDict or receiver in userd or receiver in groupd:
        receiver_file="./UserfilesInbox/"+receiver+".dat"
        sender_file="./UserfilesOutbox/"+username+".dat"
        message=username+": "+input("Enter message: ")
        KEY_r=userdata.userDict[receiver]
        KEY_s=userdata.userDict[username]
        message_r=RSA.rsa(message,RSA.keys(KEY_r,True)[0],RSA.keys(KEY_r,True)[1],True)
        with open(receiver_file,'ab') as f:
            pickle.dump(message_r,f)
        message_s=RSA.rsa(message,RSA.keys(KEY_s,True)[0],RSA.keys(KEY_s,True)[1],True)
        with open(sender_file,'ab') as f:
            pickle.dump(message,f)
        print("Message sent")
    
    elif receiver in userdata.groupDict:
        group_password=input("Enter the password of the group: ")
        group_password=hazh(group_password)
        if userdata.groupDict[receiver] == group_password:
            receiver_file="./Groups/"+receiver+".dat"
            sender_file="./UserfilesOutbox/"+username+".dat"
            message=username+": "+input("Enter message: ")
            with open(receiver_file,'ab') as f:
                message1=RSA.rsa(message,RSA.keys(group_password,True)[0],RSA.keys(group_password,True)[1],True)
                pickle.dump(message1,f)
            
            
            try:
                KEY=userdata.userDict[username]
            except:
                KEY=userd[username]


            with open(sender_file,'ab') as f:
                message2=RSA.rsa(message,RSA.keys(KEY,True)[0],RSA.keys(KEY,True)[1],True)
                pickle.dump(message2,f)
            print("Message sent")
        else:
            print("Incorrect password")
            send()

    else:
        print("This receiver does not exist.")
        send(username)


def check_inbox(username,newAccount):
    filename="./UserfilesInbox/"+username+".dat"
    if not newAccount:
        KEY=userdata.userDict[username]
    else:
        KEY=userd[username]
    with open(filename,'rb') as f:
        
        try:
            while True:
                messagelist=pickle.load(f)
                messagelist=RSA.rsa(messagelist,RSA.keys(KEY,False)[0],RSA.keys(KEY,False)[1],False)
                print(messagelist)
                print("_"*20)
        except:
            pass



def clear_messages(username):
    filename="./UserfilesInbox/"+username+".dat"
    with open(filename,'wb') as f:
        pickle.dump('',f)



def check_outbox(username):
    outbox_filename="./UserfilesOutbox/"+username+".dat"
    with open(outbox_filename,'rb') as f:
        try:
            while True:
                messagelist=pickle.load(f)
                print(messagelist)
        except:
            pass


def create_group(group_list,admin):
    group_name=input("Name of the group: ")
    if group_name in userdata.groupDict:
        print("This group name already exists, try choosing a different one")
        create_group(group_list,admin)
    else:
        group_password=input("Password of group: ")
        group_password_text=group_password
        group_password=hazh(group_password)
        for user in group_list:
            user_file="./UserfilesInbox/"+user+".dat"
            message="A new group called "+group_name+" has been created by "+admin+" and the password is "+group_password_text
            try:
                KEY=userdata.userDict[user]
            except:
                KEY=userd[user]
            message=RSA.rsa(message,RSA.keys(KEY,True)[0],RSA.keys(KEY,True)[1],True)
            with open(user_file,'ab') as f:
                pickle.dump(message,f)
        with open("userdata.py",'a') as f:
            write_text="\ngroupDict['"+group_name+"'] = '"+group_password+"'"
            f.write(write_text)
        groupd[group_name] = group_password

    
    group_path="./Groups/"+group_name+".dat"
    with open(group_path,'wb') as f:
        message="A new group called "+group_name+" has been created by "+admin
        message=RSA.rsa(message,RSA.keys(group_password,True)[0],RSA.keys(group_password,True)[1],True)
        pickle.dump(message,f)
    
    check_group_inbox(group_name,True)



def check_group_inbox(group_name,newGroup):
    if not newGroup:     
        group_password=input("Enter the password: ")
        group_password=hazh(group_password)
        if userdata.groupDict[group_name] == group_password:
            group_path="./Groups/"+group_name+".dat"
            with open(group_path,'rb') as f:
                try:
                    while True:
                        message=pickle.load(f)
                        message=RSA.rsa(message,RSA.keys(group_password,False)[0],RSA.keys(group_password,False)[1],False)
                        print(message)
                        print("_"*20)
                except:
                    pass        
        else:
            print("The password is incorrect, try again")
            check_group_inbox(group_name,False)

    else:
        group_path="./Groups/"+group_name+".dat"
        with open(group_path,'rb') as f:
                try:
                    while True:
                        message=pickle.load(f)
                        print(message)
                        print("_"*20)
                except:
                    pass    



def loginMenu(username,newAccount):
    print("\n\n\n\n")
    print("These are all the tasks you can perform: ")
    print("1.Send a message")
    print("2.Check your individual inbox")
    print("3.Log out")
    print("4.Erase all messages in your inbox")
    print("5.Check your outbox")
    print("6.Create a group")
    print("7.Check your group inbox")
    response=input("Enter your response: ")
    if response == "1":
        send(username)
    elif response == "2":
        check_inbox(username,newAccount)
    elif response == "3":
        return
    elif response == "4":
        clear_messages(username)
    elif response == "5":
        check_outbox(username)
    elif response == "6":
        number_of_members=int(input("How many members do you want in the group: "))
        group_list=[]
        i=0
        while i<number_of_members:
            user=input("Enter the name of member "+str(i+1)+": ")
            if user in userdata.userDict or user in userd:
                group_list.append(user)
                i+=1
            else:
                print("This member does not exist")
                print("Try again\n\n")
        create_group(group_list,username)
    elif response == "7":
        group_name=input("Enter the name of the group you want to check: ")
        check_group_inbox(group_name,False)
    else:
        print("Invalid input")
    input("Press Enter to continue...\n\n")
    loginMenu(username,newAccount)


def login(username,password,newAccount):
    password=hazh(password)
    if not newAccount:
        try:
            if userd[username] == password:
                loginMenu(username)
            else:
                print("Wrong password")
                password=input("Enter the password: ")
                login(username,password,False)
        except:
            if userdata.userDict[username] == password:
                loginMenu(username,newAccount)
            else:
                print("Wrong password")
                password=input("Enter the password: ")
                login(username,password,False)
        
            
    else:
        loginMenu(username,True)



def Menu():
    print("\n\n\nChoose what you want to do: ")
    print("1.Create an account")
    print("2.Login")
    print("3.Exit")
    response=input("Enter your response: ")
    if response == "1":
        create_account()
    elif response == "2":
        username=input("Enter your username: ")
        if username in userdata.userDict or username in userd:
            password=input("Enter your password: ")
            login(username,password,False)
        else:
            print("\n\nThis account doesn't exist")
            print("Try entering a valid username or create an account by this name")
    elif response == "3":
        exit()
    else:
        print("Invalid response")
    input("Press Enter to continue...\n\n")
    Menu()

Menu()