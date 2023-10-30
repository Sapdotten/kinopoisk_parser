import os
from os.path import join, abspath
from os import listdir, path
import csv
from task_1 import add_line


def create_dir(dir: path) -> None:
    """Creates a new directory if it doesn't exist

    Args:
        dir (path): path for directory
    """
    if not os.path.isdir(dir):
        os.makedirs(dir)

def copy_file(old_path: path, new_path: path):
    """copies file from old dir to new dir

    Args:
        old_path (path): path copy from
        new_path (path): path copy to
    """
    os.system(f'copy {old_path} {new_path}')

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
            copy_file(old_path, new_path)
            add_line("task_2_annotation.csv", new_path, class_)


if __name__=="__main__":
    copy_dataset((join("task_2_datset")))