from bootstrap import project_root
from card.card_images_creator import Card_Images_Creator

model = Card_Images_Creator(
    icons_per_card = 8, 
    path_to_icons_folder = project_root+"/lib/icons/76_letters_and_digits/"
)
model.create(shuffle_each_card=False)