from enum import Enum

class Planner_Type(Enum):
    SIMPLE_RANDOM = "random"
    SIMPLE_REGULAR_SLICES = "simple_regular_slices"
    SIMPLE_ADJUSTABLE_SLICES = "simple_adjustable_slices"
    ADVANCED_REGULAR_SLICES = "advanced_regular_slices"
    ADVANCED_ADJUSTABLE_SLICES = "advanced_adjustable_slices"
    ADVANCED_SNAPSHOT_BASED_ADJUSTABLE_SLICES = "advanced_snapshot_based_adjustable_slices"