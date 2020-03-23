import re
import sys


"""
Unify functions' names by using only lowercase chars, and replacing "_" with "|"
"""
def fixFunctionName(line):
    splitted_line = line.split(" ")
    name = splitted_line[0]
    name = re.sub( '(?<!^)(?=[A-Z])', '_', name ).lower()
    name = name.replace("_","|")
    splitted_line[0] = name
    return " ".join(splitted_line)


"""
This function is for fast manipulation on the preprocessed data.
It takes the origin file as given from preprocess, and processes it further using the current analysis.
"""
def fixLines(flie_to_fix, new_file_name):
    with open(new_file_name, 'w') as f:
        with open(flie_to_fix, 'r') as o:
            lines = o.readlines()
            # now, apply changes to all lines.
            for line in lines:
                fixed_line = fixFunctionName(line)
                f.write(fixed_line)
            

if __name__ == "__main__":
    flie_to_fix = sys.argv[1]
    new_file_name = sys.argv[2]
    fixLines(flie_to_fix, new_file_name)
