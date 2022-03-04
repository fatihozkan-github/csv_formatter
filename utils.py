from constants import Constants
import random


def get_root(path: str):
    print(path)


def format_csv(row_list):
    for row in row_list:
        assert isinstance(row, list)
        for _ in (0, 1):
            row.pop(1)
            row.append("")
            row.insert(5, "")
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


def fix_coordinates(row_list: list, image_size=512, decimal=8, debug=False):
    """• Assumes that the height & width of the image are equal."""
    new_row_list = []
    for row in row_list:
        for i in [3, 4, 7, 8]:
            if not 0.0 <= float(str(row[i])) <= 1.0:
                row[i] = round(float(str(row[i])) / image_size, decimal)
                if debug:
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
