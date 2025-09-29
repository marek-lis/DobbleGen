import math
import random
from PIL import Image

class Card_Image_Planner:
    def __init__(self, 
                 canvas_size=1024,          # 1024 = card's size of 1024x1024px
                 base_item_size=256,        # 256 = icon's size of 256x256px
                 min_scale=0.5,             # 0.5 = 50% icon's scale
                 max_scale=1.0,             # 1.0 = 100% icon's scale
                 padding_from_edge=10,      # 10 = 10 pixels from circle's edge
                 slice_distance_factor=0.6, # 0.5 = middle of radius, 0.7 = towards card's edge
                 delta_center=20,           # 20 = +/-20px random placement of the central icon
                 delta_angle=0.2,           # 0.2 = +/-20% of angle, 0.02 = +/-2% of angle
                 delta_radius=0.1,          # 0.1 = +/-10% of radius, 0.01 = +/-1% of radius
                 max_attempts=99,           # 99 = 99 attempts to place a single icon
            ):
        self.canvas_size = canvas_size
        self.base_item_size = base_item_size
        self.radius = canvas_size // 2
        self.min_scale = min_scale
        self.max_scale = max_scale
        self.padding_from_edge = padding_from_edge
        self.slice_distance_factor = slice_distance_factor
        self.delta_center = delta_center
        self.delta_angle = delta_angle
        self.delta_radius = delta_radius
        self.max_attempts = max_attempts

        # create a circle shaped mask:
        self.circle_mask = Image.new("1", (canvas_size, canvas_size), 0)
        from PIL import ImageDraw
        draw = ImageDraw.Draw(self.circle_mask)
        draw.ellipse(
            (padding_from_edge, padding_from_edge,
             canvas_size - padding_from_edge,
             canvas_size - padding_from_edge),
            fill=1
        )

    def _prepare_image(self, path, scale, rotation):
        from PIL import Image
        img = Image.open(path).convert("RGBA")
        size = max(1, int(self.base_item_size * scale))
        img = img.resize((size, size), Image.BICUBIC)
        img = img.rotate(rotation, expand=True)
        return img

    def _get_mask(self, img):
        return img.split()[3].point(lambda p: 1 if p>0 else 0).convert("1")

    def _check_collision(self, occupancy_map, mask, x, y):
        from PIL import ImageChops, Image
        temp = Image.new("1", (self.canvas_size, self.canvas_size), 0)
        temp.paste(mask, (x, y))
        overlap = ImageChops.logical_and(temp, occupancy_map)
        return overlap.getbbox() is not None

    def _check_inside_circle(self, mask, x, y):
        from PIL import ImageChops, ImageOps, Image
        temp = Image.new("1", (self.canvas_size, self.canvas_size), 0)
        temp.paste(mask, (x, y))
        outside = ImageChops.logical_and(temp, ImageOps.invert(self.circle_mask))
        return outside.getbbox() is None

    def plan(self, paths):
        from PIL import Image
        """
        returns a list of  dicts: 
        { 
            "path", 
            "x", 
            "y", 
            "scale", 
            "rotation" 
        }
        """
        n = len(paths)
        while True:  # retry when planning failed
            occupancy_map = Image.new("1", (self.canvas_size, self.canvas_size), 0)
            placements = []

            # middle icon:
            central_scale = random.uniform(self.max_scale*0.7, self.max_scale)
            central_rotation = random.randint(0, 359)
            central_img = self._prepare_image(paths[0], central_scale, central_rotation)
            central_mask = self._get_mask(central_img)

            cx = self.radius + random.randint(-self.delta_center, self.delta_center)
            cy = self.radius + random.randint(-self.delta_center, self.delta_center)
            x = cx - central_img.width // 2
            y = cy - central_img.height // 2

            occupancy_map.paste(central_mask, (x, y))
            placements.append({"path": paths[0], "x": cx, "y": cy,
                               "scale": central_scale, "rotation": central_rotation})

            # if only 1 icon then ready:
            slices = n - 1
            if slices == 0:
                return placements

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
                    angle_offset = random.uniform(-angle_per_slice * self.delta_angle, angle_per_slice * self.delta_angle)
                    radius_offset = random.uniform(-slice_radius_base * self.delta_radius, slice_radius_base * self.delta_radius)
                    r = slice_radius_base + radius_offset

                    cx = int(self.radius + r * math.cos(angle_center + angle_offset))
                    cy = int(self.radius + r * math.sin(angle_center + angle_offset))
                    x = cx - img.width // 2
                    y = cy - img.height // 2

                    if not self._check_inside_circle(mask, x, y):
                        continue
                    if self._check_collision(occupancy_map, mask, x, y):
                        continue

                    occupancy_map.paste(mask, (x, y))
                    placements.append({"path": path, "x": cx, "y": cy,
                                       "scale": scale, "rotation": rotation})
                    placed = True
                    break

                if not placed:
                    success = False
                    print("Failed to place an icon without collision.")
                    break  # if failed, break the loop and start from the beginning

            if success:
                return placements
