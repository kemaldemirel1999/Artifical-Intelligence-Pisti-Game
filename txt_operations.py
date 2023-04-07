import os

class TxtOperations:

    '''
        İlgili sınıf dosya işlemleri(read-write) yapmaktadır.
    '''
    def __init__(self):
        self.deck_path = os.getcwd() + "/decks/"

    def write_txt(self, filename, computer_deck, person_deck):
        file = open(self.deck_path+ filename, "w")
        file.write("Computer's Deck:\n")
        for line in computer_deck:
            info = str(line[0]) + ", "+line[1] + ", " +line[2]
            file.write(info)
            file.write("\n")
        file.write("\n************\n\n")
        file.write("Person's Deck:\n")
        for line in person_deck:
            info = str(line[0]) + ", " + line[1] + ", " + line[2]
            file.write(info)
            file.write("\n")
        file.close()





