from utils import format_csv, get_root, xml_to_csv, xml_handler
from menu import init_menu, handle_menu_event
from custom_io import read_csv


if __name__ == '__main__':
    print("Welcome to CSV formatter, if you have problems using this tool, visit: "
          "https://github.com/fatihozkan-github/csv_formatter")
    while True:
        show_menu = False
        use_tool = False
        print('Add your csv file to project directory. When you are ready, insert filename below. '
              'You can also drag your file here.\n'
              'If you want to use XML to CSV tool leave empty.')
        given_file_name = input('File name: ')
        if given_file_name == "":
            use_tool = True
        root_path = get_root(given_file_name)
        row_list = []
        try:
            row_list = read_csv(file_name=given_file_name)
            row_list = format_csv(row_list)
            show_menu = True
        except (Exception,):
            if given_file_name != "":
                print("No such file or directory. Check your file location & name.")
                show_menu = False

        while use_tool:
            xml_handler()

        while show_menu:
            index = 0
            init_menu()
            try:
                index = int(input('Enter your choice: '))
            except(Exception,):
                print("Invalid input, please enter an int value.")
            handle_menu_event(index, row_list, root_path=root_path)
