import mysql.connector as sql
from tabulate import tabulate 
from mysql.connector import Error

# Connecting SQL to python
try:
    print("\n--> Initiating SQL Connection <--\n")
    password=input("-- Enter Password :")
    SQLconnection=sql.connect(
        host='localhost', 
        user='root', 
        passwd=password
        )
    cr=SQLconnection.cursor()
    access=True
    print("\n--> Connected Successfully <--")
except Error as err:
    access=False
    print(f"X-> An exception occurred, {err} <-X")
    print("--> Rerun the program to retry <--")

# Creating database (Main_Menu option 1)
def createdatabase(taskname="None"):
    starter_table(taskname=taskname)
    dbname=input("New Database name: ")
    if dbname=="/q":
        main(access)
    print('\n--> Executing Query <--')
    try:
        cr.execute(f"CREATE DATABASE {dbname}")
        print('--> Query OK <--\n')
        database(dbname) # After database is created, it gets used automatically
    except Error as err:
        print(f"X-> An exception occurred, {err} <-X")
        main(access)

# Using database (Main_Menu option 2)
def database(dbname,taskname="None"):
    try:
        cr.execute("USE "+dbname)
        starter_table(dbname,header=f"{dbname} Database",taskname=taskname)
        print(f"\n--> {dbname} IN USE <--\n")
        dbmenu=[
            [1,"Create Table"],
            [2,"Add Data to Table"],
            [3,"Edit Data on a Table"],
            [4,"Display Tables"],
            [5,"Run a query"],
            [6,"Exit"]
        ]
        print(tabulate(dbmenu,tablefmt="fancy_grid"))
        user=input("Enter task no: ")
        if user=="/q":
            main(access)
        if user=="1":
            while True:
                tbname=input("Enter new table name:")
                if tbname=="/q":
                    main(access)
                cr.execute("SHOW TABLES")
                data=cr.fetchall()
                for i in data:
                    if i[0]==tbname:
                        print("X-> An exception occurred, Table already exists <-X")
                        print("--> Try Again or enter /q to exit <--")
                        proceed=False
                        break
                    else:
                        proceed=True
                if proceed==True:
                    break                    
            columncount=int(input("Enter no of columns:"))
            tablecreation(dbname,tbname,columncount)
        tbname=findtable(dbname)
        if user=="2":
            dataentry(dbname,tbname)
        elif user=="3":
            dataedit(dbname,tbname)
        elif user=="4":
            display(dbname,tbname)
        elif user=="5":
            queryrunner()
            database(dbname,taskname="None")
        else: 
            main(access)
    except Error as err:
        print(f"X-> An exception occurred, {err} <-X")
        main(access)

# Creating Table (Database option 1)
def tablecreation(dbname,tbname,columncount):
    starter_table(dbname,tbname,header=f"{dbname} Database",taskname="Creating a Table")
    i=0
    while i<columncount:
        print("----------------------------")
        rowtitle=input("Enter Row Title: ")
        variables=input("Enter datatype: ")
        if "/q" in [rowtitle,variables]:
            database(dbname)
        cr.execute(f"USE {dbname}")
        if i==0:
            try:
                cr.execute(f"CREATE TABLE {tbname}({rowtitle} {variables})")
                SQLconnection.commit()
                print(f"--> Column #{i+1} created <--")
                cont=True
                i+=1
            except Error as err:
                print(f"X-> An exception occurred while creating {tbname}, '{err}' <-X")
                break
        else:
            try:
                cr.execute(f"ALTER TABLE {tbname} ADD {rowtitle} {variables}")
                SQLconnection.commit()
                print(f"--> Column #{i+1} created <--")
                cont=True
                i+=1
            except Error as err:
                print(f"X-> An exception occurred while creating {rowtitle}, '{err}' <-X")
                cr.execute(f"DROP TABLE {tbname}")
                break 
    if cont==True:            
        print(f"--> {tbname} created sucessfully <--")
        cr.execute(f"DESCRIBE {tbname}")
        output=cr.fetchall()
        header=["Field","Type","Null","Key","Default","Extra"]
        print(tabulate(output,header,tablefmt="fancy_grid"))
    database(dbname)

