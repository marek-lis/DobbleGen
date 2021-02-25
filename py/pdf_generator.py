from disk_scanner import *
from fpdf import FPDF
import math
import os

class PDF_Generator:

    # card images list
    __symbols = None
    # number of files with card images
    __symbols_num = -1
    # card images list
    __cards = None
    # number of files with card images
    __cards_num = -1
    # cols per page
    __colspp = -1
    # rows per page
    __rowspp = -1
    # cards per page
    __cardspp = -1
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
    # path to dir with cards
    __path_to_dir_with_cards = None
    # path to dir with symbols
    __path_to_dir_with_symbols = None

    def __init__(self, path_to_dir_with_cards, path_to_dir_with_symbols):
        self.__colspp = 2
        self.__rowspp = 3
        self.__cardspp = self.__colspp * self.__rowspp
        # A4 size is 210 x 297 mm
        self.__pw = 210
        self.__ph = 297
        self.__path_to_dir_with_cards = path_to_dir_with_cards
        self.__path_to_dir_with_symbols = path_to_dir_with_symbols
        self.__recalculate()

    def __scan_symbols(self, path_to_dir_with_symbols):
        self.__symbols = scan_dir_for_files(path_to_dir_with_symbols)
        self.__symbols_num = len(self.__symbols)
        print("Found %d symbols." % (self.__symbols_num))

    def __scan_cards(self, path_to_dir_with_cards):
        self.__cards = scan_dir_for_files(path_to_dir_with_cards)
        self.__cards_num = len(self.__cards)
        print("Found %d cards." % (self.__cards_num))

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
        print("Card size: %d x %d." % (self.__cw, self.__ch))
        print("Card radius: %d." % (self.__cr))

    def __add_markers(self):
        self.__pdf.image("./lib/marker.png", 0, 0)
        self.__pdf.image("./lib/marker.png", self.__pw - 1, 0)
        self.__pdf.image("./lib/marker.png", self.__pw - 1, self.__ph - 1)
        self.__pdf.image("./lib/marker.png", 0, self.__ph - 1)

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

    def __add_external_pages(self, path):
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
            col = i % self.__colspp
            row = math.floor(i / self.__colspp)
            px = col * self.__cw + self.__cw / 2
            py = row * self.__ch + self.__ch / 2
            self.__pdf.image(path + format(index, '02d') + ".png", px -
                             self.__cr / 2 + 1, py - self.__cr/2 + 1, self.__cr - 2)
            index += 1

    def set_page_format(self, cols, rows):
        self.__colspp = cols
        self.__rowspp = rows
        self.__cardspp = cols * rows
        self.__recalculate()

    def generate_pdf(self, path, output_file_name):
        self.__scan_cards(self.__path_to_dir_with_cards)
        self.__scan_symbols(self.__path_to_dir_with_symbols)
        if self.__cards_num > 0:
            print("Generating PDF file with %d cards, %d cards per A4 page." % (self.__cards_num, self.__cardspp))
            self.__init_PDF()
            if self.__symbols_num > 0:
                self.__add_intro_page(self.__pdf, self.__symbols)
            if self.__cards_num > 0:
                self.__add_external_pages(path + "cards/")
            self.__pdf.output(path + output_file_name + ".pdf")