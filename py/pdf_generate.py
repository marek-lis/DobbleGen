from pdf_generator import PDF_Generator
from datetime import datetime 

path_to_output_dir = "./output/medical/"
path_to_dir_with_cards = "./output/medical/cards/"
path_to_dir_with_symbols = "./output/medical/symbols/"

now = datetime.now()
file_name = str(now.year)+""+format(now.month, '02d')+""+format(now.day, '02d')+"_" + \
    format(now.hour, '02d')+""+format(now.minute, '02d') + \
    ""+format(now.second, '02d')

pg = PDF_Generator(path_to_dir_with_cards, path_to_dir_with_symbols)
pg.set_page_format(2, 3)
pg.generate_pdf(path_to_output_dir, file_name)