class Player:
    def __init__(self, name):
        self.name = name
        self.money = 1500  # Starting money in Monopoly
        self.properties = []  # Start with no properties
        self.position = 0  # Start at the "GO" position

    def move(self, steps):
        self.position = (self.position + steps) % 40

    def update_holdings(self, tile):
        if tile.tile_type == "property" and self.money >= tile.cost:
            self.buy_property(tile)

    def buy_property(self, tile):
        self.money -= tile.cost
        self.properties.append(tile)

    def place_building(self):
        for tile in self.properties:
            if tile.place_house() and self.money >= tile.house_cost:
                self.money -= tile.house_cost
            elif tile.place_hotel() and self.money >= tile.hotel_cost:
                self.money -= tile.hotel_cost

    def pay_money(self, amount):
        self.money -= amount
        self.money = max(self.money, 0)

    def receive_money(self, amount):
        self.money += amount

    def get_total_value(self):
        return self.money + sum(tile.cost + (tile.houses * tile.house_cost) + (tile.hotels * tile.hotel_cost) for tile in self.properties)