from icon.test_pics_generator import Test_Pics_Generator
import os

generator = Test_Pics_Generator()
icons_num = 57
output_path = "lib/icons/" + str(icons_num) + "_test_squares/"
os.makedirs(output_path, exist_ok=True)
for i in range(icons_num):
    generator.create(output_path, i)
