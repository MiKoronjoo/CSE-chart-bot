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

    def __eq__(self, string: str):
        return self.name == string

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


def get__pres_str(course_id: int):
    result = data[course_id].name + '\n*****'
    for pre_id in data[course_id].pres:
        result += '\n' + data[pre_id].name

    return result


def get_all_pres(course_id: int, result=None):
    if result is None:
        result = []
    for pre_id in data[course_id].pres:
        result.append(pre_id)
        result = get_all_pres(pre_id, result)

    return result


def get_all_pres_str(course_id: int):
    result = data[course_id].name + '\n*****'
    pres = set(get_all_pres(course_id))
    for pre_id in pres:
        result += '\n' + data[pre_id].name

    return result


if __name__ == '__main__':
    data = load_data()