# Adding Data to table (Database option 2)
def dataentry(dbname,tbname):
    menu=[
        [1,"Add Data Manually"],
        [2,"Import CSV file"]
    ]
    starter_table(dbname,tbname,header=f'Data Editing',taskname="Data Entry")
    print(tabulate(menu,tablefmt="fancy_grid"))
    user=input("Enter task no: ")
    if user=="/q":
        database(dbname)
    cr.execute(f"USE {dbname}")
    if user=="1":
        starter_table(dbname,tbname,header=f'{tbname} Table',taskname="Manual data addition")
        datacount=int(input("Enter no. of data to input: "))
        for i in range(datacount):
            cr.execute(f"DESCRIBE {tbname}")
            print(f"--> DATA ENTRY #{i+1} <--")
            alldata=()
            for j in cr:
                data=input(f"{j[0]}: ")
                try:
                    data=int(data)
                except:
                    pass
                alldata+=(data,)
            cr.execute(f"INSERT INTO {tbname} VALUES {alldata}")
            SQLconnection.commit()
            print(f"Entered data: {alldata}")
        print("SUCCESS")
    if user=="2":
        csvtosql(dbname,tbname)
    database(dbname)

# imports data from CSV file
def csvtosql(dbname,tbname):
    import csv
    filename=input("Enter file path: ")
    if filename=="/q":
        main(access)
    file_name=''
    # To avoid user misinput
    for i in filename:
        if i!='"':
            file_name+=i
    with open(file_name,"r") as f:
        csvr=csv.reader(f,delimiter=',')
        for i in csvr:
            # To avoid possible variable type errors
            for j in i:
                indexx=i.index(j)
                try:
                    J=int(j)
                    i[indexx]=J
                except:
                    continue
            # To convert it into a tuple
            data=()
            for j in i:
                data+=(j,)
            cr.execute(f"USE {dbname}")
            cr.execute(f"INSERT INTO {tbname} VALUES {data}")
            SQLconnection.commit()
            print(f"Entered data: {data}")
        print("--> SUCCESS <--")

# Edit Data in table (Database option 3)
def dataedit(dbname,tbname):
    menu=[
        [1,"Alter table"],
        [2,"Update table"],
        [3,"Delete a record"],
        [4,"Run a query"],
        [5,"Exit"]
    ]
    starter_table(dbname,tbname,header=f'{tbname} Table',taskname="Data Editing")
    print(tabulate(menu,tablefmt="fancy_grid"))
    user=input("Enter task no: ")
    if user=="/q":
        database(dbname)
    if user=="1":
        alter(dbname,tbname)
    if user=="2":
        update(dbname,tbname)
    if user=="3":
        delete(dbname,tbname)
    if user=="4":
        queryrunner()
        dataedit(dbname,tbname)
    database(dbname)

# Alter a table (Dataedit option 1)
def alter(dbname,tbname):
    menu=[
        [1,"Add a Column"],
        [2,"Drop a Column"],
        [3,"Rename a Column"],
        [4,"Modify a Coloumn Datatype"],
        [5,"Run a query"],
        [6,"Exit"]
    ]
    starter_table(dbname,tbname,header="Edit Database",taskname="Alter Table")
    print(tabulate(menu,tablefmt="fancy_grid"))
    user=int(input("Enter task no: "))
    if user=="/q":
        dataedit(dbname,tbname)
    if user!=5 and user!=6:
        tasknamee=findtask(menu,user)
        starter_table(dbname,tbname,header=f"Alter {tbname} Table",taskname=tasknamee)
        colname=input("Enter Column name:")
    if user==1:
        datatype=input("Enter datatype:")
        try:
            cr.execute(f"ALTER TABLE {tbname} ADD {colname} {datatype}")
            SQLconnection.commit()
            print('--> Query OK <--')
        except Error as err:
            print(f"X-> An exception occurred, {err} <-X")
    elif user==2:
        try:
            cr.execute(f"ALTER TABLE {tbname} DROP {colname}")
            SQLconnection.commit()
            print('--> Query OK <--')
        except Error as err:
            print(f"X-> An exception occurred, {err} <-X")
    elif user==3:
        newname=input("Enter new name: ")
        try:
            cr.execute(f"ALTER TABLE {tbname} RENAME {colname} TO {newname}")
            SQLconnection.commit()
            print('--> Query OK <--')
        except Error as err:
            print(f"X-> An exception occurred, {err} <-X")       
    elif user==4:
        newdatatype=input("Enter new datatype: ")
        try:
            cr.execute(f"ALTER TABLE {tbname} MODIFY {colname} {newdatatype}")
            SQLconnection.commit()
            print('--> Query OK <--')
        except Error as err:
            print(f"X-> An exception occurred, {err} <-X")
    elif user==5:
        queryrunner()
        alter(dbname,tbname)
    dataedit(dbname,tbname)

