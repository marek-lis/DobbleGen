from datetime import datetime
from disk_scanner import *
from cards_creator import Cards_Creator
from dobble_generator import Dobble_Generator

symbols_per_card = 8

files = scan_dir_for_files("./lib/img/")
files_num = len(files)
print("Found %d files." % (files_num))

gen = Dobble_Generator(8, True)
cards = gen.generate_cards()

now = datetime.now()
file_name = str(now.year)+""+format(now.month, '02d')+""+format(now.day, '02d')+"_" + \
    format(now.hour, '02d')+""+format(now.minute, '02d') + \
    ""+format(now.second, '02d')+"_"+format(files_num, '0d') + \
    "C_"+format(symbols_per_card, '0d')+"S"

cc = Cards_Creator(8, cards, files)
cc.set_page_format(2, 3)
cc.generate("./output/" + file_name + ".pdf")
