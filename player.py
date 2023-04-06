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
        # self.print_card_memory()
        if self.is_computer:
            return self.computer_move(cards_on_desk, beaten)
        else:
            return self.person_move(cards_on_desk)

    def computer_move(self, cards_on_desk, beaten):
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

    def person_move(self, cards_on_desk):
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

    def computer_decision(self, deck_on_desk):
        top_card_on_desk = self.get_top_card_on_desk(deck_on_desk)
        if top_card_on_desk is not None:  # Masa üzerinde kart bulunduğu durumda.
            matched_cards = self.find_matched_cards(top_card_on_desk)
            if len(matched_cards) != 0:
                playing_card = matched_cards[0]
                for card in matched_cards:
                    if card[0] != "j":
                        playing_card = card
                        index = self.get_index_of_card(playing_card)
                        return playing_card, index
                index = self.get_index_of_card(playing_card)
                return playing_card, index
            else:
                # Algoritmaya göre en optimal hamle yapılmalıdır.

                # Olasılıklarına göre işlem yapılır.
                sorted_deck_by_probability, opponent_deck_probability = self.get_sorted_opponent_deck_probabilities()
                sorted_deck_by_value = self.sort_deck_by_value()

                # rakibin o an elinde en az olasılık olarak bulunan kartlar bulunur.
                least_prob_cards = []
                for card in sorted_deck_by_probability:
                    card_name = card[0]
                    if opponent_deck_probability[card_name] == opponent_deck_probability[sorted_deck_by_probability[0][0]]:
                        least_prob_cards.append(card)

                # En az olasılığı kartlar arasından en optimal olan kart seçilir.
                for i in range(len(least_prob_cards)):
                    for j in range(len(least_prob_cards)-1):
                        if least_prob_cards[j][3] > least_prob_cards[j+1][3]:
                            tmp = least_prob_cards[j]
                            least_prob_cards[j] = least_prob_cards[j+1]
                            least_prob_cards[j+1] = tmp
                least_val_and_prob_cards = least_prob_cards.copy()
                if len(least_val_and_prob_cards) > 1 and (least_val_and_prob_cards[0][0] == "a" or least_val_and_prob_cards[0][0] == "j"):
                    picked_card = least_val_and_prob_cards[0]
                    for card in least_val_and_prob_cards:
                        if card[0] == "a":
                            picked_card = card
                    index = self.get_index_of_card(card)
                    return picked_card, index
                else:
                    picked_card = least_val_and_prob_cards[0]
                    index = self.get_index_of_card(picked_card)
                    return picked_card, index


        else:  # Masa üzerinde kart bulunmamaktadır.
            # Algoritmaya göre en optimal hamle yapılmalıdır.

            # Olasılıklarına göre işlem yapılır.
            sorted_deck_by_probability, opponent_deck_probability = self.get_sorted_opponent_deck_probabilities()
            sorted_deck_by_value = self.sort_deck_by_value()

            # rakibin o an elinde en az olasılık olarak bulunan kartlar bulunur.
            least_prob_cards = []
            for card in sorted_deck_by_probability:
                card_name = card[0]
                if opponent_deck_probability[card_name] == opponent_deck_probability[sorted_deck_by_probability[0][0]]:
                    least_prob_cards.append(card)

            # En az olasılığı kartlar arasından en optimal olan kart seçilir.
            for i in range(len(least_prob_cards)):
                for j in range(len(least_prob_cards) - 1):
                    if least_prob_cards[j][3] > least_prob_cards[j + 1][3]:
                        tmp = least_prob_cards[j]
                        least_prob_cards[j] = least_prob_cards[j + 1]
                        least_prob_cards[j + 1] = tmp
            least_val_and_prob_cards = least_prob_cards.copy()

            # En uygun kartlar belirlenir ve puan durumu veya işlevsellik(Joker[J]) gibi durumlar incelenir.
            if len(least_val_and_prob_cards) > 1 and (
                    least_val_and_prob_cards[0][0] == "a" or least_val_and_prob_cards[0][0] == "j"):
                picked_card = least_val_and_prob_cards[0]
                for card in least_val_and_prob_cards:
                    if card[0] == "a":
                        picked_card = card
                index = self.get_index_of_card(card)
                return picked_card, index
            else:
                picked_card = least_val_and_prob_cards[0]
                index = self.get_index_of_card(picked_card)
                return picked_card, index

    def sort_deck_by_value(self):
        sorted_deck_by_val = self.deck.copy()
        for i in range(len(self.deck)):
            for j in range(len(self.deck)-1):
                if sorted_deck_by_val[j][3] > sorted_deck_by_val[j+1][3]:
                    tmp = sorted_deck_by_val[j]
                    sorted_deck_by_val[j] = sorted_deck_by_val[j+1]
                    sorted_deck_by_val[j+1] = tmp
        return sorted_deck_by_val

    def get_sorted_opponent_deck_probabilities(self):
        opponent_deck_prob = self.get_card_probabilities()
        opponent_deck_length = len(self.deck) - 1
        for card_name in opponent_deck_prob:
            opponent_deck_prob[card_name] *= opponent_deck_length

        unsorted_deck = self.deck.copy()
        for i in range(len(unsorted_deck)):
            for j in range(len(unsorted_deck)-1):
                if opponent_deck_prob[unsorted_deck[j][0]] > opponent_deck_prob[unsorted_deck[j+1][0]]:
                    tmp = unsorted_deck[j]
                    unsorted_deck[j] = unsorted_deck[j+1]
                    unsorted_deck[j+1] = tmp
        sorted_deck_by_probability = unsorted_deck
        return sorted_deck_by_probability, opponent_deck_prob

    def get_card_probabilities(self):
        known_cards = self.cards_memory.copy()
        for card in self.deck:
            known_cards.append(card)
        card_counter = {"a": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "j": 0, "k": 0,
                        "q": 0}
        for card in known_cards:
            card_name = card[0]
            card_counter[card_name] += 1
        num_of_unknown_cards = self.total_card - len(known_cards)
        card_probabilities = {}
        card_probabilities["a"] = round(((4 - card_counter["a"]) / num_of_unknown_cards) * 100 ,1)
        card_probabilities["j"] = round(((4 - card_counter["j"]) / num_of_unknown_cards) * 100 ,1)
        card_probabilities["k"] = round(((4 - card_counter["k"]) / num_of_unknown_cards) * 100 ,1)
        card_probabilities["q"] = round(((4 - card_counter["q"]) / num_of_unknown_cards) * 100 ,1)
        for i in range(2, 11):
            card_name = str(i)
            card_probabilities[card_name] =  round(((4 - card_counter[card_name]) / num_of_unknown_cards) * 100,1)
        return card_probabilities

    def find_matched_cards(self, top_card_on_desk):
        matched_cards = []
        for card in self.deck:
            if card[0] == top_card_on_desk[0] or card[0] == "j":
                matched_cards.append(card)
        return matched_cards

    def get_index_of_card(self, card):
        for i in range(len(self.deck)):
            if self.deck[i][0] == card[0]:
                return i
        return 0

    def print_card_memory(self):
        print("Memory:", end="")
        for card in self.cards_memory:
            print(card, ", ", end="")
        print()

    def remove_card_from_deck(self, index):
        del self.deck[index]

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
            point = point + card[3]
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
