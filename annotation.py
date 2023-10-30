import csv
from os import listdir, path
from os.path import  join, abspath


def make_annotation(annotation_file: path) -> None:
    """Build an annotation file

    Args:
        annotation_file (path): dir where will be saved annotation
    """
    classes = ["good", "bad"]
    for class_ in classes:
        dir = join('dataset', class_)
        with open(annotation_file, 'a+') as file:
            fw = csv.writer(file, delimiter = ",", lineterminator="\r")
            for elem in listdir(dir):
                fw.writerow([abspath(join(dir, elem)),
                            join(dir, elem),
                            class_])
    
        

if __name__ == "__main__":
    make_annotation("annotation.csv")
    print("Annotation is done")