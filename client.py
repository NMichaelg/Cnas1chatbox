# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 17:38:20 2022

@author: Asus
"""

import socket
import threading

nickname = input("Choose a nickname : ")

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('127.0.0.1', 25565))

def receive():
    while (True):
        try:
            message = client.recv(1024).decode("ascii")
            if message == 'u are connected to the host. Nickname ?' :
                client.send(nickname.encode('ascii')) 
            else :
                print(message)
        except:
            print("Error server corrupt or sth")
            client.close()
            break

def write():
    while (True):
        message = f'{nickname}: {input("")}'
        client.send(message.encode("ascii"))
        
recieve_thread  = threading.Thread(target=receive)
recieve_thread.start()

write_thread  = threading.Thread(target=write)
write_thread.start()