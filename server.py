# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 17:01:38 2022

@author: Asus
"""
# SERVER SIDE
import socket
import threading
host = "127.0.0.1"
port = 25565

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((host,port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while (True):
        try:
            message = client.recv(1024);
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            print(f'{nickname} left the chat ')
            broadcast(f'{nickname} left the chat'.encode("ascii"))
            nicknames.remove(nickname)
            break;
def receive():
    while(True):
        client,address = server.accept()
        print(f"Connected with {str(address)}".encode("ascii"))
        
        client.send("u are connected to the host. Nickname ?".encode("ascii"))
        nickname = client.recv(1024).decode("ascii")
        nicknames.append(nickname)
        clients.append(client)
        
        print(f'{nickname} join the chat')
        broadcast(f'{nickname} join the chat'.encode("ascii"))
        client.send("U have join the chat".encode("ascii"))
        
        serverthread = threading.Thread(target=handle,args = (client,))
        serverthread.start()

print("server is listening")
receive()