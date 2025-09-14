import math
import random
from PIL import Image

class Card_Image_Planner:
    def __init__(self, 
                 canvas_size=1024,          # 1024 = card's size of 1024x1024px
                 min_scale=0.5,             # 0.5 = 50% icon's scale
                 max_scale=1.0,             # 1.0 = 100% icon's scale
                 padding_from_edge=30,      # 30 = 30 pixels from circle's edge
                 slice_distance_factor=0.6, # 0.5 = middle of radius, 0.7 = towards card's edge
                 max_attempts=99,           # 99 = 99 attempts to place a single icon
            ):
        self.canvas_size = canvas_size
        self.radius = canvas_size // 2 - padding_from_edge
        self.min_scale = min_scale
        self.max_scale = max_scale
        self.slice_distance_factor = slice_distance_factor
        self.max_attempts = max_attempts
        self.padding_from_edge = padding_from_edge

    def _collides(self, placement, others):
        new_img = Image.open(placement["path"]).convert("RGBA")
        w, h = new_img.size
        new_img = new_img.resize((int(w * placement["scale"]), int(h * placement["scale"])))
        new_img = new_img.rotate(placement["rotation"], expand=True)
        new_mask = new_img.split()[3]  # alpha

        nx, ny = int(placement["x"] - new_img.width / 2), int(placement["y"] - new_img.height / 2)

        for other in others:
            other_img = Image.open(other["path"]).convert("RGBA")
            ow, oh = other_img.size
            other_img = other_img.resize((int(ow * other["scale"]), int(oh * other["scale"])))
            other_img = other_img.rotate(other["rotation"], expand=True)
            other_mask = other_img.split()[3]

            ox, oy = int(other["x"] - other_img.width / 2), int(other["y"] - other_img.height / 2)

            # overlap bbox
            x0 = max(nx, ox)
            y0 = max(ny, oy)
            x1 = min(nx + new_img.width, ox + other_img.width)
            y1 = min(ny + new_img.height, oy + other_img.height)

            if x0 < x1 and y0 < y1:
                # crop mask
                new_crop = new_mask.crop((x0 - nx, y0 - ny, x1 - nx, y1 - ny))
                other_crop = other_mask.crop((x0 - ox, y0 - oy, x1 - ox, y1 - oy))

                # check pixel by pixel
                for px1, px2 in zip(new_crop.getdata(), other_crop.getdata()):
                    if px1 > 0 and px2 > 0:
                        return True

        return False

    def plan(self, icon_files):
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
        n = len(icon_files)
        placements = []

        # central icon:
        center_icon = icon_files[0]
        cx, cy = self.canvas_size // 2, self.canvas_size // 2
        center_scale = random.uniform(self.min_scale, self.max_scale)
        center_rot = random.randint(0, 359)

        placements.append({
            "path": center_icon,
            "x": cx,
            "y": cy,
            "scale": center_scale,
            "rotation": center_rot
        })

        # remaining icons (n-1)
        for i, icon_path in enumerate(icon_files[1:], start=1):
            angle = 2 * math.pi * (i - 1) / (n - 1)
            placed = False

            for _ in range(self.max_attempts):
                base_r = (self.radius - self.padding_from_edge) * self.slice_distance_factor
                radius_offset = random.uniform(-0.15 * self.radius, 0.15 * self.radius)
                angle_offset = random.uniform(-math.pi / (n - 1), math.pi / (n - 1))

                r = base_r + radius_offset
                a = angle + angle_offset

                x = cx + r * math.cos(a)
                y = cy + r * math.sin(a)

                scale = random.uniform(self.min_scale, self.max_scale)
                rot = random.randint(0, 359)

                placement = {
                    "path": icon_path,
                    "x": x,
                    "y": y,
                    "scale": scale,
                    "rotation": rot
                }

                if not self._collides(placement, placements):
                    placements.append(placement)
                    placed = True
                    break

            if not placed:
                # fallback – place icon anyway, we don't want to lose it
                placements.append(placement)

        return placements
