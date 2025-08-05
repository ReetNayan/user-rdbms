import mysql.connector
import hasher
import randWord

salt = "BestProject" # salt used to hash passwords

database = mysql.connector.connect(host="localhost", user="root", passwd="root")

mycursor = database.cursor()

mycursor.execute("SHOW DATABASES LIKE 'LoginRecordSystemDB' ;") # check if database already exists or not
getData=mycursor.fetchone() # fetch the returned data and store as a list
# if no database like this exists the list returned will be empty
if getData == None:
    #create database and table
    mycursor.execute("CREATE DATABASE LoginRecordSystemDB ;")
    mycursor.execute("USE LoginRecordSystemDB ;")
    mycursor.execute("CREATE TABLE Users \
                    (user_id INT AUTO_INCREMENT PRIMARY KEY,\
                    username VARCHAR(50) NOT NULL UNIQUE,\
                    password_hash VARCHAR(255) NOT NULL,\
                    email VARCHAR(100) NOT NULL UNIQUE,\
                    full_name VARCHAR(100),\
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);")
    mycursor.execute("CREATE TABLE LoginRecords (\
                    record_id INT AUTO_INCREMENT PRIMARY KEY,\
                    user_id INT NOT NULL,\
                    login_attempt_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\
                    ip_address VARCHAR(45),\
                    status ENUM('success', 'failure') NOT NULL,\
                    FOREIGN KEY (user_id) REFERENCES Users(user_id)\
                    );")
    mycursor.execute("CREATE TABLE FailedLoginAttempts (\
                    attempt_id INT AUTO_INCREMENT PRIMARY KEY,\
                    attempt_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\
                    ip_address VARCHAR(45),\
                    reason VARCHAR(255)\
                    );")
    mycursor.execute("CREATE TABLE UserRoles (\
                    role_id INT AUTO_INCREMENT PRIMARY KEY,\
                    role_name VARCHAR(50) NOT NULL UNIQUE,\
                    description VARCHAR(255)\
                    );")
    mycursor.execute("CREATE TABLE UserRoleMappings (\
                    mapping_id INT AUTO_INCREMENT PRIMARY KEY,\
                    user_id INT NOT NULL,\
                    role_id INT NOT NULL,\
                    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\
                    FOREIGN KEY (user_id) REFERENCES Users(user_id),\
                    FOREIGN KEY (role_id) REFERENCES UserRoles(role_id)\
                    );")
    print("# Created 5 entities - Users, LoginRecords, FailedLoginAttempts, UserRoles, UserRoleMappings")
    # insert user roles in UserRoles table
    # admin - update user roles, view db data
    # standard - can view his LoginRecords
    # moderator - delete a user, view FailedLoginAttempts
    mycursor.execute("INSERT INTO UserRoles(role_name) VALUES('admin')")
    mycursor.execute("INSERT INTO UserRoles(role_name) VALUES('standard')")
    mycursor.execute("INSERT INTO UserRoles(role_name) VALUES('moderator')")


    mycursor.execute("CREATE VIEW UserLoginRecordsView AS\
        SELECT *\
        FROM LoginRecords;")
    

    '''mycursor.execute("DELIMITER //\
\
CREATE TRIGGER FailedLoginAttempts_Overflow\
AFTER INSERT ON FailedLoginAttempts\
FOR EACH ROW\
BEGIN\
    DECLARE row_count INT;\
\
    SELECT COUNT(*) INTO row_count FROM FailedLoginAttempts;\
\
    IF row_count > 10 THEN\
        DELETE * FROM FailedLoginAttempts;\
    END IF;\
END //\
\
DELIMITER ;")'''

else:
    mycursor.execute("USE LoginRecordSystemDB ;")
    print("# USE LoginRecordSystemDB ;")
def startTransaction():
    mycursor.execute("START TRANSACTION;")
    mycursor.execute("SAVEPOINT SAVE_1;")
