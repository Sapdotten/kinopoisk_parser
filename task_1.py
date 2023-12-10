import csv
from os import listdir
from os.path import join, abspath


def add_line(annotation_file: str, path_: str, class_name: str) -> None:
    """Add a line about file to .csv file

    Args:
        annotation_file (path): path to annotation file
        path_ (path): path to file of dataset
        class_name (str): name of class of file
    """
    with open(annotation_file, 'a+') as file:
        fw = csv.writer(file, delimiter=",", lineterminator="\r")
        fw.writerow([abspath(path_), path_, class_name])


def make_annotation(annotation_file: str, dataset_dir: str) -> None:
    """Build an annotation file

    Args:
        annotation_file (path): dir where will be saved annotation
    """
    classes = ["good", "bad"]
    for class_ in classes:
        dir = join('dataset', class_)
        for elem in listdir(dir):
            add_line(annotation_file, dataset_dir, class_)


if __name__ == "__main__":
    make_annotation("task_1_annotation.csv")
    print("Annotation is done")
