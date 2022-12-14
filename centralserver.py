import socket
import threading
import sys
import os
import tqdm
from database import *

connection_list=[]
name_list = []
addr_list=[]
# This list is used to remove connection from the list
clean_list = []
FORMAT="utf-8"
host=socket.gethostbyname(socket.gethostname())
ADDR=(host,3007)

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    server.bind(ADDR)
except socket.error as message:
    print('error on server')
    sys.exit()

server.listen()



def on_new_connection(conn,addr):
    connected=True
    while connected:
        request=conn.recv(4096).decode(FORMAT)
        commands = request.split(" ")
        if commands[0] == ":authenticate":
          print(commands)
          state = authenticate(commands[1], commands[2])
          if state:
            name_list.append(commands[1])
            # print(commands[3] + commands[4])
            addr_list.append(commands[3]+commands[4])
            # print(addr_list)
            clean_list.append(addr)
          conn.send(str(state).encode(FORMAT))
        elif commands[0] == ":register":
          print(commands)
          state = add_user(commands[1], commands[2])
          conn.send(str(state).encode(FORMAT))
        elif commands[0] ==":get_list":
            # conn.send(str(f'{len(addr_list)} ').encode(FORMAT))
            # msg = str(len(name_list))
            print(commands)
            msg = ""
            for idx, ele in enumerate(name_list):
                #connect to database to get name
                # conn.send(ele.encode(FORMAT))
                # msg += f"{ele}-({addr_list[idx][0]},{str(addr_list[idx][1])}) "
                msg += f"{ele}-{addr_list[idx]} "
                # msg=" ("+addr_list[idx][0]+","+str(addr_list[idx][1])+")"
            msg=msg.encode(FORMAT)
            conn.send(msg)
        elif commands[0] == ":disconnect":
            print(addr," disconnected!")
            connection_list.remove(conn)
            # print(name_list)
            # print(addr_list.index(addr))
            clean_idx = clean_list.index(addr)
            clean_list.pop(clean_idx)
            name_list.pop(clean_idx)
            addr_list.pop(clean_idx)
            print("Total connection: ",len(connection_list))
            return
        elif request=="file.msg":
            receiver(conn)
            continue



# file receiving
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
def receiver(client_socket):
    # receive the file infos
    # receive using client socket, not server socket
    received = client_socket.recv(BUFFER_SIZE).decode()                        #HERER
    print(received)
    filename, filesize = received.split(SEPARATOR)
    # remove absolute path if there is
    filename = os.path.basename(filename)
    # convert to integer
    filesize = int(filesize)
    # start receiving the file from the socket
    # and writing to the file stream
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)

    new_filename="new"+filename

    with open(new_filename, "wb") as f:
        while True:
            # read 1024 bytes from the socket (receive)
            bytes_read = client_socket.recv(BUFFER_SIZE)                           #HERER
            if  len(bytes_read)!=BUFFER_SIZE:    
                # nothing is received
                # file transmitting is done
                f.close()
                break
            # write to the file the bytes we just received
            print(len(bytes_read))
            f.write(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))
    print("file rec done") 
    return
    # close the client socket
    #client_socket.close()
    # close the server socket
    
#file receiving  
    


print("server is running")
while True:
    # toggle = input()
    # print(toggle)
    # if toggle == 1:
    #   server.close()
    conn,addr=server.accept()
    connection_list.append(conn)
    print("HERE")
    # addr_list.append(addr)
    # print(addr_list)
    print("New connection [",addr,"] connected!\n")
    print("Total connection: ",len(connection_list))
    thread=threading.Thread(target=on_new_connection,args=(conn,addr,))
    thread.start()
