import math
import random
from PIL import Image, ImageDraw

class Card_Image_Creator:

    def __init__(self, canvas_size=1024, base_item_size=256,
                 min_scale=0.3, max_scale=1.0):
        self.__canvas_size = canvas_size
        self.__base_item_size = base_item_size
        self.__radius = canvas_size // 2
        self.__min_scale = min_scale
        self.__max_scale = max_scale

    def __prepare_img(self, path, scale, rotate=True):
        img = Image.open(path).convert("RGBA")
        size = int(self.__base_item_size * scale)
        img = img.resize((size, size), Image.BICUBIC)
        if rotate:
            angle = random.randint(0, 359)
            img = img.rotate(angle, resample=Image.BICUBIC, expand=True)
        return img

    def __inside_circle(self, cx, cy, w, h):
        center_x, center_y = self.__radius, self.__radius
        corners = [(cx, cy), (cx + w, cy), (cx, cy + h), (cx + w, cy + h)]
        return all((x - center_x)**2 + (y - center_y)**2 <= self.__radius**2 for x, y in corners)

    def __collides(self, placed, x, y, w, h):
        for px, py, pw, ph in placed:
            if not (x + w <= px or x >= px + pw or y + h <= py or y >= py + ph):
                return True
        return False

    def create(self, list_with_paths_to_icons, output_path):
        canvas = Image.new("RGBA", (self.__canvas_size, self.__canvas_size), (255,255,255,0))
        placed = []

        # draw background
        draw = ImageDraw.Draw(canvas)
        draw.ellipse((2,2,self.__canvas_size-2,self.__canvas_size-2), fill='#FFFFFF', outline='#CCCCCC', width=3)

        n = len(list_with_paths_to_icons)
        # sort from smallest to biggest
        scales = [random.uniform(self.__min_scale, self.__max_scale) for _ in range(n)]
        scales.sort(reverse=True)

        # divide circle into layers
        num_layers = max(1, n // 2)
        layer_radii = [self.__radius * (i+1)/num_layers for i in range(num_layers)]

        for i, (img_path, scale) in enumerate(zip(list_with_paths_to_icons, scales)):
            img = self.__prepare_img(img_path, scale)
            w, h = img.size

            # bigger icons in the center layer
            layer_idx = min(i, len(layer_radii)-1)
            r_layer = layer_radii[layer_idx]

            # calculate random angle and radius in the center layer
            best_pos = None
            max_attempts = 2000
            for _ in range(max_attempts):
                angle = random.uniform(0, 2*math.pi)
                r = r_layer - w/2 + random.uniform(-w/4, w/4)
                cx = int(self.__radius + r * math.cos(angle) - w/2)
                cy = int(self.__radius + r * math.sin(angle) - h/2)
                if not self.__inside_circle(cx, cy, w, h):
                    continue
                if self.__collides(placed, cx, cy, w, h):
                    continue
                best_pos = (cx, cy)
                break

            if best_pos is None:
                # if not in the best pos, then reduce scale and try again
                attempt_scale = scale
                while attempt_scale > self.__min_scale:
                    attempt_scale *= 0.9
                    img = self.__prepare_img(img_path, attempt_scale)
                    w, h = img.size
                    for _ in range(max_attempts):
                        angle = random.uniform(0, 2*math.pi)
                        r = r_layer - w/2 + random.uniform(-w/4, w/4)
                        cx = int(self.__radius + r * math.cos(angle) - w/2)
                        cy = int(self.__radius + r * math.sin(angle) - h/2)
                        if not self.__inside_circle(cx, cy, w, h):
                            continue
                        if self.__collides(placed, cx, cy, w, h):
                            continue
                        best_pos = (cx, cy)
                        break
                    if best_pos:
                        break

            if best_pos:
                cx, cy = best_pos
                canvas.alpha_composite(img, (cx, cy))
                placed.append((cx, cy, w, h))
            else:
                print(f"Failed to place the picture {img_path}")

        canvas.save(output_path, dpi=(600, 600), format='PNG', subsampling=0, quality=100)
        print(f"✅ *Saved {output_path}.")

# import os
# from composer import CircleImageComposer

# images = [
#     "lib/rect/01.png", 
#     "lib/rect/02.png", 
#     "lib/rect/03.png", 
#     "lib/rect/04.png", 
#     "lib/rect/05.png",
#     "lib/rect/06.png",
#     "lib/rect/07.png",
#     ]

# # utworzenie obiektu kompozytora
# composer = CircleImageComposer(
#     canvas_size=1024,
#     base_item_size=256,
#     min_scale=0.5, 
#     max_scale=1.1 
# )

# # composer.generate(
# #     source_images=images,
# #     output_path="random_maxfilled_dynamic.png"
# # )

# num_generations = 50

# output_dir = "generated_circles"
# os.makedirs(output_dir, exist_ok=True)

# for i in range(1, num_generations+1):
#     output_path = os.path.join(output_dir, f"circle_{i}.png")
#     composer.generate(images, output_path)