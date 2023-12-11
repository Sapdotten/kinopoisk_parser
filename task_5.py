import csv
import os


class FilesIterator:
    def __init__(self, dir: str, class_: str):
        """
        Args:
            annotation_file (str): file with annotation for dataset
            class_ (str): class for iteration
        """
        self.class_ = class_
        self.dir = dir
        self.returned_files = set()

    def __iter__(self):
        return self

    def __next__(self):

        for filename in os.listdir(os.path.join(self.dir, self.class_)):
            f = os.path.join(os.path.join(self.dir, self.class_, filename))
            if f not in self.returned_files:
                self.returned_files.add(f)
                return f
        raise StopIteration


if __name__ == '__main__':
    tr = FilesIterator('dataset', 'bad')
    for elem in tr:
        print(elem)
