from collections import deque
import copy

def rotate_list(data, amount):
    """ rotates a list by the specified amount

    eg: rotate_list([1,2,3], 1) -> returns [3,1,2]

    Args:
        data:   the list to rotate
        amount: how many times
    Returns:
        the rotated list
    """
    d = deque(data)
    d.rotate(amount)
    return list(d)

def pad_1d_list(data, element, thickness=1):
    """ Adds padding at the start and end of a list

    This will make a shallow copy of the original

    eg: pad_1d_list([1,2], 0) -> returns [0,1,2,0]

    Args:
        data:      the list to pad
        element:   gets added as padding (if its an object, it won't be instanced, just referenced in the lists)
        thickness: how many layers of padding
    Returns:
        the padded list
    """
    # shallow copy
    data = copy.copy(data)
    for i in range(thickness):
        data.insert(0, element)
        data.append(element)
    return data

def pad_2d_list(data, element, thickness=1):
    """ Adds padding "around" a list of lists

    List should be a "rectangle".  
    For the result, every list will be a copied singel instance. Contants will be the same reference

    eg: pad_2d_list([[1]], 0) -> returns [[0,0,0], [0,1,0], [0,0,0]]

    Args:
        data:      the list to pad
        element:   gets added as padding (if its an object, it won't be instanced, just referenced in the lists)
        thickness: how many layers of padding
    Returns:
        the padded list
    """
    res = []

    # pad sides
    for i in range(len(data)):
        res.append(pad_1d_list(data[i], element, thickness))

    # pad top and bottom
    width = len(res[0])
    padding = [element] * width
    # copy the padding first, else both sides will reference the same list
    return pad_1d_list(res, padding.copy(), thickness)

def pad_3d_list(data, element, thickness=1):
    """ adds padding "around" a list of lists of lists

    List should be a "box".  
    For the result, every list will be a copied singel instance. Contants will be the same reference

    Args:
        data:      the list to pad
        element:   gets added as padding (if its an object, it won't be instanced, just referenced in the lists)
        thickness: how many layers of padding
    Returns:
        the padded list
    """
    res = []

    # pad sides
    for i in range(len(data)):
        res.append(pad_2d_list(data[i], copy.copy(element), thickness))

    # pad top and bottom
    width = len(res[0])
    height = len(res[0][0])
    padding = [[element] * height] * width
    print(padding)
    # copy the padding first, else both sides will reference the same list
    x = pad_1d_list(res, padding.copy(), thickness)
    print(x)
    return x

