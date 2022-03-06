from rich import print
from rich.prompt import Prompt
from rich.table import Table

from champlistloader import load_some_champs
from core import Champion, Match, Shape, Team
from socket import socket

def input_champion(prompt: str,
                   color: str,
                   champions: dict[Champion],
                   player1: list[str],
                   player2: list[str]) -> None:

    # Prompt the player to choose a champion and provide the reason why
    # certain champion cannot be selected
    while True:
        conn.send(f'[{color}]{prompt} Please select a champion:'.encode())
        champ_pick = conn.recv(1024).decode()
        match champ_pick:
            case name if name not in champions:
                conn.send(f'[{color}]The champion {name} is not available. Try again. '.encode())
            case name if name in player1:
                conn.send(f'[{color}]{name} is already in your team. Try again. '.encode())
            case name if name in player2:
                conn.send(f'[{color}]{name} is in the enemy team. Try again. '.encode())
            case _:
                player1.append(name)
                conn.send(f'[{color}]{name} has been chosen by {prompt}. '.encode())
                break

champions = load_some_champs()
player1 = []
player2 = []


sock = socket()

sock.bind(("localhost", 5555))

sock.listen()
print("The server is ready to recieve")

while True:
    #figure out how to send tables to client
    conn, _=sock.accept()

    for x in range(2):
        input_champion('Player 1', 'red', champions, player1, player2)
        input_champion('Player 2', 'blue', champions, player2, player1)
    conn.send("CLOSING".encode())
    conn.close()


    # Print a summary
