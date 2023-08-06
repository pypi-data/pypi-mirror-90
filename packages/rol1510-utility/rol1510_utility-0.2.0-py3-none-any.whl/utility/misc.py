from collections import deque

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
    """ adds padding at the start and end of a list

    eg: pad_1d_list([1,2], 0) -> returns [0,1,2,0]

    Args:
        data:      the list to pad
        element:   gets added as padding
        thickness: how many layers of padding
    Returns:
        the list for chaining
    """
    for i in range(thickness):
        data.insert(0, element)
        data.append(element)
    return data

def pad_2d_list(data, element, thickness=1):
    """ adds padding "around" a list of lists

    List should be a "rectangle"  
    eg: pad_2d_list([[1]], 0) -> returns [[0,0,0], [0,1,0], [0,0,0]]

    Args:
        data:      the list to pad
        element:   gets added as padding
        thickness: how many layers of padding
    Returns:
        the list for chaining
    """
    # pad sides
    for i in range(len(data)):
        pad_1d_list(data[i], element, thickness)

    # pad top and bottom
    width = len(data[0])
    top_bottom_padding = [element] * width
    pad_1d_list(data, top_bottom_padding, thickness)
    return data

def pad_3d_list(data, element, thickness=1):
    """ adds padding "around" a list of lists of lists

    List should be a "box"

    Args:
        data:      the list to pad
        element:   gets added as padding
        thickness: how many layers of padding
    Returns:
        the list for chaining
    """
    # pad sides
    for i in range(len(data)):
        pad_2d_list(data[i], element, thickness)

    # pad top and bottom
    width = len(data[0])
    height = len(data[0][0])
    padding = [[element] * height] * width
    pad_1d_list(data, padding, thickness)
    return data


