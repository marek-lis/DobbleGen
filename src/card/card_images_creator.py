import os
from card.planner.planner_type import Planner_Type
from card.cards_model_creator import Cards_Model_Creator
from card.card_image_creator import Card_Image_Creator

class Card_Images_Creator:
    
    def __init__(self,
                 planner_type,                # planner type taken from Planner_Type
                 icons_per_card,              # number of icons per card
                 path_to_icons_folder,        # path to icons folder
                 min_scale=0.65,              # 0.50 = 50% icon's scale
                 max_scale=1.00,              # 1.00 = 100% icon's scale
                 padding_from_edge=20,        # 10 = 10 pixels from circle's edge
                 min_icon_distance=10,        # 10 = 10 pixels from other icons non transparent pixels
                 slice_distance_factor=0.60,  # 0.5 = middle of radius, 0.7 = towards card's edge
                 delta_center=20,             # 20 = +/-20px random placement of the central icon
                 delta_angle=0.2,             # 0.2 = +/-20% of angle, 0.02 = +/-2% of angle
                 delta_radius=0.1,            # 0.1 = +/-10% of radius, 0.01 = +/-1% of radius
                 max_attempts=99,             # 99 = 99 attempts to place a single icon
            ):
        self.__planner_type = planner_type
        self.__icons_per_card = icons_per_card
        self.__path_to_icons_folder = path_to_icons_folder
        self.__min_scale = min_scale
        self.__max_scale = max_scale
        self.__padding_from_edge = padding_from_edge
        self.__min_icon_distance = min_icon_distance
        self.__slice_distance_factor = slice_distance_factor
        self.__delta_center = delta_center
        self.__delta_angle = delta_angle
        self.__delta_radius = delta_radius
        self.__max_attempts = max_attempts

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
                planner_type = self.__planner_type,
                min_scale = self.__min_scale,
                max_scale = self.__max_scale,
                padding_from_edge = self.__padding_from_edge,
                min_icon_distance = self.__min_icon_distance,
                slice_distance_factor = self.__slice_distance_factor,
                delta_center = self.__delta_center,
                delta_angle = self.__delta_angle,
                delta_radius = self.__delta_radius,
                max_attempts = self.__max_attempts,
            )
            image_creator.create(
                model_creator.get_icon_files(index),
                f"{model_creator.get_cards_output_folder_path()}/{index:02d}.png"
            )

