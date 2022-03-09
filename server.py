from rich import print
from rich.prompt import Prompt
from rich.table import Table

from champlistloader import load_some_champs
from core import Champion, Match, Shape, Team
from socket import socket
import pickle
champions = load_some_champs()
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
print("The server is ready to recieve")

print_available_champs(champions)
print(available_champs)
while True:
    #figure out how to send tables to client
    conn, _=sock.accept()
    conn.send(pickle.dumps(available_champs))


    #for x in range(2):
        #input_champion('Player 1', 'red', champions, player1, player2)
        #input_champion('Player 2', 'blue', champions, player2, player1)
    conn.send("CLOSING".encode())
    conn.close()


    # Print a summary
