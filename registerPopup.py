from tkinter import *
from backend import *

def register_popup():
    win=Toplevel()
    win.title("Register In...")
    # Set the size and position of the pop-window
    w2 = 400  # width
    h2 = 300  # height
    x2 = 550  # x-position
    y2 = 300  # y-position
    win.geometry("%dx%d+%d+%d" % (w2, h2, x2, y2))
    win.resizable(False,False)

    name=Label(win,text="Name : ")
    name.pack()
    name.place(x=4,y=8)

    fnameDis=Label(win,text="First Name : ")
    fnameDis.pack()
    fnameDis.place(x=50,y=8)

    fnameEntry=Entry(win)
    fnameEntry.pack()
    fnameEntry.place(x=160,y=8)

    lnameDis=Label(win,text="Last Name :")
    lnameDis.pack()
    lnameDis.place(x=50,y=30)

    lnameEntry=Entry(win)
    lnameEntry.pack()
    lnameEntry.place(x=160,y=30)

    emailDis=Label(win,text="Email ID : ")
    emailDis.pack()
    emailDis.place(x=4,y=60)

    emailEntry=Entry(win)
    emailEntry.pack()
    emailEntry.place(x=70,y=60)

    userIDDis=Label(win,text="Unique User Name :")
    userIDDis.pack()
    userIDDis.place(x=4,y=90)

    userIDEntry=Entry(win)
    userIDEntry.pack()
    userIDEntry.place(x=138,y=90)

    maxChar=Label(win,text="(Maximum 4 Characters)")
    maxChar.pack()
    maxChar.place(x=130,y=110)

    passwordDis=Label(win,text="Password : ")
    passwordDis.pack()
    passwordDis.place(x=4,y=135)

    passwordEntry=Entry(win)
    passwordEntry.pack()
    passwordEntry.place(x=75,y=135)

    userRoleDis=Label(win,text="User Role -")
    userRoleDis.pack()
    userRoleDis.place(x=4,y=208)

    userRoleVar = StringVar(win)
    userRoleVar.set("standard")
    userRole = OptionMenu(win, userRoleVar, "admin", "standard", "moderator")
    userRole.pack()
    userRole.place(x=83,y=200)


    def register_pushed():
        f_name = fnameEntry.get()
        l_name = lnameEntry.get()
        email = emailEntry.get()
        username = userIDEntry.get()
        password = passwordEntry.get()

        register_to_database(f_name,l_name,username,email,password)

        userRoleSelected = userRoleVar.get()
        userId=findUserId(username)
        if userRoleSelected == 'admin':
            AssignRoles(userId, 1)
        elif userRoleSelected == 'standard':
            AssignRoles(userId, 2)
        else:
            AssignRoles(userId, 3)

    register=Button(win,text="Register User",command=register_pushed)
    register.pack()
    register.place(x=210,y=250)

