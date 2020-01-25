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
    __symbols_per_card = 8
    # prime number = __symbolsPerCard - 1
    __n = __symbols_per_card - 1
    # square n
    __n2 = __n ** 2
    # shuffle symbols on card True/False
    __shuffle_symbols_on_card = False
    # symbol names
    __names = []
    # symbol ids
    __ids = []
    # output cards
    __cards = []

    def __init__(self, symbols_per_card, shuffle_symbols_on_card):
        self.__ids = []
        self.__names = []
        self.__cards = []
        self.__n = symbols_per_card - 1
        self.__n2 = self.__n ** 2
        self.__symbols_per_card = symbols_per_card
        self.__shuffle_symbols_on_card = shuffle_symbols_on_card
        self.__number_of_cards = self.__calculate_number_of_cards()
        self.__number_of_symbols = self.__calculate_number_of_symbols()

    def __generate_test_symbols(self):
        self.__ids = []
        self.__names = []
        for symbol in range(self.__number_of_symbols):
            self.__ids.append(str(symbol+1))
            self.__names.append("symbol"+str(symbol+1))

    def __calculate_number_of_cards(self):
        # total number of cards that can be generated following the Dobble rules: n^2 + n+ 1 (eg.: 7^2 + 7 + 1 = 57)
        return self.__n**2 + self.__n + 1

    def __calculate_number_of_symbols(self):
        # total number of symbols needed to generated maximum number of cards: n^2 + n+ 1 (eg.: 7^2 + 7 + 1 = 57)
        return self.__n**2 + self.__n + 1

    def __generate_header(self):
        # generate first row: 1 .. symbols count
        return [col + 1 for col in range(self.__symbols_per_card)]

    def __generate_template(self):
        # generate template matrix
        return [col + self.__symbols_per_card + 1 for col in range(self.__n2)]

    def __genereate_first_block(self):
        # generate the first block of size: n rows x symbols_per_card cols
        result = []
        row = 1
        while row < self.__symbols_per_card:
            result.append(1)
            result += [2 + self.__n * row + col for col in range(self.__n)]
            row += 1
        return result

    def __generate_second_block(self, template, block_num):
        # generate the second block of size: n rows x symbols_per_card cols
        result = []
        row = 0
        while row < self.__n:
            result.append(block_num)
            result += [template[col * self.__n + row]
                       for col in range(self.__n)]
            row += 1
        return result

    def __generate_next_block(self, template, block_num):
        # generate block_num block of size: n rows x symbols_per_card cols
        result = []
        offset = block_num - 2
        row = 0
        while row < self.__n:
            result.append(block_num)
            result += [template[(col * self.__n + (row + col * offset) %
                                 self.__n) % self.__n2] for col in range(self.__n)]
            row += 1
        return result

    def __shuffle_cards(self):
        # shuffle symbols on each card
        if self.__shuffle_symbols_on_card:
            for card in self.__cards:
                shuffle(card)

    def __split_into_chunks(self, cards):
        # split cards list into chunks of length n+1
        return [cards[i:i+self.__symbols_per_card]
                for i in range(0, len(cards), self.__symbols_per_card)]

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
            'numberOfCards': self.__number_of_cards,
            'numberOfSymbols': self.__number_of_symbols,
            'symbolsPerCard': self.__symbols_per_card,
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
        template = self.__generate_template()
        result = self.__generate_header()
        result += self.__genereate_first_block()
        result += self.__generate_second_block(template, 2)
        for i in range(self.__n-1):
            result += self.__generate_next_block(template, 2 + i + 1)
        # print(result)
        self.__cards = self.__split_into_chunks(result)
        self.__shuffle_cards()
        # print(self.__cards)
        return self.__cards

    def print_cards(self):
        self.generate_cards()
        self.__output_all_cards()

    def print_json(self):
        self.generate_cards()
        self.__output_json()
