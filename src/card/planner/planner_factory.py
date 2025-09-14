import importlib
from card.planner.planner_type import Planner_Type

class Planner_Factory:
    MODULE_MAP = {
        Planner_Type.RANDOM: "card.planner.impl.card_image_random_planner",
        Planner_Type.IDEAL_SLICE: "card.planner.impl.card_image_ideal_slices_planner",
        Planner_Type.ADJUSTABLE_SLICE: "card.planner.impl.card_image_adjustable_slices_planner",
    }

    CLASS_NAME = "Card_Image_Planner"

    @staticmethod
    def create(method: Planner_Type, **kwargs):
        module_name = Planner_Factory.MODULE_MAP[method]
        module = importlib.import_module(module_name)
        planner_class = getattr(module, Planner_Factory.CLASS_NAME)
        return planner_class(**kwargs)