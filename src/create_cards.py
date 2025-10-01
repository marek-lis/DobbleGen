from bootstrap import project_root
from card.planner.planner_type import Planner_Type
from card.card_images_creator import Card_Images_Creator

icons_folder_name = "57_letters_pl"

creator = Card_Images_Creator(
    planner_type = Planner_Type.ADVANCED_ADJUSTABLE_SLICES,
    icons_per_card = 8,
    path_to_icons_folder = f"{project_root}/lib/icons/{icons_folder_name}/",
    min_scale=0.65, 
    max_scale=1.25,
    padding_from_edge=50, 
    min_icon_distance=20, 
    slice_distance_factor=0.65,
    delta_center=40,
    delta_angle=0.2,
    delta_radius=0.1,
    max_attempts=99,
)
creator.create(
    shuffle_each_card=True
)