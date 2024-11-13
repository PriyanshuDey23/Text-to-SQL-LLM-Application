# This code will be responsible for pushing the record in sqllite database

import sqlite3

# Connect to SQLlite Database
connection=sqlite3.connect("student.db") # student.db :- database name , If doesnot exit then it will create

# Create a cursor record to insert records/create table
cursor=connection.cursor() # Cursor will be responsible for traversing through entire table whthter add/retrive the records

# Create the Table
table_info="""

Create table STUDENT(Name VARCHAR(25), Class VARCHAR(25), Section VARCHAR(25) );

"""
cursor.execute(table_info) # table creates with the columns

# Insert Records
cursor.execute(''' Insert Into STUDENT values('Priyanshu','Data science','A')''')
cursor.execute(''' Insert Into STUDENT values('Rahul','AI','B')''')
cursor.execute(''' Insert Into STUDENT values('Arnab','Machine Learning','C')''')
cursor.execute(''' Insert Into STUDENT values('Subinoy','Software Engineering','D')''')
cursor.execute(''' Insert Into STUDENT values('Arpan','Devops','E')''')


# Display all the records
print("The Inserted Records are ")
data=cursor.execute(''' Select * from STUDENT''')
for row in data:
    print(row)

# Db file crated E:\Text-to-SQL-LLM-Application\student.db