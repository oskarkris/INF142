from socket import socket
from rich import print
from rich.prompt import Prompt
from rich.table import Table

from champlistloader import load_some_champs
from core import Champion, Match, Shape, Team
from socket import socket, timeout
import pickle
import time


def player1():
    sock1 = socket()
    sock1.connect(("localhost", 5555,))

    sock2 = socket()
    sock2.connect(('localhost', 5555))
   
    print(sock1.recv(1024).decode())
    print(sock2.recv(1024).decode())
    champ_select = pickle.loads(sock1.recv(4096))
    print(champ_select)
    champ_select = pickle.loads(sock2.recv(4096))
    print(champ_select)


    while True:
        print('new round')
        print(sock1.recv(1024).decode())
        sock1.send(input().encode())

        try:
            print(sock1.recv(1024).decode())
            continue
        except timeout:
            pass

        time.sleep(1)

        print(sock2.recv(1024).decode())
        #champ_pick = input()
        sock2.send(input().encode())
        time.sleep(1)
        try:
            print(sock2.recv(1024).decode())
            continue
        except socket.timeout:
            pass
    #champion_select = pickle.loads(sock1.recv(4096)) 
    #print(champion_select)
    #champ_pick = input()
    #sock.send(champ_pick.encode())

    #champion_select = pickle.loads(sock2.recv(4096)) 
    #print(champion_select)
    #champ_pick = input()
    #sock.send(champ_pick.encode())
player1()


"""while True: 
    champion_select = pickle.loads(sock.recv(4096)) 
    print(champion_select)
    champ_pick = input()
    sock.send(champ_pick.encode())
"""