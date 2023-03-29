class Player:

    def __init__(self, is_computer):
        self.deck = []
        self.score = 0
        self.is_computer = is_computer
        self.cards_memory = []
        self.winned_cards = []

    def play(self, cards_on_desk, beaten):
        if self.is_computer:
            if beaten:
                deck_on_desk = cards_on_desk[:]
                self.add_cards_memory(deck_on_desk)
                print("Computer can see the every card:")
            else:
                deck_on_desk = cards_on_desk[3:len(cards_on_desk)]
                self.add_cards_memory(deck_on_desk)
                print("Computer cannot see every card:")

        else:
            self.print_deck()
            index = int(input("Enter card index that you want to play:"))
            top_card_on_desk = cards_on_desk[len(cards_on_desk) - 1]
            playing_card = self.deck[index]
            playing_card = self.deck[index]
            del self.deck[index]
            if self.is_it_successfull(top_card_on_desk, playing_card):
                return playing_card, True
            else:
                return playing_card, False

    def add_cards_memory(self, cards_on_desk):
        for card in cards_on_desk:
            if not self.cards_memory.__contains__(card):
                self.cards_memory.append(card)

    def is_it_successfull(self, top_card_on_desk, playing_card):
        if (top_card_on_desk[0] == playing_card[0] and top_card_on_desk[1] == playing_card[1]) or playing_card[
            0] == "j":
            return True
        else:
            return False

    def add_winned_cards(self, adding_winned_cards):
        for card in adding_winned_cards:
            self.winned_cards.append(card)

    def calculate_score(self):
        point = 0
        for card in self.winned_cards:
            if card[0] == "j":
                point = point + 1
        self.score = self.score + point

    def clear_winned_cards(self):
        self.winned_cards = []

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
