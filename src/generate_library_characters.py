from icon.characters_generator import Characters_Generator
import os

letters_and_digits = [
  {'character': 'A', 'color': "#1FF952"},
  {'character': 'Ą', 'color': "#FDFD0F"},
  {'character': 'B', 'color': "#FC4C49"},
  {'character': 'C', 'color': "#6028C1"},
  {'character': 'Ć', 'color': "#FDEF4D"},
  {'character': 'D', 'color': "#17F8A2"},
  {'character': 'E', 'color': '#FF6F4B'},
  {'character': 'Ę', 'color': "#33F497"},
  {'character': 'F', 'color': "#05F97F"},
  {'character': 'G', 'color': "#DB4C4C"},
  {'character': 'H', 'color': "#68DC42"},
  {'character': 'I', 'color': "#24F519"},
  {'character': 'J', 'color': '#FE68B8'},
  {'character': 'K', 'color': '#4022A5'},
  {'character': 'L', 'color': "#FFAE00"},
  {'character': 'Ł', 'color': '#68F4F7'},
  {'character': 'M', 'color': '#9469E6'},
  {'character': 'N', 'color': "#601BC0"},
  {'character': 'Ń', 'color': "#EB4744"},
  {'character': 'O', 'color': '#C4867A'},
  {'character': 'Ó', 'color': '#EBFB22'},
  {'character': 'P', 'color': "#5BC1E3"},
  {'character': 'Q', 'color': '#FF6F4B'},
  {'character': 'R', 'color': "#2E7CF0"},
  {'character': 'S', 'color': '#51E3F1'},
  {'character': 'Ś', 'color': "#7DF061"},
  {'character': 'T', 'color': '#C70AA9'},
  {'character': 'U', 'color': "#3AEE7C"},
  {'character': 'V', 'color': '#DA2A48'},
  {'character': 'W', 'color': "#F7AC2A"},
  {'character': 'X', 'color': '#B74CE7'},
  {'character': 'Y', 'color': "#1FE3E3"},
  {'character': 'Z', 'color': "#58F1BC"},
  {'character': 'Ż', 'color': "#2AEB18"},
  {'character': 'Ź', 'color': "#C3F947"},
  {'character': 'a', 'color': "#D28108"},
  {'character': 'ą', 'color': "#63EFFF"},
  {'character': 'b', 'color': "#AFFE82"},
  {'character': 'c', 'color': "#59F0BB"},
  {'character': 'ć', 'color': '#08E71B'},
  {'character': 'd', 'color': "#F37F3C"},
  {'character': 'e', 'color': '#E1A3D8'},
  {'character': 'ę', 'color': "#F5D639"},
  {'character': 'f', 'color': '#73F25A'},
  {'character': 'g', 'color': '#E5BB49'},
  {'character': 'h', 'color': "#04DD7B"},
  {'character': 'i', 'color': "#934AFF"},
  {'character': 'j', 'color': "#4479FF"},
  {'character': 'k', 'color': "#7ED730"},
  {'character': 'l', 'color': "#74C40A"},
  {'character': 'ł', 'color': "#DCEB03"},
  {'character': 'm', 'color': "#23EEF2"},
  {'character': 'n', 'color': '#D001CA'},
  {'character': 'ń', 'color': "#60EEF8"},
  {'character': 'o', 'color': '#2DBE60'},
  {'character': 'ó', 'color': "#B05CA9"},
  {'character': 'p', 'color': "#5BEDB1"},
  {'character': 'q', 'color': '#2282DD'},
  {'character': 'r', 'color': "#97E4F8"},
  {'character': 's', 'color': "#D418AB"},
  {'character': 'ś', 'color': "#AF7DFF"},
  {'character': 't', 'color': "#F06542"},
  {'character': 'u', 'color': "#5DBBFA"},
  {'character': 'v', 'color': '#F95B07'},
  {'character': 'w', 'color': '#85CF22'},
  {'character': 'x', 'color': "#E0CD50"},
  {'character': 'y', 'color': "#FFB732"},
  {'character': 'z', 'color': "#3DD876"},
  {'character': 'ż', 'color': "#7476F4"},
  {'character': 'ź', 'color': "#DD164F"},
  {'character': '0', 'color': "#BCF061"},
  {'character': '1', 'color': "#E72121"},
  {'character': '2', 'color': "#3793D9"},
  {'character': '3', 'color': '#11EAF9'},
  {'character': '4', 'color': "#1FD76C"},
  {'character': '5', 'color': '#C1D202'},
  {'character': '6', 'color': "#79DC1D"},
  {'character': '7', 'color': "#FA961C"},
  {'character': '8', 'color': '#62C546'},
  {'character': '9', 'color': "#D9255E"},
  {'character': '+', 'color': '#A98525'},
  {'character': '-', 'color': '#E98525'},
  {'character': '*', 'color': '#F98525'},
  {'character': '?', 'color': '#C98525'},
  {'character': '!', 'color': '#B98525'},
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
font_path = "lib/fonts/Ranchers.ttf"

input_57_letters_digits = "ABCDEFGHIJKLMNOPRSTUWXYZabcdefghijklmnoprstuwxyz123456789"
input_57_letters_pl_v1 = "AĄBCĆDEĘFGHIJKLŁMNOÓPQRSŚTUWXYZŹŻabcdefghijklmnoprstuwxyz"
input_57_letters_pl_v2 = "AĄBCĆDEĘFGHIJKLŁMNŃOÓPRSŚTUWYZŹŻaąbcdeęfghijklłmnńprstuwy"
input_43_letters_pl_digits = "AĄBCĆDEĘFGHIJKLŁMNOÓPQRSŚTUWXYZŹŻ1234567890"
input_31_letters_pl = "AĄBCĆDEĘFGHIJKLŁMNOÓPRSŚTUWXYZŻ"

selected_characters = map_string_to_colors(input_57_letters_pl_v2)

letter_pics_generator = Characters_Generator(
    characters = selected_characters, 
    font_path = font_path, 
    font_size = 235, 
    width = 256, 
    height = 256
  )
letter_pics_generator.generate_images(output_path)