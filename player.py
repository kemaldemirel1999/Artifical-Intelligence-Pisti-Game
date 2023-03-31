class Player:

    def __init__(self, is_computer):
        self.deck = []
        self.score = 0
        self.is_computer = is_computer
        self.cards_memory = []
        self.winned_cards = []
        self.num_of_all_winned_cards = 0
        self.num_of_pisti = 0
        self.total_card = 52

    def play(self, cards_on_desk, beaten):
        if self.is_computer:
            deck_on_desk = cards_on_desk[:]
            if not beaten:
                deck_on_desk = cards_on_desk[3:len(cards_on_desk)]
            self.add_cards_memory(deck_on_desk)
            top_card_on_desk = self.get_top_card_on_desk(deck_on_desk)
            playing_card, index = self.computer_decision(deck_on_desk)
            self.print_deck()
            print("Computer's Played Card:", playing_card)
            self.remove_card_from_deck(index)

            return playing_card, self.is_it_successfull(top_card_on_desk, playing_card)

        else:
            self.print_deck()
            top_card_on_desk = self.get_top_card_on_desk(cards_on_desk)
            while True:
                index = int(input("Enter card index that you want to play:"))
                if self.check_deck_index_validity(index):
                    playing_card = self.deck[index]
                    self.remove_card_from_deck(index)
                    return playing_card, self.is_it_successfull(top_card_on_desk, playing_card)
                else:
                    print("Hatali Index Girildi. Tekrar Deneyiniz.")

    def remove_card_from_deck(self, index):
        del self.deck[index]

    def computer_decision(self, deck_on_desk):
        num_of_card_on_desk = len(deck_on_desk)
        cards_on_memory = self.cards_memory
        card_probabilities = self.find_card_probabilities()
        top_card_on_desk = self.get_top_card_on_desk(deck_on_desk)
        if num_of_card_on_desk > 0:
            playing_card = None
            card_found = False
            for card in self.deck:
                if card[0] == top_card_on_desk[0] and least_prob_cards.__contains__(card[0]):
                    playing_card = card
                    card_found = True
                    break
            if not card_found:
                for card in self.deck:
                    if card[0] == top_card_on_desk[0]:
                        playing_card = card
                        card_found = True
                        break
            if not card_found:
                card_probabilities = self.find_card_probabilities()
                least_prob_card = self.deck[0]
                # Olasılığın yanında puan kıyaslaması da yap.
                proper_cards_with_probabilities = []
                for card in self.deck:
                    if card_probabilities[card[0]] < card_probabilities[least_prob_card[0]]:
                        least_prob_card = card
                        break
                for card in self.deck:
                    if card_probabilities[least_prob_card[0]] == card_probabilities[card[0]]:
                        proper_cards_with_probabilities.append(card)
                # En düşük olasılıklar arasından en düşük puanlı kart seçilir.
                lowest_val_card = proper_cards_with_probabilities[0]


                playing_card = least_prob_card
            index = self.get_index_of_card(playing_card)
            return playing_card, index

        elif num_of_card_on_desk == 0:
            card_found = False
            for card in self.deck:
                if least_prob_cards.__contains__(card[0]):
                    playing_card = card
                    card_found = True
                    break
            if not card_found:
                playing_card = self.get_least_value_card()
            return None
    def sort_deck_by_value(self):
        None
    def sort_deck_by_probability(self):
        card_probabilities = self.find_card_probabilities()
        sorted_deck = self.deck.copy()


    def get_index_of_card(self, card):
        for i in range(len(self.deck)):
            if self.deck[i][0] == card[0]:
                return i
        return 0

    def print_card_probabilities(self, card_probabilities):
        print("Q:", card_probabilities["q"])
        print("J:", card_probabilities["j"])
        print("K:", card_probabilities["k"])
        print("A:", card_probabilities["a"])
        for i in range(1, 10):
            print(i, ":", card_probabilities[str(i)])

    def find_card_probabilities(self):
        count_a, count_j, count_q, count_k, digit_card_counter, remaining_total_card = self.find_num_of_played_cards()
        card_probabilities = {}
        card_probabilities["a"] = (4 - count_a) / remaining_total_card
        card_probabilities["j"] = (4 - count_j) / remaining_total_card
        card_probabilities["k"] = (4 - count_k) / remaining_total_card
        card_probabilities["q"] = (4 - count_q) / remaining_total_card

        for i in range(1, 10):
            index = str(i)
            card_probabilities[index] = (4 - digit_card_counter[index]) / remaining_total_card
        return card_probabilities

    def find_num_of_played_cards(self):
        count_a = 0
        count_j = 0
        count_q = 0
        count_k = 0
        digit_card_counter = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0}
        for card in self.cards_memory:
            card_name = card[0]
            if card_name == "a":
                count_a = count_a + 1
            elif card_name == "j":
                count_j = count_j + 1
            elif card_name == "q":
                count_q = count_q + 1
            elif card_name == "k":
                count_k = count_k + 1
            else:
                digit_card_counter[card_name] = digit_card_counter[card_name] + 1

        total = 0
        for i in range(1, 10):
            total = total + digit_card_counter[str(i)]

        remaining_total_card = self.total_card - (count_a + count_j + count_k + count_q + total)
        return count_a, count_j, count_q, count_k, digit_card_counter, remaining_total_card

    def check_deck_index_validity(self, index):
        if index < 0 or index > len(self.deck) - 1:
            return False
        else:
            return True

    def get_top_card_on_desk(self, cards_on_desk):
        if cards_on_desk is None or len(cards_on_desk) < 1:
            return None
        else:
            return cards_on_desk[len(cards_on_desk) - 1]

    def add_cards_memory(self, cards_on_desk):
        for card in cards_on_desk:
            if not self.cards_memory.__contains__(card):
                print("Adding_card:",card)
                self.cards_memory.append(card)

    def is_it_successfull(self, top_card_on_desk, playing_card):
        if top_card_on_desk is None:
            return False
        elif (top_card_on_desk[0] == playing_card[0]) or playing_card[0] == "j":
            return True
        else:
            return False

    def add_winned_cards(self, adding_winned_cards):
        for card in adding_winned_cards:
            self.winned_cards.append(card)

    def get_num_of_all_winned_cards(self):
        return self.num_of_all_winned_cards

    def calculate_score(self):
        point = 0
        for card in self.winned_cards:
            if card[0] == "j":
                point = point + 1
            elif card[0] == "10" and card[1] == "diamond":
                point = point + 3
            elif card[0] == "2" and card[1] == "clover":
                point = point + 2
            elif card[0] == "a":
                point = point + 1
        point = point + 10 * self.num_of_pisti
        self.num_of_pisti = 0
        self.score = self.score + point

    def clear_winned_cards(self):
        self.num_of_all_winned_cards = self.num_of_all_winned_cards + len(self.winned_cards)
        self.winned_cards = []

    def increase_num_of_pisti(self):
        self.num_of_pisti = self.num_of_pisti + 1

    def print_deck(self):
        print("My deck: ", end="")
        for card in self.deck:
            card_info = str(card[0]) + ", " + card[1] + ", " + card[2]
            print("{" + card_info + "}, ", end="")
        print("")

    def set_deck(self, deck):
        self.deck = deck

    def get_deck(self):
        return self.deck

    def increase_score(self, adding_score):
        self.score = self.score + adding_score
