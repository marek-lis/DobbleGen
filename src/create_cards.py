from bootstrap import project_root
from card.planner.planner_type import Planner_Type
from card.card_images_creator import Card_Images_Creator

icons_folder_name = "57_letters_pl"

creator = Card_Images_Creator(
    planner_type = Planner_Type.ADVANCED_ADJUSTABLE_SLICE,
    icons_per_card = 8,
    path_to_icons_folder = f"{project_root}/lib/icons/{icons_folder_name}/"
)
creator.create(
    shuffle_each_card=True
)