def rollBack():
    mycursor.execute("ROLLBACK TO SAVE_1;")

def sign_in(user,password):
    access=None
    command=""
    #looking up for the entered user

    reason="Incorrect " # to write in FailedLoginAttempts we store which one from username or email was incorrect
    if len(user) <=4:
        command = "SELECT username from Users WHERE username='"+user+"' ;"
        reason += "USERNAME"
    else:
        command = "SELECT email from Users WHERE email='"+user+"' ;"
        reason += "EMAIL"
    mycursor.execute(command)

    if mycursor.fetchone()==None:  # checking if user exists in the database
        print("# User does not exists")
        access=False
        write_FailedLoginAttempts(reason)
    else:
        command=""
        #if username/Email is correct check for true password
        if len(user) <= 4:
            command = "SELECT full_name, password_hash, user_id from Users WHERE username='" + user + "' ;"
        else:
            command = "SELECT full_name, password_hash, user_id from Users WHERE email='" + user + "' ;"

        mycursor.execute(command)
        returnedData = mycursor.fetchone()  # returned data is stored as a list in respective manner
        # like this, returnedData = ('F_Name','L_Name','password_hash','Salt')

        passwd_hash = returnedData[1]  # returned password hash is at index num 2 in returnedData
        userid = returnedData[2] # fetch the user_id for writing and editing various stuff
        hashof_psswd_entered = hasher.sha256(password, salt)  # returned salt is at index num 3 in returnedData
        
        # We hash the password entered with stored salt and compare it with original password hash
        
        if hashof_psswd_entered == passwd_hash:  # checking if stored password hash matches with the entered password hash
            access = True
            welcome(returnedData[0]) # print welcome message in which name of user is included
            
        else:
            access=False
        status = 'success' if access else 'failure' # set ENUM for LoginRecords table
        write_LoginRecords(userid, status)  # write this to LoginRecords table
    return access


def welcome(fetchedData):
    print("\nYou are "+fetchedData+"! ")
    print("Welcome to your dashboard.")

def write_LoginRecords(userid, status):
    randomIpAddr=randWord.genrtIpAddr()
    values=(userid, status, randomIpAddr)
    insert_command="INSERT INTO LoginRecords(user_id, status, ip_address) VALUES(%s, %s, %s)"
    mycursor.execute(insert_command, values)
    database.commit()

def write_FailedLoginAttempts(reason):
    values=(reason,)
    insert_command="INSERT INTO FailedLoginAttempts(reason) VALUES(%s)"
    mycursor.execute(insert_command, values)
    database.commit()

def viewLoginRecords():
    mycursor.execute("SELECT * FROM UserLoginRecordsView;")
    for (rec_id, u_id, l_att_time, ip_addr, sts) in mycursor:
        #print(u_id)
        #fname = findName(u_id)
        print("Attempted login at {} from address {} - {}".format(l_att_time, ip_addr, sts))



def register_to_database(fname, lname, username, email, passwd):

    # Now, we will retrieve the data from database based upon the
    # entered username or email and compare with the existing data in database
    # if any of those are same user will have to enter any different thing from that.
    u = None
    e = None

    command = "SELECT username from Users WHERE username='"+username+"' ;"
    mycursor.execute(command)
    u = False if mycursor.fetchone()==None else True

    command = "SELECT email from Users WHERE email='"+email+"' ;"
    mycursor.execute(command)
    e = False if mycursor.fetchone()==None else True

    if u is False and e is False:
        # Now, we check if email and user name are in
        # correct format or not. Then only we can insert
        # the data into the database.
        if len(username) <= 4 and email.find('@') > 0:

            # We now hash the password entered with given given salt and
            # store the hashed password alongwith salt
            password_hash = hasher.sha256(passwd, salt)
            values = (username, password_hash, email, fname+" "+lname)
            insert_command = "INSERT INTO Users(username, password_hash, email, full_name) VALUES(%s,%s,%s,%s)"
            mycursor.execute(insert_command, values)
            database.commit()

            print("# Registered USER -- ", username)
        else:
            print("# Username or Email is entered in wrong format. Try again!")
    elif u is True and e is False :
        print("# Username not available")
    elif e is True and u is False:
        print("# Email not available")
    elif e is True and u is True:
        print("# Username and Email already reagistered")
    else:
        print("@@! Some error occurred while registering the user")
        print("@@! Please check if all things are entered correctly")

