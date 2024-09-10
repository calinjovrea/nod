import socket
import tkinter as tk
from tkinter import ttk

HOST = '172.17.252.31'
PORT = 5000

# myip.is

def ask_blockchain():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((HOST,PORT))
    server.send("BLOC".encode('utf-8'))
    print(server.recv(4096).decode('utf-8'))
    server.close()

# tkinter._test()

root = tk.Tk()
ttk.Label(root, text="NODE", padding=(30,10)).pack()
greet_button = ttk.Button(root, text='Receive Blockchain !', command=ask_blockchain).pack()
root.mainloop()