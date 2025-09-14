import math
import random
from PIL import Image, ImageDraw, ImageChops, ImageOps

class Card_Image_Creator:
    def __init__(self, canvas_size=1024, 
                 base_item_size=256,
                 min_scale=0.5, 
                 max_scale=1.0, 
                 padding_from_circle=10,
                 max_attempts_per_icon=50, 
                 slice_distance_factor=0.6):
        self.canvas_size = canvas_size
        self.base_item_size = base_item_size
        self.radius = canvas_size // 2
        self.min_scale = min_scale
        self.max_scale = max_scale
        self.padding_from_circle = padding_from_circle
        self.max_attempts = max_attempts_per_icon
        self.slice_distance_factor = slice_distance_factor

        self.circle_mask = Image.new("1", (canvas_size, canvas_size), 0)
        draw = ImageDraw.Draw(self.circle_mask)
        draw.ellipse(
            (padding_from_circle, padding_from_circle,
             canvas_size - padding_from_circle,
             canvas_size - padding_from_circle),
            fill=1
        )

    def _prepare_image(self, path, scale):
        img = Image.open(path).convert("RGBA")
        size = max(1, int(self.base_item_size * scale))
        img = img.resize((size, size), Image.BICUBIC)
        angle = random.randint(0, 359)
        img = img.rotate(angle, expand=True)
        return img

    def _get_mask(self, img):
        # Alpha channel -> binary mask (1 = non-transparent)
        return img.split()[3].point(lambda p: 1 if p>0 else 0).convert("1")

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

    def create(self, paths, output_path):
        n = len(paths)
        while True: 
            canvas = Image.new("RGBA", (self.canvas_size, self.canvas_size), (255,255,255,0))
            draw = ImageDraw.Draw(canvas)
            draw.ellipse(
                (self.padding_from_circle, self.padding_from_circle,
                 self.canvas_size - self.padding_from_circle,
                 self.canvas_size - self.padding_from_circle),
                fill='#FFFFFF', outline='#CCCCCC', width=3
            )

            occupancy_map = Image.new("1", (self.canvas_size, self.canvas_size), 0)
            placed_icons = []

            # middle icon (n)
            central_scale = random.uniform(self.max_scale*0.7, self.max_scale)
            central_img = self._prepare_image(paths[0], central_scale)
            central_mask = self._get_mask(central_img)
            cx = self.radius - central_img.width // 2 + random.randint(-20, 20)
            cy = self.radius - central_img.height // 2 + random.randint(-20, 20)
            canvas.alpha_composite(central_img, (cx, cy))
            occupancy_map.paste(central_mask, (cx, cy))
            placed_icons.append((central_mask, cx, cy))

            # check if all other slices are already placed and if not, the keep repeating the while loop
            slices = n - 1
            if slices == 0:
                canvas.save(output_path, dpi=(600,600), format='PNG', subsampling=0, quality=100)
                print(f"✅ Saved {output_path}")
                return

            angle_per_slice = 2*math.pi / slices
            slice_radius_base = (self.radius - self.padding_from_circle) * self.slice_distance_factor

            success = True
            for i, path in enumerate(paths[1:], start=0):
                placed = False
                for attempt in range(self.max_attempts):
                    scale = random.uniform(self.min_scale, self.max_scale)
                    img = self._prepare_image(path, scale)
                    mask = self._get_mask(img)

                    # Kąt w środku slice + losowy offset
                    angle_center = i * angle_per_slice + angle_per_slice / 2
                    angle_offset = random.uniform(-angle_per_slice*0.2, angle_per_slice*0.2)
                    radius_offset = random.uniform(-slice_radius_base*0.1, slice_radius_base*0.1)
                    r = slice_radius_base + radius_offset

                    x = int(self.radius + r * math.cos(angle_center + angle_offset) - img.width//2)
                    y = int(self.radius + r * math.sin(angle_center + angle_offset) - img.height//2)

                    # Sprawdzenie czy ikona mieści się w okręgu
                    if not self._check_inside_circle(mask, x, y):
                        continue
                    # Pixel-perfect kolizja z wszystkimi wcześniej wstawionymi ikonami
                    if self._check_collision(occupancy_map, mask, x, y):
                        continue

                    # Wstawienie ikony
                    canvas.alpha_composite(img, (x, y))
                    occupancy_map.paste(mask, (x, y))
                    placed_icons.append((mask, x, y))
                    placed = True
                    break

                if not placed:
                    success = False
                    break  # restart całej karty

            if success:
                canvas.save(output_path, dpi=(600,600), format='PNG', subsampling=0, quality=100)
                print(f"✅ Saved {output_path}")
                return
