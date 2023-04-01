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
        self.txt_operations = TxtOperations()

    def start(self):
        self.shuffle(self.all_cards)

        cards_on_desk = self.all_cards[0:4]
        beaten = False
        for round in range(0, 6):
            print("***************************************")
            print(f"Round{round + 1}:")
            computer_deck, person_deck = self.give_players_their_cards(round)

            # Oyun dosyaya kaydedilir.
            self.write_file_game_info(computer_deck, person_deck, round)

            for turn in range(1, 9):
                print("------------------------------------------------")
                self.show_cards_on_the_desk(cards_on_desk, beaten)
                if turn % 2 == 1:
                    cards_on_desk, beaten, playing_card = self.person_turn(beaten, cards_on_desk)
                else:
                    cards_on_desk, beaten, playing_card = self.computer_turn(beaten, cards_on_desk)

                self.save_card_info(playing_card)

            # Oyuncu skorları hesaplanır.
            self.calculate_players_score()
            # Kazanılan kartlar listesi sıfırlanır.
            self.clear_players_winned_cards()

        self.find_game_result()

    def write_file_game_info(self, computer_deck, person_deck, round):
        filename = "tur" + str(round + 1) + ".txt"
        self.txt_operations.write_txt(filename, computer_deck, person_deck)

    def save_card_info(self, playing_card):
        arr = []
        arr.append(playing_card)
        self.computer.add_cards_memory(arr)
        self.person.add_cards_memory(arr)

    def computer_turn(self, beaten, cards_on_desk):
        playing_card, is_successful = self.computer.play(cards_on_desk, beaten)
        if is_successful:
            self.computer.add_cards_memory(cards_on_desk)
            if self.is_pisti(cards_on_desk, playing_card):
                print("Pisti Yapildi.")
                self.computer.increase_num_of_pisti()
            cards_on_desk.append(playing_card)
            self.computer.add_winned_cards(cards_on_desk)
            cards_on_desk = self.clear_the_cards_on_desk()
            beaten = True
        else:
            cards_on_desk.append(playing_card)
        return cards_on_desk, beaten, playing_card

    def person_turn(self, beaten, cards_on_desk):
        playing_card, is_successful = self.person.play(cards_on_desk, beaten)
        if is_successful:
            if self.is_pisti(cards_on_desk, playing_card):
                print("Pisti yapildi.")
                self.person.increase_num_of_pisti()
            cards_on_desk.append(playing_card)
            self.person.add_winned_cards(cards_on_desk)
            cards_on_desk = self.clear_the_cards_on_desk()
            beaten = True
        else:
            cards_on_desk.append(playing_card)
        return cards_on_desk, beaten, playing_card

    def is_pisti(self, cards_on_desk, playing_card):
        if len(cards_on_desk) == 1 and playing_card[0] != "j":
            return True
        else:
            return False

    def find_game_result(self):
        self.calculate_player_with_more_card()
        if self.computer.score > self.person.score:
            print("Computer win the game.")
            print("Computer score:",self.computer.score)
            print("Person score:",self.person.score)
        elif self.computer.score < self.person.score:
            print("Person win the game.")
            print("Computer score:", self.computer.score)
            print("Person score:", self.person.score)
        else:
            print("Nobody wins the game. Draw")
            print("Computer score:", self.computer.score)
            print("Person score:", self.person.score)

    def calculate_player_with_more_card(self):
        if self.person.get_num_of_all_winned_cards() > self.computer.get_num_of_all_winned_cards():
            self.person.increase_score(3)
        elif self.person.get_num_of_all_winned_cards() < self.computer.get_num_of_all_winned_cards():
            self.computer.increase_score(3)

    def calculate_players_score(self):
        self.person.calculate_score()
        self.computer.calculate_score()

    def clear_players_winned_cards(self):
        self.person.clear_winned_cards()
        self.computer.clear_winned_cards()

    def clear_the_cards_on_desk(self):
        cards_on_desk = []
        return cards_on_desk

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
        for i in range(1, 11):
            if i == 1:
                cards.append(["a", "clover", "black", 1])
                continue
            else:
                if i == 2:
                    cards.append([str(i), "clover", "black", 2])
                else:
                    cards.append([str(i), "clover", "black", 0])
        cards.append(["j", "clover", "black", 1])
        cards.append(["q", "clover", "black", 0])
        cards.append(["k", "clover", "black", 0])

        for i in range(1, 11):
            if i == 1:
                cards.append(["a", "diamond", "red", 1])
                continue
            else:
                if i == 10:
                    cards.append([str(i), "diamond", "red", 3])
                else:
                    cards.append([str(i), "diamond", "red", 0])
        cards.append(["j", "diamond", "red", 1])
        cards.append(["q", "diamond", "red", 0])
        cards.append(["k", "diamond", "red", 0])

        for i in range(1, 11):
            if i == 1:
                cards.append(["a", "heart", "red", 1])
                continue
            else:
                cards.append([str(i), "heart", "red", 0])
        cards.append(["j", "heart", "red", 1])
        cards.append(["q", "heart", "red", 0])
        cards.append(["k", "heart", "red", 0])

        for i in range(1, 11):
            if i == 1:
                cards.append(["a", "spade", "black", 1])
                continue
            else:
                cards.append([str(i), "spade", "black", 0])
        cards.append(["j", "spade", "black", 1])
        cards.append(["q", "spade", "black", 0])
        cards.append(["k", "spade", "black", 0])
        return cards
