from utils.disk_scanner import scan_dir_for_files
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
    # cards distnace in mm
    __cd = -1
    # card width
    __cw = -1
    # card height
    __ch = -1
    # card radius
    __cr = -1
    # page width in mm
    __pw = -1
    # page height in mm
    __ph = -1
    # path to dir with cards
    __path_to_dir_with_cards = None
    # path to dir with symbols
    __path_to_dir_with_symbols = None

    def __init__(self, path_to_dir_with_cards, path_to_dir_with_symbols):
        self.__colspp = 2
        self.__rowspp = 3
        self.__cardspp = self.__colspp * self.__rowspp
        self.__cd = 12
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
        self.__cw = 77
        # self.__cw = self.__pw / self.__colspp
        self.__ch = 77
        # self.__ch =  self.__ph / self.__rowspp
        self.__cr = min(self.__cw, self.__ch)
        print("Card size: %d x %d." % (self.__cw, self.__ch))
        print("Card radius: %d." % (self.__cr))

    def __get_left(self):
        total_cards_width = self.__cw * self.__colspp
        total_cards_distance = self.__cd * self.__colspp + self.__cd
        return (self.__pw - (total_cards_width + total_cards_distance)) / 2

    def __get_top(self):
        total_cards_height = self.__ch * self.__rowspp
        total_cards_distance = self.__cd * self.__rowspp
        return (self.__ph - (total_cards_height + total_cards_distance)) / 2

    def __add_page_markers(self):
        self.__pdf.image("./lib/marker.png", 0, 0)
        self.__pdf.image("./lib/marker.png", self.__pw - 1, 0)
        self.__pdf.image("./lib/marker.png", self.__pw - 1, self.__ph - 1)
        self.__pdf.image("./lib/marker.png", 0, self.__ph - 1)

    def __add_card_markers(self, cx, cy):
        ch2 = self.__ch / 2
        cx_left = cx - 45
        cy_top = cy - ch2 - 5
        cx_right = cx + 45
        cy_bottom = cy + ch2 + 5
        left = self.__get_left()
        self.__pdf.line(left, cy_top, self.__pw - left, cy_top)
        self.__pdf.line(cx_left, cy_top, cx_left - 2, cy_top + 10)
        self.__pdf.line(cx_right, cy_top, cx_right + 2, cy_top + 10)
        self.__pdf.line(left, cy_bottom, self.__pw - left, cy_bottom)
        self.__pdf.line(cx_left - 2, cy_bottom - 10, cx_left, cy_bottom)
        self.__pdf.line(cx_right + 2, cy_bottom - 10, cx_right, cy_bottom)
        print("Adding card markers for (%d, %d) markers added at (%d, %d) and (%d, %d)" %(cx, cy, cx_left, cy_bottom, cx_right, cy_bottom))

    def __add_card(self, file_path, col, row):
        center_x = self.__get_left() + self.__cd + col * (self.__cw + self.__cd) + self.__cw / 2
        center_y = self.__get_top()  + self.__cd + row * (self.__ch + self.__cd) + self.__ch / 2
        self.__add_card_markers(center_x, center_y)
        self.__pdf.image(file_path, center_x - self.__cr / 2, center_y - self.__cr/2, self.__cr)

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
            #print(col, row, text)
            pdf.image(file, page_left + col * 40,
                      page_top + row * 20 - 16, h=12)
            pdf.text(page_left + col * 40, page_top + row * 20, text)
            i += 1
            if i >= self.__cards_num:
                break

    def __add_external_pages(self, path):
        # generate all pages
        index = 0
        page_num = 0
        # top = (self.__ph - (self.__ch * self.__rowspp)) / 2
        # left = (self.__pw - (self.__cw * self.__colspp)) / 2
        left = self.__get_left()
        top  = self.__get_top()
        cards_total = len(self.__cards)
        pages_total = math.ceil(cards_total / self.__cardspp)
        # iterate thgrough all cards
        while index < cards_total:
            i = index % self.__cardspp
            # generate 6 cards per page
            if i == 0:
                page_num += 1
                self.__pdf.add_page()
                self.__add_page_markers()
                print("Generating page %d out of %d." %
                      (page_num, pages_total))
            col = i % self.__colspp
            row = math.floor(i / self.__colspp)
            px = left + col * self.__cw + self.__cw / 2
            py = top + row * self.__ch + self.__ch / 2
            file_path = path + format(index, '02d') + ".png"
            # if col == 0:
            # self.__add_card_markers(px, py)
            # self.__pdf.image(path + format(index, '02d') + ".png", px -
            #                  self.__cr / 2 + 0, py - self.__cr/2 + 0, self.__cr - 0)
            self.__add_card(file_path, col, row)
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