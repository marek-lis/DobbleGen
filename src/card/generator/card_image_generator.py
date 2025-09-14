from PIL import Image, ImageDraw

class Card_Image_Generator:
    def __init__(self, 
            canvas_size = 1024, 
            padding_from_circle = 10,
            fill_color = '#FFFFFF',
            outline_color = '#CCCCCC',
            outline_width = 3
        ):
        self.canvas_size = canvas_size
        self.padding_from_circle = padding_from_circle
        self.fill_color = fill_color
        self.outline_color = outline_color
        self.outline_width = outline_width

    def __draw_ellipse_background(self):
        draw = ImageDraw.Draw(self.card)
        draw.ellipse(
            (
                self.padding_from_circle, 
                self.padding_from_circle,
                self.canvas_size - self.padding_from_circle,
                self.canvas_size - self.padding_from_circle
            ),
            fill = self.fill_color, 
            outline = self.outline_color, 
            width = self.outline_width
        )

    def __draw_icon(self, placement):
        icon = Image.open(placement["path"]).convert("RGBA")
        w, h = icon.size
        icon = icon.resize((int(w * placement["scale"]), int(h * placement["scale"])), resample=Image.LANCZOS)
        icon = icon.rotate(placement["rotation"], expand=True, resample=Image.BICUBIC)

        x = int(placement["x"] - icon.width / 2)
        y = int(placement["y"] - icon.height / 2)

        self.card.alpha_composite(icon, (x, y))

    def generate(self, placements, output_path):
        self.card = Image.new("RGBA", (self.canvas_size, self.canvas_size), (255, 255, 255, 0))
        self.__draw_ellipse_background()
        for placement in placements:
            self.__draw_icon(placement)
        self.card.save(output_path, dpi=(600, 600), format='PNG', subsampling=0, quality=100)
