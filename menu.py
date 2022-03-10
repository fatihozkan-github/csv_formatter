from utils import add_data_type, fix_coordinates, change_extension
from custom_io import write_to_csv

menu_options = {
    1: 'Add Data Types',
    2: 'Change Image Extension',
    3: 'Adjust Coordinates',
    4: 'Save Finalized CSV',
    5: 'Exit',
}


def init_menu():
    for key in menu_options.keys():
        print(key, '-', menu_options[key])


def handle_first_case(row_list):
    print("Please enter train, validation, test ratios respectively. Separate them with commas.\n"
          "Example: 0.8, 0.1, 0.1, their sum must be equal to 1.0.\n"
          "If you do not know what you are doing just leave empty. Formatter will handle it with default values.")
    try:
        a, b, c = input("Train Ratio, Validation Ratio, Test Radio: ").split(',')
    except(Exception,):
        print("Input error, using default value: 0.8, 0.1, 0.1\n...")
        a, b, c = 0.8, 0.1, 0.1
    try:
        add_data_type(row_list, train_ratio=float(a), validate_ratio=float(b), test_ratio=float(c))
        print("Data types added.")
    except(Exception,):
        print("Add data type error.")


def handle_second_case(row_list):
    try:
        print("Supported image formats (due to Model Maker): JPEG, PNG, GIF, BMP, ICO")
        target_extension = str(input("Target Extension: "))
        supported_formats = ['jpeg', 'png', 'gif', 'bmp', 'ico']
        if not supported_formats.__contains__(target_extension):
            print("Input error, using default value: jpeg")
            target_extension = 'jpeg'
        change_extension(row_list, target_extension=target_extension)
        print('Image extensions changed.')
    except(Exception,):
        print('Image extension change failed.')


def handle_third_case(row_list):
    print("Enter parameters (Optional)")
    image_size = int(input("Image size(Default:512): "))
    decimal = int(input("Decimal(Default:8): "))
    fix_coordinates(row_list, image_size=int(image_size), decimal=int(decimal))
    print("Coordinates adjusted.")


def handle_menu_event(index: int, row_list: list, root_path: str):
    if index == 1:
        handle_first_case(row_list)
    elif index == 2:
        handle_second_case(row_list)
    elif index == 3:
        handle_third_case(row_list)
    elif index == 4:
        write_to_csv(row_list, root_path)
    elif index == 5:
        print('Thanks & goodbye! -F')
        exit()
    else:
        print('Invalid option. Please enter a number between 1 and 6.')
