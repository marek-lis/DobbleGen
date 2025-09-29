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

        # center char
        x = (box_width - text_width) / 2 - bbox[0]
        y = (box_height - text_height) / 2 - bbox[1]

        # draw char 
        draw.text((x, y), text, font=font, **kwargs)

        # draw the dot marker in bottom left corner
        dot_radius = 15 
        offset_x = text_width * 0.25
        offset_y = text_height * 0.05
        
        # bottom left corner of the text - offset
        left_bottom_x = x + bbox[0] - offset_x
        left_bottom_y = y + bbox[3] + offset_y
        
        # the dot marker can't go out of the picture!
        left_bottom_x = max(dot_radius, min(box_width - dot_radius, left_bottom_x))
        left_bottom_y = max(dot_radius, min(box_height - dot_radius, left_bottom_y))
        
        # copy the fill and stroke details from the character:
        fill_color = kwargs.get('fill', None)
        stroke_width = kwargs.get('stroke_width', None)
        
        # draw the dot marker in the bottom left corner using the same style
        draw.ellipse(
            (left_bottom_x - dot_radius, left_bottom_y - dot_radius,
            left_bottom_x + dot_radius, left_bottom_y + dot_radius),
            fill=fill_color,
            outline=(0,0,0),
            width = stroke_width
        )

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

            file_name = f"{file_number:02}.png"
            file_number += 1
            image.save(os.path.join(output_path, file_name), dpi=(600, 600), format='PNG', subsampling=0, quality=100)