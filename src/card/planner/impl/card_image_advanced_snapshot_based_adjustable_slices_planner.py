import math
import random
from typing import List, Dict, Optional
from PIL import Image
import numpy as np

class Card_Image_Planner:
    def __init__(self, 
                 canvas_size=1024,          # 1024 = card's size of 1024x1024px
                 base_item_size=256,        # 256 = icon's size of 256x256px
                 min_scale=0.75,            # 0.50 = 50% icon's scale
                 max_scale=1.00,            # 1.00 = 100% icon's scale
                 padding_from_edge=10,      # 10 = 10 pixels from circle's edge
                 slice_distance_factor=0.5, # 0.5 = middle of radius, 0.7 = towards card's edge
                 delta_center=30,           # 20 = +/-20px random placement of the central icon
                 delta_angle=0.2,           # 0.2 = +/-20% of angle, 0.02 = +/-2% of angle
                 delta_radius=0.1,          # 0.1 = +/-10% of radius, 0.01 = +/-1% of radius
                 max_attempts=999,          # 999 = 999 attempts to place a single icon
            ):
        self.canvas_size = canvas_size
        self.base_item_size = base_item_size
        self.min_scale = min_scale
        self.max_scale = max_scale
        self.padding_from_edge = padding_from_edge
        self.slice_distance_factor = slice_distance_factor
        self.delta_center = delta_center
        self.delta_angle = delta_angle
        self.delta_radius = delta_radius
        self.max_attempts = max_attempts
        self.radius = canvas_size // 2

        # Circle Mask (True = Allowed Inside)
        yy, xx = np.mgrid[:canvas_size, :canvas_size]
        r = self.radius - padding_from_edge
        self._circle_mask = ((xx - self.radius)**2 + (yy - self.radius)**2) <= r**2

    def _prepare_icon_image(self, path: str, scale: float, rotation: float) -> Image.Image:
        # load the cion and change its size and rotation
        img = Image.open(path).convert("RGBA")
        size = max(1, int(self.base_item_size * scale))
        img = img.resize((size, size), resample=Image.LANCZOS)
        img = img.rotate(rotation, expand=True, resample=Image.BICUBIC)
        return img

    def _render_icon_only_view(self, icon_img: Image.Image, cx: int, cy: int) -> Optional[Image.Image]:
        # returns canvas with the next icon only
        # (cx,cy) = center position of the icon
        # if icon exceeds canvas, its position is illegal
        x = int(cx - icon_img.width // 2)
        y = int(cy - icon_img.height // 2)
        # if any part of the icon exceeds canvas, icon positions is illegal
        if x < 0 or y < 0 or x + icon_img.width > self.canvas_size or y + icon_img.height > self.canvas_size:
            return None
        canvas = Image.new("RGBA", (self.canvas_size, self.canvas_size), (0,0,0,0))
        canvas.alpha_composite(icon_img, (x, y))
        return canvas

    def _future_view_inside_circle(self, future_view: Image.Image) -> bool:
        # check if all the non-transparent pixels of the future view (with the next icon) are inside the circle
        alpha = np.array(future_view.split()[3]) > 0  # boolean
        outside = np.logical_and(alpha, np.logical_not(self._circle_mask))
        return not np.any(outside)

    def _pixel_perfect_overlap(self, current_view: Image.Image, future_view: Image.Image) -> bool:
        # check if current and future view have any common non transparent pixel
        # returns True when collision between those views occurs
        cur_a = np.array(current_view.split()[3]) > 0
        fut_a = np.array(future_view.split()[3]) > 0
        return np.any(np.logical_and(cur_a, fut_a))

    def _accept_icon_and_update_current_view(self,
                                             current_view: Image.Image,
                                             icon_img: Image.Image,
                                             cx: int, cy: int,
                                             placement_record: Dict) -> bool:
        # creates the future view (canvas with the next icon), 
        # checkes if the next icon is placed inside the circle and the future view collides with the current view
        # if the future view with the next icon has no collision with the current view and the next icon is inside the circle
        # the next icon is added to the current view and this method returns true
        future_view = self._render_icon_only_view(icon_img, cx, cy)
        if future_view is None:
            return False  # next icon exceeds the canvas

        # 1) is the next icon inside the circle?
        if not self._future_view_inside_circle(future_view):
            return False

        # 2) is there any collision between the current view and the future view?
        if self._pixel_perfect_overlap(current_view, future_view):
            return False

        # if both above chcecks are successfull, 
        # update the currnet view with the next icon from the future view
        x = int(cx - icon_img.width // 2)
        y = int(cy - icon_img.height // 2)
        current_view.alpha_composite(icon_img, (x, y))

        # set the cx,cy position of the icon
        # the caller will set the scale, rotation and path
        placement_record.update({"x": cx, "y": cy, "scale": None, "rotation": None})
        return True

    def plan(self, paths: List[str]) -> List[Dict]:
        #paths: list of paths to icons (index 0 = the central icon)
        #returns the list of placements in the following format: 
        # [{"path":..., "x":..., "y":..., "scale":..., "rotation":...}, ...]
        n = len(paths)
        if n == 0:
            return []

        attempt_card = 0
        while True:
            attempt_card += 1
            placements: List[Dict] = []
            current_view = Image.new("RGBA", (self.canvas_size, self.canvas_size), (0,0,0,0))

            # central icon placement
            central_scale = random.uniform(self.max_scale * 0.7, self.max_scale)
            central_rot = random.randint(0, 359)
            central_img = self._prepare_icon_image(paths[0], central_scale, central_rot)
            cx = self.radius + random.randint(-self.delta_center, self.delta_center)
            cy = self.radius + random.randint(-self.delta_center, self.delta_center)

            # future view with central icon only, perform checks
            future_view = self._render_icon_only_view(central_img, cx, cy)
            if future_view is None:
                continue 
            if not self._future_view_inside_circle(future_view):
                continue 

            # current view is empty so far, so no checkes between the current and the future are needed
            placements.append({"path": paths[0], "x": cx, "y": cy, "scale": central_scale, "rotation": central_rot})
            # add central icon to the current view
            current_view.alpha_composite(central_img, (int(cx - central_img.width//2), int(cy - central_img.height//2)))

            if n == 1:
                return placements

            # cetnral icon done, proceed with all the other icons
            slices = n - 1
            angle_per_slice = 2 * math.pi / slices
            slice_radius_base = (self.radius - self.padding_from_edge) * self.slice_distance_factor

            success_card = True
            for i, path in enumerate(paths[1:], start=0):
                placed = False
                for attempt_icon in range(self.max_attempts):
                    # random transfomrations
                    scale = random.uniform(self.min_scale, self.max_scale)
                    rotation = random.randint(0, 359)
                    icon_img = self._prepare_icon_image(path, scale, rotation)

                    # calculate the proposed position
                    angle_center = i * angle_per_slice + angle_per_slice / 2
                    angle_offset = random.uniform(-angle_per_slice * self.delta_angle,
                                                  angle_per_slice * self.delta_angle)
                    radius_offset = random.uniform(-slice_radius_base * self.delta_radius,
                                                   slice_radius_base * self.delta_radius)
                    r = slice_radius_base + radius_offset
                    cx = int(self.radius + r * math.cos(angle_center + angle_offset))
                    cy = int(self.radius + r * math.sin(angle_center + angle_offset))

                    placement_record = {"path": path, "x": None, "y": None, "scale": scale, "rotation": rotation}

                    # create the future view with the next icon only
                    future_view = self._render_icon_only_view(icon_img, cx, cy)
                    if future_view is None:
                        # if exceeds the cavnas, retry
                        continue

                    # 1) check if content of the future view is inside the circle
                    if not self._future_view_inside_circle(future_view):
                        continue

                    # 2) pixel-perfect collision check between the current and the future view
                    if self._pixel_perfect_overlap(current_view, future_view):
                        continue

                    # 3) if no collision detected between the current and the future view, then add the icon from the future view to current view
                    current_view.alpha_composite(icon_img, (int(cx - icon_img.width//2), int(cy - icon_img.height//2)))
                    # save placement
                    placement_record["x"] = cx
                    placement_record["y"] = cy
                    placements.append(placement_record)
                    placed = True
                    # icon has been placed
                    break  

                if not placed:
                    print("Card creation failed!")
                    success_card = False
                    break  # restart the whole card

            if success_card:
                return placements