"""
a command line application that tells you the amount of code written in specific languages
"""
from toml_langs import *
from code_class import *

# create Code object
code_obj = Code()

# get files and lines of code number
code_obj.test_files()

code_obj.count_lines()
code_obj.get_found_languages()

# output
code_obj.test_output()
