"""
School configuration - actual physical resources available.
"""

from models import Classroom, RoomType


def create_actual_classrooms() -> list[Classroom]:
    """
    Create the actual classrooms available at the school.

    Available facilities:
    - 10 general purpose classrooms
    - 1 chemistry lab
    - 1 biology/science lab
    - 1 computer lab
    - 1 robotics lab
    - 1 gymnasium (with basketball court and weights room)

    Total: 15 rooms

    Note: Art classes will use general classrooms.
    """
    classrooms = []

    # 10 General purpose classrooms
    for i in range(1, 11):
        classrooms.append(Classroom(
            id=f"ROOM_{i}",
            name=f"Room {100 + i}",
            room_type=RoomType.GENERAL,
            capacity=25
        ))

    # Chemistry lab
    classrooms.append(Classroom(
        id="CHEM_LAB",
        name="Chemistry Lab",
        room_type=RoomType.CHEMISTRY_LAB,
        capacity=25
    ))

    # Biology/Science lab
    classrooms.append(Classroom(
        id="BIO_LAB",
        name="Biology/Science Lab",
        room_type=RoomType.BIOLOGY_LAB,
        capacity=25
    ))

    # Computer lab
    classrooms.append(Classroom(
        id="COMP_LAB",
        name="Computer Lab",
        room_type=RoomType.COMPUTER_LAB,
        capacity=25
    ))

    # Robotics lab
    classrooms.append(Classroom(
        id="ROBOTICS_LAB",
        name="Robotics Lab",
        room_type=RoomType.ROBOTICS_LAB,
        capacity=25
    ))

    # Gymnasium (with basketball court and weights room)
    classrooms.append(Classroom(
        id="GYM",
        name="Gymnasium",
        room_type=RoomType.GYM,
        capacity=50  # Larger capacity for PE classes
    ))

    return classrooms


# Pre-built classroom list
ACTUAL_CLASSROOMS = create_actual_classrooms()

# Summary
CLASSROOM_SUMMARY = {
    "general": 10,
    "chemistry_lab": 1,
    "biology_lab": 1,
    "computer_lab": 1,
    "robotics_lab": 1,
    "gymnasium": 1,
    "total": 15
}