# Update a table (Dataedit option 2)
def update(dbname,tbname):
    starter_table(dbname,tbname,header="Data Editing",taskname="Updating Table")
    cr.execute(f'USE {dbname}')
    cr.execute(f'DESCRIBE {tbname}')
    coltitle=[]
    for i in cr:
        j=i[0]
        coltitle.append(j)
    menu=[]
    for i in range(len(coltitle)):
        item=[i+1,coltitle[i]]
        menu.append(item)
    print(tabulate(menu,tablefmt="fancy_grid",stralign="center"))
    while True:
        try:
            edit=input("\n>> Select the coloumn to edit <<\n::> ")
            edited=input("\n>> Enter the new data <<\n::> ")
            query=f"UPDATE {tbname} SET {findtask(menu,edit)}={edited}"
            where=input("\n>> Select the coloumn to edit in terms with (Press ENTER to continue without constraints) <<\n::> ")
            if "/q" in [edit,edited,where]:
                dataedit(dbname,tbname)
            if where!='':
                whered=input("\n>> Enter the data to edit in terms with <<\n::> ")
                query+=f" WHERE {findtask(menu,where)}='{whered}'"
            break
        except Error as err:
            print(f"X-> An exception occurred, {err} <-X")
            print(">> Try Again <<\n")
    try:
        cr.execute(query)
        SQLconnection.commit()
        print('--> Query OK <--')
    except Error as err:
        print(f"X-> An exception occurred, {err} <-X")
    dataedit(dbname,tbname)

# Delete an entry in table (Dataedit option 3)
def delete(dbname,tbname):
    where=input("WHERE: ")
    if where=="/q":
        dataedit(dbname,tbname)
    try:
        cr.execute(f"DELETE FROM {tbname} WHERE {where}")
        SQLconnection.commit()
        print('--> Query OK <--')
    except Error as err:
        print(f"X-> An exception occurred, {err} <-X")    
    dataedit(dbname,tbname)

