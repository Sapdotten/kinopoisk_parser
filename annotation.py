import csv
from os import listdir, path
from os.path import  join, abspath

def fill_csv(annotaton_file: path ,dir: path, class_name: str) -> None:
    """addes a notes about files in dir in a annotation file

    Args:
        annotaton_file (path): dir where will be saved annotation
        dir (path): dir with dataset
        class_name (str): class of dataset
    """
    with open(annotaton_file, 'a+') as file:
        fw = csv.writer(file, delimiter = ",", lineterminator="\r")
        for elem in listdir(dir):
            fw.writerow([abspath(join(dir, elem)),
                         join(dir, elem),
                         class_name])

def make_annotation(annotation_file: path) -> None:
    """Build an annotation file

    Args:
        annotation_file (path): dir where will be saved annotation
    """
    dataset_dir = 'dataset'
    good_dir = join(dataset_dir, "good")
    bad_dir = join(dataset_dir, "bad")
    fill_csv(annotation_file, good_dir, "good")
    fill_csv(annotation_file, bad_dir, "bad")
    
        

if __name__ == "__main__":
    make_annotation("annotation.csv")
    print("Annotation is done")