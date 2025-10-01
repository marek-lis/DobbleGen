from card.planner.planner_type import Planner_Type
from card.planner.planner_factory import Planner_Factory
from card.generator.card_image_generator import Card_Image_Generator

class Card_Image_Creator:
    def __init__(self, 
                 planner_type=Planner_Type.ADVANCED_REGULAR_SLICES, # RANDOM, IDEAL_SLICE, ADJUSTABLE_SLICE
                 canvas_size=1024,                                  # 1024 = card's size of 1024x1024px
                 base_item_size=256,                                # 256 = icon's size of 256x256px
                 min_scale=0.65,                                    # 0.50 = 50% icon's scale
                 max_scale=1.00,                                    # 1.00 = 100% icon's scale
                 padding_from_edge=20,                              # 10 = 10 pixels from circle's edge
                 min_icon_distance=10,                              # 10 = 10 pixels from other icons non transparent pixels
                 slice_distance_factor=0.60,                        # 0.5 = middle of radius, 0.7 = towards card's edge
                 delta_center=20,                                   # 20 = +/-20px random placement of the central icon
                 delta_angle=0.2,                                   # 0.2 = +/-20% of angle, 0.02 = +/-2% of angle
                 delta_radius=0.1,                                  # 0.1 = +/-10% of radius, 0.01 = +/-1% of radius
                 max_attempts=99,                                   # 99 = 99 attempts to place a single icon
            ):
        
        if planner_type == Planner_Type.SIMPLE_RANDOM: 
                self.planner = Planner_Factory.create(
                    Planner_Type.SIMPLE_RANDOM,
                    canvas_size=canvas_size,
                    # base_item_size=256,
                    min_scale=min_scale,
                    max_scale=max_scale,
                    padding_from_edge=padding_from_edge,
                    slice_distance_factor=slice_distance_factor,
                    max_attempts=max_attempts,
                )

        elif planner_type == Planner_Type.SIMPLE_REGULAR_SLICES:
                self.planner = Planner_Factory.create(
                    Planner_Type.SIMPLE_REGULAR_SLICES,
                    canvas_size=canvas_size,
                    base_item_size=base_item_size,
                    min_scale=min_scale,
                    max_scale=max_scale,
                    padding_from_edge=padding_from_edge,
                    slice_distance_factor=slice_distance_factor,
                    max_attempts=max_attempts,
                )

        elif planner_type == Planner_Type.SIMPLE_ADJUSTABLE_SLICES:
                self.planner = Planner_Factory.create(
                    Planner_Type.SIMPLE_ADJUSTABLE_SLICES,
                    canvas_size=canvas_size,
                    base_item_size=base_item_size,
                    min_scale=min_scale,
                    max_scale=max_scale,
                    padding_from_edge=padding_from_edge,
                    slice_distance_factor=slice_distance_factor,
                    delta_center=delta_center,
                    delta_angle=delta_angle,
                    delta_radius=delta_radius,
                    max_attempts=max_attempts,
                )

        elif planner_type == Planner_Type.ADVANCED_REGULAR_SLICES:
                self.planner = Planner_Factory.create(
                    Planner_Type.ADVANCED_REGULAR_SLICES,
                    canvas_size=canvas_size,
                    base_item_size=base_item_size,
                    min_scale=min_scale,
                    max_scale=max_scale,
                    padding_from_edge=padding_from_edge,
                    slice_distance_factor=slice_distance_factor,
                    max_attempts=max_attempts,
                )

        elif planner_type == Planner_Type.ADVANCED_ADJUSTABLE_SLICES:
                self.planner = Planner_Factory.create(
                    Planner_Type.ADVANCED_ADJUSTABLE_SLICES,
                    canvas_size=canvas_size,
                    base_item_size=base_item_size,
                    min_scale=min_scale,
                    max_scale=max_scale,
                    padding_from_edge=padding_from_edge,
                    min_icon_distance=min_icon_distance,
                    slice_distance_factor=slice_distance_factor,
                    delta_center=delta_center,
                    delta_angle=delta_angle,
                    delta_radius=delta_radius,
                    max_attempts=max_attempts,
                )

        elif planner_type == Planner_Type.ADVANCED_SNAPSHOT_BASED_ADJUSTABLE_SLICES:
                self.planner = Planner_Factory.create(
                    Planner_Type.ADVANCED_SNAPSHOT_BASED_ADJUSTABLE_SLICES,
                    canvas_size=canvas_size,
                    base_item_size=base_item_size,
                    min_scale=min_scale,
                    max_scale=max_scale,
                    padding_from_edge=padding_from_edge,
                    slice_distance_factor=slice_distance_factor,
                    delta_center=delta_center,
                    delta_angle=delta_angle,
                    delta_radius=delta_radius,
                    max_attempts=max_attempts,
                )
        
        self.generator = Card_Image_Generator(canvas_size=canvas_size)

    def create(self, 
               icon_files, 
               output_path
            ):
        placements = self.planner.plan(icon_files)
        self.generator.generate(placements, output_path)
