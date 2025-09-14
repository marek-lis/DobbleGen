from bootstrap import project_root
from card.planner.planner_type import Planner_Type
from card.card_images_creator import Card_Images_Creator

creator = Card_Images_Creator(
    planner_type = Planner_Type.ADJUSTABLE_SLICE,
    icons_per_card = 8,
    path_to_icons_folder = project_root+"/lib/icons/76_letters_and_digits/"
)
creator.create(
    shuffle_each_card=True
)