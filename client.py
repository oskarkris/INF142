from socket import socket
from rich import print
from rich.prompt import Prompt
from rich.table import Table

from champlistloader import load_some_champs
from core import Champion, Match, Shape, Team
from socket import socket
import pickle



sock = socket()
sock.connect(("localhost",5555))
while True: #figure out how to only run this while connected to server
    #print(available_champs) #figure out how to remove rows from rich.table
    champion_select = pickle.loads(sock.recv(4096)) 
    print(champion_select)
    print(f"From Server: {champion_select}")
    champ_pick = input()
    sock.send(champ_pick.encode())

sock.close()
