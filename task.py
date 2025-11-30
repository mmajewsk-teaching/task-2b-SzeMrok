import json
import logging
from typing import Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_data(path: str) -> dict[str, Any]:
    try:
        with open(path, "r") as f:
            data: dict[str, Any] = json.load(f)
        logger.info(f"loaded {path}")
        return data
    
    except FileNotFoundError:
        logger.warning("file not found, creating empty structure")
        return {}
    
    except Exception as e:
        logger.error(f"error loading {path}: {e}")
        return {}


def save_data(path: str, data: dict[str, Any]) -> None:
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        logger.info(f"saved {path}")
        
    except Exception as e:
        logger.error(f"error saving {path}: {e}")


def add_student(schools: dict[str, Any], school: str, full: str) -> None:
    s = schools[school]["students"]
    
    if full not in s:
        s.append(full)
        logger.info(f"{full} added to {school} students")
    else:
        logger.warning(f"{full} already in {school}")


def add_course(schools: dict[str, Any], school: str, course: str) -> None:
    c = schools[school]["courses"]
    
    if course not in c:
        c[course] = {}
        logger.info(f"{course} added for {school}")
    else:
        logger.warning(f"{course} exists in {school}")


def add_grade(
    schools: dict[str, Any],
    school: str,
    course: str,
    full: str,
    test: str,
    grade: int,
) -> None:
    course_data = schools[school]["courses"][course]
    
    if full not in course_data:
        course_data[full] = {}

    course_data[full][test] = grade
    logger.info(f"{school.upper()}:{full} got {grade} from {test} in {course}")


def avg_student_in_course(schools: dict[str, Any], school: str, course: str, full: str) -> float:
    course_data = schools[school]["courses"][course]
    
    if full not in course_data:
        return 0.0
    tests = list(course_data[full].values())
    
    return sum(tests) / len(tests) if tests else 0.0


def avg_student_total(schools: dict[str, Any], school: str, full: str) -> float:
    grades: list[int] = []
    
    for course in schools[school]["courses"].values():
        if full in course:
            for g in course[full].values():
                grades.append(g)
    
    return sum(grades) / len(grades) if grades else 0.0


def avg_course(schools: dict[str, Any], school: str, course: str) -> float:
    course_data = schools[school]["courses"][course]
    grades = [g for st in course_data.values() for g in st.values()]
    
    return sum(grades) / len(grades) if grades else 0.0


def avg_school(schools: dict[str, Any], school: str) -> float:
    grades: list[int] = []
    
    for course in schools[school]["courses"].values():
        for st in course.values():
            for g in st.values():
                grades.append(g)
                
    return sum(grades) / len(grades) if grades else 0.0


def demo() -> dict[str, Any]:
    schools: dict[str, Any] = {"school 1": {"students": [], "courses": {}}, "school 2": {"students": [], "courses": {}}}
    course_list = ["math", "physics", "programming", "history", "biology", "english"]
    for s in schools:
        for c in course_list:
            add_course(schools, s, c)

    for i in range(1, 21):
        full = f"name{i} surname{i}"

        if i % 2 == 0:
            add_student(schools, "school 1", full)
        if i % 2 == 1 or i % 3 == 0:
            add_student(schools, "school 2", full)

        for s in schools:
            if full in schools[s]["students"]:
                for c in course_list:
                    for t in range(1, 4):
                        g = (i * t + len(c)) % 6 + 1
                        add_grade(schools, s, c, full, f"test{t}", g)

    return schools


if __name__ == "__main__":
    path = "school_data.json"
    data = load_data(path)
    
    if not data:
        data = demo()
        save_data(path, data)
    
    s = data
    st = "name1 surname1"
    
    logger.info(avg_student_total(s, "school 2", st))
    logger.info(avg_student_in_course(s, "school 2", "math", st))
    logger.info(avg_course(s, "school 1", "math"))
    logger.info(avg_school(s, "school 1"))
