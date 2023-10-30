import csv
from typing import Union


class FilesIterator:
    returned_files: set
    file: str
    def __init__(self, annotation_file: str, class_: str):
        """
        Args:
            annotation_file (str): file with annotation for dataset
            class_ (str): class for iteration
        """
        self.class_ = class_
        self.file = annotation_file
        self.returned_files = set()

    def __iter__(self):
        return self
    
    def __next__(self):
        with open(self.file, 'r+') as file:
            fr = csv.reader(file, delimiter = ',', lineterminator="\r")
            for row in fr:
                if row[2]==self.class_ and row[0] not in self.returned_files:
                    self.returned_files.add(row[0])
                    return row[0]
            raise StopIteration


if __name__=='__main__':
    tr = FilesIterator('task_3_annotation.csv', 'bad')
    for elem in tr:
        print(elem)