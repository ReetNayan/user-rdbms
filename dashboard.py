from tkinter import *
from backend import *
def dashboard(roleid, user):
    if roleid==1:
        admin_dashboard(user)
    if roleid==2:
        standard_dashboard(user)
    if roleid==3:
        moderator_dashboard(user)
def admin_dashboard(user):
    win=Toplevel()
    win.title("DASHBOARD - "+user)
    # Set the size and position of the pop-window
    w2 = 400  # width
    h2 = 300  # height
    x2 = 550  # x-position
    y2 = 300  # y-position
    win.geometry("%dx%d+%d+%d" % (w2, h2, x2, y2))
    win.resizable(False,False)

    name=Label(win,text="[ADMIN] ")
    name.pack()
    name.place(x=4,y=8)

    def showDB_pushed():
        showDB()
    
    viewLoginRecordsBttn=Button(win,text="View Database",command=showDB_pushed)
    viewLoginRecordsBttn.pack()
    viewLoginRecordsBttn.place(x=4,y=30)

    updateRoleDis=Label(win,text="Update user's role: ")
    updateRoleDis.pack()
    updateRoleDis.place(x=16,y=60)

    updateRoleUsernameDis=Label(win,text="Enter username: ")
    updateRoleUsernameDis.pack()
    updateRoleUsernameDis.place(x=16,y=90)

    updateRoleUsernameLabel=Entry(win)
    updateRoleUsernameLabel.pack()
    updateRoleUsernameLabel.place(x=16,y=120)

    userRoleDis=Label(win,text="New Role -")
    userRoleDis.pack()
    userRoleDis.place(x=8,y=150)

    newRoleVar = StringVar(win)
    newRoleVar.set("2")
    newRoleSelect = OptionMenu(win, newRoleVar, "1", "2", "3")
    newRoleSelect.pack()
    newRoleSelect.place(x=32,y=180)

    def updateButton_pushed():
        roleUpdate(updateRoleUsernameLabel.get(), newRoleVar.get())
        print("# Update successfull")

    updateBttn=Button(win,text="Update User's Role",command=updateButton_pushed)
    updateBttn.pack()
    updateBttn.place(x=90,y=160)
def standard_dashboard(user):
    win=Toplevel()
    win.title("DASHBOARD - "+user)
    # Set the size and position of the pop-window
    w2 = 400  # width
    h2 = 300  # height
    x2 = 550  # x-position
    y2 = 300  # y-position
    win.geometry("%dx%d+%d+%d" % (w2, h2, x2, y2))
    win.resizable(False,False)

    name=Label(win,text="[STANDARD USER] ")
    name.pack()
    name.place(x=4,y=8)

    def viewLoginRecords_pushed():
        viewLoginRecords()
    
    viewLoginRecordsBttn=Button(win,text="View Your Login Records",command=viewLoginRecords_pushed)
    viewLoginRecordsBttn.pack()
    viewLoginRecordsBttn.place(x=4,y=30)
def moderator_dashboard(user):
    win=Toplevel()
    win.title("DASHBOARD - "+user)
    # Set the size and position of the pop-window
    w2 = 400  # width
    h2 = 300  # height
    x2 = 550  # x-position
    y2 = 300  # y-position
    win.geometry("%dx%d+%d+%d" % (w2, h2, x2, y2))
    win.resizable(False,False)

    name=Label(win,text="[MODERATOR] ")
    name.pack()
    name.place(x=4,y=8)
    
    userDelDis=Label(win,text="User Delete - ")
    userDelDis.pack()
    userDelDis.place(x=4,y=28)

    userDelField=Entry(win)
    userDelField.pack()
    userDelField.place(x=150,y=28)

    def deleteUser_pushed():
        deleteUser(userDelField.get())
    
    def failedLoginAttempts_pushed():
        viewFailedLoginAttempts()

    viewLoginRecordsBttn=Button(win,text="Delete User",command=deleteUser_pushed)
    viewLoginRecordsBttn.pack()
    viewLoginRecordsBttn.place(x=24,y=78)

    viewFailedLoginBttn=Button(win,text="Show Failed Login Attempts",command=failedLoginAttempts_pushed)
    viewFailedLoginBttn.pack()
    viewFailedLoginBttn.place(x=24,y=150)

    

    

    
