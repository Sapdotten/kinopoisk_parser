import csv
from os import listdir
from os.path import isfile, join, abspath


def make_annotation():
    good_dir = join("dataset", "good")
    bad_dir = join("dataset", "bad")
    with open("annotation.csv", "w") as f:
        fw = csv.writer(f, delimiter = ",", lineterminator="\r")
        for elem in listdir(good_dir):
            fw.writerow([abspath(join(good_dir, elem)),
                        join(good_dir, elem),
                        "good"])
        for elem in listdir(good_dir):
            fw.writerow([abspath(join(bad_dir, elem)),
                        join(good_dir, elem),
                        "bad"])
        



if __name__ == "__main__":
    make_annotation()
    print("Annotation is done")