import collections

def get_name_variant(input_list, uppercase=True, lowercase=True, capitalize=True, include_original=True):
    """
    Returns a list with variants of the input list

    :param input_list: <list> list of strings
    :param uppercase: <bool>
    :param lowercase: <bool>
    :param capitalize: <bool>
    :param include_original: <bool>
    :return: a new list with the variants of the input list based on the properties that are set
    """
    new_list = []
    for string in input_list:
        if uppercase:
            new_list.append(string.upper())
        if lowercase:
            new_list.append(string.lower())
        if capitalize:  # string might not start with an actual letter
            new_letters = []
            for letter in string:
                if letter.isalpha():
                    letter = letter.upper()
                new_letters.append(letter)
            new_list.append("".join(new_letters))
    if include_original:
        new_list.extend(input_list)

    return remove_duplicates(new_list)

def remove_duplicates(input_list):
    """
    Returns a list without duplicates

    :param input_list: <list>
    :return: <list> without duplicates
    """

    return list(dict.fromkeys(input_list))

def blend_floats(percentage, list_1, list_2):
    """
    Returns a list that is the blended value of list_1 and list_2 based on the percentage. The percentage is the
    percentage that list_1 will keep. For example:


    list1 = [10.0, 20.0, 30.0]
    list2 = [5.0, 10.0, 15.0]

    print(utils.blend_lists(50, list1, list2))
    >> [7.5, 15.0, 22.5]

    print(utils.blend_lists(80, list1, list2))
    >>[9.0, 18.0, 27.0]


    :param percentage:
    :param list_1: <list> list of floats
    :param list_2: <list> list of floats
    :return: <list> with blended values
    """

    percentage_list_1 = percentage
    percentage_list_2 = 100 - percentage

    new_values = []

    for value_1, value_2 in zip(list_1, list_2):
        new_value_1 = (value_1 / 100) * percentage_list_1
        new_value_2 = (value_2 / 100) * percentage_list_2

        new_value = new_value_1 + new_value_2

        new_values.append(new_value)

    return new_values


def difference(list_of_lists):
    """
    Returns a lists with all the elements that list1 and list2 don't have in common

    :param list1: <list>
    :param list2: <list>
    :return: <list> with all the elements that list1 and list2 don't have in common
    """
    new_list = []
    for index, current_list in enumerate(list_of_lists):
        try:
            next_list = list_of_lists[index + 1]
        except:
            return new_list
        new_list = (list(list(set(current_list)-set(next_list)) + list(set(next_list)- set(current_list))))

    return new_list

def average(list):
    """
    returns the average value of all the values in the list

    :param list: <list> int/float
    :return: a float value with the average
    """
    return float(sum(list) / len(list))

def column_average(list_of_lists):
    """
    Return on list with the averages of every column

    list_of_lists =  [[2.0, 3.0],
                      [5.0, 6.0]]
    average_2(list_of_lists)
    # Result: [3.5, 4.5] #

    :param list_of_lists: *list* containing other lists. List have to be the same length
    :return: *list* with avg numbers
    """
    return list(map(lambda x: sum(x)/len(x), zip(*list_of_lists)))

def common(list1, list2):
    """
    Returns a lists with all the elements that list1 and list2 have in common

    :param list1: <list>
    :param list2: <list>
    :return: a lists with all the elements that list1 and list2 have in common
    """
    return set(list1).intersection(list2)

def flatten(input_list):
    """
    https://gist.github.com/layzerar/4243626
    If the input list contains tuples or other lists, appends the values of these to the main list

    :param input_list: <list>
    :return: <list> without any other lists of tuples
    """
    result = []
    for item in input_list:
        if isinstance(item, collections.Iterable) and not isinstance(item, str):
            for sub in flatten(item):
                result.append(sub)
        else:
            result.append(item)
    return result

def get_longest_list(list_of_lists):
    """
    Given a list of lists, the longest of the lists is returned

    :param list_of_lists: <list> of lists
    :return: the longest <list>
    """
    return max(list_of_lists, key=len)

def get_shortest_list(list_of_lists):
    """
    Given a list of lists, the shortest of the lists is returned

    :param list_of_lists: *list* of lists
    :return: the shortest *list*
    """
    return min(list_of_lists, key=len)
