from datetime import date, datetime, timedelta
from random import randint, choice
import faker
from sqlalchemy import select, desc, select, and_

from sqlalchemy import func

from src.models import Teacher, Student, Discipline, Grade, Group
from src.db import session

"""SELECT s.fullname, ROUND(AVG(g.grade), 2) AS average_grade
FROM grades g
JOIN students s ON s.id = g.student_id
GROUP BY s.fullname
ORDER BY average_grade DESC
LIMIT 5
;"""


def select_1():
    result = session.query(Student.fullname, func.round(func.avg(Grade.grade), 1).label('avg_grade')) \
        .select_from(Grade) \
        .join(Student) \
        .group_by(Student.id) \
        .order_by(desc('avg_grade')) \
        .limit(5).all()
    return result


"""-- 2. Знайти студента із найвищим середнім балом з певного предмета
SELECT d.name, s.fullname, ROUND(AVG(g.grade), 2) AS average_grade
FROM grades g
JOIN students s ON s.id = g.student_id
JOIN disciplines d ON d.id = g.discipline_id
WHERE d.id = 2  -- id предмета
GROUP BY d.name, s.fullname
ORDER BY average_grade DESC
LIMIT 5
;"""


def select_2(discipline_id):
    result = session.query(Discipline.name,
                           Student.fullname,
                           func.round(func.avg(Grade.grade), 1).label('avg_grade')
                           ) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .filter(Discipline.id == discipline_id) \
        .group_by(Student.id, Discipline.name) \
        .order_by(desc('avg_grade')) \
        .limit(1).all()
    return result


"""-- 3. Знайти середній бал у групах з певного предмета
SELECT d.name, gr.name, ROUND(AVG(g.grade), 2) AS average_grade
FROM grades g
JOIN students s ON s.id = g.student_id
JOIN disciplines d ON d.id = g.discipline_id
JOIN [groups] gr ON gr.id = s.group_id
WHERE d.id = 6 --discipline id
GROUP BY gr.name, d.name
ORDER BY average_grade DESC
;"""


def select_3(discipline_id):
    result = session.query(Discipline.name,
                           Group.name,
                           func.round(func.avg(Grade.grade), 1).label('avg_grade')
                           ) \
        .select_from(Grade) \
        .join(Student, Student.id == Grade.student_id) \
        .join(Discipline, Discipline.id == discipline_id) \
        .join(Group, Group.id == Student.group_id) \
        .filter(Discipline.id == discipline_id) \
        .group_by(Group.name, Discipline.name) \
        .order_by(func.avg(Grade.grade).desc()) \
        .all()
    return result


"""-- 4. Знайти середній бал на потоці (по всій таблиці оцінок)
SELECT ROUND(AVG(g.grade), 2) AS average_grade
FROM grades g;"""


def select_4():
    result = session.query(func.round(func.avg(Grade.grade), 1).label('average_grade')).scalar()
    return f"Average grade: {result}"


"""-- 5. Знайти які курси читає певний викладач

SELECT t.fullname, d.name  
FROM disciplines d
JOIN teachers t ON d.teacher_id  = t.id
--WHERE t.id = 1 -- вказати teachers id для вибору конкретного викладача
ORDER BY t.fullname
;"""


def select_5(teacher_id):
    result = (
        session.query(Teacher.fullname, Discipline.name)
        .join(Discipline, Discipline.teacher_id == Teacher.id)
        .filter(Teacher.id == teacher_id)
        .order_by(Teacher.fullname)
    ).all()
    return result


"""-- 6. Знайти список студентів у певній групі.
SELECT g.name, s.fullname  
FROM groups g
JOIN students s ON g.id = s.group_id
WHERE g.id = 2 -- вказати group_id для вибору конкретної групи
ORDER BY g.id, s.fullname
;"""


def select_6(group_id):
    result = (
        session.query(Group.name, Student.fullname)
        .join(Student, Group.id == Student.group_id)
        .filter(Group.id == group_id)
        .order_by(Group.id, Student.fullname)
    ).all()
    return result


"""-- 7. Знайти оцінки студентів у окремій групі з певного предмета

SELECT g2.name, d.name, s.fullname, g.grade
FROM grades g
JOIN disciplines d ON g.discipline_id = d.id
JOIN students s ON g.student_id = s.id
JOIN groups g2 ON s.group_id = g2.id
WHERE g2.id = 1 AND d.id = 2 -- select group id and discipline id
ORDER BY s.fullname, g.grade DESC
;"""


def select_7(group_id, discipline_id):
    result = (
        session.query(
            Group.name.label('group_name'),
            Discipline.name.label('discipline_name'),
            Student.fullname,
            Grade.grade
        )
        .join(Discipline, Discipline.id == Grade.discipline_id)
        .join(Student, Student.id == Grade.student_id)
        .join(Group, Student.group_id == Group.id)
        .filter(Group.id == group_id, Discipline.id == discipline_id)
        .order_by(Student.fullname, Grade.grade.desc())
    ).all()
    return result


