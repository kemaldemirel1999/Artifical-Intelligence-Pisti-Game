from txt_operations import TxtOperations
from player import Player

class Pisti:

    def __init__(self):
        self.J = 1
        self.KARO_10 = 3
        self.SINEK_10 = 3
        self.VALE = 1
        self.AS = 1
        self.PISTI = 10
        self.total_card = 52

    def play(self):
        for round in range(6):
            print(round)
        computer = Player(True)
        person = Player(False)

    def shuffle(self, deck):
        None