# Displaying Tables (Database option 4)
def display(dbname,tbname):
    starter_table(dbname,tbname,header=f'{tbname} Table',taskname="Table Display")
    cr.execute(f'USE {dbname}')
    cr.execute(f'DESCRIBE {tbname}')
    coltitle=[]
    for i in cr:
        j=i[0]
        coltitle.append(j)
    menu=[['0',"*"]]
    for i in range(len(coltitle)):
        item=[i+1,coltitle[i]]
        menu.append(item)
    print(tabulate(menu,tablefmt="fancy_grid",stralign="center"))
    while True:
        col=input("\n>> Select the coloumn to display (seperate with ',' in case of selecting multiple columns) <<\n::> ")
        where=input("\n>> Select the coloumn to edit in terms with (Press ENTER to continue without constraints) <<\n::> ")
        proceed=True
        if "/q" in [col,where]:
            database(dbname)
        if "0" in col and "," in col:
            print("X-> An exception occurred <-X")
            continue
        elif "0"==col:
            query=f"SELECT * FROM {tbname}"
        elif "," in col:
            cols=col.split(",")
            colname=''
            for i in cols:
                if i<str((len(coltitle)+1)):
                    taskname=findtask(menu,i)
                    if i!=col[-1]:
                        colname+=taskname+","
                    else:
                        colname+=taskname
                else:
                    proceed=False
                    print("X-> An exception occurred, OUT OF RANGE SELECTION<-X")
                    break
            query=f"SELECT {colname} FROM {tbname}"
        elif len(col)==1 and col<str((len(coltitle)+1)) and col!="*":
            colname=findtask(menu,col)
            query=f"SELECT {colname} FROM {tbname}"
        else:
            print("X-> An exception occurred <-X")
            continue
        if where!='' and proceed!=False:
            whered=input("\n>> Enter the data to edit in terms with <<\n::> ")
            oper=[[0,"="],
                  [1,">"],
                  [2,"<"],
                  [3,"<="],
                  [4,">="]]
            print(tabulate(oper,tablefmt="fancy_grid",stralign="center"))
            op=input("\n>> Enter the operator to edit in terms with <<\n::> ")
            query+=f" WHERE {findtask(menu,where)}{findtask(oper,op)}'{whered}'"
        break
    if proceed!=False:
        try:
            cr.execute(query)
            output=cr.fetchall()
            cr.execute(f'DESCRIBE {tbname}')
            for i in cr:
                j=i[0]
                coltitle.append(j)
            print(query)
            print(tabulate(output,coltitle,tablefmt="psql",stralign="center"))
        except Error as err:
            print(f"X-> An exception occurred, {err} <-X")
    #database(dbname)

# Running a simple query (multiple calls)
def queryrunner():
    print("#-> Enter Query <-#")
    print("#-> Type /q to exit queryrunner <-#")
    while True:
        query=input("-> ")
        if query=="/q":
            print("--> Safely Exiting Queryrunner")
            break
        try:
            cr.execute(query) 
            query=query.upper()
            if "SELECT" in query or "DESCRIBE" in query or "DESC" in query or "SHOW" in query:
                output=cr.fetchall()
                # To extract the name of columns for headers
                if "SELECT" in query:
                    coltitle=[]
                    queryy=query.split("FROM ")
                    queryyy=queryy[1]
                    queryyyy=queryyy.split()
                    tbname=queryyyy[0]
                    cr.execute(f'DESCRIBE {tbname}')
                    for i in cr:
                        j=i[0]
                        coltitle.append(j)
                    print(tabulate(output,coltitle,tablefmt="psql",stralign="center"))
                else: 
                    print(tabulate(output,tablefmt="psql",stralign="center"))
            else:
                SQLconnection.commit()
                print('--> Query OK <--')
        except Error as err:
            print(err)

# Starter Table
def starter_table(dbname="None",tbname="None",header="_--_--_ SQL Simplifier _--_--_",taskname="None"):
    list=[]
    list.append([f'Selected Database  |  {dbname}'])
    list.append([f'Selected Table     |  {tbname}'])
    list.append([f'Selected Task      |  {taskname}'])
    print(tabulate(list,[header],tablefmt="fancy_grid"))
    print()

# Task Finder
def findtask(alltask,user):
    for task in alltask:
        taskno=str(task[0])
        if taskno==user:
            return task[1]

# Table Finder
def findtable(dbname):
    cr.execute(f"USE {dbname}")
    cr.execute("SHOW TABLES")
    data=cr.fetchall()
    menu=[]
    for i in range(len(data)):
        menu.append([i+1,data[i][0]])
    print()
    print(tabulate(menu,tablefmt="fancy_grid"))
    user=input("\nEnter table no. to select : ")
    tablename=findtask(menu,user)
    return tablename

# Main Menu
def main(access):
    if access==True: 
        starter_table(header="Main Menu")
        menu=[
            [1,"Create Database"],
            [2,"Use Database"],
            [3,"Run a Query"],
            [4,"Exit"]]
        print(tabulate(menu,tablefmt="fancy_grid"))
        user=input("Enter task no : ")
        if user=="1":
            createdatabase(taskname=findtask(menu,user))
        if user=="2":
            dbname=input("Enter existing database name: ")
            database(dbname,findtask(menu,user))
        if user=="3":
            queryrunner()
            main(access)

main(access)