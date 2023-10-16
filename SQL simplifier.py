import mysql.connector as sql
from tabulate import tabulate 
from mysql.connector import Error

# Connecting SQL to python
try:
    print("--> Initiating SQL Connection <--")
    host_name='localhost'
    user_name='root'
    password=input("- Enter Password :")
    SQLconnection=sql.connect(
        host=host_name, 
        user=user_name, 
        passwd=password
        )
    cr=SQLconnection.cursor()
    access=True
    print("--> Connected Successfully <--")
except Error as err:
    access=False
    print(f"X-> An exception occurred, {err} <-X")
    print("--> Rerun the program to retry <--")

# Creating database (Main_Menu option 1)
def createdatabase():
    dbname=input("New Database name: ")
    print('--> Executing Query <--')
    try:
        cr.execute(f"CREATE DATABASE {dbname}")
        print('--> Query OK <--')
        database(dbname) # After database is created, it gets used automatically
    except Error as err:
        print(f"X-> An exception occurred, {err} <-X")
        main(access)

# Using database (Main_Menu option 2)
def database(dbname):
    try:
        cr.execute("USE "+dbname)
        print(f"--> {dbname} IN USE <--")
        dbmenu=[
            [1,"Create Table"],
            [2,"Add Data to table"],
            [3,"Edit Data on a table"],
            [4,"Run a query"],
            [5,"Exit"]
        ]
        print(tabulate(dbmenu,tablefmt="simple_grid"))
        user=input("Enter task no: ")
        if user=="1":
            tbname=input("Enter new table name:")
            columncount=int(input("Enter no of columns:"))
            tablecreation(dbname,tbname,columncount)
        elif user=="2":
            tbname=input("Enter existing table name:")
            dataentry(dbname,tbname)
        elif user=="3":
            tbname=input("Enter existing table name:")
            dataedit(dbname,tbname)
        elif user=="4":
            queryrunner()
        else: 
            main(access)
    except Error as err:
        print(f"X-> An exception occurred, {err} <-X")
        main(access)

# Running a simple query (Main_Menu option 3)
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
            try:
                if "SELECT" in query.upper():
                    output=cr.fetchall()
                    print(tabulate(output,tablefmt="simple_grid"))
                else:
                    SQLconnection.commit()
                    print('--> Query OK <--')
            except:
                pass
        except Error as err:
            print(err)
    main(access)

# Creating Table
def tablecreation(dbname,tbname,columncount):
    for i in range(columncount):
        print("----------------------------")
        rowtitle=input("Enter Row Title: ")
        variables=input("Enter datatype: ")
        cr.execute(f"USE {dbname}")
        if i==0:
            try:
                cr.execute(f"CREATE TABLE {tbname}({rowtitle} {variables})")
                SQLconnection.commit()
                print(f"--> Column #{i+1} created <--")
            except Error as err:
                print(f"X-> An exception occurred while creating {tbname}, '{err}' <-X")
        else:
            try:
                cr.execute(f"ALTER TABLE {tbname} ADD {rowtitle} {variables}")
                SQLconnection.commit()
                print(f"--> Column #{i+1} created <--")
            except Error as err:
                print(f"X-> An exception occurred while creating {rowtitle}, '{err}' <-X")
    print(f"--> {tbname} created sucessfully <--")
    cr.execute(f"DESCRIBE {tbname}")
    output=cr.fetchall()
    header=["Field","Type","Null","Key","Default","Extra"]
    print(tabulate(output,header,tablefmt="simple_grid"))
    database(dbname)

# Adding Data to table
def dataentry(dbname,tbname):
    cr.execute(f"USE {dbname}")
    datacount=int(input("Enter no. of data to input: "))
    for i in range(datacount):
        cr.execute(f"DESCRIBE {tbname}")
        print(f"--> DATA ENTRY #{i+1} <--")
        alldata=()
        for j in cr:
            data=input(f"{j[0]}: ")
            alldata+=(data,)
        cr.execute(f"INSERT INTO {tbname} VALUES {alldata}")
        SQLconnection.commit()
        print(f"Entered data: {alldata}")
    print("SUCCESS")
    database(dbname)

# Edit Data in table
def dataedit(dbname,tbname):
    menu=[
        [1,"Alter table"],
        [2,"Update table"],
        [3,"Delete a record"],
        [4,"Run a query"],
        [5,"Exit"]
    ]
    print(tabulate(menu,tablefmt="simple_grid"))
    user=input("Enter task no : ")
    if user=="1":
        alter(dbname,tbname)
    if user=="2":
        update(dbname,tbname)
    if user=="3":
        delete(dbname,tbname)
    if user=="4":
        queryrunner()

# Alter a table
def alter(dbname,tbname):
    menu=[
        [1,"Add Column"],
        [2,"Drop Column"],
        [3,"Rename Column"],
        [4,"Modify Column"],
        [5,"Run a query"],
        [6,"Exit"]
    ]
    print(tabulate(menu,tablefmt="simple_grid"))
    user=int(input("Enter task no : "))
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
    dataedit(dbname,tbname)

# Update a table
def update(dbname,tbname):
    edit=input("SET: ")
    where=input("WHERE: ")
    try:
        cr.execute(f"UPDATE TABLE {tbname} SET {edit} WHERE {where}")
        SQLconnection.commit()
        print('--> Query OK <--')
    except Error as err:
        print(f"X-> An exception occurred, {err} <-X")
    dataedit(dbname,tbname)

# Delete an entry in table
def delete(dbname,tbname):
    where=input("WHERE: ")
    try:
        cr.execute(f"DELETE FROM TABLE {tbname} WHERE {where}")
        SQLconnection.commit()
        print('--> Query OK <--')
    except Error as err:
        print(f"X-> An exception occurred, {err} <-X")    
    dataedit(dbname,tbname)

# Main Menu
def main(access):
    if access==True:
        menu=[
            [1,"Create Database"],
            [2,"Use Database"],
            [3,"Run a Query"],
            [4,"Exit"]
        ]
        print(tabulate(menu,tablefmt="simple_grid"))

        user=input("Enter task no : ")
        if user=="1":
            createdatabase()
        if user=="2":
            dbname=input("Enter existing database name: ")
            database(dbname)
        if user=="3":
            queryrunner()

main(access)