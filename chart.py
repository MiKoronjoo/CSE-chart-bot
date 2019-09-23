import enum
import pickle

from config import data_path


class CourseType(enum.Enum):
    GENERAL = 'GENERAL'
    BASE = 'BASE'
    MAIN = 'MAIN'
    OPTIONAL = 'OPTIONAL'


class Course:
    def __init__(self, name, unit=3, course_type=CourseType.MAIN):
        self.name = name
        self.id = len(data)
        self.pres = []  # prerequisites
        self.unit = unit
        self.type = course_type

    def add_pre(self, course_id: int):
        self.pres.append(course_id)

    def __str__(self):
        return self.name


def save_data():
    with open(data_path, 'wb') as file:
        pickle.dump(data, file)


def load_data():
    try:
        file = open(data_path, 'rb')
        data = pickle.load(file)
        file.close()
    except FileNotFoundError:
        data = []

    return data


def new_course(name: str, unit: int = 3, course_type=CourseType.MAIN):
    name = name.replace('ي', 'ی').replace('ك', 'ک')
    data.append(Course(name, unit, course_type))
    save_data()


if __name__ == '__main__':
    data = load_data()
