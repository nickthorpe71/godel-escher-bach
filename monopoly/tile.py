class Tile:
    def __init__(self, name, tile_type, cost=0, rent=0, house_cost=0, hotel_cost=0):
        self.name = name
        self.tile_type = tile_type
        self.cost = cost
        self.rent = rent
        self.house_cost = house_cost
        self.hotel_cost = hotel_cost
        self.houses = 0
        self.hotels = 0

    def __repr__(self):
        return f"{self.name} ({self.tile_type})"

    def calculate_rent(self):
        if self.hotels > 0:
            return self.rent + (self.hotel_cost * self.hotels)
        else:
            return self.rent + (self.house_cost * self.houses)

    def place_house(self):
        if self.houses < 4:
            self.houses += 1
            return True
        return False

    def place_hotel(self):
        if self.houses == 4:
            self.houses = 0
            self.hotels += 1
            return True
        return False