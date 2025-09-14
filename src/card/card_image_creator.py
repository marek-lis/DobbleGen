from card.planner.planner_type import Planner_Type
from card.planner.planner_factory import Planner_Factory
from card.generator.card_image_generator import Card_Image_Generator

class Card_Image_Creator:
    def __init__(self, 
                 planner_type=Planner_Type.IDEAL_SLICE, # RANDOM, IDEAL_SLICE, ADJUSTABLE_SLICE
                 canvas_size=1024,                      # 1024 = card's size of 1024x1024px
                 base_item_size=256,                    # 256 = icon's size of 256x256px
                 min_scale=0.5,                         # 0.5 = 50% icon's scale
                 max_scale=1.0,                         # 1.0 = 100% icon's scale
                 padding_from_edge=10,                  # 10 = 10 pixels from circle's edge
                 delta_center=20,                       # 20 = +/-20px random placement of the central icon
                 delta_angle=0.2,                       # 0.2 = +/-20% of angle, 0.02 = +/-2% of angle
                 delta_radius=0.1,                      # 0.1 = +/-10% of radius, 0.01 = +/-1% of radius
                 slice_distance_factor=0.6,             # 0.5 = middle of radius, 0.7 = towards card's edge
                 max_attempts=50,                       # 50 = 50 attempts to place a single icon
            ):
        
        match planner_type:
            case Planner_Type.RANDOM:
                self.planner = Planner_Factory.create(
                    Planner_Type.RANDOM,
                    canvas_size=1024,
                    # base_item_size=256,
                    min_scale=0.5,
                    max_scale=1.0,
                    padding_from_edge=10,
                    slice_distance_factor=0.6,
                    max_attempts=99,
                )

            case Planner_Type.IDEAL_SLICE:
                self.planner = Planner_Factory.create(
                    Planner_Type.IDEAL_SLICE,
                    canvas_size=1024,
                    base_item_size=256,
                    min_scale=0.5,
                    max_scale=1.0,
                    padding_from_edge=10,
                    slice_distance_factor=0.6,
                    max_attempts=99,
                )

            case Planner_Type.ADJUSTABLE_SLICE:
                self.planner = Planner_Factory.create(
                    Planner_Type.ADJUSTABLE_SLICE,
                    canvas_size=1024,
                    base_item_size=256,
                    min_scale=0.5,
                    max_scale=1.0,
                    padding_from_edge=10,
                    slice_distance_factor=0.6,
                    delta_center=delta_center,
                    delta_angle=delta_angle,
                    delta_radius=delta_radius,
                    max_attempts=99,
                )
        
        self.generator = Card_Image_Generator(canvas_size=canvas_size)

    def create(self, 
               icon_files, 
               output_path
            ):
        placements = self.planner.plan(icon_files)
        self.generator.generate(placements, output_path)