def findUserId(identifier):
    command1 = "SELECT user_id from Users WHERE username='" + identifier + "' ;"
    command2 = "SELECT user_id from Users WHERE email='" + identifier + "' ;"
    mycursor.execute(command1)
    returnedData = mycursor.fetchone()
    if returnedData==None:
        mycursor.execute(command2)
        returnedData = mycursor.fetchone()
    return returnedData[0]

def findName(userid):
    command = "SELECT full_name from Users WHERE user_id=" + str(userid) + " ;"
    mycursor.execute(command)
    fname = ""
    for (f_name) in mycursor:
        fname=f_name
    return fname

def findRoleId(identifier):
    command1 = "SELECT user_id from Users WHERE username='" + identifier + "' ;"
    command2 = "SELECT user_id from Users WHERE email='" + identifier + "' ;"
    mycursor.execute(command1)
    returnedData = mycursor.fetchone()
    if returnedData==None:
        mycursor.execute(command2)
        returnedData = mycursor.fetchone()
    
    command3 = "SELECT role_id from UserRoleMappings WHERE user_id='" + str(returnedData[0]) + "' ;"
    mycursor.execute(command3)
    returnedData = mycursor.fetchone()
    return returnedData[0]

def AssignRoles(userid, roleid):
    checkEmpty="SELECT mapping_id from UserRoleMappings WHERE user_id='" + str(userid) + "' ;"
    mycursor.execute(checkEmpty)
    noMapping = mycursor.fetchone()

    if noMapping == None:
        print(userid,"--",roleid)
        values=(userid, roleid)
        insert_command="INSERT INTO UserRoleMappings(user_id, role_id) VALUES(%s,%s)"
        mycursor.execute(insert_command, values)
        database.commit()
        print("# Role assigned successfully")
    else:
        print("# User's role already assigned")

def showDB():
    print("------ADMIN COMMAND------")
    mycursor.execute("SELECT username, user_id from Users;")
    print("Usernames in database ---")
    print("Usernames >> User Id")
    for (u_name, u_id) in mycursor:
        print(u_name ," >> ",u_id)
    print()

    mycursor.execute("SELECT role_id, role_name from UserRoles;")
    print("Role >> Role Name")
    for (r_id, r_name) in mycursor:
        print(r_id," >> ",r_name)
    print()

    mycursor.execute("SELECT user_id, role_id from UserRoleMappings;")
    print("Role Mappings ---")
    print("User ID >> Role ID")
    for (u_id, r_id) in mycursor:
        print(u_id," >> ",r_id)

def roleUpdate(username, newrole):
    userId=findUserId(username)
    mycursor.execute("UPDATE UserRoleMappings set role_id="+str(newrole)+" where user_id="+str(userId))
    database.commit()

def deleteUser(username):
    command="SELECT username from Users WHERE username='"+username+"' ;"
    mycursor.execute(command)
    if mycursor.fetchone() == None:
        print("@@! User does not exist")
    else:
        command="DELETE FROM Users WHERE username='"+username+"' ;"
        mycursor.execute(command)

def viewFailedLoginAttempts():
    mycursor.execute("SELECT * from FailedLoginAttempts;")
    print()
    print("Failed Login Attempts ---")
    for (a_id, a_time, ip_addr, reason) in mycursor:
        print("From ADDRESS {} login attempted at {}. Reason {}".format(ip_addr, a_time, reason))