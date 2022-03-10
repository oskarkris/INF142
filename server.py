from ctypes import addressof
from email.headerregistry import Address
from ssl import ALERT_DESCRIPTION_BAD_CERTIFICATE_HASH_VALUE
from tracemalloc import start
from rich import print
from rich.prompt import Prompt
from rich.table import Table
from champlistloader import load_some_champs
from core import Champion, Match, Shape, Team
from socket import socket
from threading import Thread
import pickle
import time
champions = load_some_champs()

print(champions)
def print_available_champs(champions: dict[Champion]) -> None:
    global available_champs
    # Create a table containing available champions
    available_champs = Table(title='Available champions')

    # Add the columns Name, probability of rock, probability of paper and
    # probability of scissors
    available_champs.add_column("Name", style="cyan", no_wrap=True)
    available_champs.add_column("prob(:raised_fist-emoji:)", justify="center")
    available_champs.add_column("prob(:raised_hand-emoji:)", justify="center")
    available_champs.add_column("prob(:victory_hand-emoji:)", justify="center")

    # Populate the table
    for champion in champions.values():
        available_champs.add_row(*champion.str_tuple)


print_available_champs(champions)

def input_champion(prompt: str,
                   color: str,
                   champions: dict[Champion],
                   player1: list[str],
                   player2: list[str],
                   id:tuple) -> None:
    while True:
        print(id == all_connections[0])
        id.send(f'[{color}]{prompt} Please select a champion:'.encode())
        champ_pick = id.recv(1024).decode()
        match champ_pick:
            case name if name not in champions:
                id.send(f'[{color}]The champion {name} is not available. Try again. '.encode())
            case name if name in player1:
                id.send(f'[{color}]{name} is already in your team. Try again. '.encode())
            case name if name in player2:
                id.send(f'[{color}]{name} is in the enemy team. Try again. '.encode())
            case _:
                 if id == all_connections[0]:
                    id = all_connections[1]
                 else:
                    id = all_connections[0]
                 player1.append(name)                    
                 id.send(f'[{color}]{name} has been chosen by {prompt}. '.encode())
                 break

player1 = []
player2 = []

def print_match_summary(match: Match) -> None:

    EMOJI = {
        Shape.ROCK: ':raised_fist-emoji:',
        Shape.PAPER: ':raised_hand-emoji:',
        Shape.SCISSORS: ':victory_hand-emoji:'
    }

    # For each round print a table with the results
    for index, round in enumerate(match.rounds):

        # Create a table containing the results of the round
        round_summary = Table(title=f'Round {index+1}')

        # Add columns for each team
        round_summary.add_column("Red",
                                 style="red",
                                 no_wrap=True)
        round_summary.add_column("Blue",
                                 style="blue",
                                 no_wrap=True)

        # Populate the table
        for key in round:
            red, blue = key.split(', ')
            round_summary.add_row(f'{red} {EMOJI[round[key].red]}',
                                  f'{blue} {EMOJI[round[key].blue]}')
        print(round_summary)
        print('\n')

    # Print the score
    red_score, blue_score = match.score
    print(f'Red: {red_score}\n'
          f'Blue: {blue_score}')

    # Print the winner
    if red_score > blue_score:
        print('\n[red]Red victory! :grin:')
    elif red_score < blue_score:
        print('\n[blue]Blue victory! :grin:')
    else:
        print('\nDraw :expressionless:')

sock = socket()
sock.bind(("localhost", 5555))
sock.listen()
all_connections = []
print_available_champs(champions)
def start_server():
    while True:     
        global sock
        global conn
        conn, address = sock.accept()
        print('accepted', conn, 'from', address)
        all_connections.append(conn)
        Thread(target=threaded_client).start()


def threaded_client():
    if len(all_connections) !=2:
        print("Waiting for players")
        time.sleep(3)
    else:
        all_connections[0].send(("Welcome player1").encode())
        time.sleep(1)
        all_connections[1].send(("Welcome player2").encode())
        time.sleep(1)
        all_connections[0].send(pickle.dumps(available_champs))
        time.sleep(1)
        all_connections[1].send(pickle.dumps(available_champs))
        time.sleep(1)
        for x in range (2):
            input_champion('Player 1', 'red', champions, player1, player2,all_connections[0])
            input_champion('Player 2', 'blue', champions, player2, player1,all_connections[1])
start_server()    
    # Print a summary
"""
        conn.sendall(pickle.dumps(available_champs))
        for x in range(0,2):
            input_champion('Player 1', 'red', champions, player1, player2,x)
            input_champion('Player 2', 'blue', champions, player2, player1,x)
        conn.send("CLOSING".encode())
        conn.close()
"""