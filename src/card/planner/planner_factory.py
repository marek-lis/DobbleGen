import importlib
from card.planner.planner_type import Planner_Type

class Planner_Factory:
    PACKAGE = "card.planner.impl."
    MODULE_MAP = {
        Planner_Type.SIMPLE_RANDOM: f"{PACKAGE}card_image_simple_random_planner",
        Planner_Type.SIMPLE_REGULAR_SLICES: f"{PACKAGE}card_image_simple_regular_slices_planner",
        Planner_Type.SIMPLE_ADJUSTABLE_SLICES: f"{PACKAGE}card_image_simple_adjustable_slices_planner",
        Planner_Type.ADVANCED_REGULAR_SLICES: f"{PACKAGE}card_image_advanced_regular_slices_planner",
        Planner_Type.ADVANCED_ADJUSTABLE_SLICES: f"{PACKAGE}card_image_advanced_adjustable_slices_planner",
        Planner_Type.ADVANCED_SNAPSHOT_BASED_ADJUSTABLE_SLICES: f"{PACKAGE}card_image_advanced_snapshot_based_adjustable_slices_planner",
    }

    CLASS_NAME = "Card_Image_Planner"

    @staticmethod
    def create(method: Planner_Type, **kwargs):
        module_name = Planner_Factory.MODULE_MAP[method]
        module = importlib.import_module(module_name)
        planner_class = getattr(module, Planner_Factory.CLASS_NAME)
        return planner_class(**kwargs)