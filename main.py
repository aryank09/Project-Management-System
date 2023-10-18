#importing necessary modules for the runnnig of the program
import tkinter
import mysql.connector
import admin
import employee
import sys

#establishing mysql connection
mydb=mysql.connector.connect(host='localhost',user='root',password='root',database='crm')
mycursor=mydb.cursor()
mycursor.execute('create table if not exists admin(username varchar(10) primary key,password varchar(10));')
mycursor.execute('create table if not exists employee(username varchar(10) primary key,password varchar(10));')
mydb.commit()

def exit():
    sys.exit()

#running the user nterface
m=tkinter.Tk()
mbutton_1=tkinter.Button(text = "Admin" ,command=admin.admin_account).pack()
mbutton_2=tkinter.Button(text = "Employee",command=employee.employee_account).pack()
mbutton_3=tkinter.Button(text = "Exit",command=exit).pack()
m.mainloop()
