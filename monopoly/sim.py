import sys
from player import Player
from game import MonopolyGame

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 monopoly_sim.py <num_rounds>")
        sys.exit(1)

    try:
        num_rounds = int(sys.argv[1])
    except ValueError:
        print("Please provide a valid integer for the number of rounds.")
        sys.exit(1)

    # Create players
    player_names = ['Alice', 'Bob', 'Charlie', 'Diana']
    players = [Player(name) for name in player_names]

    # Initialize the game
    game = MonopolyGame(players)

    # Play the specified number of rounds
    for round_num in range(1, num_rounds + 1):
        game.play_round()
      
    game.display_holdings(round_num)

if __name__ == "__main__":
    main()