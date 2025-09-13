import os
from card.cards_model_creator import Cards_Model_Creator
from card.card_image_creator import Card_Image_Creator

class Card_Images_Creator:
    
    def __init__(self, icons_per_card, path_to_icons_folder):
        self.__icons_per_card = icons_per_card
        self.__path_to_icons_folder = path_to_icons_folder

    def create(self, shuffle_each_card = True):
        model_creator = Cards_Model_Creator(
            self.__icons_per_card,
            self.__path_to_icons_folder,
            shuffle_each_card==shuffle_each_card
        )
        model_creator.create(shuffle_each_card)
        output_path = model_creator.get_cards_output_folder_path()
        print(f"Output path: {output_path}")
        os.makedirs(output_path)

        for index in range(model_creator.get_cards_total_num()):
            image_creator = Card_Image_Creator(
                canvas_size=1024,
                base_item_size=256,
                min_scale=0.5,
                max_scale=1.3
            )
            image_creator.create(
                model_creator.get_icon_files(index),
                f"{model_creator.get_cards_output_folder_path()}/{index:02d}.png"
            )

