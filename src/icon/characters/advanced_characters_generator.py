from PIL import Image, ImageDraw, ImageFont
import os

class Characters_Generator:
    def __init__(self, characters, font_path, max_font_size, width, height, background_color=(255,255,255,0)):
        self.characters = characters
        self.font_path = font_path
        self.max_font_size = max_font_size
        self.width = width
        self.height = height
        self.background_color = background_color

    def __choose_font_by_target_size(self, ch, stroke_width, max_width, max_height):
        """Select the largest font size that fits both width and height constraints."""
        font_size = self.max_font_size
        while font_size > 4:
            font = ImageFont.truetype(self.font_path, font_size)
            temp = Image.new("L", (self.width, self.height), 0)
            td = ImageDraw.Draw(temp)
            bbox = td.textbbox((0,0), ch, font=font, stroke_width=stroke_width)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
            if text_w <= max_width and text_h <= max_height:
                return font, bbox
            font_size -= 1
        font = ImageFont.truetype(self.font_path, 4)
        temp = Image.new("L", (self.width, self.height), 0)
        td = ImageDraw.Draw(temp)
        bbox = td.textbbox((0,0), ch, font=font, stroke_width=stroke_width)
        return font, bbox

    def __draw_one(self, image, ch, dot_radius, dot_padding, dot_margin_frac, letter_dot_padding,
                   stroke_width, stroke_fill, fill):
        draw = ImageDraw.Draw(image)

        # Calculate top position for the dot relative to the image bottom
        dot_top = self.height - dot_radius - dot_padding - letter_dot_padding

        # Maximum available width and height for the letter
        max_letter_height = max(1, dot_top)
        max_letter_width = max(1, self.width - 2*stroke_width - dot_radius*2 - int(self.width*dot_margin_frac))

        # Select font size so letter fits both height and width
        font, bbox = self.__choose_font_by_target_size(ch, stroke_width, max_letter_width, max_letter_height)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        # Position the letter so its bottom aligns above the dot plus letter_dot_padding
        y_letter = dot_top - text_h - bbox[1]
        x_letter = (self.width - text_w) / 2 - bbox[0]

        # Draw the letter with stroke
        draw.text((x_letter, y_letter), ch, font=font, fill=fill, stroke_width=stroke_width, stroke_fill=stroke_fill)

        # Create a mask to find the letter bounding box
        mask = Image.new("L", (self.width, self.height), 0)
        md = ImageDraw.Draw(mask)
        md.text((x_letter, y_letter), ch, font=font, fill=255, stroke_width=stroke_width)
        letter_bbox = mask.getbbox()
        l_left, l_top, l_right, l_bottom = letter_bbox if letter_bbox else (0,0,0,0)

        # Calculate dot horizontal position relative to the left edge of the letter
        horizontal_padding_px = max(1, int((l_right - l_left) * dot_margin_frac)) if (l_right - l_left) > 0 else max(1, int(text_w * dot_margin_frac))
        dot_x = l_left - dot_radius - horizontal_padding_px
        if dot_x < dot_radius:
            dot_x = max(dot_radius, l_left + horizontal_padding_px)
        dot_y = self.height - dot_radius - dot_padding

        # Clamp dot to stay within image bounds
        dot_x = max(dot_radius, min(self.width - dot_radius - 1, int(dot_x)))
        dot_y = max(dot_radius, min(self.height - dot_radius - 1, int(dot_y)))

        # Draw the dot using the same stroke width and stroke color as the letter
        draw.ellipse(
            (dot_x - dot_radius, dot_y - dot_radius, dot_x + dot_radius, dot_y + dot_radius),
            fill=fill,
            outline=stroke_fill,
            width=stroke_width
        )

    def generate_images(self, 
                        output_path, 
                        dot_radius=10, 
                        dot_padding=16, 
                        dot_margin_frac=0.08,
                        letter_dot_padding=16, 
                        stroke_width=4, 
                        stroke_fill=(0,0,0,255)
                    ):
        """Generate PNG images for all characters in self.characters."""
        os.makedirs(output_path, exist_ok=True)
        for i, ch in enumerate(self.characters, 1):
            img = Image.new("RGBA", (self.width, self.height), self.background_color)
            fill = ch.get("color", (0,0,0,255))
            self.__draw_one(img, ch["character"], dot_radius, dot_padding, dot_margin_frac,
                            letter_dot_padding, stroke_width, stroke_fill, fill)
            fname = f"{i:02}.png"
            img.save(os.path.join(output_path, fname), format="PNG")
