from txt_operations import TxtOperations
from player import Player
import random


class Pisti:
    '''
        Pisti oyununun kontrol edildiği class'dır.
    '''
    def __init__(self):
        self.all_cards = self.get_all_cards() # Oyun kartları oluşturulur.
        self.computer = Player(True) # Bilgisayar oyuncusu Player içerisine True verilince oluşturulmuştur olur.
        self.person = Player(False) # İnsan olan oyuncu Player içerisine True verilince oluşturulmuş olur.
        self.txt_operations = TxtOperations() # Dosya işlemleri için kullanılacaktır.
        self.latest_winner = "" # Yerdeki kartları en son alan kişiyi temsil eder.

    def start(self):
        self.shuffle(self.all_cards) # İskambil kartlarını rastgele olacak şekilde karıştırır.
        cards_on_desk = self.all_cards[0:4]
        self.save_card_info(cards_on_desk[3])
        beaten = False # Yerdeki kapalı ilk 3 kartın gösterilip gösterilmeyeceğini belirler.
        for round in range(0, 6):
            print("***************************************")
            print(f"Round{round + 1}:")
            computer_deck, person_deck = self.give_players_their_cards(round) # Oyunculara kartlar dağıtılır.
            self.write_file_game_info(computer_deck, person_deck, round) # Oyun dosyaya kaydedilir.
            for turn in range(1, 9):
                print("------------------------------------------------")
                self.show_cards_on_the_desk(cards_on_desk, beaten)
                if turn % 2 == 1:
                    # Oyunu oynayan kişinin sırasıdır.
                    cards_on_desk, beaten, playing_card = self.person_turn(beaten, cards_on_desk)
                else:
                    # Bilgisarın sırasıdır.
                    cards_on_desk, beaten, playing_card = self.computer_turn(beaten, cards_on_desk)

                # Oynanan kart bilgisayarın hamlesini optimize etmek için kullanılacaktır
                # Daha iyi sonuçlar almak için bilgisayarın hafızasına kayıt edilecektir.
                self.save_card_info(playing_card)

            # Oyuncu skorları hesaplanır.
            self.calculate_players_score()
            # Kazanılan kartlar listesi sıfırlanır.
            self.clear_players_winned_cards()

        # Oyun sonunda masada kalan kartların toplam puanı hesaplanır
        point = 0
        for card in cards_on_desk:
            point = point + card[3]
        # Yerde kalan kartların puanı hesaplandıktan sonra yerdeki kartları en son kazanan oyuncuya bu puan verilir.
        if self.latest_winner == "computer":
            self.computer.add_winned_cards(cards_on_desk)
            self.computer.increase_score(point)
            self.computer.num_of_all_winned_cards += len(cards_on_desk)
        elif self.latest_winner == "person":
            self.person.add_winned_cards(cards_on_desk)
            self.person.increase_score(point)
            self.person.num_of_all_winned_cards += len(cards_on_desk)
        # Oyun sonucu hesaplanır.
        self.find_game_result()


    def computer_turn(self, beaten, cards_on_desk):
        # Bilgisayar hamlesini yapar. Oynanılan kart ve hamlenin başarılı olup olmadığı bilgisi elde edilir.
        playing_card, is_successful = self.computer.play(cards_on_desk, beaten)

        if is_successful: # Hamle başarılı ise gerekli işlemler yapılır.
            self.computer.add_cards_memory(cards_on_desk) # Oyun masasında yerdeki kartlar bilgisayar hafızasına kaydedilir.
            if self.is_pisti(cards_on_desk, playing_card): # Eğer pişti ise
                print("Pisti Yapildi.")
                self.computer.increase_num_of_pisti() # yapılan pişti sayısı artırılır.
            cards_on_desk.append(playing_card) # oynanılan masaya eklenir.
            self.computer.add_winned_cards(cards_on_desk) # yerdeki kartlar kazanılan kartlar listesine eklenir.
            cards_on_desk = self.clear_the_cards_on_desk() # yerdeki kartlar masadan temizlenir.
            beaten = True # ilk turda 3ü kapalı 1i açık kart durumu için kullanılır. Hamle başarılı olduğundan 'true' olur.
            self.latest_winner = "computer"
        else:
            cards_on_desk.append(playing_card) # en son oynanılan kart masaya eklenir.
        return cards_on_desk, beaten, playing_card

    def person_turn(self, beaten, cards_on_desk):
        # Oynanılan kart ve hamlenin başarılı olup olmadığı bilgisi elde edilir.
        playing_card, is_successful = self.person.play(cards_on_desk, beaten)
        if is_successful:
            if self.is_pisti(cards_on_desk, playing_card):
                print("Pisti yapildi.")
                self.person.increase_num_of_pisti() # Yapılan pişti sayısı artırılır.
            cards_on_desk.append(playing_card) # kart oyun masasına eklenir.
            self.person.add_winned_cards(cards_on_desk) # masadaki kartlar kazanılan kartlara eklenir.
            cards_on_desk = self.clear_the_cards_on_desk() # oyun masası temizlenir
            beaten = True # ilk turda 3ü kapalı 1i açık kart durumu için kullanılır. Hamle başarılı olduğundan 'true' olur.
            self.latest_winner = "person"
        else:
            cards_on_desk.append(playing_card) # en son oynanılan kart masaya eklenir.
        return cards_on_desk, beaten, playing_card

    # Pisti olup olmadığı kontrol edilir.
    def is_pisti(self, cards_on_desk, playing_card):
        if len(cards_on_desk) == 1 and playing_card[0] != "j":
            return True
        else:
            return False

    # Her oyuncunun destesi dosyaya yazılır
    def write_file_game_info(self, computer_deck, person_deck, round):
        filename = "tur" + str(round + 1) + ".txt"
        self.txt_operations.write_txt(filename, computer_deck, person_deck)

    # İlgili kart veya kartlar oyuncunun hafızasına kaydedilir.
    def save_card_info(self, playing_card):
        arr = [playing_card]
        self.computer.add_cards_memory(arr)
        self.person.add_cards_memory(arr)

    # Oyun sonucu hesaplanır. Oyuncuların puanları ve kazanan kişi belirlenir.
    def find_game_result(self):
        self.calculate_player_with_more_card()
        if self.computer.score > self.person.score:
            print("Computer win the game.")
            print("Computer score:", self.computer.score)
            print("Person score:", self.person.score)
        elif self.computer.score < self.person.score:
            print("Person win the game.")
            print("Computer score:", self.computer.score)
            print("Person score:", self.person.score)
        else:
            print("Nobody wins the game. Draw")
            print("Computer score:", self.computer.score)
            print("Person score:", self.person.score)

    # Oyun sonunda daha fazla karta sahip olan oyuncu 3 puan kazanır
    def calculate_player_with_more_card(self):
        if self.person.get_num_of_all_winned_cards() > self.computer.get_num_of_all_winned_cards():
            self.person.increase_score(3)
        elif self.person.get_num_of_all_winned_cards() < self.computer.get_num_of_all_winned_cards():
            self.computer.increase_score(3)

    # Oyuncuların puanları hesaplanır.
    def calculate_players_score(self):
        self.person.calculate_score()
        self.computer.calculate_score()

    # Her tur sonunda, oyuncuların kazandığı kartları siler.
    def clear_players_winned_cards(self):
        self.person.clear_winned_cards()
        self.computer.clear_winned_cards()

    # Oyun masasındaki kartları temizler.
    def clear_the_cards_on_desk(self):
        cards_on_desk = []
        return cards_on_desk

    # Oyunculara her turda kartların dağıtılmasını sağlar.
    def give_players_their_cards(self, round):
        computer_deck = self.all_cards[8 * round + 4: 8 * round + 8]
        person_deck = self.all_cards[8 * round + 8: 8 * round + 12]
        self.person.set_deck(person_deck)
        self.computer.set_deck(computer_deck)
        return computer_deck, person_deck

    # Oyun kartların rastgele olacak şekilde karıştırır.
    def shuffle(self, deck):
        random.shuffle(deck)

    # Masa üzerindeki kartları konsolda gösterir. En alttaki karttan en yukarıya doğru göstermektedir.
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

    # Kart destesini oluşturur.
    # İlgili kartların puanları atanır.
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
