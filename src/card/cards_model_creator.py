import ast
import re
from bootstrap import project_root
from datetime import datetime
from utils.disk_scanner import fix_path
from random import shuffle
from utils.disk_scanner import scan_dir_for_files

class Cards_Model_Creator:

    def __init__(self, icons_per_card, path_to_icon_files, shuffle_each_card):
        self.__icons_per_card = icons_per_card
        self.__path_to_icon_files = path_to_icon_files
        self.__shuffle_each_card = shuffle_each_card
        self.__output_folder_path = None
        self.__icon_files = None
        self.__icon_files_total_num = None
        self.__cards_total_num = None
        self.__show_debug = True
        self.__cards_model = []

    def __debug(self, text):
        if self.__show_debug:
            print(text)

    def __create_folder_name(self):
        now = datetime.now()
        return str(now.year)+""+format(now.month, '02d')+""+format(now.day, '02d')+"_" + \
                    format(now.hour, '02d')+""+format(now.minute, '02d') + \
                    ""+format(now.second, '02d')+"_"+format(self.__cards_total_num, '0d') + \
                    "C_"+format(self.__icons_per_card, '0d')+"S"
        
    def __create_output_folder_path(self):
        print(f"Creating output folder path: {project_root}")
        self.__output_folder_path = project_root + "/output/" + self.__create_folder_name() + "/"
        print(f"Creating output folder path: {self.__output_folder_path}")
        
    def __load_template(self, shuffle_each_card):
        self.__cards_model = []
        max_value = None
        path_to_template = project_root + f"/lib/templates/{self.__icons_per_card:02d}S.txt"
        with open(path_to_template, 'r') as file:
            counter = 0
            self.__debug("Importing the following card data:")
            for line in file:
                line = line.strip()
                if line:  # skip empty lines
                    cleaned_line = re.sub(r'\b0+(\d)', r'\1', line) # remove leading 0's
                    try:
                        parsed_list = ast.literal_eval(cleaned_line)
                        if isinstance(parsed_list, list):
                            counter = counter + 1
                            if shuffle_each_card:
                                shuffle(parsed_list)
                            self.__debug(f"{counter}: {parsed_list}")
                            current_max = max(parsed_list)
                            if max_value is None or current_max > max_value:
                                max_value = current_max
                            self.__cards_model.append(parsed_list)
                        else:
                            raise ValueError(f"Wrong line format: {line}")
                    except Exception as e:
                        print(f"Error when parsing template: {line}\n{e}")
        self.__cards_total_num = counter
        self.__debug(f"Found {counter} cards.")
        self.__debug(f"The quantity of symbols needed is {max_value}.")

    def __search_for_icons(self):
        self.__debug("Importing the following symbols:")
        self.__icon_files = scan_dir_for_files(self.__path_to_icon_files)
        self.__icon_files_total_num = len(self.__icon_files)
        for icon_file in self.__icon_files:
            self.__debug(icon_file)
        self.__debug(f"Found {self.__icon_files_total_num} icons.")

    def create(self, show_debug=True):
        self.__load_template(self.__shuffle_each_card)
        self.__search_for_icons()
        self.__create_output_folder_path()

    def get_icons_per_card(self):
        return self.__icons_per_card
    
    def get_cards_model(self):
        return self.__cards_model
    
    def get_cards_total_num(self):
        return len(self.__cards_model)

    def get_icon_files(self, card_number=None):
        result = self.__icon_files
        if card_number != None:
            card_model = self.__cards_model[card_number]
            print(f"Card #: {card_number+1:02d}, card model: {card_model}")
            # tempalte values start from 1, but icon files list index starts from 0, so i-1 is the correct index:
            result = [self.__icon_files[i-1] for i in card_model]
        return result
    
    def get_output_folder_path(self):
        return self.__output_folder_path
    
    def get_cards_output_folder_path(self):
        return f"{self.__output_folder_path}/cards"


