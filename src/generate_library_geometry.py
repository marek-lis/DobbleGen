from icon.geometry.geometric_shapes_generator import Geometric_Shapes_Generator
import os

output_path = 'lib/icons/80_geometry/'
os.makedirs(output_path, exist_ok=True)
generator = Geometric_Shapes_Generator()
generator.create(output_path)