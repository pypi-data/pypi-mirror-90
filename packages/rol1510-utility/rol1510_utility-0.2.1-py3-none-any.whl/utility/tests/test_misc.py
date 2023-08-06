# So you can execute the file with python to test the file
if __name__ == "__main__":
    import subprocess
    # use -k <string> to only run tests which contain the provided string
    subprocess.run('pytest -vv')
    exit()

# the repo path has to be added to sys.path, or else this package won't be found
import sys, os
parent_dir = os.path.join(os.path.dirname(__file__), '..\\..')

# imports for the tests
import pytest
import copy
from utility.misc import *

def test_rotate_list():
    l = [1, 2, 3]
    assert rotate_list(l, 1) == [3, 1, 2]
    assert l == [1, 2, 3]

    assert rotate_list(l, -1) == [2, 3, 1]
    assert rotate_list(l, 2) == [2, 3, 1]

    assert rotate_list(l, 3) == [1, 2, 3]

    assert rotate_list(l, 4) == [3, 1, 2]
    assert rotate_list(l, 7) == [3, 1, 2]

def test_pad_1d_list_padding():
    # test expected behavior
    l = [1, 2, 3]
    o = [0, 1, 2, 3, 0]
    assert pad_1d_list(l, 0) == o
    assert l != o # pad_1d_list should not change the original

    # test thickness argument
    assert pad_1d_list([1, 2], 0, -1) == [1, 2]
    assert pad_1d_list([1, 2], 0)     == [0, 1, 2, 0]
    assert pad_1d_list([1, 2], 0, 1)  == [0, 1, 2, 0]
    assert pad_1d_list([1, 2], 0, 2)  == [0, 0, 1, 2, 0, 0]

    # test differne objects as elements
    assert pad_1d_list([1, 2], '#-#') == ['#-#', 1, 2, '#-#']
    assert pad_1d_list([1, 2], [1,2]) == [[1,2], 1, 2, [1,2]]

def test_pad_1d_list_object_references():
    # outputs different object
    l = [1, 2, 3]
    o = [0, 1, 2, 3, 0]
    res = pad_1d_list(l, 0)
    assert res == o
    assert res != l # output and input should not be the same object

    # in this case, the result should not change
    l[1] = 5
    assert res == o

    # change of the padding will only change one
    res[0] = 1
    assert res == [1, 1, 2, 3, 0]

    # containing objects
    l = [[1], [2], [3]]
    p = [4]
    o = [[4], [1], [2], [3], [4]]
    res = pad_1d_list(l, p)
    assert res == o

    # should change the output
    l[0][0] = 8
    assert res == [[4], [8], [2], [3], [4]]

    p[0] = 0
    assert res == [[0], [8], [2], [3], [0]]

    # change of the padding should change both
    res[0][0] = 1
    assert res == [[1], [8], [2], [3], [1]]

def test_pad_2d_list_padding():
    # test expected behavior
    l = [[1, 2],
         [3, 4]]
    o = [[0, 0, 0, 0],
         [0, 1, 2, 0],
         [0, 3, 4, 0],
         [0, 0, 0, 0]]
    assert pad_2d_list(l, 0) == o
    assert l != o # pad_2d_list should not change the original

    # test thickness argument
    l  = [[1]]
    o1 = [[0, 0, 0],
          [0, 1, 0],
          [0, 0, 0]]
    o2 = [[0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0],
          [0, 0, 1, 0, 0],
          [0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0]]

    assert pad_2d_list(copy.deepcopy(l), 0,-1) == l
    assert pad_2d_list(copy.deepcopy(l), 0, 0) == l
    assert pad_2d_list(copy.deepcopy(l), 0, 1) == o1
    assert pad_2d_list(copy.deepcopy(l), 0, 2) == o2

    # test different dimensions
    l = [[1, 2]]
    o = [[0, 0, 0, 0],
         [0, 1, 2, 0],
         [0, 0, 0, 0]]
    assert pad_2d_list(copy.deepcopy(l), 0) == o

    l = [[1], [2]]
    o = [[0, 0, 0],
         [0, 1, 0],
         [0, 2, 0],
         [0, 0, 0]]
    assert pad_2d_list(copy.deepcopy(l), 0) == o

