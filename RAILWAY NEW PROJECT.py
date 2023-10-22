import random
import pymysql

mydb=pymysql.connect(user='root', password='kanikmakhija', host='localhost')
mycursor=mydb.cursor()

#Creation of Database
mycursor.execute("create database if not exists railwaysdb")
mycursor.execute("use railwaysdb")

#Creation of tables
mycursor.execute("create table if not exists tdetails(tno int,tname varchar(20),startpoint varchar(20),endpoint varchar(20),dtime varchar(20),atime varchar(20),totalseats int,reservedseats int default 0);")
mycursor.execute("create table if not exists pdata(pnr int,custname varchar(20),mail varchar(20),jrdate varchar(10),train varchar(20),food varchar(7),seatnumber int);")
#Function to check if seats are available
def seats():
    global t
    mycursor.execute("Select * from tdetails where tname=%s and totalseats>reservedseats;",(t,))
    row=mycursor.fetchone()
    try:
        if len(row)==0:
            error
        else:
            L.append(t)
    except:
        print("Sorry for the inconvenience . All seats for this train are reserved")
        print("Please choose another train.")
        t=input("enter name of train:")
        seats()

#Function to generate seat number
def seatno():
    mycursor.execute("Select * from pdata where train=%s;",(t,))
    rows=mycursor.fetchall()
    global n
    n=1
    for x in rows:
        n=n+1
    return n

#Function for booking ticket
def registercust():
    global L
    L=[]
    pnr=random.randint(1000,9999)
    L.append(pnr)
    name=input("enter name:")
    L.append(name)
    mail=input("enter email id:")
    L.append(mail)
    jr_date=input("enter date of journey:")
    L.append(jr_date)
    global t
    t=input("enter name of train:")
    seats()
    seatno()
    food=input("enter your food preference (veg/non-veg):")
    L.append(food)
    L.append(n)
    cust=(L)
    sql="insert into pdata(pnr,custname,mail,jrdate,train,food,seatnumber)values(%s,%s,%s,%s,%s,%s,%s)"
    mycursor.execute(sql,cust)
    mydb.commit()
    mycursor.execute("update tdetails set reservedseats=reservedseats+1 where tname=%s;",(t,))
    print("Your ticket has been booked")
    print("=================================")
    print("        INDIAN RAILWAYS          ")
    print("           E-Ticket              ")
    print(" NAME:",name)
    print(" PNR NUMBER:",pnr)
    print(" TRAIN:",t)
    print(" DATE OF JOURNEY:",jr_date)
    print(" SEAT NUMBER:",n)
    print(" FOOD:",food)
    print(" PRICE(including meal):",4000)
    print("=================================")

#Function to add train
def addtrain():
    L=[]
    tno=int(input("enter train number:"))
    L.append(tno)
    tname=input("enter train name:")
    L.append(tname)
    startpoint=input("enter start point:")
    L.append(startpoint)
    endpoint=input("enter enter endpoint:")
    L.append(endpoint)
    dtime=input("enter departure time:")
    L.append(dtime)
    atime=input("enter arrival time:")
    L.append(atime)
    totalseats=input("enter total seats :")
    L.append(totalseats)       
    cust=(L)
    sql="insert into tdetails(tno,tname,startpoint,endpoint,dtime,atime,totalseats)values(%s,%s,%s,%s,%s,%s,%s);"
    mycursor.execute(sql,cust)
    mydb.commit()
    print("The train has been added")

#Function to view trains
def traindetails():
    sql4="select * from tdetails;"
    mycursor.execute(sql4)
    rows=mycursor.fetchall()
    for x in rows:
              print(x)

#Function to cancel ticket
def cancelticket():
    pnrno=input("enter your pnr number")
    train=input("enter train name")
    conf=int(input("are you sure , enter 1 to cancel ticket"))
    if conf==1 :
        mycursor.execute("delete from pdata where pnr=%s;",(pnrno,))
        mycursor.execute("update tdetails set reservedseats=reservedseats-1 where tname=%s;",(train,))
        print("The ticket has been cancelled")
    else:
        print("Your ticket is not cancelled")

#Function to modify train details
def modtrain():
    trno=int(input("Enter train number of the train "))
    choice=int(input("For modifying the train details you would have to enter all the details again \n if you want to continue enter 1 "))
    if choice==1:
        mycursor.execute("delete from tdetails where tno=%s;",(trno,))
        L=[]
        tno=int(input("enter train number:"))
        L.append(tno)
        tname=input("enter train name:")
        L.append(tname)
        startpoint=input("enter start point:")
        L.append(startpoint)
        endpoint=input("enter enter endpoint:")
        L.append(endpoint)
        dtime=input("enter departure time:")
        L.append(dtime)
        atime=input("enter arrival time:")
        L.append(atime)
        totalseats=input("enter total seats :")
        L.append(totalseats)       
        cust=(L)
        sql="insert into tdetails(tno,tname,startpoint,endpoint,dtime,atime,totalseats)values(%s,%s,%s,%s,%s,%s,%s)"
        mycursor.execute(sql,cust)
        mydb.commit()
        print("The record has been updated") 
    else:
        print("The process is cancelled")

#Function to delete train        
def deltrain():
    trno=int(input("Enter train number of the train "))
    choice=int(input("Are you sure to delete train details \n press 1 to confirm"))
    if choice==1:
        mycursor.execute("delete from tdetails where tno=%s;",(trno,))
        print("The train details have been deleted")
    else:
        print("The process is cancelled")

