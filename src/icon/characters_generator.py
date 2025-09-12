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

    def generate_images(self, output_path):
        os.makedirs(output_path, exist_ok=True)
        file_number = 1

        for char in self.__characters:
            # create new image with alpha channel
            image = Image.new("RGBA", (self.__width, self.__height), self.__background_color)
            draw = ImageDraw.Draw(image)
            # load font
            font = ImageFont.truetype(self.__font_path, self.__font_size, encoding='UTF-8')
            # center text
            text_width, text_height = draw.textsize(char['character'], font)
            x = (self.__width - text_width) / 2
            y = (self.__height - text_height) / 2
            # add black outline around character
            outline_color = (0, 0, 0, 255)
            outline_width = 5
            draw.text((x, y), char['character'], fill=char['color'], font=font, stroke_width=outline_width, stroke_fill=outline_color)
            # add dot in the bottom left corner
            dot_color = char['color']
            dot_size = 20
            dot_x = 10
            dot_y = self.__height - dot_size - 10
            outline_width = 6
            # draw.ellipse((dot_x, dot_y, dot_x + dot_size, dot_y + dot_size), fill=dot_color, outline=outline_color, width=outline_width)
            draw.ellipse((dot_x, dot_y, dot_x + dot_size, dot_y + dot_size), fill=dot_color, outline=outline_color, width=outline_width)

            file_name = f"{file_number:02}.png"
            file_number += 1
            image.save(os.path.join(output_path, file_name), dpi=(600, 600), format='PNG', subsampling=0, quality=100)