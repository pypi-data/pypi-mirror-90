import sqlite3
import secrets

class Basic():
    __connection = None
    __c = None

    def __init__(self, filename):
        self.username = None
        self.filename = filename

        global __connection
        global __c

        __connection = sqlite3.connect("{}.db".format(filename))
        __c = __connection.cursor()
        __c.execute("""CREATE TABLE IF NOT EXISTS account (
            username text,
            password text
        )
        """)
        __connection.commit()

    def signup(self, username=None, password=None, autotask=False):
        global __c
        global __connection
        if autotask == False:
            __c.execute("SELECT * FROM account")
            users = __c.fetchall()
            __connection.commit()
            users = [i[0] for i in users]

            if username not in users:
                __c.execute("INSERT INTO account VALUES(?,?)", (username, password))
                __connection.commit()
                return True
            else:
                return False
        else:
            username1 = input("Please make a username: ")
            password1 = input("Please make a password for security: ")

            __c.execute("SELECT * FROM account")
            users = __c.fetchall()
            __connection.commit()

            users = [i[0] for i in users]

            if username1 in users:
                while True:
                    username1 = input("The username you entered is already in use. Please make another one: ")
                    if username1 not in users:
                        break

            print("This username is perfect")

            __c.execute("INSERT INTO account VALUES(?,?)", (username1, password1))
            __connection.commit()
            self.username = username1
            return True

    def login(self, username=None, password=None, autotask=False):
        global __c
        global __connection
        if not autotask:
            __c.execute("SELECT * FROM account")
            users = __c.fetchall()
            __connection.commit()

            permission = False
            for i in users:
                if (i[0] == username) and (i[1] == password):
                    permission = True
                    break
            return permission
        else:
            username1 = input("Please enter your username: ")
            self.username = username1
            password1 = input("Please enter your password: ")
            __c.execute("SELECT * FROM account")
            users = __c.fetchall()
            __connection.commit()

            permission = False
            for i in users:
                if (i[0] == username1) and (i[1] == password1):
                    permission = True
                    break
            return permission

    def deluser(self, username=None, password=None, autotask=False):
        global __c
        global __connection
        test = Basic(self.filename)
        if autotask == False:
            if test.login(username, password):
                __c.execute("DELETE FROM account WHERE username = '{}'".format(username))
                __connection.commit()
                return True
            else:
                return False
        else:
            username = input("Please enter your username: ")
            self.username = username
            password = input("Please enter your password for confirmation: ")
            if test.login(username, password):
                password = input("Please enter your password again for confirmation: ")
                if test.login(username, password):
                    global username1
                    username1 = username
                    __c.execute("DELETE FROM account WHERE username = '{}'".format(username))
                    __connection.commit()
                    return True
                else:
                    return False
            else:
                return False
    
    def usernames(self):
        global __c
        global __connection

        __c.execute("SELECT * FROM account")
        lst = __c.fetchall()
        __connection.commit()

        lst = [i[0] for i in lst]
        return lst

    def secure(self):
        global __connection
        __connection.close()

class ExtraPass():
    __connection = None
    __c = None

    def __init__(self, filename):
        self.filename = filename
        self.username = None

        global __connection
        global __c

        __connection = sqlite3.connect("{}.db".format(filename))
        __c = __connection.cursor()
        __c.execute("""CREATE TABLE IF NOT EXISTS account (
            username text,
            password text,
            extra text
        )""")

    def login(self, username=None, password=None, extra=None, autotask=False):
        global __connection
        global __c

        if autotask == False:
            __c.execute("SELECT * FROM account")
            lst = __c.fetchall()
            __connection.commit()

            permission = False
            for i in lst:
                if (i[0] == username) and (i[1] == password) and (i[2] == extra):
                    permission = True
                    break

            return permission
        else:
            username = input("Please enter your username: ")
            password = input("Please enter your password: ")
            extra = input("Please enter the extra layer of password you added: ")

            __c.execute("SELECT * FROM account")
            lst = __c.fetchall()
            __connection.commit()

            permission = False
            for i in lst:
                if (i[0] == username) and (i[1] == password) and (i[2] == extra):
                    permission = True
                    break
            if permission:
                self.username = username
            return permission

    def signup(self, username=None, password=None, extra=None, autotask=False):
        global __connection
        global __c

        if autotask == False:
            __c.execute("SELECT * FROM account")
            lst = __c.fetchall()
            __connection.commit()

            lst = [i[0] for i in lst]

            if username in lst:
                return False
            else:
                __c.execute("INSERT INTO account VALUES ('{}', '{}', '{}')".format(username, password, extra))
                __connection.commit()
                return True
        else:
            username = input("Please make a username: ")
            password = input("Please make a password: ")
            extra = input("Please enter another password that can be different for extra layer of security: ")

            __c.execute("SELECT * FROM account")
            lst = __c.fetchall()
            __connection.commit()

            lst = [i[0] for i in lst]

            if username in lst:
                while True:
                    username = input("The username you entered is already in use. Please enter another one: ")
                    if username not in lst:
                        break
                    else:
                        continue
            print("This username is perfect!")

            __c.execute("INSERT INTO account VALUES ('{}', '{}', '{}')".format(username, password, extra))
            __connection.commit()
            self.username = username
            return True


    def deluser(self, username=None, password=None, extra=None, autotask=False):
        global __c
        global __connection

        test = ExtraPass(self.filename)
        if autotask == False:
            if test.login(username, password, extra):
                __c.execute("DELETE FROM account WHERE username = '{}'".format(username))
                __connection.commit()
                return True
            else:
                return False
        else:
            username = input("Please enter your username: ")
            password = input("Please enter your password for confirmation: ")
            extra = input("Please enter the password you gave for extra layer (Password 2): ")

            if test.login(username, password, extra):
                global username1
                username1 = username
                __c.execute("DELETE FROM account WHERE username = '{}'".format(username))
                __connection.commit()

                self.username = username
                return True
            else:
                return False

    def usernames(self):
        global __c
        global __connection

        __c.execute("SELECT * FROM account")
        lst = __c.fetchall()
        __connection.commit()

        lst = [i[0] for i in lst]
        return lst

    def secure(self):
        global __connection
        __connection.close()

def passgen(len=10, caplock="mix"):
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "h", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    symbols = ["@", "#", "%", "!", "*", ">", "<", "$"]

    generartor = secrets.SystemRandom()
    result = []
    for i in range(len):
        a = generartor.choice(letters)
        if caplock == True:
            a = a.upper()
        elif caplock == False:
            a = a.lower()
        else:
            pass
        result.append(a)

    result.append(generartor.choice(symbols))

    for i in range(4):
        a = generartor.choice(numbers)
        result.append(a)


    result = [str(i) for i in result]

    return "".join(result)