import csv


def read_csv(file_name=''):
    return list(csv.reader(open(file_name)))


def write_to_csv(output_list: list, root_path: str):
    if not root_path.__contains__('\\'):
        writer = csv.writer(open("output.csv", "w", newline=''))
        writer.writerows(output_list)
        print("Writing task completed, see: output.csv")
    else:
        writer = csv.writer(open(root_path + "\\output.csv", "w", newline=''))
        writer.writerows(output_list)
        print("Writing task completed, see: " + root_path + "output.csv")
