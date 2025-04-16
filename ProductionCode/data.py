import os

def get_data(filename):
    data_folder = os.path.join(os.path.dirname(__file__), '../Data')
    file_path = os.path.join(data_folder, filename)
    
    with open(file_path, "r", encoding="utf-8") as f:
        data = f.readlines()
    
    cleaned_data = [clean_line(line) for line in data]


    return cleaned_data

def clean_line(line):
    """
    Cleans a line of data by removing leading and trailing whitespace.
    """
    print(line[3])
    return line.strip()

if __name__ == "__main__":
    data = get_data("test_data.csv")
    print(data[3])


