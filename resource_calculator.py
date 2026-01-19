"""
Resource calculator for determining minimum classrooms and teachers needed.
"""

from collections import defaultdict
from dataclasses import dataclass
from typing import Optional
import math

from models import (
    Course, Classroom, Teacher, RoomType, SubjectArea,
    GraduationPath, CourseLevel
)
from course_catalog import COURSE_CATALOG
from graduation_paths import get_all_paths, get_all_required_courses


@dataclass
class ResourceRequirements:
    """Calculated resource requirements."""
    min_classrooms: dict[RoomType, int]
    min_teachers: dict[SubjectArea, int]
    total_sections_per_period: dict[int, int]  # year -> sections needed
    course_sections: dict[str, int]  # course_code -> number of sections


class ResourceCalculator:
    """Calculates minimum resources needed for the school."""

    def __init__(
        self,
        students_per_path: dict[GraduationPath, int],
        max_class_size: int = 25,
        periods_per_day: int = 6
    ):
        self.students_per_path = students_per_path
        self.max_class_size = max_class_size
        self.periods_per_day = periods_per_day
        self.paths = get_all_paths()

    def calculate_sections_needed(self) -> dict[str, dict[int, int]]:
        """
        Calculate how many sections of each course are needed per year.
        Returns: {course_code: {year: num_sections}}
        """
        # Count students needing each course per year
        course_demand = defaultdict(lambda: defaultdict(int))

        for path, num_students in self.students_per_path.items():
            path_plan = self.paths[path]
            for year_plan in path_plan.year_plans:
                for code in year_plan.get_all_courses():
                    course_demand[code][year_plan.year] += num_students

        # Calculate sections needed (ceil of students / max_class_size)
        sections_needed = defaultdict(dict)
        for code, year_demands in course_demand.items():
            for year, num_students in year_demands.items():
                sections_needed[code][year] = math.ceil(num_students / self.max_class_size)

        return dict(sections_needed)

    def calculate_concurrent_sections(self) -> dict[int, dict[RoomType, int]]:
        """
        Calculate maximum concurrent sections by room type per year.
        This determines minimum classrooms needed.
        """
        sections_needed = self.calculate_sections_needed()

        # For each year, calculate sections by room type
        year_room_sections = defaultdict(lambda: defaultdict(int))

        for code, year_sections in sections_needed.items():
            course = COURSE_CATALOG.get(code)
            if not course:
                continue

            for year, num_sections in year_sections.items():
                room_type = course.room_type_required
                year_room_sections[year][room_type] += num_sections

        return dict(year_room_sections)

    def calculate_min_classrooms(self) -> dict[RoomType, int]:
        """
        Calculate minimum classrooms needed by type.

        The key insight is that all years (freshman through senior) run simultaneously,
        so we need to handle the peak concurrent demand across all years.
        """
        sections_needed = self.calculate_sections_needed()

        # Group sections by room type across ALL years (simultaneous)
        room_type_sections = defaultdict(int)

        for code, year_sections in sections_needed.items():
            course = COURSE_CATALOG.get(code)
            if not course:
                continue

            room_type = course.room_type_required
            # Sum across all years since all grades run simultaneously
            total_sections = sum(year_sections.values())
            room_type_sections[room_type] += total_sections

        # Each room can host (periods_per_day) sections
        # Minimum rooms = ceil(total_sections / periods_per_day)
        min_rooms = {}
        for room_type, total_sections in room_type_sections.items():
            min_rooms[room_type] = math.ceil(total_sections / self.periods_per_day)

        return min_rooms

    def calculate_min_teachers(self) -> dict[SubjectArea, dict[str, int]]:
        """
        Calculate minimum teachers needed by subject area.
        Returns: {subject_area: {"regular": count, "ap": count}}

        Teachers can teach up to (periods_per_day - 1) sections per day
        (one period for planning).
        """
        sections_needed = self.calculate_sections_needed()
        max_teaching_periods = self.periods_per_day - 1  # Planning period

        # Group sections by subject area and level
        subject_sections = defaultdict(lambda: {"regular": 0, "ap": 0})

        for code, year_sections in sections_needed.items():
            course = COURSE_CATALOG.get(code)
            if not course:
                continue

            total_sections = sum(year_sections.values())
            key = "ap" if course.level == CourseLevel.AP else "regular"
            subject_sections[course.subject_area][key] += total_sections

        # Calculate teachers needed
        # AP teachers can teach regular courses, but regular teachers can't teach AP
        min_teachers = {}
        for subject, levels in subject_sections.items():
            ap_sections = levels["ap"]
            regular_sections = levels["regular"]

            # First, calculate AP teachers needed
            ap_teachers = math.ceil(ap_sections / max_teaching_periods)

            # AP teachers can also teach regular sections
            ap_teacher_capacity = ap_teachers * max_teaching_periods - ap_sections
            remaining_regular = max(0, regular_sections - ap_teacher_capacity)

            # Calculate additional regular teachers needed
            regular_teachers = math.ceil(remaining_regular / max_teaching_periods)

            min_teachers[subject] = {
                "ap_qualified": ap_teachers,
                "regular_only": regular_teachers,
                "total": ap_teachers + regular_teachers
            }

        return min_teachers

    def calculate_requirements(self) -> ResourceRequirements:
        """Calculate all resource requirements."""
        sections_needed = self.calculate_sections_needed()

        # Flatten course sections
        course_sections = {}
        for code, year_sections in sections_needed.items():
            course_sections[code] = sum(year_sections.values())

        # Calculate sections per period per year
        year_room_sections = self.calculate_concurrent_sections()
        total_sections_per_year = {}
        for year, room_sections in year_room_sections.items():
            total_sections_per_year[year] = sum(room_sections.values())

        return ResourceRequirements(
            min_classrooms=self.calculate_min_classrooms(),
            min_teachers=self.calculate_min_teachers(),
            total_sections_per_period=total_sections_per_year,
            course_sections=course_sections
        )


