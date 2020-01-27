from datetime import datetime
from disk_scanner import *
from cards_creator import Cards_Creator
from dobble_generator import Dobble_Generator

files = scan_dir_for_files("./lib/img/")
print("Found %d files." % (len(files)))

gen = Dobble_Generator(8, True)
cards = gen.generate_cards()

now = datetime.utcnow()
file_name = str(now.year)+"_"+format(now.month, '02d')+"_"+format(now.day, '02d')+"-" + \
    format(now.hour, '02d')+"_"+format(now.minute, '02d') + \
    "_"+format(now.second, '02d')

cc = Cards_Creator(8, cards, files)
cc.generate("./output/" + file_name + ".pdf")
