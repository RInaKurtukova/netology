response = requests.get()


class Animals:
    weight = 0
    height = 0
    voice = None

    def __init__(self, weight, height, colour, voice):
        self.weight = weight
        self.height = height
        self.colour = colour
        self.voice = voice


class Cows(Animals):
    colour = brown
    voice = "Moo!"


class Goats(Animals):
    colour = white
    voice = "Baa!"


class Sheep(Animals):
    colour = grey
    voice = "Baaa!"


class Pigs(Animals):
    colour = pink
    voice = "Oink!"


class Ducks(Animals):
    colour = feather_brown
    voice = "Quack!"


class Geese(Animals):
    colour = feather_verywhite
    voice = "Quack!"


class Chickens(Animals):
    colour = feather_white
    voice = "Quack!"


cow_0 = Cows(200, 130, brown, "Moo!")
cow_1 = Cows(220, 140, brown, "Moo!")

duck_0 = Ducks(4, 20, feather_brown, "Quack!")

sheep_0 = Sheep(100, 90, grey, "Baa!")