#Function to search train by starting point
def startptdet():
    startpt=input("Enter starting point of train")
    mycursor.execute("Select * from tdetails where startpoint=%s;",(startpt,))
    rows=mycursor.fetchall()
    for x in rows:
              print(x)

#Function to search train by destination
def desigdet():
    desig=input("Enter destination of train")
    mycursor.execute("Select * from tdetails where endpoint=%s;",(desig,))
    rows=mycursor.fetchall()
    for x in rows:
              print(x)

#Function to search train by name
def tnamedet():
    tname=input("Enter name of train")
    mycursor.execute("Select * from tdetails where tname=%s;",(tname,))
    rows=mycursor.fetchall()
    for x in rows:
              print(x)

#Function to search train by train number
def tnodet():
    tno=input("Enter train number of train")
    mycursor.execute("Select * from tdetails where tno=%s;",(tno,))
    rows=mycursor.fetchall()
    for x in rows:
              print(x)

#Function to view passengers of a train
def pastraindet():
    tname=input("Enter name of train")
    mycursor.execute("Select * from pdata where train=%s;",(tname,))
    rows=mycursor.fetchall()
    for x in rows:
              print(x)

#Function to search passenger by name
def pasnamedet():
    name=input("Enter name of passenger")
    mycursor.execute("Select * from pdata where custname=%s;",(name,))
    rows=mycursor.fetchall()
    for x in rows:
              print(x)

#Functions to view all passengers
def pdetails():
    mycursor.execute("select * from pdata ;")
    rows=mycursor.fetchall()
    for x in rows:
              print(x)

#Menu for admin
def admnMenuset():
    print("                 INDIAN RAILWAYS                       ")
    print("#######################################################")
    print("#                                                     #")
    print("#             1. TRAIN DETAILS                        #")
    print("#                1.1 ADDING TRAIN                     #")
    print("#                1.2 MODIFYING TRAIN DETAILS          #") 
    print("#                1.3 DELETING TRAIN DETAILS           #")
    print("#                1.4 SEARCHING TRAIN                  #")
    print("#                    1.41 SEARCH ALL                  #")
    print("#                    1.42 SEARCH BY STARTING POINT    #")
    print("#                    1.43 SEARCH BY DESTINATION       #")
    print("#                    1.44 SEARCH BY NAME              #")
    print("#                    1.45 SEARCH BY TRAIN NUMBER      #")
    print("#             2. USER DETAILS                         #")
    print("#                2.1 SEARCH ALL                       #")
    print("#                2.2 SEARCH BY TRAIN                  #")
    print("#                2.3 SEARCH BY NAME                   #")
    print("#             3. EXIT                                 #")
    print("#                                                     #")
    print("#######################################################")
    inp=float(input("ENTER YOUR CHOICE :"))
    if inp==1.1:
        addtrain()
    elif inp==1.2:
        modtrain()
    elif inp==1.3:
        deltrain()
    elif inp==1.41:
        traindetails()
    elif inp==1.42:
        startptdet()
    elif inp==1.43:
        desigdet()
    elif inp==1.44:
        tnamedet()
    elif inp==1.45:
        tnodet()
    elif inp==2.1:
        pdetails()
    elif inp==2.2:
        pastraindet()
    elif inp==2.3:
        pasnamedet()
    elif inp==3:
        quit()
    else:
        print("Invalid choice entered")
        admnMenuset()

#Menu for user        
def userMenuset():
    print("                 INDIAN RAILWAYS                     ")
    print("#####################################################")
    print("#                                                   #")                  
    print("#            1. BOOKING TICKET                      #")
    print("#            2. CANCELLING TICKET                   #")
    print("#            3. VIEW TICKET DETAILS                 #")
    print("#            4. VIEWING TRAINS                      #")
    print("#              4.1 SEARCH BY STARTING POINT         #")
    print("#              4.2 SEARCH BY DESTINATION            #")
    print("#              4.3 SEARCH BY TRAIN NAME             #")
    print("#              4.4 SEARCH ALL                       #")
    print("#            5. EXIT                                #")
    print("#                                                   #")
    print("#####################################################")
    inp=float(input("enter your choice"))
    if inp==1:
        registercust()
    elif inp==2:
        cancelticket()
    elif inp==3:
        pasnamedet()
    elif inp==4.1:
        startptdet()
    elif inp==4.2:
        desigdet()
    elif inp==4.3:
        tnamedet()
    elif inp==4.4:
        traindetails()
    elif inp==5:
        quit()
    else:
        print("Invalid choice entered")
        userMenuset()

#login
def login():        
    admn=int(input("select 1 for admin \nselect 2 for user "))
    if admn==1 :
        adid=input("enter admin id ")
        pswd=int(input("enter password "))
        if adid=="admin@123" and pswd==0000:
            admnMenuset()
        else:
            print("Login failed")
    if admn==2 :
        usid=input("enter user id ")
        pswd=int(input("enter password "))
        if usid=="user@123" and pswd==0000:
            userMenuset()
        else:
            print("Login failed")

login()

def runagain():
    runagn=input("\n want to run again y/n:")
    while(runagn.lower()=='y'):
        login()
        runagn=input("\n want to run again y/n:")
    else:
        quit()
runagain()            
