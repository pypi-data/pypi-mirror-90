# So you can execute the file with python to test the file
if __name__ == "__main__":
    import subprocess
    # use -k <string> to only run tests which contain the provided string
    subprocess.run('pytest')
    exit()

# the repo path has to be added to sys.path, or else this package won't be found
import sys, os
parent_dir = os.path.join(os.path.dirname(__file__), '..\\..')

# imports for the tests
import pytest
from utility.file_io import *

def test_replace_file_name():
    assert replace_file_name('A_file.py', 'B_new.py') == 'B_new.py'
    assert replace_file_name('A_file.py', 'B_new') == 'B_new'
    assert replace_file_name('A_file', 'B_new') == 'B_new'

    assert replace_file_name('dir/A_file.py', 'B_new.py') == 'dir/B_new.py'

    if sys.platform.startswith('win'):
        # Backslashes only work on windows
        assert replace_file_name('\\dir\\A_file.py', 'B_new.py') == '\\dir\\B_new.py'

    assert replace_file_name('dir1/dir2/A_file.py', 'B_new.py') == 'dir1/dir2/B_new.py'

    assert replace_file_name('dir/.py', 'B_new') == 'dir/B_new'
    with pytest.raises(ValueError):
        replace_file_name('dir/', 'B_new')
