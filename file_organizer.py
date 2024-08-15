class FileOrganizer:

    def __init__(self):
        """
        Initialize the empty directory structure.
        """
        self.final_directory = {}

    def create_action(self, create_dir_content, directory_structure=None):
        """
        Creates a directory in the directory structure.
        :param create_dir_content (str) : path of the directory to create
        :param directory_structure(dict) : Directory structure to work on,
                                this variable is used for edit_action method
        :return: Updated final directory structure.
        """
        if directory_structure is None:
            directory_structure = self.final_directory

        create_list = create_dir_content.split("/")
        create_directory = self.final_directory
        for item in create_list:
            if item not in create_directory:
                create_directory[item] = {}
            create_directory = create_directory[item]
        return self.final_directory

    def move_action(self, move_file_src, move_file_dest):
        """
        Moves a file or directory from source to destination
        :param move_file_src: Source path of the directory or file to move
        :param move_file_dest: Destination path of the directory or file will be moved to.
        :return: None (Because it keeps updating the self.final_directory and accessed all over the class)
        """
        src_move_list = move_file_src.split("/")
        item_to_be_moved = src_move_list[-1]

        moving_item = self.final_directory

        for index, item in enumerate(src_move_list):
            if item in moving_item.keys() and item_to_be_moved in moving_item[item]:
                moving_item = moving_item[item].pop(item_to_be_moved)
            elif item in moving_item.keys():
                moving_item = moving_item.pop(item)

        if moving_item == {}:
            item_to_be_placed = src_move_list[-1]
        else:
            item_to_be_placed = item_to_be_moved + "/" + "/".join(self.dict_to_path(moving_item))
        self.create_action("%s/%s" % (move_file_dest, item_to_be_placed), moving_item)
        return

    def delete_action(self, delete_directory):
        """
        Deletes a directory or the file to be deleted.
        :param delete_directory(str): path of the directory to be deleted
        :return: None (Because it keeps updating the self.final_directory and accessed all over the class)
        """

        delete_list = delete_directory.split("/")

        deleting_dictionary = self.final_directory
        for index, item in enumerate(delete_list):
            if item in deleting_dictionary.keys():
                if index == len(delete_list) - 1:
                    if deleting_dictionary[item]:
                        deleting_dictionary.pop(item)
                    else:
                        print(f"Cannot delete {delete_directory} - {item} does not exist")
                else:
                    deleting_dictionary = deleting_dictionary[item]
            else:
                print(f"Cannot delete {delete_directory} - {item} does not exist")
                break
        return

    def list_action(self, current_directory=None, space=0):
        """
        Lists the contents of the directory in the indented way.
        :param current_directory (dict): Current directory structure to list.
        :param space (int): Number of spaces for indentation
        :return: None
        """
        if current_directory is None:
            current_directory = self.final_directory

        for item in sorted(current_directory.keys()):
            print(" " * space + item)
            if current_directory[item]:
                self.list_action(current_directory=current_directory[item], space=space + 2)
        return

    def dict_to_path(self, dictionary, path=[]):
        """
        Converts dictionary to path.
        Example: {"fruits":{"apples":{"fuji"}}} to ["fruits", "apples", "fuji"]
        :param dictionary: dictionary to convert to path
        :param path: The list of the elements
        :return: List of path elements
        """
        if dictionary != {}:
            for key, value in dictionary.items():
                if isinstance(value, dict):
                    path = self.dict_to_path(value, path + [key])
                else:
                    path.append(key)
        return path


def input_actions(input_str: str):
    """
    Function reads input string and based on action it redirects to corresponding function in FileOrganizer class.
    :param input_str: input string which contains the actions
    :return: None
    """
    actions = input_str.split("\n")
    file_organizer_obj = FileOrganizer()
    for each_action in actions:
        commands = each_action.split()
        if commands[0] == "CREATE":
            print(each_action)
            file_organizer_obj.create_action(commands[1])
        elif commands[0] == "MOVE":
            print(each_action)
            file_organizer_obj.move_action(commands[1], commands[2])
        elif commands[0] == "DELETE":
            print(each_action)
            file_organizer_obj.delete_action(commands[1])
        elif commands[0] == "LIST":
            print(each_action)
            file_organizer_obj.list_action()
    return


input_string = """CREATE fruits
CREATE vegetables
CREATE grains
CREATE fruits/apples
CREATE fruits/apples/fuji
LIST
CREATE grains/squash
MOVE grains/squash vegetables
CREATE foods
MOVE grains foods
MOVE fruits foods
MOVE vegetables foods
LIST
DELETE fruits/apples
DELETE foods/fruits/apples
LIST"""

input_actions(input_string)
