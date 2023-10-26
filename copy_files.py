import os
from os.path import join, abspath
from os import listdir
import csv

def annotation(file_name: str,data: list[list]):
    with open(file_name, 'w') as f:
        fw = csv.writer(f, delimiter = ",", lineterminator="\r")
        for elem in data:
            fw.writerow(elem)

def copy_dataset(new_directory: os.path):
    good_dir = join("dataset", "good")
    bad_dir = join("dataset", "bad")
    path = os.path.join(new_directory)
    if not os.path.isdir(path):
        os.makedirs(path)
    annot = []
    for elem in listdir(good_dir):
        rel_new_dir = join(new_directory, "good_"+elem)
        abs_new_dir = abspath(rel_new_dir)
        os.system(f'copy {abspath(join(good_dir, elem))} {abs_new_dir}')
        annot.append([abs_new_dir, rel_new_dir, "good"])
    for elem in listdir(good_dir):
        rel_new_dir = join(new_directory, "bad_"+elem)
        abs_new_dir = abspath(rel_new_dir)
        os.system(f'copy {abspath(join(good_dir, elem))} {abspath(join(new_directory, "bad_"+elem))}')
        annot.append([abs_new_dir, rel_new_dir, "bad"])
    annotation("new_directory"+"_annot.csv", annot)


if __name__=="__main__":
    copy_dataset((join("new_dataset")))