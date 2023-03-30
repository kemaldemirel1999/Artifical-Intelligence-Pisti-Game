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
        self.all_cards = self.get_all_cards()
        self.computer = Player(True)
        self.person = Player(False)

    def start(self):
        self.shuffle(self.all_cards)
        txt_operations = TxtOperations()
        cards_on_desk = self.all_cards[0:4]
        beaten = False
        for round in range(0, 6):
            print("*************")
            print(f"Round{round + 1}:")
            filename = "tur" + str(round + 1) + ".txt"
            computer_deck, person_deck = self.give_players_their_cards(round)
            for turn in range(1, 9):
                print("Turn:", turn)
                self.show_cards_on_the_desk(cards_on_desk, beaten)
                if turn % 2 == 1:
                    playing_card, is_successful = self.person.play(cards_on_desk, beaten)
                    if is_successful:
                        self.person.add_cards_memory(cards_on_desk)
                        if self.is_pisti(cards_on_desk):
                            print("Pisti yapildi.")
                            self.person.increase_num_of_pisti()
                        cards_on_desk.append(playing_card)
                        self.person.add_winned_cards(cards_on_desk)
                        self.clear_the_cards_on_desk(cards_on_desk)
                    else:
                        cards_on_desk.append(playing_card)
                else:
                    playing_card, is_successful = self.computer.play(cards_on_desk, beaten)
                    if is_successful:
                        self.computer.add_cards_memory(cards_on_desk)
                        if self.is_pisti(cards_on_desk):
                            print("Pisti Yapildi.")
                            self.computer.increase_num_of_pisti()
                        cards_on_desk.append(playing_card)
                        self.computer.add_winned_cards(cards_on_desk)
                        self.clear_the_cards_on_desk(cards_on_desk)
                    else:
                        cards_on_desk.append(playing_card)

                self.computer.add_cards_memory(playing_card)
                self.person.add_cards_memory(playing_card)

            # Turn is finished. If exists, next turn

            self.calculate_players_score()
            self.clear_players_winned_cards()
            print("Person Score:", self.person.score)
            print("Computer score:", self.computer.score)
            txt_operations.write_txt(filename, computer_deck, person_deck)

        self.find_game_result()

    def is_pisti(self, cards_on_desk):
        if len(cards_on_desk) == 1:
            return True
        else:
            return False

    def find_game_result(self):
        self.calculate_player_with_more_card()
        if self.computer.score > self.person.score:
            print("Computer win the game.")
        elif self.computer.score < self.person.score:
            print("Person win the game.")
        else:
            print("Nobody wins the game. Draw")

    def calculate_player_with_more_card(self):
        if self.person.get_num_of_all_winned_cards() > self.computer.get_top_card_on_desk():
            self.person.increase_score(3)
        elif self.person.get_num_of_all_winned_cards() < self.computer.get_top_card_on_desk():
            self.computer.increase_score(3)

    def calculate_players_score(self):
        self.person.calculate_score()
        self.computer.calculate_score()

    def clear_players_winned_cards(self):
        self.person.clear_winned_cards()
        self.computer.clear_winned_cards()

    def clear_the_cards_on_desk(self, cards_on_desk):
        cards_on_desk = []

    def give_players_their_cards(self, round):
        computer_deck = self.all_cards[8 * round + 4: 8 * round + 8]
        person_deck = self.all_cards[8 * round + 8: 8 * round + 12]
        self.person.set_deck(person_deck)
        self.computer.set_deck(computer_deck)
        return computer_deck, person_deck

    def shuffle(self, deck):
        random.shuffle(deck)

    def show_cards_on_the_desk(self, cards_on_the_desk, beaten):
        print("From Bottom to Top cards: ", end="")
        card_index = 0
        for card in cards_on_the_desk:
            card_info = str(card[0]) + ", " + card[1] + ", " + card[2]
            if beaten or card_index >= 3:
                print("{" + card_info + "}, ", end="")
            else:
                print("{" + "*" + "}, ", end="")
            card_index = card_index + 1
        print("")

    def get_all_cards(self):
        cards = []
        for i in range(10):
            if i == 0:
                cards.append(["a", "clover", "black"])
                continue
            else:
                cards.append([str(i), "clover", "black"])
        cards.append(["j", "clover", "black"])
        cards.append(["q", "clover", "black"])
        cards.append(["k", "clover", "black"])

        for i in range(10):
            if i == 0:
                cards.append(["a", "diamond", "red"])
                continue
            else:
                cards.append([str(i), "diamond", "red"])
        cards.append(["j", "diamond", "red"])
        cards.append(["q", "diamond", "red"])
        cards.append(["k", "diamond", "red"])

        for i in range(10):
            if i == 0:
                cards.append(["a", "heart", "red"])
                continue
            else:
                cards.append([str(i), "heart", "red"])
        cards.append(["j", "heart", "red"])
        cards.append(["q", "heart", "red"])
        cards.append(["k", "heart", "red"])

        for i in range(10):
            if i == 0:
                cards.append(["a", "spade", "black"])
                continue
            else:
                cards.append([str(i), "spade", "black"])
        cards.append(["j", "spade", "black"])
        cards.append(["q", "spade", "black"])
        cards.append(["k", "spade", "black"])
        return cards
