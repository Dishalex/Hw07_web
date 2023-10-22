from datetime import date, datetime, timedelta
from random import randint, choice
import faker
from sqlalchemy import select, desc, select, and_

from sqlalchemy import func

from src.models import Teacher, Student, Discipline, Grade, Group
from src.db import session


def select_1():
    result = session.query(Student.fullname, func.round(func.avg(Grade.grade), 1).label('avg_grade')) \
        .select_from(Grade).join(Student).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()
    return result


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
        .join(Group)\
        .filter(and_(Discipline.id == discipline_id, Group.id == group_id, Grade.date_of == subquery)) \
        .order_by(desc(Grade.date_of)) \
        .all()
    return result


if __name__ == "__main__":
    print(select_1())
    print(select_2(8))
    print(select_12(2,3))

    """3
1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
2. Знайти студента із найвищим середнім балом з певного предмета.
3. Знайти середній бал у групах з певного предмета.
4. Знайти середній бал на потоці (по всій таблиці оцінок).
5. Знайти які курси читає певний викладач.
6. Знайти список студентів у певній групі.
7. Знайти оцінки студентів у окремій групі з певного предмета.
8. Знайти середній бал, який ставить певний викладач зі своїх предметів.
9. Знайти список курсів, які відвідує певний студент.
10.Список курсів, які певному студенту читає певний викладач.

11. Середній бал, який певний викладач ставить певному студентові.
12. Оцінки студентів у певній групі з певного предмета на останньому занятті.
"""

