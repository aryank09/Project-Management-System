import mysql.connector
import tkinter
import math
import mail
from tabulate import tabulate

mydb=mysql.connector.connect(host='localhost',user='root',password='root',database='crm')
mycursor=mydb.cursor()
mycursor.execute('create table if not exists data(goal varchar(20), subtask1 varchar(50), subtask2 varchar(50), subtask3 varchar(50), subtask4 varchar(50), subtask5 varchar(50), total_hours int(10), no_of_working_days int(225), total_expense int(225), employees_pay int(225), cost int(225), profit int(225));')
mydb.commit()

def create_admin_account():
    username=input('Please enter the new admin username: ')
    password=input('Please enter the new admin password: ')
    mycursor.execute("Insert into admin values('%s','%s')"%(username,password))
    mydb.commit()
    print('Employee account is created!')
    
def create_employee_account():
    username=input('Please enter the new employee username: ')
    password=input('Please enter the new employee password: ')
    mycursor.execute("Insert into employee values('%s','%s')"%(username,password))
    mydb.commit()
    print('Employee account is created!')

def create_new_project():
    goal=input('Enter your goal for the project: ')#taking inputs from the admin for the assignment
    
    while True:
        print('Please enter 5 subtasks: ')
        list1=list()
        for a in range(5):
            milestone=input('Enter your sub-task: ')
            list1.append(milestone)#making a list of the milestones

        #employee
        num2=int(input("\nPlease enter the number of employees you want to assign to the project: "))#asking for the number of employees
        list2=list()
        for a in range(num2):
            employee=input('Please enter the name of the employee: ')
            list2.append(employee)#making a list for the name of employees

        #time required to complete the work 
        total_hours=int(input('Total Number of hours required to complete the work: '))
        print('We are considering each working day to  have 8 hours')
        final_days=math.ceil(total_hours/8)
        print('Number of working days required are',final_days)

        while True:
            #total expense of the project
            total_expense=int(input('\nEnter the amount of money recieved for the project: '))
            #dividing the expenses
            employees_pay=int(input('Enter the amount each employee will earn: '))
            cost=int(input('Enter the cost of the project: '))
            profit=total_expense-(cost+employees_pay*num2)
            if (cost+employees_pay*num2 )< total_expense:
                print('The project gives profit ')
                print('The profit from the project is',profit)
                break
            elif (cost+employees_pay*num2)==total_expense:
                print('The project gives no profit')
                break
            else:
                print('The project will be in loss')
                print('The loss from the project is(- indicates loss)',profit)
                option=input('Do you want to enter the costs again?(Y/N): ')
                if option=='Y':
                    continue
                else:
                    break
                       
        emails=input('Please enter your email address to recieve the project report: ')
                
        mycursor.execute("insert into data values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');"%(goal,str(list1[0]),str(list1[1]),str(list1[2]),str(list1[3]),str(list1[4]),str(total_hours),str(final_days),str(total_expense),str(employees_pay),str(cost),str(profit)))
        mydb.commit()
        mycursor.execute("SELECT * FROM data where goal='%s'"%goal)
        myresult=mycursor.fetchall()
        data=tabulate(myresult, headers=['goal','subtask1','subtask2','subtask3','subtask4','subtask5','total_hours','no_of_working_days','total_expense','employees_pay','cost','profit'], tablefmt='psql')
        data=str(data)
        print('\nWe will now be sending a project memo')
        mail.email(emails,data)#calling the function
        print('The mail has been sent!')
        break

def access_old_data():
    while True:
        sql=("SELECT * FROM data")
        mycursor.execute(sql)
        myresult=mycursor.fetchall()
        print(tabulate(myresult, headers=['goal','subtask1','subtask2','subtask3','subtask4','subtask5','total_hours','no_of_working_days','total_expense','employees_pay','cost','profit'], tablefmt='psql'))
        choice=input('Please enter Y if you want to change any part of the data: ')
        if choice=='Y':
            choice2=input('Please enter 1 if you want update data else enter 2 if you want to remove project data: ')
            if choice2=='1':
                data_where=input('Please enter the goal name: ')
                data_column=input('Please enter the column name: ')
                data_change=input('Please enter what the new data piece will be: ')
                if data_column=='total_expense':
                    employee_count=int(input('Please enter the number of employees: '))
                    result=[tup for tup in myresult if tup[0]==data_where]
                    result=list(result[0])
                    result[8]=int(data_change)
                    result[11]=(result[8])-((result[10])+(result[9])*employee_count)
                    mycursor.execute("update data set %s='%s' where goal='%s'"%(data_column,data_change,data_where))
                    mycursor.execute("update data set profit='%s' where goal='%s'"%(result[11],data_where))
                    mydb.commit()
                    continue
                elif data_column=='employees_pay':
                    employee_count=int(input('Please enter the number of employees: '))
                    result=[tup for tup in myresult if tup[0]==data_where]
                    result=list(result[0])
                    result[9]=int(data_change)
                    result[11]=result[8]-(result[10]+result[9]*employee_count)
                    mycursor.execute("update data set %s='%s' where goal='%s'"%(data_column,data_change,data_where))
                    mycursor.execute("update data set profit='%s' where goal='%s'"%(result[11],data_where))
                    mydb.commit()
                    continue
                elif data_column=='cost':
                    employee_count=int(input('Please enter the number of employees: '))
                    result=[tup for tup in myresult if tup[0]==data_where]
                    result=list(result[0])
                    result[10]=int(data_change)
                    result[11]=result[8]-(result[10]+result[9]*employee_count)
                    mycursor.execute("update data set %s='%s' where goal='%s'"%(data_column,data_change,data_where))
                    mycursor.execute("update data set profit='%s' where goal='%s'"%(result[11],data_where))
                    mydb.commit()
                    continue
                elif data_column=='total_hours':
                    result=[tup for tup in myresult if tup[0]==data_where]
                    result=list(result[0])
                    result[6]=int(data_change)
                    result[7]=math.ceil(result[6]/8)
                    mycursor.execute("update data set %s='%s' where goal='%s'"%(data_column,data_change,data_where))
                    mycursor.execute("update data set no_of_working_days='%s' where goal='%s'"%(result[7],data_where))
                    mydb.commit()
                    continue
                else:
                    mycursor.execute("update data set %s='%s' where goal='%s'"%(data_column,data_change,data_where))
                    mydb.commit()
                    continue
            elif choice2=='2':
                project_name=input('Please enter the name of the project whose data you want to remove: ')
                mycursor.execute("delete from data where goal='%s'"%project_name)
                mydb.commit()
                continue
            else:
                print('invalid choice!')
                continue
        else:
            break

def admin_account():
    while True:
        username=input('Please enter the username: ')
        password=input('Please enter the password: ')
        mycursor.execute("select password from admin where username='%s'"%username)
        row=mycursor.fetchall()
        if row==[]:
            print('Please try try again')
            continue
        for i in row:
            if i[0]==str(password):
                while True:
                    m=tkinter.Tk()
                    mbutton_1=tkinter.Button(text = "Create Employee Account", command=create_employee_account).pack()
                    mbutton_2=tkinter.Button(text = "Access Old Data", command=access_old_data).pack()
                    mbutton_3=tkinter.Button(text = "Create New Project",command=create_new_project).pack()
                    mbutton_4=tkinter.Button(text = "Create Admin Account",command=create_admin_account).pack()
                    m.mainloop()

            else:
                print('Please try again')
                continue
        
    
