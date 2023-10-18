#importing necessary modules
import tkinter
import mysql.connector
import admin
import employee
import sys

#establishing connection
mydb=mysql.connector.connect(host='localhost',user='root',password='root',database='crm')
mycursor=mydb.cursor()
#running the comands
mycursor.execute('create table if not exists admin(username varchar(10) primary key,password varchar(10));')
mycursor.execute('create table if not exists employee(username varchar(10) primary key,password varchar(10));')
#saving the changes
mydb.commit()

#function the exit program
def exit():
    sys.exit()

#creating buttons for running the program and connection them to necessary functions
m=tkinter.Tk()
mbutton_1=tkinter.Button(text = "Admin" ,command=admin.admin_account).pack()
mbutton_2=tkinter.Button(text = "Employee",command=employee.employee_account).pack()
mbutton_3=tkinter.Button(text = "Exit",command=exit).pack()
m.mainloop()
