from bootstrap import project_root
from card.planner.planner_type import Planner_Type
from card.card_images_creator import Card_Images_Creator
from pdf.pdf_generator import PDF_Generator

# enter directory name with icons in /lib/icons/...
icons_dir_name = "76_letters_and_digits"
# enter directory name with output in /output/...
output_dir_name = "20250914_221337_57C_8S"

path_to_output_dir = f"{project_root}/output/{output_dir_name}/"
path_to_dir_with_cards = f"{project_root}/output/{output_dir_name}/cards"
path_to_dir_with_icons = f"{project_root}/lib/icons/{icons_dir_name}/"
output_file_name = f"{output_dir_name}.pdf"

creator = Card_Images_Creator(
    planner_type = Planner_Type.ADJUSTABLE_SLICE,
    icons_per_card = 8,
    path_to_icons_folder = f"{project_root}/lib/icons/{icons_dir_name}/"
)
creator.create(
    shuffle_each_card=True
)

pg = PDF_Generator(path_to_dir_with_cards, path_to_dir_with_icons)
pg.set_page_format(2, 3)
pg.generate_pdf(path_to_output_dir, output_file_name)