import os
from os.path import join, abspath
from os import listdir, path
import csv

def add_line(annotation_file: path, path_: path, class_name: str) -> None:
    """Add a line about copied file to .csv file

    Args:
        annotation_file (path): path to annotation file
        path_ (path): path to copied file of dataset
        class_name (str): name of class of file
    """
    with open(annotation_file, 'a+') as file:
        fw = csv.writer(file, delimiter = ",", lineterminator="\r")
        fw.writerow([abspath(path_), path_, class_name])

def create_dir(dir: path) -> None:
    """Creates a new directory if it doesn't exist

    Args:
        dir (path): path for directory
    """
    if not os.path.isdir(dir):
        os.makedirs(dir)

def copy_dataset(new_dir: os.path) -> None:
    """Copies a dataset to new directory

    Args:
        new_dir (os.path): new directory of dataset
    """
    classes = ["good", "bad"]
    create_dir(new_dir)

    for class_ in classes:
        dir = join('dataset', class_)
        for elem in listdir(dir):
            new_path = join(new_dir, class_+'_'+elem)
            old_path = join(dir, elem)
            os.system(f'copy {old_path} {new_path}')
            add_line("copies_annotation.csv", new_path, class_)


if __name__=="__main__":
    copy_dataset((join("new_dataset")))