import math
import random
from PIL import Image
import numpy as np

class Card_Image_Planner:
    def __init__(self, 
                 canvas_size=1024,          # 1024 = card's size of 1024x1024px
                 base_item_size=256,        # 256 = icon's size of 256x256px
                 min_scale=0.75,            # 0.5 = 50% icon's scale
                 max_scale=1.25,            # 1.0 = 100% icon's scale
                 padding_from_edge=10,      # 10 = 10 pixels from circle's edge
                 slice_distance_factor=0.5, # 0.5 = middle of radius, 0.7 = towards card's edge
                 delta_center=30,           # 20 = +/-20px random placement of the central icon
                 delta_angle=0.2,           # 0.2 = +/-20% of angle, 0.02 = +/-2% of angle
                 delta_radius=0.1,          # 0.1 = +/-10% of radius, 0.01 = +/-1% of radius
                 max_attempts=199,          # 199 = 99 attempts to place a single icon
            ):
        self.canvas_size = canvas_size
        self.radius = canvas_size // 2
        self.base_item_size = base_item_size
        self.min_scale = min_scale
        self.max_scale = max_scale
        self.padding_from_edge = padding_from_edge
        self.slice_distance_factor = slice_distance_factor
        self.delta_center = delta_center
        self.delta_angle = delta_angle
        self.delta_radius = delta_radius
        self.max_attempts = max_attempts

        # maska koła
        self.circle_mask = np.zeros((canvas_size, canvas_size), dtype=np.uint8)
        yy, xx = np.mgrid[:canvas_size, :canvas_size]
        cx, cy = self.radius, self.radius
        r = self.radius - padding_from_edge
        self.circle_mask[((xx - cx)**2 + (yy - cy)**2) <= r**2] = 1

    def _prepare_image(self, path, scale, rotation):
        img = Image.open(path).convert("RGBA")
        size = max(1, int(self.base_item_size * scale))
        img = img.resize((size, size), Image.BICUBIC)
        img = img.rotate(rotation, expand=True)
        return img

    def _get_mask(self, img):
        alpha = np.array(img.split()[3])
        return (alpha > 0).astype(np.uint8)

    def _check_collision(self, occupancy_map, mask, x, y):
        h, w = mask.shape
        if x < 0 or y < 0 or x + w > self.canvas_size or y + h > self.canvas_size:
            return True
        submap = occupancy_map[y:y+h, x:x+w]
        return np.any(np.logical_and(submap, mask))

    def _check_inside_circle(self, mask, x, y):
        h, w = mask.shape
        if x < 0 or y < 0 or x + w > self.canvas_size or y + h > self.canvas_size:
            return False
        submap = self.circle_mask[y:y+h, x:x+w]
        outside = np.logical_and(mask, submap == 0)
        return not np.any(outside)

    def plan(self, paths):
        n = len(paths)
        while True:  # retry until all icons are placed
            occupancy_map = np.zeros((self.canvas_size, self.canvas_size), dtype=np.uint8)
            placements = []

            # Środkowa ikona
            central_scale = random.uniform(self.max_scale*0.7, self.max_scale)
            central_rot = random.randint(0, 359)
            central_img = self._prepare_image(paths[0], central_scale, central_rot)
            central_mask = self._get_mask(central_img)
            cx = self.radius + random.randint(-self.delta_center, self.delta_center)
            cy = self.radius + random.randint(-self.delta_center, self.delta_center)
            x = cx - central_img.width // 2
            y = cy - central_img.height // 2
            if not self._check_inside_circle(central_mask, x, y):
                continue
            occupancy_map[y:y+central_mask.shape[0], x:x+central_mask.shape[1]] |= central_mask
            placements.append({"path": paths[0], "x": cx, "y": cy,
                               "scale": central_scale, "rotation": central_rot})

            if n == 1:
                return placements

            # slice’y
            slices = n - 1
            angle_per_slice = 2 * math.pi / slices
            slice_radius_base = (self.radius - self.padding_from_edge) * self.slice_distance_factor

            success = True
            for i, path in enumerate(paths[1:], start=0):
                placed = False
                for attempt in range(self.max_attempts):
                    scale = random.uniform(self.min_scale, self.max_scale)
                    rotation = random.randint(0, 359)
                    img = self._prepare_image(path, scale, rotation)
                    mask = self._get_mask(img)

                    angle_center = i * angle_per_slice + angle_per_slice / 2
                    angle_offset = random.uniform(-angle_per_slice * self.delta_angle,
                                                  angle_per_slice * self.delta_angle)
                    radius_offset = random.uniform(-slice_radius_base * self.delta_radius,
                                                   slice_radius_base * self.delta_radius)
                    r = slice_radius_base + radius_offset

                    cx = int(self.radius + r * math.cos(angle_center + angle_offset))
                    cy = int(self.radius + r * math.sin(angle_center + angle_offset))
                    x = cx - mask.shape[1] // 2
                    y = cy - mask.shape[0] // 2

                    if not self._check_inside_circle(mask, x, y):
                        continue
                    if self._check_collision(occupancy_map, mask, x, y):
                        continue

                    occupancy_map[y:y+mask.shape[0], x:x+mask.shape[1]] |= mask
                    placements.append({"path": path, "x": cx, "y": cy,
                                       "scale": scale, "rotation": rotation})
                    placed = True
                    break

                if not placed:
                    success = False
                    break  # retry whole card

            if success:
                return placements
