import xml.etree.ElementTree as ET
from constants import Constants
import pandas as pd
import random
import glob
import os


def get_root(file: str):
    root_path = file.split('\\')[-1]
    return file.replace(root_path, '')


def format_csv(row_list: list):
    if row_list[0].__contains__('filename'):
        row_list.pop(0)
    for row in row_list:
        assert isinstance(row, list)
        for _ in (0, 1):
            row.append("")
            row.insert(4, "")
    return row_list


def add_data_type(row_list: list, train_ratio=0.8, validate_ratio=0.1, test_ratio=0.1, debug=False):
    """
    • Adds the data types to csv rows.
    • Initial proportions are adjusted according to official documentation.
    """
    if train_ratio + validate_ratio + test_ratio != 1.0:
        raise Exception("sum of train, validate and test ratios must be equal to 1.0, current: "
                        + str(train_ratio + validate_ratio + test_ratio))
    else:
        list_len = len(row_list)
        train_number, validate_number, test_number = \
            int(list_len * train_ratio), int(list_len * validate_ratio), int(list_len * test_ratio)
        if debug:
            print("Train Number: " + str(train_number), "Validate Number: " + str(validate_number),
                  "Test Number: " + str(test_number))
        i = 0
        indices = [*range(0, len(row_list), 1)]
        while i < test_number:
            generated_index = random.randint(0, len(row_list))
            if indices.__contains__(generated_index):
                row_list[generated_index].insert(0, Constants.DATA_TYPE_TEST)
                indices.remove(generated_index)
                i += 1

        i = 0
        while i < validate_number:
            generated_index = random.randint(0, len(row_list))
            if indices.__contains__(generated_index):
                row_list[generated_index].insert(0, Constants.DATA_TYPE_VALIDATE)
                indices.remove(generated_index)
                i += 1

        for row in row_list:
            if row[0] != Constants.DATA_TYPE_TEST and row[0] != Constants.DATA_TYPE_VALIDATE:
                row.insert(0, Constants.DATA_TYPE_TRAIN)


def fix_coordinates(row_list: list, image_size=512, decimal=8):
    """• Assumes that the height & width of the image are equal."""
    new_row_list = []
    for row in row_list:
        for i in [3, 4, 7, 8]:
            if not 0.0 <= float(str(row[i])) <= 1.0:
                row[i] = round(float(str(row[i])) / image_size, decimal)
                if True:
                    print("ACTUAL: " + str(float(str(row[i])) / image_size))
                    print("ROUNDED: " + str(round(float(str(row[i])) / image_size, decimal)))
        new_row_list.append(row)

    return new_row_list


def change_extension(row_list, target_extension='jpeg'):
    """
    • Changes the extensions in the csv file so you do not have to
    create a new csv file after changing the extension of images.

    • Supported extensions (due to TFLite Model Maker): JPEG, PNG, GIF, BMP, ICO
    """
    for row in row_list:
        row[1] = str(row[1]).split('.').pop(0)
        row[1] = '.'.join([str(row[1]), str(target_extension)])
    return row_list


def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            width = int(root.find('size')[0].text),
            height = int(root.find('size')[1].text),
            value = (root.find('filename').text,
                     member[0].text,
                     float(member[4][0].text) / (width[0]),
                     float(member[4][1].text) / (height[0]),
                     float(member[4][2].text) / (width[0]),
                     float(member[4][3].text) / (height[0]),
                     )
            xml_list.append(value)
    column_name = ['filename', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def xml_handler():
    print('\n* XML to CSV Tool *\nAdd your folder to project directory. When you are ready insert folder name below.\n'
          'OR you can drag your folder here.')
    given_folder_name = input('Folder name: ')

    if given_folder_name.endswith("\""):
        given_folder_name = given_folder_name.split("\"")[1]

    try:
        xml_df = xml_to_csv(given_folder_name)
        xml_df.to_csv(given_folder_name + '/labels.csv', index=False)
        print('Successfully converted XML files to CSV! See output.csv')
        os.system("main.py")
    except (Exception,):
        print("An error has occurred.")
        os.system("main.py")
