import traceback
import os
import copy
import base64

def trace(message):
    """
    Runs a traceback. Sometimes handy for debugging purposes

    :param message: <string> message to display
    :return: None
    """
    print(message)
    print(traceback.format_exc())

def key_extract(search_key, dictionary):
    #https://stackoverflow.com/questions/9807634/find-all-occurrences-of-a-key-in-nested-python-dictionaries-and-lists
    if hasattr(dictionary, 'items'):
        for key, value in dictionary.items():
            if key == search_key:
                yield value
            if isinstance(value, dict):
                for result in key_extract(search_key, value):
                    yield result
            elif isinstance(value, list):
                for d in value:
                    for result in key_extract(search_key, d):
                        yield result



def object_copy(instance, init_args=None):
    #https://stackoverflow.com/questions/48338847/how-to-copy-a-class-instance-in-python
    if init_args:
        new_obj = instance.__class__(**init_args)
    else:
        new_obj = instance.__class__()
    if hasattr(instance, '__dict__'):
        for k in instance.__dict__ :
            try:
                attr_copy = copy.deepcopy(getattr(instance, k))
            except Exception as e:
                attr_copy = object_copy(getattr(instance, k))
            setattr(new_obj, k, attr_copy)

        new_attrs = list(new_obj.__dict__.keys())
        for k in new_attrs:
            if not hasattr(instance, k):
                delattr(new_obj, k)
        return new_obj
    else:
        return instance

def try_number_parse(value):
    try:
        return int(value)
    except ValueError as err:
        pass

    try:
        return float(value)
    except ValueError as err:
        pass

    return value

def image_to_string(image_file_path):
    """
    Returns a string representation of an image, useful to store in a json file

    :param image_file_path: <string>
    :return: <string> utf-8 encode string of the image
    """
    if os.path.isfile(image_file_path):
        with open(image_file_path, 'rb') as image_file_path:
            return base64.b64encode(image_file_path.read()).decode("utf-8")

def string_to_image_byte_array(value):
    """
    Given a string representation of an image, returns a bytearray that can be used to load the image
    For example:
    pixmap = QPixmap()
    pixmap.loadFromData(string_to_image_byte_array("QWfsdk39f9ck39FmfsfFE#c3DK:))

    :param value: <string> representation of an image
    :return: <byteArray>
    """
    return base64.b64decode(value)


