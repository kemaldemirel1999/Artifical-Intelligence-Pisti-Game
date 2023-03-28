from txt_operations import TxtOperations
from player import Player
import random


class Pisti:

    def __init__(self):
        self.J = 1
        self.DIAMOND_10 = 3
        self.CLOVER_2 = 2
        self.AS = 1
        self.PISTI = 10
        self.total_card = 52

        self.all_cards = self.get_all_cards()
        self.shuffle(self.all_cards)
        self.computer = Player(True)
        self.person = Player(False)

    def play(self):
        txt_operations = TxtOperations()
        cards_on_desk = self.all_cards[0:4]
        for round in range(0, 6):
            print("*************")
            print(f"Round{round+1}:")
            filename = "tur" + str(round + 1) + ".txt"

            computer_deck = self.all_cards[8 * round+4: 8 * round + 8]
            person_deck = self.all_cards[8 * round + 8: 8 * round + 12]
            self.person.give_deck(person_deck)
            self.computer.give_deck(computer_deck)

            for turn in range(8):
                if turn %2 == 0:    # Person Turn
                    None
                else:               # Computer Turn
                    None




            txt_operations.write_txt(filename, computer_deck, person_deck)

    def shuffle(self, deck):
        random.shuffle(deck)

    def get_all_cards(self):
        cards = []
        for i in range(10):
            if i == 0:
                cards.append(["a", "clover", "black"])
                continue
            else:
                cards.append([i, "clover", "black"])
        cards.append(["j", "clover", "black"])
        cards.append(["q", "clover", "black"])
        cards.append(["k", "clover", "black"])

        for i in range(10):
            if i == 0:
                cards.append(["a", "diamond", "red"])
                continue
            else:
                cards.append([i, "diamond", "red"])
        cards.append(["j", "diamond", "red"])
        cards.append(["q", "diamond", "red"])
        cards.append(["k", "diamond", "red"])

        for i in range(10):
            if i == 0:
                cards.append(["a", "heart", "red"])
                continue
            else:
                cards.append([i, "heart", "red"])
        cards.append(["j", "heart", "red"])
        cards.append(["q", "heart", "red"])
        cards.append(["k", "heart", "red"])

        for i in range(10):
            if i == 0:
                cards.append(["a", "spade", "black"])
                continue
            else:
                cards.append([i, "spade", "black"])
        cards.append(["j", "spade", "black"])
        cards.append(["q", "spade", "black"])
        cards.append(["k", "spade", "black"])
        return cards
