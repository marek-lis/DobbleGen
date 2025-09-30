import math
import random
from PIL import Image
import numpy as np
from scipy.ndimage import distance_transform_edt
from typing import List, Dict, Optional


class Card_Image_Planner:
    def __init__(self,
                canvas_size=1024,               # 1024 = card's size of 1024x1024px
                base_item_size=256,             # 256 = icon's size of 256x256px
                min_scale=0.75,                 # 0.50 = 50% icon's scale
                max_scale=1.00,                 # 1.00 = 100% icon's scale
                padding_from_edge = 10,         # 10 = minimum 10 pixels distance of an icon from the cards edge
                min_icon_distance = 30,         # 30 = minimum 30 pixels distance between icons non transparent pixels
                slice_distance_factor=0.5,      # 0.5 = middle of radius, 0.7 = towards card's edge
                delta_center=30,                # 20 = +/-20px random placement of the central icon
                delta_angle=0.2,                # 0.2 = +/-20% of angle, 0.02 = +/-2% of angle
                delta_radius=0.1,               # 0.1 = +/-10% of radius, 0.01 = +/-1% of radius
                max_attempts=99,                # 99 = 99 attempts to place a single icon
            ):
        self.canvas_size = canvas_size
        self.radius = canvas_size // 2
        self.base_item_size = base_item_size
        self.min_scale = min_scale
        self.max_scale = max_scale
        self.padding_from_edge = padding_from_edge
        self.min_icon_distance = min_icon_distance
        self.slice_distance_factor = slice_distance_factor
        self.delta_center = delta_center
        self.delta_angle = delta_angle
        self.delta_radius = delta_radius
        self.max_attempts = max_attempts

        # full circle (True = point inside the circle)
        yy, xx = np.mgrid[:canvas_size, :canvas_size]
        cx, cy = self.radius, self.radius
        full_circle = ((xx - cx) ** 2 + (yy - cy) ** 2) <= (self.radius ** 2)
        # distance map: the number of pixels (Euclidean) to the nearest pixel outside the circle
        # distance_transform_edt counts the distance to the nearest zero
        # dt_edge[p] = the distance from p to the nearest zero (outside).
        self._dt_edge = distance_transform_edt(full_circle)  # float array

    # ---------------- helpers ----------------
    def _prepare_image(self, path: str, scale: float, rotation: float) -> Image.Image:
        img = Image.open(path).convert("RGBA")
        size = max(1, int(self.base_item_size * scale))
        img = img.resize((size, size), resample=Image.BICUBIC)
        img = img.rotate(rotation, expand=True, resample=Image.BICUBIC)
        return img

    def _get_mask(self, img: Image.Image) -> np.ndarray:
        alpha = np.array(img.split()[3])
        return (alpha > 0).astype(np.uint8)  # 1 = non-transparent

    # ---------------- placement checks using distance transforms ----------------
    def _compute_dt_occ(self, occupancy_map: np.ndarray) -> np.ndarray:
        # occupancy_map: 2D uint8 array (1 = occupied pixel, 0 = free)
        # returns dt_occ: float array with for each free pixel distance to nearest occupied pixel.
        # If occupancy_map has no 1s, return very large values.
        if occupancy_map.sum() == 0:
            # no occupied pixels -> return very large distances
            return np.full_like(occupancy_map, fill_value=1e6, dtype=float)
        # distance_transform_edt computes distance to nearest zero for non-zero elements.
        # We want distances for background pixels to nearest occupied pixel.
        # Passing (occupancy_map == 0) gives True for free pixels, and the EDT result for those
        # is distance to nearest zero (i.e. occupied pixel in original). This matches our need.
        dt = distance_transform_edt(occupancy_map == 0)
        return dt  # float array

    # ---------------- main planner ----------------
    def plan(self, paths: List[str]) -> List[Dict]:
        # Returns list of placements: {"path", "x", "y", "scale", "rotation"}
        # Implements:
        # - CURRENT_VIEW represented by occupancy_map (binary)
        # - for each candidate icon: compute its mask, map mask indices to global coords,
        #   check: no overlap with occupancy_map (pixel-perfect), dt_occ > min_icon_distance,
        #   dt_edge >= padding_from_edge
        if len(paths) == 0:
            return []

        n = len(paths)
        attempt_card = 0

        while True:  # retry whole card until success
            attempt_card += 1
            occupancy_map = np.zeros((self.canvas_size, self.canvas_size), dtype=np.uint8)
            placements: List[Dict] = []

            # middle icon
            central_scale = random.uniform(self.max_scale * 0.7, self.max_scale)
            central_rot = random.randint(0, 359)
            central_img = self._prepare_image(paths[0], central_scale, central_rot)
            central_mask = self._get_mask(central_img)
            cx = self.radius + random.randint(-self.delta_center, self.delta_center)
            cy = self.radius + random.randint(-self.delta_center, self.delta_center)
            x0 = cx - central_mask.shape[1] // 2
            y0 = cy - central_mask.shape[0] // 2

            # bounds check
            if x0 < 0 or y0 < 0 or x0 + central_mask.shape[1] > self.canvas_size or y0 + central_mask.shape[0] > self.canvas_size:
                continue

            # get global coords of mask pixels
            ys, xs = np.nonzero(central_mask)
            global_xs = x0 + xs
            global_ys = y0 + ys

            # 1) edge padding check (dt_edge)
            dt_edge_at_pixels = self._dt_edge[global_ys, global_xs]
            if (dt_edge_at_pixels < self.padding_from_edge).any():
                continue

            # 2) occupancy overlap (should be none for central)
            if occupancy_map[global_ys, global_xs].any():
                continue

            # 3) min distance check (occupancy empty -> dt_occ large)
            dt_occ = self._compute_dt_occ(occupancy_map)
            if self.min_icon_distance > 0:
                if (dt_occ[global_ys, global_xs] <= self.min_icon_distance).any():
                    continue

            # accept central
            occupancy_map[global_ys, global_xs] = 1
            placements.append({"path": paths[0], "x": cx, "y": cy, "scale": central_scale, "rotation": central_rot})

            # if only one icon
            if n == 1:
                return placements

            # precompute slice radius base in safe manner (avoid going to edge)
            slice_radius_base = (self.radius - self.padding_from_edge) * self.slice_distance_factor

            success_card = True
            for i, path in enumerate(paths[1:], start=0):
                placed = False

                # compute distance transform once per icon attempt block (updates when occupancy changes)
                dt_occ = self._compute_dt_occ(occupancy_map)

                for attempt_icon in range(self.max_attempts):
                    scale = random.uniform(self.min_scale, self.max_scale)
                    rotation = random.randint(0, 359)
                    img = self._prepare_image(path, scale, rotation)
                    mask = self._get_mask(img)

                    angle_center = i * (2 * math.pi / (n - 1)) + (math.pi * 2) / (2 * (n - 1))
                    angle_offset = random.uniform(- (2 * math.pi / (n - 1)) * self.delta_angle,
                                                  (2 * math.pi / (n - 1)) * self.delta_angle)
                    radius_offset = random.uniform(-slice_radius_base * self.delta_radius,
                                                   slice_radius_base * self.delta_radius)
                    r = slice_radius_base + radius_offset

                    cx = int(self.radius + r * math.cos(angle_center + angle_offset))
                    cy = int(self.radius + r * math.sin(angle_center + angle_offset))
                    x = cx - mask.shape[1] // 2
                    y = cy - mask.shape[0] // 2

                    # bounds check (icon must be fully on canvas)
                    if x < 0 or y < 0 or x + mask.shape[1] > self.canvas_size or y + mask.shape[0] > self.canvas_size:
                        continue

                    ys, xs = np.nonzero(mask)
                    global_xs = x + xs
                    global_ys = y + ys

                    # 1) edge padding
                    if (self._dt_edge[global_ys, global_xs] < self.padding_from_edge).any():
                        continue

                    # 2) direct pixel overlap (pixel-perfect)
                    if occupancy_map[global_ys, global_xs].any():
                        continue

                    # 3) min icon distance via distance transform
                    if self.min_icon_distance > 0:
                        if (dt_occ[global_ys, global_xs] <= self.min_icon_distance).any():
                            continue

                    # passed all checks -> accept
                    occupancy_map[global_ys, global_xs] = 1
                    placements.append({"path": path, "x": cx, "y": cy, "scale": scale, "rotation": rotation})
                    placed = True
                    break

                if not placed:
                    print("Card creation failed!")
                    success_card = False
                    break  # restart whole card

            if success_card:
                return placements
            # else repeat whole card attempt
