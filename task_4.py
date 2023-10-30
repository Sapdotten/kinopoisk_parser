import csv
from typing import Union

returned_files = set()

def get_next_instance(class_: str, annotation_file: str) -> Union[str, None]:
    """Returns a path to an instance of class

    Args:
        class_ (str): instance class
        annotation_file (str): path to annotation file for dataset

    Returns:
        Union[str, None]: path to file
    """
    global returned_files
    with open(annotation_file, 'r+') as file:
        fr = csv.reader(file, delimiter = ',', lineterminator="\r")
        for row in fr:
            if row[2]==class_ and row[0] not in returned_files:
                returned_files.add(row[0])
                return row[0]
    return None

if __name__=="__main__":
    for i in range(0, 1001):
        print(get_next_instance('good', 'task_3_annotation.csv'))
