import random
import matplotlib.pyplot as plt
from player import Player
from board import Board

class MonopolyGame:
    def __init__(self, players):
        self.players = players
        self.board = Board()
        self.board.players = players  # For player-related card actions

    def roll_dice(self):
        return random.randint(1, 6) + random.randint(1, 6)

    def play_round(self):
        for player in self.players:
            steps = self.roll_dice()
            player.move(steps)
            current_tile = self.board.get_tile(player.position)
            if current_tile.tile_type == "property" and current_tile not in player.properties:
                if player.money >= current_tile.cost:
                    player.buy_property(current_tile)
            elif current_tile.tile_type == "tax":
                player.pay_money(current_tile.cost)
            elif current_tile.tile_type == "go_to_jail":
                player.position = 10  # Move to Jail
            elif current_tile.tile_type == "community_chest":
                card_message = self.board.draw_community_chest_card(player)
                print(f"{player.name} drew Community Chest card: {card_message}")
            elif current_tile.tile_type == "chance":
                card_message = self.board.draw_chance_card(player)
                print(f"{player.name} drew Chance card: {card_message}")
            player.place_building()

    def display_holdings(self, round_num):
        names = [player.name for player in self.players]
        total_values = [player.get_total_value() for player in self.players]

        plt.figure(figsize=(10, 6))
        plt.bar(names, total_values, color='blue', label='Total Value')

        plt.xlabel('Players')
        plt.ylabel('Holdings')
        plt.title(f'Player Holdings After Round {round_num}')
        plt.legend()
        plt.show()