def test_pad_2d_list_object_references():
    # same list referenced twice
    a = [1, 2]
    b = [a, a]
    o = [[0, 0, 0, 0],
         [0, 1, 2, 0],
         [0, 1, 2, 0],
         [0, 0, 0, 0]]

    assert pad_2d_list(b, 0) == o
    assert b != o # pad_2d_list should not change the original

    # multiple paddings
    a = [1, 2]
    b = [a, a]
    o = [[0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 1, 2, 0, 0],
         [0, 0, 1, 2, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0,]]
    res = pad_2d_list(b, 0)
    assert pad_2d_list(res, 0) == o

def test_pad_3d_list_padding():
    # simple test
    l = [[[1]]]
    o = [
            [[0,0,0],
             [0,0,0],
             [0,0,0]],
            [[0,0,0],
             [0,1,0],
             [0,0,0]],
            [[0,0,0],
             [0,0,0],
             [0,0,0]],
        ]
    assert pad_3d_list(l, 0) == o
    assert l != o

    # test different sizes
    l = [[[1, 2]]]
    o = [
            [[0,0,0,0],
             [0,0,0,0],
             [0,0,0,0]],
            [[0,0,0,0],
             [0,1,2,0],
             [0,0,0,0]],
            [[0,0,0,0],
             [0,0,0,0],
             [0,0,0,0]],
        ]
    assert pad_3d_list(l, 0) == o

    l = [[[1],[2]]]
    o = [
            [[0,0,0],
             [0,0,0],
             [0,0,0],
             [0,0,0]],
            [[0,0,0],
             [0,1,0],
             [0,2,0],
             [0,0,0]],
            [[0,0,0],
             [0,0,0],
             [0,0,0],
             [0,0,0]],
        ]
    assert pad_3d_list(l, 0) == o

    l = [[[1]],[[2]]]
    o = [
            [[0,0,0],
             [0,0,0],
             [0,0,0]],
            [[0,0,0],
             [0,1,0],
             [0,0,0]],
            [[0,0,0],
             [0,2,0],
             [0,0,0]],
            [[0,0,0],
             [0,0,0],
             [0,0,0]],
        ]
    assert pad_3d_list(l, 0) == o

    # test complex
    l = [[[11,12,13],[13,14,15]],[[21,22,23], [23,24,25]]]
    o = [
            [[0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0]],
            [[0, 0, 0, 0, 0],
             [0,11,12,13, 0],
             [0,13,14,15, 0],
             [0, 0, 0, 0, 0]],
            [[0, 0, 0, 0, 0],
             [0,21,22,23, 0],
             [0,23,24,25, 0],
             [0, 0, 0, 0, 0]],
            [[0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0]],
        ]
    assert pad_3d_list(l, 0) == o

    # test thickness
    l = [[[1]]]
    o = [
            [[0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0]],
            [[0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0]],
            [[0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,1,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0]],
            [[0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0]],
            [[0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0]],
        ]
    assert pad_3d_list(l, 0, 0) == l
    assert pad_3d_list(l, 0, 2) == o

def test_pad_3d_list_object_references():
    l = [[[1]]]
    o1 = [
            [[0,0,0],
             [0,0,0],
             [0,0,0]],
            [[0,0,0],
             [0,1,0],
             [0,0,0]],
            [[0,0,0],
             [0,0,0],
             [0,0,0]],
        ]
    o2 = [
            [[0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0]],
            [[0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0]],
            [[0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,1,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0]],
            [[0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0]],
            [[0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0]],
        ]

    res1 = pad_3d_list(l, 0)
    res2 = pad_3d_list(res1, 0)
    assert res1 == o1
    assert res2 == o2

