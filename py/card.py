import math
from random import randrange
from PIL import Image, ImageDraw


class Card:

    __card = None

    def __init__(self):
        self.__card = Image.new('RGBA', (1024, 1024))

    def __create_background(self, card):
        background = ImageDraw.Draw(card)
        background.ellipse((0, 0, card.width-1, card.height-1),
                           fill='#FFFFFF', outline='#000000')
        return background

    def __create_icon(self, icon_url, icon_width):
        icon = Image.open(icon_url)
        ratio = icon.height / icon.width
        w = round(icon_width - randrange(0, round(icon_width/3)))
        h = round(w * ratio)
        icon = icon.resize((w, h), Image.ANTIALIAS)
        icon = icon.rotate(randrange(0, 360, 1),
                           resample=Image.BICUBIC, expand=True)
        print(icon.width, icon.height, w, h, ratio)
        return icon

    def __create_icons(self, card, icons):
        i = 0
        items = len(icons)
        # card width, card height
        (cw, ch) = (card.width, card.height)
        # card width / 4, card height / 4
        (cw4, ch4) = (round(cw/4), round(ch/4))
        # card width / 2, card height / 2
        (cw2, ch2) = (2*cw4, 2*ch4)
        angle_per_item = math.pi * 2 / (items - 1)
        for icon in icons:
            content = self.__create_icon(icon, cw4)
            # icon width, icon height
            (iw, ih) = (content.width, content.height)
            # icon width / 4, icon height / 4
            (iw4, ih4) = (round(iw/4), round(ih/4))
            # icon width / 2, icon height / 2
            (iw2, ih2) = (2*iw4, 2*ih4)
            # angle for current item
            angle = i * angle_per_item
            if i == 0:
                # place first item in the middle of the card
                (px, py) = (cw2 - iw2, ch2 - ih2)
            else:
                if i % 2 != 0:
                    mul = 1.0
                else:
                    mul = 0.5
                # place the rest of items around the card
                (px, py) = (cw2 + round(math.sin(angle) * (cw4+mul*iw4)) -
                            iw2, ch2 + round(math.cos(angle) * (ch4+mul*ih4)) - ih2)
            card.paste(content, box=(px, py), mask=content)
            #card.paste(content, box=(px, py))
            i += 1

    def __save_card(self, card, output_file):
        card.save(output_file, dpi=(600, 600),
                  format='PNG', subsampling=0, quality=100)

    def generate_card(self, icons, output_file):
        self.__create_background(self.__card)
        self.__create_icons(self.__card, icons)
        self.__save_card(self.__card, output_file)
