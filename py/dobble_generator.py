# The Dobble Algorithm - www.101computing.net/the-dobble-algorithm/
import json
from random import shuffle


class Dobble_Generator:

    # absolute base path
    __base = "http://www.konwersacje.wroclaw.pl"
    # path to image folder relative to base path
    __path = "img/"
    # image file extension
    __extension = ".png"
    # number of symbols on card (n + 1)
    __symbolsPerCard = 8
    # prime number = __symbolsPerCard - 1
    __n = __symbolsPerCard - 1
    # shuffle symbols on card True/False
    __shuffleSymbolsOnCard = False
    # symbol names
    __names = []
    # symbol ids
    __ids = []
    # output cards
    __cards = []

    def __init__(self, symbolsPerCard, shuffleSymbolsOnCard):
        self.__ids = []
        self.__names = []
        self.__cards = []
        self.__n = symbolsPerCard - 1
        self.__symbolsPerCard = symbolsPerCard
        self.__shuffleSymbolsOnCard = shuffleSymbolsOnCard
        self.__numberOfCards = self.__calculate_number_of_cards()
        self.__numberOfSymbols = self.__calculate_number_of_symbols()

    def __generate_test_symbols(self):
        self.__ids = []
        self.__names = []
        for symbol in range(self.__numberOfSymbols):
            self.__ids.append(str(symbol+1))
            self.__names.append("symbol"+str(symbol+1))

    def __calculate_number_of_cards(self):
        # total number of cards that can be generated following the Dobble rules: n^2 + n+ 1 (eg.: 7^2 + 7 + 1 = 57)
        return self.__n**2 + self.__n + 1

    def __calculate_number_of_symbols(self):
        # total number of symbols needed to generated maximum number of cards: n^2 + n+ 1 (eg.: 7^2 + 7 + 1 = 57)
        return self.__n**2 + self.__n + 1

    def __calculate_first_n_plus_1_cards(self):
        # Add first set of n+1 cards (e.g. 8 cards)
        for i in range(self.__n + 1):
            # Add new card with first symbol
            self.__cards.append([1])
            # Add n+1 symbols on the card (e.g. 8 symbols)
            for j in range(self.__n):
                self.__cards[i].append((j+1) + (i*self.__n) + 1)

    def __calculate_n_sets_of_n_cards(self):
        # Add n sets of n cards
        for k in range(2, self.__n + 2):
            for i in range(self.__n):
                # Append a new card with 1 symbol
                self.__cards.append([k])
                # Add n symbols on the card (e.g. 7 symbols)
                for j in range(0, self.__n):
                    val = self.__n + 2 + i + (k+1)*j
                    while val >= self.__n + 2 + (j+1)*self.__n:
                        val = val - self.__n
                    self.__cards[len(self.__cards)-1].append(val)

    def __shuffle_cards(self):
        # Shuffle symbols on each card
        if self.__shuffleSymbolsOnCard:
            for card in self.__cards:
                shuffle(card)

    def __output_all_cards(self):
        # Output all cards
        i = 0
        for card in self.__cards:
            i += 1
            line = str(i) + " - ["
            for number in card:
                line = line + self.__ids[number-1] + ", "
            line = line[:-2] + "]"
            print(line)

    def __output_json(self):
        output = {
            'base': self.__base,
            'path': self.__path,
            'numberOfCards': self.__numberOfCards,
            'numberOfSymbols': self.__numberOfSymbols,
            'symbolsPerCard': self.__symbolsPerCard,
            'n': self.__n,
            'cards': []
        }
        # Output all cards
        i = 0
        for card in self.__cards:
            i += 1
            pics = []
            item = {
                'cardId': i,
                'pics': pics
            }
            for number in card:
                index = number - 1
                pic = {
                    'picId': self.__ids[index],
                    'picName': self.__names[index],
                    'picFile': self.__ids[index] + self.__extension
                }
                item['pics'].append(pic)
            output['cards'].append(item)
        result = json.dumps(output, sort_keys=False, indent=3)
        print(result)

    def generate_cards(self):
        self.__cards = []
        self.__generate_test_symbols()
        self.__calculate_first_n_plus_1_cards()
        self.__calculate_n_sets_of_n_cards()
        self.__shuffle_cards()
        return self.__cards

    def print_cards(self):
        self.__cards = []
        self.__generate_test_symbols()
        self.__calculate_first_n_plus_1_cards()
        self.__calculate_n_sets_of_n_cards()
        self.__shuffle_cards()
        self.__output_all_cards()

    def print_json(self):
        self.__cards = []
        self.__generate_test_symbols()
        self.__calculate_first_n_plus_1_cards()
        self.__calculate_n_sets_of_n_cards()
        self.__shuffle_cards()
        self.__output_json()
