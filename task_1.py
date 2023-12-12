import csv
from os import listdir
from os.path import join, abspath, relpath, dirname


def add_line(annotation_file: str, path_: str, class_name: str) -> None:
    """Add a line about file to .csv file

    Args:
        annotation_file (path): path to annotation file
        path_ (path): path to file of dataset
        class_name (str): name of class of file
    """
    annot_dir = dirname(annotation_file)
    with open(annotation_file, 'a+') as file:
        fw = csv.writer(file, delimiter=";", lineterminator="\r")
        fw.writerow([abspath(path_), relpath(
            path_, annot_dir), class_name])


def make_annotation(annotation_file: str, dataset_dir: str) -> None:
    """Build an annotation file

    Args:
        annotation_file (path): dir where will be saved annotation
    """
    classes = ["good", "bad"]
    open(annotation_file, 'w').close()
    for class_ in classes:
        dir = join(dataset_dir, class_)
        for elem in listdir(dir):
            add_line(annotation_file, join(dir, elem), class_)


if __name__ == "__main__":
    make_annotation("task_1_annotation.csv")
    print("Annotation is done")
