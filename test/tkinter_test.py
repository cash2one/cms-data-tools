# -*- coding:utf-8 -*-

from Tkinter import *
import time


db = {"zb" : "zb"}
ltime = {}


def login(*args):
    pwd = db.get(user.get())
    if pwd == passwd.get():
        result.set('welcome back %s!' % user.get())
    else:
        result.set('login incorrect!')


root = Tk()
root.title("Login")
Label(root, text="Login", font=("Arial", 15)).pack()

mainFrame = Frame(root)
mainFrame.grid(column=0, row=0, sticky=(N, W, E, S))
mainFrame.columnconfigure(0, weight=1)
mainFrame.rowconfigure(0, weight=1)
mainFrame.pack()

user = StringVar()
passwd = StringVar()
result = StringVar()

username = Entry(mainFrame, textvariable=user, width=10)
username.grid(column=2, row=1, sticky=(W,))
password = Entry(mainFrame, textvariable=passwd,width=10)
password.grid(column=2, row=2, sticky=(W,))

Label(mainFrame, text="Username: ").grid(column=1, row=1, sticky=E)
Label(mainFrame, text="Password: ").grid(column=1, row=2, sticky=E)

Button(mainFrame, text="Login", command=login).grid(column=3, row=3, sticky=(W, E))
Label(mainFrame, textvariable=result).grid(column=2, row=3, sticky=(W,))

for child in mainFrame.winfo_children():
    child.grid_configure(padx=10, pady=10)

username.focus()
root.bind('<Return>', login)
root.mainloop()

def newuser():
    prompt = 'login desired:'
    while True:
        name = raw_input(prompt)
        if db.has_key(name):
            prompt = 'name taken, try another: '
            continue
        else:
            break
    pwd = raw_input('password: ')
    db[name] = pwd
    ltime[name] = time.time()

def olduser():
    name = raw_input('login: ')
    pwd = raw_input('password: ')
    passwd = db.get(name)
    if pwd == passwd:
        t = time.time()
        if t - ltime[name] < 3600:
            print 'You already logged in at:<%s>' % time.ctime(ltime[name])
            ltime[name] = t
        else:
            print 'welcome back', name
    else:
        print 'login incorrect'

def showuser():
    print "%8s\t%8s" % ("user", "passwd")
    for user in db.keys():
        print "%8s\t%8s" % (user, db[user])

def deleteuser():
    user = raw_input("user name: ")
    db.pop(user, "user not exist")
    print "delete complete"


def showmenu():
    prompt = """
(N)ew User Login
(E)xisting User Login
(S)how all user
(D)elete one user
(Q)uit
Enter choice: """
    done = False
    while not done:
        chosen = False
        while not chosen:
            try:
                choice = raw_input(prompt).strip()[0].lower()
            except(EOFError, KeyboardInterrupt):
                choice = 'q'

            print '\nYou picked: [%s]' % choice
            if choice not in 'nesdq':
                print 'invalid option, try again'
            else:
                chosen = True

        if choice == 'q':done = True
        if choice == 'n':newuser()
        if choice == 'e':olduser()
        if choice == 's':showuser()
        if choice == 'd':deleteuser()
