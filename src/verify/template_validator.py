import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re
import os

class Template_Validator:
        
        def __init__(self):
             None

        def __read_input_file(self, input_filename):
            self.__lists = {}
            with open(input_filename, "r") as file:
                line_number = 0
                for line in file:
                    match = re.match(r"\s*\[\s*(\d{1,3}(?:,\s*\d{1,3})*)\s*\],?", line.strip())
                    if match:
                        line_number = line_number + 1
                        numbers = list(map(int, match.group(1).split(",")))
                        self.__lists[line_number] = numbers

        def __calculate_matrix(self, lists):
            lines = sorted(lists.keys())
            self.__matrix = pd.DataFrame(index=lines, columns=lines)
            for i in lines:
                for j in lines:
                    common = set(lists[i]) & set(lists[j])
                    self.__matrix.loc[i, j] = len(common)

        def __export_template(self, lists, base_name, output_path):
            template_filename = f"{output_path}/result_{base_name}.txt"
            with open(template_filename, "w") as f:
                for key in sorted(lists.keys()):
                    row = lists[key]
                    formatted_row = "[" + ", ".join(f"{num:02d}" for num in row) + "],"
                    f.write(formatted_row + "\n")
            print(f"Successfully exported the Template to: \t{template_filename}")

        def __export_csv(self, matrix, base_name, output_path):
            csv_filename = f"{output_path}/result_{base_name}.csv"
            matrix.to_csv(csv_filename)
            print(f"Successfully exported the CSV to: \t{csv_filename}")

        def __export_heatmap(self, matrix, base_name, output_path):
            plt.figure(figsize=(14, 12))
            sns.heatmap(matrix.astype(int), annot=True, fmt="d", cmap="YlGnBu")
            plt.title(f"Macierz zgodności – {base_name}")
            plt.tight_layout()
            png_filename = f"{output_path}/result_{base_name}.png"
            plt.savefig(png_filename)
            # plt.show()
            print(f"Successfully exported the Heat Map to: \t{png_filename}")

        def validate(self, input_filename, output_path):
             self.__input_file_name = input_filename
             self.__output_path = output_path
             self.__base_name = os.path.splitext(os.path.basename(input_filename))[0]
             self.__read_input_file(self.__input_file_name)
             self.__calculate_matrix(self.__lists)
             self.__export_csv(self.__matrix, self.__base_name, self.__output_path)
             self.__export_heatmap(self.__matrix, self.__base_name, self.__output_path)
             self.__export_template(self.__lists, self.__base_name, self.__output_path)