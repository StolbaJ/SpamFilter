import os


def read_classification_from_file(pathToFile):
    dictForReturn = dict()
    with open(pathToFile, 'r', encoding='utf-8') as f:
        if f.readable():
            for line in f:
                actual_line = line.strip()
                actual_line = actual_line.split()
                dictForReturn.update({actual_line[0]: actual_line[1]})

    return dictForReturn


if __name__ == "__main__":
    print(read_classification_from_file("text.txt"))


