import mail
import mysql.connector
from tabulate import tabulate

mydb=mysql.connector.connect(host='localhost',user='root',password='root',database='crm')
mycursor=mydb.cursor()
mycursor.execute('create table if not exists data_employee(project_name varchar(30) primary key, done_hrs int(5), project_status varchar(30));')
mydb.commit()

def employee_input():#function for taking inputs from an employee
  name=input('Please enter the project name: ')
  done_hrs=int(input('Please enter the amount of hours you have completed: '))
  task_count=0
  for i in range(5):
    result=input('Please enter Y if you have completed task '+str(i+1)+' else enter N: ')
    if result=='Y':
      task_count+=1
  
  prog1=round((task_count/5)*100)
  str_prog1=str(prog1)
  print('You have completed '+str_prog1+'% of the total work')
  if (prog1==100):
    mycursor.execute("insert into data_employee values('%s','%s','COMPLETED')"%(name,done_hrs))
    mydb.commit()
    print('Please send an email to the admin concerning your completion\n')
    emails=input('Please enter the mail of the admin: ')
    myresult=mycursor.fetchall()
    data=tabulate(myresult, headers=['Project name','Done hours','Project status'])
    mail.email(emails,data)#calling function within function
    print('Done! Please exit the program.')
  else:
    print('Please complete your work as soon as possible')

    
def employee_account():
  while True:
    username=input('Please enter the username:')
    password=input('Please enter the password:')
    mycursor.execute("select password from employee where username='%s'"%username)
    row=mycursor.fetchall()
    if row==[]:
      print('Try again')
    for i in row:
      if i[0]==str(password):
        while True:
          employee_input()
      else:
        print('please try again')
        continue  
        

    
