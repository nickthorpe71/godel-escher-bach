from tile import Tile
import random

class Board:
    def __init__(self):
        self.tiles = [
            Tile("GO", "go"),
            Tile("Mediterranean Avenue", "property", cost=60, rent=2, house_cost=50, hotel_cost=200),
            Tile("Community Chest", "community_chest"),
            Tile("Baltic Avenue", "property", cost=60, rent=4, house_cost=50, hotel_cost=200),
            Tile("Income Tax", "tax"),
            Tile("Reading Railroad", "railroad", cost=200, rent=25),
            Tile("Oriental Avenue", "property", cost=100, rent=6, house_cost=50, hotel_cost=200),
            Tile("Chance", "chance"),
            Tile("Vermont Avenue", "property", cost=100, rent=6, house_cost=50, hotel_cost=200),
            Tile("Connecticut Avenue", "property", cost=120, rent=8, house_cost=50, hotel_cost=200),
            Tile("Jail", "jail"),
            Tile("St. Charles Place", "property", cost=140, rent=10, house_cost=100, hotel_cost=400),
            Tile("Electric Company", "utility", cost=150, rent=10),
            Tile("States Avenue", "property", cost=140, rent=10, house_cost=100, hotel_cost=400),
            Tile("Virginia Avenue", "property", cost=160, rent=12, house_cost=100, hotel_cost=400),
            Tile("Pennsylvania Railroad", "railroad", cost=200, rent=25),
            Tile("St. James Place", "property", cost=180, rent=14, house_cost=100, hotel_cost=400),
            Tile("Community Chest", "community_chest"),
            Tile("Tennessee Avenue", "property", cost=180, rent=14, house_cost=100, hotel_cost=400),
            Tile("New York Avenue", "property", cost=200, rent=16, house_cost=100, hotel_cost=400),
            Tile("Free Parking", "free_parking"),
            Tile("Kentucky Avenue", "property", cost=220, rent=18, house_cost=150, hotel_cost=600),
            Tile("Chance", "chance"),
            Tile("Indiana Avenue", "property", cost=220, rent=18, house_cost=150, hotel_cost=600),
            Tile("Illinois Avenue", "property", cost=240, rent=20, house_cost=150, hotel_cost=600),
            Tile("B&O Railroad", "railroad", cost=200, rent=25),
            Tile("Atlantic Avenue", "property", cost=260, rent=22, house_cost=150, hotel_cost=600),
            Tile("Ventnor Avenue", "property", cost=260, rent=22, house_cost=150, hotel_cost=600),
            Tile("Water Works", "utility", cost=150, rent=10),
            Tile("Marvin Gardens", "property", cost=280, rent=24, house_cost=150, hotel_cost=600),
            Tile("Go To Jail", "go_to_jail"),
            Tile("Pacific Avenue", "property", cost=300, rent=26, house_cost=200, hotel_cost=800),
            Tile("North Carolina Avenue", "property", cost=300, rent=26, house_cost=200, hotel_cost=800),
            Tile("Community Chest", "community_chest"),
            Tile("Pennsylvania Avenue", "property", cost=320, rent=28, house_cost=200, hotel_cost=800),
            Tile("Short Line", "railroad", cost=200, rent=25),
            Tile("Chance", "chance"),
            Tile("Park Place", "property", cost=350, rent=35, house_cost=200, hotel_cost=800),
            Tile("Luxury Tax", "tax"),
            Tile("Boardwalk", "property", cost=400, rent=50, house_cost=200, hotel_cost=800),
        ]

        self.chance_cards = [
            ("Advance to Go (Collect $200)", lambda player: self.advance_to_go(player)),
            ("Bank pays you dividend of $50", lambda player: self.receive_money(player, 50)),
            ("Go back 3 spaces", lambda player: self.go_back_3_spaces(player)),
            ("Go to Jail", lambda player: self.go_to_jail(player)),
            ("Pay poor tax of $15", lambda player: self.pay_money(player, 15)),
            ("Take a walk on the Boardwalk", lambda player: self.move_to_tile(player, 39)),
            ("You have been elected Chairman of the Board, pay each player $50", lambda player: self.pay_each_player(player, 50)),
        ]

        self.community_chest_cards = [
            ("Advance to Go (Collect $200)", lambda player: self.advance_to_go(player)),
            ("Bank error in your favor – Collect $200", lambda player: self.receive_money(player, 200)),
            ("Doctor's fees – Pay $50", lambda player: self.pay_money(player, 50)),
            ("Go to Jail", lambda player: self.go_to_jail(player)),
            ("Pay hospital fees of $100", lambda player: self.pay_money(player, 100)),
            ("Receive $25 consultancy fee", lambda player: self.receive_money(player, 25)),
            ("You inherit $100", lambda player: self.receive_money(player, 100)),
        ]

    def get_tile(self, position):
        return self.tiles[position % len(self.tiles)]

    def draw_chance_card(self, player):
        card = random.choice(self.chance_cards)
        card[1](player)
        return card[0]

    def draw_community_chest_card(self, player):
        card = random.choice(self.community_chest_cards)
        card[1](player)
        return card[0]

    # Card actions
    def advance_to_go(self, player):
        player.position = 0
        player.receive_money(200)

    def receive_money(self, player, amount):
        player.money += amount

    def go_back_3_spaces(self, player):
        player.position = (player.position - 3) % 40

    def go_to_jail(self, player):
        player.position = 10  # Jail position

    def pay_money(self, player, amount):
        player.money -= amount
        player.money = max(player.money, 0)

    def move_to_tile(self, player, position):
        player.position = position

    def pay_each_player(self, payer, amount):
        for player in self.players:
            if player != payer:
                payer.money -= amount
                player.money += amount
                payer.money = max(payer.money, 0)