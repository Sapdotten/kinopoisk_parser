import os
from os.path import join
from os import listdir
from task_1 import add_line


def create_dir(dir: str) -> None:
    """Creates a new directory if it doesn't exist

    Args:
        dir (path): path for directory
    """
    if not os.path.isdir(dir):
        os.makedirs(dir)


def copy_file(old_path: str, new_path: str):
    """copies file from old dir to new dir

    Args:
        old_path (path): path copy from
        new_path (path): path copy to
    """
    os.system(f'copy {old_path} {new_path}')


def copy_dataset(old_dir: str, new_dir: str, annotation_file: str) -> None:
    """Copies a dataset to new directory

    Args:
        new_dir (os.path): new directory of dataset
    """
    classes = ["good", "bad"]
    create_dir(new_dir)
    open(annotation_file, 'w').close()

    for class_ in classes:
        dir = join(old_dir, class_)
        for elem in listdir(dir):
            new_path = join(new_dir, class_+'_'+elem)
            old_path = join(dir, elem)
            copy_file(old_path, new_path)
            add_line(annotation_file, new_path, class_)


if __name__ == "__main__":
    copy_dataset((join("task_2_datset")))