def print_resource_analysis(
    students_per_path: dict[GraduationPath, int],
    max_class_size: int = 25,
    periods_per_day: int = 6
):
    """Print a detailed resource analysis."""

    calculator = ResourceCalculator(
        students_per_path=students_per_path,
        max_class_size=max_class_size,
        periods_per_day=periods_per_day
    )

    requirements = calculator.calculate_requirements()

    print("\n" + "=" * 70)
    print("RESOURCE REQUIREMENTS ANALYSIS")
    print("=" * 70)

    print("\n📊 INPUT PARAMETERS")
    print("-" * 40)
    total_students = sum(students_per_path.values())
    print(f"Total Students: {total_students}")
    for path, count in students_per_path.items():
        print(f"  - {path.value}: {count} students")
    print(f"Maximum Class Size: {max_class_size}")
    print(f"Periods Per Day: {periods_per_day}")

    print("\n" + "=" * 70)
    print("🏫 MINIMUM CLASSROOMS REQUIRED")
    print("=" * 70)

    total_rooms = 0
    room_type_names = {
        RoomType.GENERAL: "General Classrooms",
        RoomType.CHEMISTRY_LAB: "Chemistry Lab",
        RoomType.BIOLOGY_LAB: "Biology/Science Lab",
        RoomType.COMPUTER_LAB: "Computer Lab",
        RoomType.ROBOTICS_LAB: "Robotics Lab",
        RoomType.ART_ROOM: "Art Room",
        RoomType.GYM: "Gymnasium",
        RoomType.MUSIC_ROOM: "Music Room",
    }

    for room_type in RoomType:
        count = requirements.min_classrooms.get(room_type, 0)
        if count > 0:
            print(f"  {room_type_names.get(room_type, room_type.name)}: {count}")
            total_rooms += count

    print(f"\n  TOTAL CLASSROOMS: {total_rooms}")

    print("\n" + "=" * 70)
    print("👨‍🏫 MINIMUM TEACHERS REQUIRED")
    print("=" * 70)

    total_teachers = 0
    subject_names = {
        SubjectArea.HISTORY_SOCIAL_SCIENCE: "History/Social Science",
        SubjectArea.ENGLISH: "English",
        SubjectArea.MATHEMATICS: "Mathematics",
        SubjectArea.LABORATORY_SCIENCE: "Laboratory Science",
        SubjectArea.LANGUAGE_OTHER: "World Languages (Arabic)",
        SubjectArea.VISUAL_PERFORMING_ARTS: "Visual/Performing Arts",
        SubjectArea.COLLEGE_PREP_ELECTIVE: "College Prep / CS / Robotics",
        SubjectArea.PHYSICAL_EDUCATION: "Physical Education",
        SubjectArea.RELIGIOUS_STUDIES: "Religious Studies (Islamic/Quran)",
        SubjectArea.ELECTIVE: "General Electives",
    }

    for subject in SubjectArea:
        if subject in requirements.min_teachers:
            info = requirements.min_teachers[subject]
            name = subject_names.get(subject, subject.name)
            if info["total"] > 0:
                ap_note = f" ({info['ap_qualified']} AP-qualified)" if info["ap_qualified"] > 0 else ""
                print(f"  {name}: {info['total']}{ap_note}")
                total_teachers += info["total"]

    print(f"\n  TOTAL TEACHERS: {total_teachers}")

    print("\n" + "=" * 70)
    print("📚 COURSE SECTIONS REQUIRED")
    print("=" * 70)

    # Group by subject area
    courses_by_subject = defaultdict(list)
    for code, num_sections in requirements.course_sections.items():
        course = COURSE_CATALOG.get(code)
        if course:
            courses_by_subject[course.subject_area].append((course, num_sections))

    for subject in SubjectArea:
        if subject in courses_by_subject:
            print(f"\n{subject_names.get(subject, subject.name)}:")
            for course, num_sections in sorted(courses_by_subject[subject], key=lambda x: x[0].name):
                level_str = f" ({course.level.value})" if course.level != CourseLevel.REGULAR else ""
                print(f"    {course.name}{level_str}: {num_sections} section(s)")

    return requirements


if __name__ == "__main__":
    # Example with medium enrollment
    students = {
        GraduationPath.MINIMUM: 20,
        GraduationPath.PRE_MED: 20,
        GraduationPath.ENGINEERING: 20,
    }

    print_resource_analysis(students, max_class_size=25, periods_per_day=6)
