from menu import init_menu, handle_menu_event
from custom_io import read_csv
from utils import format_csv

# train_labels.csv
if __name__ == '__main__':
    print("Welcome to CSV formatter, if you have problems using this tool, visit: "
          "https://github.com/fatihozkan-github/csv_formatter")
    while True:
        print('Add your csv file to project directory. When you are ready insert filename below.\n'
              'OR you can drag your file here.')
        given_file_name = input('File name: ')
        show_menu = False
        row_list = []
        root_path = given_file_name.split('\\')[-1]
        print(root_path)
        root_path = given_file_name.replace(root_path, '')
        print(root_path)
        try:
            row_list = read_csv(file_name=given_file_name)
            row_list = format_csv(row_list)
            show_menu = True
        except (Exception,):
            print("No such file or directory. Check your file location & name.")
            show_menu = False

        while show_menu:
            index = 0
            init_menu()
            try:
                index = int(input('Enter your choice: '))
            except(Exception,):
                print("Invalid input, please enter an int value.")
            handle_menu_event(index, row_list, root_path=root_path)
