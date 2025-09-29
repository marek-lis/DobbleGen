import math
import random
from PIL import Image, ImageChops, ImageOps

class Card_Image_Planner:
    def __init__(self, 
                 canvas_size=1024,          # 1024 = card's size of 1024x1024px
                 base_item_size=256,        # 256 = icon's size of 256x256px
                 min_scale=0.5,             # 0.5 = 50% icon's scale
                 max_scale=1.0,             # 1.0 = 100% icon's scale
                 padding_from_edge=10,      # 10 = 10 pixels from circle's edge
                 slice_distance_factor=0.6, # 0.5 = middle of radius, 0.7 = towards card's edge
                 max_attempts=99,          # 99 = 99 attempts to place a single icon
            ):
        self.canvas_size = canvas_size
        self.base_item_size = base_item_size
        self.radius = canvas_size // 2
        self.min_scale = min_scale
        self.max_scale = max_scale
        self.padding_from_edge = padding_from_edge
        self.slice_distance_factor = slice_distance_factor
        self.max_attempts = max_attempts

        # create mask 
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
        img = Image.open(path).convert("RGBA")
        size = max(1, int(self.base_item_size * scale))
        img = img.resize((size, size), Image.BICUBIC)
        img = img.rotate(rotation, expand=True)
        return img

    def _get_mask(self, img):
        return img.split()[3].point(lambda p: 1 if p > 0 else 0).convert("1")

    def _check_collision(self, occupancy_map, mask, x, y):
        temp = Image.new("1", (self.canvas_size, self.canvas_size), 0)
        temp.paste(mask, (x, y))
        overlap = ImageChops.logical_and(temp, occupancy_map)
        return overlap.getbbox() is not None

    def _check_inside_circle(self, mask, x, y):
        temp = Image.new("1", (self.canvas_size, self.canvas_size), 0)
        temp.paste(mask, (x, y))
        outside = ImageChops.logical_and(temp, ImageOps.invert(self.circle_mask))
        return outside.getbbox() is None

    def plan(self, paths):
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
        placements = []
        occupancy_map = Image.new("1", (self.canvas_size, self.canvas_size), 0)

        # center icon:
        scale = random.uniform(self.max_scale * 0.7, self.max_scale)
        rotation = random.randint(0, 359)
        img = self._prepare_image(paths[0], scale, rotation)
        mask = self._get_mask(img)

        cx = self.radius + random.randint(-20, 20)
        cy = self.radius + random.randint(-20, 20)
        x = cx - img.width // 2
        y = cy - img.height // 2

        occupancy_map.paste(mask, (x, y))
        placements.append({"path": paths[0], "x": cx, "y": cy, "scale": scale, "rotation": rotation})

        # slice the card for other icons:
        slices = len(paths) - 1
        angle_per_slice = 2 * math.pi / slices
        slice_radius = (self.radius - self.padding_from_edge) * self.slice_distance_factor
        r = slice_radius

        for i, path in enumerate(paths[1:], start=0):
            success = False
            for attempt in range(self.max_attempts):
                scale = random.uniform(self.min_scale, self.max_scale)
                rotation = random.randint(0, 359)
                img = self._prepare_image(path, scale, rotation)
                mask = self._get_mask(img)

                angle_center = i * angle_per_slice + angle_per_slice / 2

                cx = int(self.radius + r * math.cos(angle_center))
                cy = int(self.radius + r * math.sin(angle_center))

                x = cx - img.width // 2
                y = cy - img.height // 2

                if not self._check_inside_circle(mask, x, y):
                    continue
                if self._check_collision(occupancy_map, mask, x, y):
                    continue

                occupancy_map.paste(mask, (x, y))
                placements.append({"path": path, "x": cx, "y": cy, "scale": scale, "rotation": rotation})
                success = True
                break

            if not success:
                # fallback: reduce scale and insert without collision check
                print("Failed to place an icon without collision.")
                scale = max(self.min_scale, scale * 0.7)
                rotation = random.randint(0, 359)
                img = self._prepare_image(path, scale, rotation)
                mask = self._get_mask(img)
                cx = int(self.radius + r * math.cos(angle_center))
                cy = int(self.radius + r * math.sin(angle_center))
                x = cx - img.width // 2
                y = cy - img.height // 2
                occupancy_map.paste(mask, (x, y))
                placements.append({"path": path, "x": cx, "y": cy, "scale": scale, "rotation": rotation})

        return placements