"""-- 8. Знайти середній бал, який ставить певний викладач зі своїх предметів

SELECT t.fullname, ROUND(AVG(g.grade), 2) AS average_grade
FROM grades g
JOIN disciplines d ON g.discipline_id = d.id
JOIN teachers t ON d.teacher_id = t.id
WHERE t.id = 4  -- select teacher id
;"""

def select_8(teacher_id):
    result = (
        session.query(
            Teacher.fullname.label('teacher_name'),
            func.round(func.avg(Grade.grade), 1).label('average_grade')
        )
        .join(Discipline, Discipline.teacher_id == Teacher.id)
        .join(Grade, Grade.discipline_id == Discipline.id)
        .filter(Teacher.id == teacher_id)
        .group_by(Teacher.fullname)
    )
    return result.one()

"""-- 9. Знайти список курсів, які відвідує студент
SELECT s.fullname, d.name
FROM disciplines d
JOIN grades g ON d.id = g.discipline_id
JOIN students s ON s.id = g.student_id
WHERE s.id = 8  -- select teacher id
ORDER BY d.name
;"""

def select_9(student_id):
    result = (
        session.query(
            Student.fullname.label('student_name'),
            Discipline.name.label('course_name')
        )
        .join(Grade, Grade.student_id == Student.id)
        .join(Discipline, Discipline.id == Grade.discipline_id)
        .filter(Student.id == student_id)
        .order_by(Discipline.name)
    ).all()
    disciplines = [d[1] for d in set(result)]
    return f"Student: {result[0][0]}, studying disciplines: {disciplines}"

"""-- 10. Список курсів, які певному студенту читає певний викладач

SELECT s.fullname AS Student, t.fullname AS Teacher, d.name AS Discipline
FROM teachers t
JOIN disciplines d ON d.teacher_id = t.id
JOIN grades g ON d.id = g.discipline_id
JOIN students s ON g.student_id = s.id
WHERE s.id = 30 AND t.id = 4  -- select teacher id and students id
ORDER BY d.name
;"""

def select_10(student_id, teacher_id):
    results = (
        session.query(
            Student.fullname.label('Student'),
            Teacher.fullname.label('Teacher'),
            Discipline.name.label('Discipline')
        )
        .join(Grade, Grade.student_id == Student.id)
        .join(Discipline, Discipline.id == Grade.discipline_id)
        .join(Teacher, Teacher.id == Discipline.teacher_id)
        .filter(Student.id == student_id, Teacher.id == teacher_id)
        .order_by(Discipline.name)
    ).all()
    res = []
    for result in set(results):
        res.append(f"Teacher: {result.Teacher}, Discipline: {result.Discipline}")
    return results[0].Student + ":" + '\n' + '\n'.join(res)

"""11. Середній бал, який певний викладач ставить певному студентові.
SELECT ROUND(AVG(g.grade), 2) AS average_grade
FROM grades g
JOIN disciplines d ON d.id = g.discipline_id
JOIN teachers t ON t.id = d.teacher_id
WHERE t.id = <teacher_id> AND g.student_id = <student_id>
"""
def select_11(teacher_id, student_id):
    av_grade = (
        session.query(func.round(func.avg(Grade.grade), 2).label('average_grade'))
        .join(Discipline, Discipline.id == Grade.discipline_id)
        .join(Teacher, Teacher.id == Discipline.teacher_id)
        .filter(Teacher.id == teacher_id)
        .filter(Grade.student_id == student_id)
    ).scalar()

    return f"Average grade assigned by teacher with (ID {teacher_id}) to Student  with (ID {student_id}): {av_grade}"

"""12. Оцінки студентів у певній групі з певного предмета на останньому занятті.
"""

def select_12(discipline_id, group_id):
    subquery = (select(Grade.date_of).join(Student).join(Group).where(
        and_(Grade.discipline_id == discipline_id, Group.id == group_id)
    ).order_by(desc(Grade.date_of)).limit(1).scalar_subquery())

    result = session.query(Discipline.name,
                           Student.fullname,
                           Group.name,
                           Grade.date_of,
                           Grade.grade
                           ) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .join(Group) \
        .filter(and_(Discipline.id == discipline_id, Group.id == group_id, Grade.date_of == subquery)) \
        .order_by(desc(Grade.date_of)) \
        .all()


    return result


if __name__ == "__main__":
    print(select_1())
    print(select_2(8))
    print(select_3(3))
    print(select_4())
    print(select_5(2))
    print(select_6(1))
    print(select_7(1, 2))
    print(select_8(2))
    print(select_9(5))
    print(select_10(12,3))
    print(select_11(2, 15))
    print(select_12(2, 3))
