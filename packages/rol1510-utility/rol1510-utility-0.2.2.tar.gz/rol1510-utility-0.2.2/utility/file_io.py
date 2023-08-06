import os
import sys
import glob

# returns the path of the executed file
def get_dir():
    """ returns the directory path of the python file executed """
    return os.path.dirname(sys.argv[0])

def get_file_paths_from_wildcard(wildcard):
    """ returns all file paths which fit the wildcard """
    if not os.path.isabs(wildcard):
        wildcard = os.path.join(get_dir(), wildcard)
    return glob.glob(wildcard)

def get_file_names_from_wildcard(wildcard):
    """ returns only the file names which fit the wildcard """
    paths = get_file_paths_from_wildcard(wildcard)
    return [os.path.basename(p) for p in paths]

def replace_file_name(path, newName):
    """ replace the file name in a path
    Args:
        path:    path or filename to replace
        newName: the new file name
    Returns:
        the new path
    Raises:
        ValueError: path does not contain a file name
    """
    name = os.path.basename(path)

    if name == '' or name == None:
        raise ValueError('path does not contain a file name')
    else:
        return path.replace(name, newName)

def process_files(func, file_wildcard):
    """ quick way to call a function for every file specified by a wildcard

    eg:
    ```
        def f(path):
            with open(path, 'r') as file:
                print(file.read())

        process_files(f, '*.py')
    ```

    Args:
        func: the processing function. Must take a path as argument (func(path) -> None)
        file_wildcard: files specified here will be processed
    """
    files = get_file_paths_from_wildcard(file_wildcard)
    for path in files:
        func(path)

def mkdir_if_nonexisting(path):
    """ Will create the given directory if it does not exist already
    Args:
        path: the path for the directory in question
    Returns:
        True if the directory was created else False
    """
    if os.path.isdir(path) == False:
        os.mkdir(path)
        return True
    return False

def remove_if_existing(path):
    """ Will delete the given file if it exists
    Args:
        path: the path for the file in question
    Returns:
        True if the file was deleted else False
    """
    if os.path.isfile(path):
        os.remove(path)
        return True
    return False

def rename_if_existing(old_name, new_name):
    """ Will rename the given file if it exists
    Args:
        old_name: the current name of the file in question
        new_name: the new name
    Returns:
        True if the file was renamed else False
    """
    if os.path.isfile(old_name):
        os.rename(old_name, new_name)
        return True
    return False
