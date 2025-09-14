from PIL import Image, ImageDraw, ImageFont
import os

class Characters_Generator:
    def __init__(self, characters, font_path, font_size, width, height, background_color=(255, 255, 255, 0)):
        self.__characters = characters
        self.__font_path = font_path
        self.__font_size = font_size
        self.__width = width
        self.__height = height
        self.__background_color = background_color

    def __draw_centered_text(self, draw, text, font, box_width, box_height, **kwargs):
        # bounding box relative to (0,0)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        # center
        x = (box_width - text_width) / 2 - bbox[0]
        y = (box_height - text_height) / 2 - bbox[1]
        # draw
        draw.text((x, y), text, font=font, **kwargs)

    def __draw_marker(self, draw, size, fill_color, outline_color, outline_width):
        dot_x = 10
        dot_width = dot_x + size
        dot_y = self.__height - size - 10
        dot_height = dot_y + size
        draw.ellipse((dot_x, dot_y, dot_width, dot_height), fill_color, outline_color, outline_width)

    def generate_images(self, output_path):
        os.makedirs(output_path, exist_ok=True)
        file_number = 1
        for char in self.__characters:
            # create new image with alpha channel
            image = Image.new("RGBA", (self.__width, self.__height), self.__background_color)
            draw = ImageDraw.Draw(image)
            # load font
            font = ImageFont.truetype(self.__font_path, self.__font_size, encoding='UTF-8')
            # draw centered character
            self.__draw_centered_text(
                draw, 
                text = char['character'], 
                font = font, 
                box_width = 256, 
                box_height = 256,  
                fill=char['color'], 
                stroke_width=5, 
                stroke_fill=(0, 0, 0, 255)
            )
            # draw dot in the bottom left corner
            self.__draw_marker(
                draw,
                size = 20,
                fill_color = char['color'],
                outline_color = (0, 0, 0, 255),
                outline_width = 6
            )

            file_name = f"{file_number:02}.png"
            file_number += 1
            image.save(os.path.join(output_path, file_name), dpi=(600, 600), format='PNG', subsampling=0, quality=100)