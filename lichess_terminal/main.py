import sys
import os
import berserk
import chess

import Game

def main():

    try:
        with open("api_key.txt") as f:
            token = f.read()
        session = berserk.TokenSession(token)
        client = berserk.clients.Client(session)
        board = berserk.clients.Board(session)
    except:
        print("The API-key is either empty or wrong. Please run the command 'lichesskey' and input your API-key correctly. If you need more help, please see the instructions in the Github README: \nhttps://github.com/Cqsi/lichess_terminal#how-to-generate-a-personal-api-token")
        os._exit(0)

    # Gets your account data, e.g ["id"], ["username"]
    account_data = client.account.get()
    player_id = account_data["id"]

    # Welcome text
    print("Welcome to Lichess!\n")
    print("What kind of chess do you want to play?")
    print("1. Rapid (10+0)\n2. Classical (30+0)\n")
    num = input("Enter 1 or 2: ")
    time = 0

    if num=="1":
        time=10
    elif num=="2":
        time=30
    else:
        # This needs improvement, something like a while/for loop
        print("Something went wrong, please enter the lichess command again.")
        sys.exit()

    board.seek(time, 0)
    print("Searching after opponent...")

    for event in board.stream_incoming_events():
        if event['type'] == 'gameStart':

            print("An opponent was found!")

            isWhite = True
            color = "Black" # We set the color to the opposite color of the player
            
            if player_id != client.games.export(event['game']['id'])['players']['white']['user']['id']:
                isWhite = False
                color = "White"
                print("You're playing as black!")
                print("White's turn...")
            else:
                print("You're playing as white!")
            game = Game.Game(board, event['game']['id'], player_id, isWhite, color)
            game.start()
        
if __name__=="__main__":
    main()