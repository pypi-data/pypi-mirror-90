import os
import json
import pickle
from collections import OrderedDict

from . import decorators


@decorators.timeit
def write_json(data, file_path):
    """
    Writes a json file

    :param data: <dict> data
    :param file_path: <string> where to save the file
    :return: None
    """
    folder_name = os.path.dirname(file_path)
    if not os.path.isdir(folder_name):
        os.makedirs(os.path.dirname(file_path))

    with open(file_path, "w") as filename:
        json.dump(data, filename, indent=4)

@decorators.timeit
def read_json(file_path, ordered_dict=False):
    """
    Reads a json file

    :param file_path: <string> file_path
    :param ordered_dict: <bool> If set to True, will return the dictionary with keys in the same order as the json file
    :return: <dict>
    """
    with open(file_path, "r") as filename:
        if ordered_dict:
            return json.load(filename, object_pairs_hook=OrderedDict)
        else:
            return json.load(filename)

@decorators.timeit
def write_pickle(dictionary, file_path):
    """
    Writes a pickle file

    :param data: <dict> data
    :param file_path: <string> where to save the file
    :return: None
    """
    folder_name = os.path.dirname(file_path)
    if not os.path.isdir(folder_name):
        os.makedirs(os.path.dirname(file_path))

    with open(file_path, "wb") as data_file:
        pickle.dump(dictionary, data_file)

@decorators.timeit
def read_pickle(filename):
    """
    Reads a json file

    :param filename: <string> file_path
    :return: <dict>
    """
    with open(filename, "rb") as filename:
        return pickle.load(filename)


def file_content_to_list(file_path):
    """
    Convenience readable one liner to read a file's content to a list

    :param file_path: <string> path to the file
    :return: None
    """
    with open(file_path) as f:
        lines = f.readlines()

    return lines


def write_list_to_file(input_list, filepath, add_new_line=False):
    """
    Convenience readable one liner that writes the content of a list to a file, line by line

    :param input_list: <list> content
    :param filepath: <string> path to file
    :param add_new_line: <bool> whether or not to add an extra newline (\n) at the end of every line
    :return: None
    """
    with open(filepath, 'w') as outfile:
        for line in input_list:
            if add_new_line is True:
                outfile.write("\n".join(str(line) for line in input_list))
            else:
                outfile.write(line)


