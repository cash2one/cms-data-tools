#!/usr/bin/env python

from socket import *
from Tkinter import *
import threading

HOST = '192.168.7.122'
PORT = 21568
BUFSIZE = 1024
ADDR = (HOST, PORT)




def receive():
    while True:
        data = tcpCliSock.recv(BUFSIZE)
        text.insert(END, data+"\n")




def send():

    data = content.get()
    tcpCliSock.send(data+"\r\n")
#    text.insert(END, "[client]: " + data +'\n')

root = Tk()
content = StringVar()

text = Text(root)
text.pack()
e = Entry(root, textvariable=content)
e.pack()
btn = Button(root, text="Send", command=send)
btn.pack()

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)
t = threading.Thread(target=receive)
t.setDaemon(True)
t.start()

root.mainloop()
tcpCliSock.close()


# while True:
#     data = raw_input('> ')
#     if not data:
#         break
#     tcpCliSock.send(data)
#     data = tcpCliSock.recv(BUFSIZE)
#     if not data:
#         break;
#     print data

