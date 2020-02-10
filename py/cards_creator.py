from fpdf import FPDF
import math


class Cards_Creator:

    # n prime number
    __n = -1
    # number of symbols per card = n + 1
    __sn = -1
    # symbol width
    __sw = -1
    # cols per page
    __colspp = -1
    # rows per page
    __rowspp = -1
    # cards per page
    __cardspp = -1
    # images list
    __files = None
    # cards list
    __cards = None
    # card width
    __cw = -1
    # card height
    __ch = -1
    # card radius
    __cr = -1
    # page width
    __pw = -1
    # page height
    __ph = -1

    def __init__(self, symbols_per_card, cards, files):
        self.__colspp = 2
        self.__rowspp = 3
        self.__cardspp = self.__colspp * self.__rowspp
        self.__n = symbols_per_card - 1
        self.__sn = symbols_per_card
        self.__files = files
        self.__cards = cards
        # A4 size is 210 x 297 mm
        self.__pw = 210
        self.__ph = 297
        self.__recalculate()

    def __init_PDF(self):
        # init pdf generation
        self.__pdf = FPDF()
        self.__pdf.set_margins(left=5, top=5, right=5)
        self.__pdf.set_compression(False)

    def __recalculate(self):
        # A4 size can contain rows x columns cards
        self.__cw = self.__pw / self.__colspp
        self.__ch = self.__ph / self.__rowspp
        self.__cr = min(self.__cw, self.__ch)
        self.__sw = self.__cr / 4
        print("Card size: %d x %d." % (self.__cw, self.__ch))
        print("Card radius: %d." % (self.__cr))

    def __add_markers(self):
        self.__pdf.image("./lib/marker.png", 0, 0)
        self.__pdf.image("./lib/marker.png", self.__pw - 1, 0)
        self.__pdf.image("./lib/marker.png", self.__pw - 1, self.__ph - 1)
        self.__pdf.image("./lib/marker.png", 0, self.__ph - 1)

    def __add_image_to_card(self, x, y, r, i, file_index):
        delta_angle = math.pi * 2 / (self.__sn - 1)
        angle = delta_angle * i
        if i < 1:
            px = x - self.__sw / 2
            py = y - self.__sw / 2
        else:
            if i % 2 == 0:
                delta = -6
            else:
                delta = 1
            px = x + ((r+delta) * math.cos(angle) - self.__sw / 2)
            py = y + ((r+delta) * math.sin(angle) - self.__sw / 2)
        self.__pdf.image(self.__files[file_index-1], px, py, self.__sw)

    def __add_card_to_pdf(self, card, col, row, r):
        for i in range(len(card)):
            px = col * self.__cw + self.__cw / 2
            py = row * self.__ch + self.__ch / 2
            self.__add_image_to_card(px, py, r, i, card[i])
        self.__pdf.image("./lib/circle.png", px - self.__cr /
                         2 + 1, py - self.__cr/2 + 1, self.__cr - 2)

    def __add_pages(self):
        # generate all pages
        index = 0
        page_num = 0
        cards_total = len(self.__cards)
        pages_total = math.ceil(cards_total / self.__cardspp)
        # iterate thgrough all cards
        while index < cards_total:
            i = index % self.__cardspp
            # generate 6 cards per page
            if i == 0:
                page_num += 1
                self.__pdf.add_page()
                self.__add_markers()
                print("Generating page %d out of %d." %
                      (page_num, pages_total))
            card = self.__cards[index]
            col = i % self.__colspp
            row = math.floor(i / self.__colspp)
            self.__add_card_to_pdf(card, col, row, self.__cr / 3)
            index += 1

    def __add_intro_page(self, pdf, files):
        cols = 5
        page_top = 50
        page_left = 15
        page_width = 200
        page_height = 270
        pdf.add_font('Font', '', "C:\Windows\Fonts\Verdana.ttf", uni=True)
        pdf.add_font('Font', 'B', "C:\Windows\Fonts\Verdana.ttf", uni=True)
        pdf.add_page()
        pdf.set_font('Font', 'B', 20)
        pdf.cell(page_width, 10, "DOBBLE",
                 border=0, ln=0, align="C")
        pdf.set_font('Font', '', 14)
        pdf.text(
            25, 25, "Oto symbole, jakie możesz napotkać na poszczególnych kartach:")
        pdf.set_font('Font', 'B', 9)
        i = 0
        for file in files:
            col = i % cols
            row = math.floor(i / cols)
            text = file.split(
                '/')[-1:][0].split('.')[-2:-1][0].replace('_', ' ')
            print(col, row, text)
            pdf.image(file, page_left + col * 40,
                      page_top + row * 20 - 16, h=12)
            pdf.text(page_left + col * 40, page_top + row * 20, text)
            i += 1

    def set_page_format(self, cols, rows):
        self.__colspp = cols
        self.__rowspp = rows
        self.__cardspp = cols * rows
        self.__recalculate()

    def generate(self, file):
        if len(self.__files) >= len(self.__cards):
            print("Generating PDF file with %d cards, %d cards per A4 page, %d symbols per card." %
                  (len(self.__cards), self.__cardspp, self.__sn))
            self.__init_PDF()
            self.__add_intro_page(self.__pdf, self.__files)
            self.__add_pages()
            self.__pdf.output(file)
