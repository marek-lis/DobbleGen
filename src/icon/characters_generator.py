from PIL import Image, ImageDraw, ImageFont
import os

class Characters_Generator:
    def __init__(self, characters, font_path, font_size, width, height, background_color=(255, 255, 255, 0)):
        self.characters = characters
        self.font_path = font_path
        self.font_size = font_size
        self.width = width
        self.height = height
        self.background_color = background_color
        self.color_index = 0

    def generate_images(self, output_path):
        os.makedirs(output_path, exist_ok=True)
        file_number = 1

        for char in self.characters:
            # create new image with alpha channel
            image = Image.new("RGBA", (self.width, self.height), self.background_color)
            draw = ImageDraw.Draw(image)
            # load font
            font = ImageFont.truetype(self.font_path, self.font_size, encoding='UTF-8')
            # center text
            text_width, text_height = draw.textsize(char['character'], font)
            x = (self.width - text_width) / 2
            y = (self.height - text_height) / 2
            # add black outline around character
            outline_color = (0, 0, 0, 255)
            outline_width = 5
            draw.text((x, y), char['character'], fill=char['color'], font=font, stroke_width=outline_width, stroke_fill=outline_color)
            # add dot in the bottom left corner
            dot_color = char['color']
            dot_size = 20
            dot_x = 10
            dot_y = self.height - dot_size - 10
            outline_width = 6
            # draw.ellipse((dot_x, dot_y, dot_x + dot_size, dot_y + dot_size), fill=dot_color, outline=outline_color, width=outline_width)
            draw.ellipse((dot_x, dot_y, dot_x + dot_size, dot_y + dot_size), fill=dot_color, outline=outline_color, width=outline_width)

            file_name = f"{file_number:02}.png"
            file_number += 1
            image.save(os.path.join(output_path, file_name))