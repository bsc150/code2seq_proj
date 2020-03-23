import random
import sys

# possible proportions: 0.7, 0.15, 0.15

TRAIN_SIZE = 0.70
TEST_SIZE = 0.15
VALIDATION_SIZE = 0.15


"""
Divide data in file into 3 different files, train validation and test.
Each function is decided to be in train,test,or validation, together with ALL it's possible flows.
"""
def divide(file):
    train_file = open("data/assembly/assembly.train.raw.txt", 'w')
    validation_file = open("data/assembly/assembly.val.raw.txt", 'w')
    test_file = open("data/assembly/assembly.test.raw.txt", 'w')
    with open(file, 'r') as f:
        lines = f.readlines()
        last_line = None
        last_res = None
        for line in lines:
            splitted_line = line.split(" ")
            if splitted_line[0] != last_line:
                last_line = splitted_line[0]
                last_res = random.choices([0,1,2], [0.7,0.15,0.15])[0]
            # before splitting the data, we can add more manipulations on lines.    
            #to_write = line.replace("||","|").split("CONS")[0] + "CONS,DUM\n"
            to_write = line
            if last_res == 0:
                train_file.write(to_write)
            elif last_res == 1:
                validation_file.write(to_write)
            elif last_res == 2:
                test_file.write(to_write)
    train_file.close()
    validation_file.close()
    test_file.close()


if __name__ == "__main__":
    file = sys.argv[1]
    divide(file)
