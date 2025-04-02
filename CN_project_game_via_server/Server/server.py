import socket
from _thread import *
import sys
import random

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = 'localhost'
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

currentId = "0"
pos = ["0:50,50", "1:100,100"]
roles = ['runner', 'seeker']


def assign_role():
    role = random.choice(roles)
    roles.remove(role)
    return role

def threaded_client(conn):
    global currentId, pos
    conn.send(str.encode(currentId))
    currentId = "1"

    # Assign roles
    role = assign_role()

    reply = role  # Send the role to the client
    conn.send(str.encode(reply))
    role = reply

    # Wait for the second player to connect
    while True:
        if len(pos) == 2:
            break

    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                print("Received: " + reply)
                arr = reply.split(":")
                id = int(arr[0])
                pos[id] = reply

                if id == 0: nid = 1
                if id == 1: nid = 0

                reply = pos[nid][:]
                print("Sending: " + reply)

            conn.sendall(str.encode(reply))
        except:
            break

    print("Connection Closed")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn,))
