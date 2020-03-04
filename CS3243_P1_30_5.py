import os
import sys
import copy
import Queue as Q
import datetime
import math
import subprocess

# To print the puzzle in 2d matrix
from itertools import chain

import CS3243_P1_30_1 as UninformedSearch
import CS3243_P1_30_2 as InformedHeuristic1
import CS3243_P1_30_3 as InformedHeuristic2
import CS3243_P1_30_4 as InformedHeuristic3

if __name__ == "__main__":
    # do NOT modify below

    # argv[0] represents the name of the file that is being executed
    # argv[1] represents name of input file
    if len(sys.argv) != 2:
        raise ValueError("Wrong number of arguments!")
    
    folder = sys.argv[1]
    test_cases = os.listdir(folder)
    for test_case in test_cases:
        with open('experiment_result.txt', 'a') as g:
            g.write(test_case + '\n')

        subprocess.call([sys.executable, 'CS3243_P1_30_1.py', folder + test_case, "out.txt"])

