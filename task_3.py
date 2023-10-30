from os.path import join
from os import listdir, path
from task_1 import add_line
from task_2 import create_dir, copy_file
import random

class RandomNumber:
    """Class for generating a random number"""
    generated_numbers: set = set(range(0, 10000))
    @classmethod
    def get_number(cls) -> int:
        """Generates random num between 0 and 10000

        Returns:
            int: random num
        """
        if not cls.generated_numbers:
            cls.generated_numbers = set(range(0, 10000))
        unique_number = random.choice(list(cls.generated_numbers))
        cls.generated_numbers.remove(unique_number)
        return unique_number

def get_name()->str:
    """Generate a random num name of file
    """
    num = RandomNumber.get_number()
    return format(num, '04d')+'.txt'

def copy_dataset(new_dir: str) -> None:
    """Copies a dataset to new directory with new random names

    Args:
        new_dir (str): new directory of dataset
    """
    classes = ["good", "bad"]
    create_dir(new_dir)

    for class_ in classes:
        dir = join('dataset', class_)
        for elem in listdir(dir):
            new_path = join(new_dir, get_name())
            old_path = join(dir, elem)
            copy_file(old_path, new_path)
            add_line("task_3_annotation.csv", new_path, class_)


if __name__=="__main__":
    copy_dataset("task_3_dataset")