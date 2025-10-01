from icon.characters_generator import Characters_Generator
import os

letters_and_digits = [
  {'character': 'A', 'color': '#729DE2'},
  {'character': 'Ą', 'color': '#885941'},
  {'character': 'B', 'color': '#DA4A48'},
  {'character': 'C', 'color': '#391674'},
  {'character': 'Ć', 'color': '#A59C34'},
  {'character': 'D', 'color': '#D4B1A9'},
  {'character': 'E', 'color': '#FF6F4B'},
  {'character': 'Ę', 'color': '#2CCB7E'},
  {'character': 'F', 'color': '#8EDDB6'},
  {'character': 'G', 'color': '#863D52'},
  {'character': 'H', 'color': '#CAFCBA'},
  {'character': 'I', 'color': '#9FFEDB'},
  {'character': 'J', 'color': '#FE68B8'},
  {'character': 'K', 'color': '#4022A5'},
  {'character': 'L', 'color': '#DEBA0B'},
  {'character': 'Ł', 'color': '#68F4F7'},
  {'character': 'M', 'color': '#9469E6'},
  {'character': 'N', 'color': '#441D7A'},
  {'character': 'Ń', 'color': '#C43D3A'},
  {'character': 'O', 'color': '#C4867A'},
  {'character': 'Ó', 'color': '#EBFB22'},
  {'character': 'P', 'color': '#3F8299'},
  {'character': 'Q', 'color': '#FF6F4B'},
  {'character': 'R', 'color': '#225DB4'},
  {'character': 'S', 'color': '#51E3F1'},
  {'character': 'Ś', 'color': '#639557'},
  {'character': 'T', 'color': '#C70AA9'},
  {'character': 'U', 'color': '#58BC9E'},
  {'character': 'V', 'color': '#DA2A48'},
  {'character': 'W', 'color': '#C9AB79'},
  {'character': 'X', 'color': '#B74CE7'},
  {'character': 'Y', 'color': '#0D9695'},
  {'character': 'Z', 'color': '#7EF8CD'},
  {'character': 'Ż', 'color': '#1CDE0B'},
  {'character': 'Ź', 'color': '#50F947'},
  {'character': 'a', 'color': '#093505'},
  {'character': 'ą', 'color': '#2C99A5'},
  {'character': 'b', 'color': '#346402'},
  {'character': 'c', 'color': '#215714'},
  {'character': 'ć', 'color': '#08E71B'},
  {'character': 'd', 'color': '#FCA777'},
  {'character': 'e', 'color': '#E1A3D8'},
  {'character': 'ę', 'color': '#F0D23F'},
  {'character': 'f', 'color': '#73F25A'},
  {'character': 'g', 'color': '#E5BB49'},
  {'character': 'h', 'color': '#069554'},
  {'character': 'i', 'color': '#6117D2'},
  {'character': 'j', 'color': '#5E1EF0'},
  {'character': 'k', 'color': '#738B60'},
  {'character': 'l', 'color': '#5EA108'},
  {'character': 'ł', 'color': '#41DAAB'},
  {'character': 'm', 'color': '#997A7B'},
  {'character': 'n', 'color': '#D001CA'},
  {'character': 'ń', 'color': '#30A1AA'},
  {'character': 'o', 'color': '#2DBE60'},
  {'character': 'ó', 'color': '#462443'},
  {'character': 'p', 'color': '#5BBB93'},
  {'character': 'q', 'color': '#2282DD'},
  {'character': 'r', 'color': '#B94487'},
  {'character': 's', 'color': '#A03FB3'},
  {'character': 'ś', 'color': '#481D8B'},
  {'character': 't', 'color': '#D48471'},
  {'character': 'u', 'color': '#05474B'},
  {'character': 'v', 'color': '#F95B07'},
  {'character': 'w', 'color': '#85CF22'},
  {'character': 'x', 'color': '#B0A76A'},
  {'character': 'y', 'color': '#E5813E'},
  {'character': 'z', 'color': '#717C71'},
  {'character': 'ż', 'color': '#B751F6'},
  {'character': 'ź', 'color': '#CB1245'},
  {'character': '0', 'color': '#728B46'},
  {'character': '1', 'color': '#D01F62'},
  {'character': '2', 'color': '#333E59'},
  {'character': '3', 'color': '#11EAF9'},
  {'character': '4', 'color': '#2282DD'},
  {'character': '5', 'color': '#C1D202'},
  {'character': '6', 'color': '#8FDC1D'},
  {'character': '7', 'color': '#E0EDAD'},
  {'character': '8', 'color': '#62C546'},
  {'character': '9', 'color': '#D98525'}
]

char_color_dict = {item['character']: item['color'] for item in letters_and_digits}

def map_string_to_colors(input_string):
    result = []
    for char in input_string:
        if char in char_color_dict:
            result.append({'character': char, 'color': char_color_dict[char]})
        else:
            result.append({'character': char, 'color': '#FF0000'})
    return result


output_path = 'lib/icons/57_letters_pl/'
font_path = "lib/fonts/DynaPuff-Bold.ttf"

input_57_letters_digits = "ABCDEFGHIJKLMNOPRSTUWXYZabcdefghijklmnoprstuwxyz123456789"
input_57_letters_pl_v1 = "AĄBCĆDEĘFGHIJKLŁMNOÓPQRSŚTUWXYZŹŻabcdefghijklmnoprstuwxyz"
input_57_letters_pl_v2 = "AĄBCĆDEĘFGHIJKLŁMNŃOÓPRSŚTUWYZŹŻaąbcdeęfghijklłmnńprstuwy"
input_43_letters_pl_digits = "AĄBCĆDEĘFGHIJKLŁMNOÓPQRSŚTUWXYZŹŻ1234567890"
input_31_letters_pl = "AĄBCĆDEĘFGHIJKLŁMNOÓPRSŚTUWXYZŻ"

selected_characters = map_string_to_colors(input_57_letters_pl_v2)

letter_pics_generator = Characters_Generator(
    characters = selected_characters, 
    font_path = font_path, 
    font_size = 240, 
    width = 256, 
    height = 256
  )
letter_pics_generator.generate_images(output_path)