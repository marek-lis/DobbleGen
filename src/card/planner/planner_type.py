from enum import Enum

class Planner_Type(Enum):
    RANDOM = "random"
    IDEAL_SLICE = "ideal_slice"
    ADJUSTABLE_SLICE = "adjustable_slice"
    ADVANCED_IDEAL_SLICE = "advanced_ideal_slice"
    ADVANCED_ADJUSTABLE_SLICE = "advanced_adjustable_slice"