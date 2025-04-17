import os
import csv
import ast

def get_data(filename):
    file_path = get_filepath(filename)

    data = read_file(file_path)

    cleaned_data = clean_data(data)

    return cleaned_data

def get_filepath(filename):
    """
    Returns the file path of the given filename.
    """
    data_folder = os.path.join(os.path.dirname(__file__), '../Data')
    file_path = os.path.join(data_folder, filename)

    return file_path

def clean_data(data):
    header = [data[0]]
    cleaned_data = [clean_line(line) for line in data[1:]]

    return header + cleaned_data

def read_file(file_path):
    """
    Reads a file and returns its contents.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = list(csv.reader(f))

    return data

def clean_line(line):
    """
    Cleans a line of data by removing leading and trailing whitespace.
    """

    line = fix_ingredients(line)

    return line

def fix_ingredients(line):
    line[3] = ast.literal_eval(line[3])

    print(line)
    return line

if __name__ == "__main__":
    a = get_data("test_data.csv")
    print(a)
