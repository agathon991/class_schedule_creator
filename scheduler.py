"""
Constraint-based scheduler for creating the master schedule.
"""

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional
import random

from models import (
    Course, Classroom, Teacher, RoomType, SubjectArea,
    GraduationPath, CourseLevel, Section
)
from course_catalog import COURSE_CATALOG
from graduation_paths import get_all_paths
from resource_calculator import ResourceCalculator


@dataclass
class ScheduledSection:
    """A fully scheduled section."""
    course_code: str
    section_id: int
    period: int
    semester: int  # 1 or 2
    classroom_id: str
    teacher_id: str
    student_ids: list[str] = field(default_factory=list)

    @property
    def course(self) -> Course:
        return COURSE_CATALOG[self.course_code]


@dataclass
class MasterSchedule:
    """The complete master schedule for the school."""
    sections: list[ScheduledSection]
    classrooms: list[Classroom]
    teachers: list[Teacher]

    def get_sections_by_period(self, period: int, semester: int = 1) -> list[ScheduledSection]:
        """Get all sections scheduled for a specific period."""
        return [s for s in self.sections if s.period == period and s.semester == semester]

    def get_teacher_schedule(self, teacher_id: str, semester: int = 1) -> dict[int, ScheduledSection]:
        """Get a teacher's schedule by period."""
        schedule = {}
        for section in self.sections:
            if section.teacher_id == teacher_id and section.semester == semester:
                schedule[section.period] = section
        return schedule

    def get_classroom_schedule(self, classroom_id: str, semester: int = 1) -> dict[int, ScheduledSection]:
        """Get a classroom's schedule by period."""
        schedule = {}
        for section in self.sections:
            if section.classroom_id == classroom_id and section.semester == semester:
                schedule[section.period] = section
        return schedule

    def validate(self) -> list[str]:
        """Validate the schedule for constraint violations."""
        errors = []

        for semester in [1, 2]:
            for period in range(1, 7):
                sections = self.get_sections_by_period(period, semester)

                # Check classroom conflicts
                classrooms_used = defaultdict(list)
                for section in sections:
                    classrooms_used[section.classroom_id].append(section)

                for classroom_id, classroom_sections in classrooms_used.items():
                    if len(classroom_sections) > 1:
                        courses = [s.course.name for s in classroom_sections]
                        errors.append(
                            f"Classroom conflict: {classroom_id} has multiple courses "
                            f"in period {period}, semester {semester}: {courses}"
                        )

                # Check teacher conflicts
                teachers_used = defaultdict(list)
                for section in sections:
                    teachers_used[section.teacher_id].append(section)

                for teacher_id, teacher_sections in teachers_used.items():
                    if len(teacher_sections) > 1:
                        courses = [s.course.name for s in teacher_sections]
                        errors.append(
                            f"Teacher conflict: {teacher_id} has multiple courses "
                            f"in period {period}, semester {semester}: {courses}"
                        )

        return errors


class Scheduler:
    """Creates the master schedule using constraint satisfaction."""

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

        self.calculator = ResourceCalculator(
            students_per_path=students_per_path,
            max_class_size=max_class_size,
            periods_per_day=periods_per_day
        )

    def create_classrooms(self) -> list[Classroom]:
        """Create the minimum required classrooms."""
        min_rooms = self.calculator.calculate_min_classrooms()
        classrooms = []

        room_names = {
            RoomType.GENERAL: "Room",
            RoomType.CHEMISTRY_LAB: "Chem Lab",
            RoomType.BIOLOGY_LAB: "Bio Lab",
            RoomType.COMPUTER_LAB: "Computer Lab",
            RoomType.ROBOTICS_LAB: "Robotics Lab",
            RoomType.ART_ROOM: "Art Room",
            RoomType.GYM: "Gymnasium",
            RoomType.MUSIC_ROOM: "Music Room",
        }

        for room_type, count in min_rooms.items():
            for i in range(1, count + 1):
                room_id = f"{room_type.name}_{i}"
                name = f"{room_names.get(room_type, room_type.name)} {i}"
                classrooms.append(Classroom(
                    id=room_id,
                    name=name,
                    room_type=room_type,
                    capacity=self.max_class_size
                ))

        return classrooms

    def create_teachers(self) -> list[Teacher]:
        """Create the minimum required teachers."""
        min_teachers = self.calculator.calculate_min_teachers()
        teachers = []

        subject_abbrev = {
            SubjectArea.HISTORY_SOCIAL_SCIENCE: "HIST",
            SubjectArea.ENGLISH: "ENG",
            SubjectArea.MATHEMATICS: "MATH",
            SubjectArea.LABORATORY_SCIENCE: "SCI",
            SubjectArea.LANGUAGE_OTHER: "ARAB",
            SubjectArea.VISUAL_PERFORMING_ARTS: "ART",
            SubjectArea.COLLEGE_PREP_ELECTIVE: "TECH",
            SubjectArea.PHYSICAL_EDUCATION: "PE",
            SubjectArea.RELIGIOUS_STUDIES: "REL",
        }

        for subject, info in min_teachers.items():
            abbrev = subject_abbrev.get(subject, subject.name[:4])

            # Create AP-qualified teachers
            for i in range(1, info["ap_qualified"] + 1):
                teacher_id = f"{abbrev}_AP_{i}"
                teachers.append(Teacher(
                    id=teacher_id,
                    name=f"{abbrev} Teacher {i} (AP)",
                    subject_areas=[subject],
                    can_teach_ap=True,
                    max_periods_per_day=self.periods_per_day - 1
                ))

            # Create regular teachers
            for i in range(1, info["regular_only"] + 1):
                teacher_id = f"{abbrev}_REG_{i}"
                teachers.append(Teacher(
                    id=teacher_id,
                    name=f"{abbrev} Teacher {i + info['ap_qualified']}",
                    subject_areas=[subject],
                    can_teach_ap=False,
                    max_periods_per_day=self.periods_per_day - 1
                ))

        return teachers

    def create_schedule(self) -> MasterSchedule:
        """Create the master schedule using a greedy constraint-based approach."""
        classrooms = self.create_classrooms()
        teachers = self.create_teachers()
        sections_needed = self.calculator.calculate_sections_needed()

        # Track what's available per period
        # {semester: {period: {classroom_id: bool, teacher_id: bool}}}
        classroom_available = {
            1: {p: {c.id: True for c in classrooms} for p in range(1, self.periods_per_day + 1)},
            2: {p: {c.id: True for c in classrooms} for p in range(1, self.periods_per_day + 1)}
        }
        teacher_available = {
            1: {p: {t.id: True for t in teachers} for p in range(1, self.periods_per_day + 1)},
            2: {p: {t.id: True for t in teachers} for p in range(1, self.periods_per_day + 1)}
        }

        # Track teacher load
        teacher_sections = defaultdict(int)

        scheduled_sections = []
        section_counter = 0

        # Sort courses by constraints (most constrained first)
        def course_priority(code):
            course = COURSE_CATALOG.get(code)
            if not course:
                return 0
            priority = 0
            # AP courses are more constrained (fewer qualified teachers)
            if course.level == CourseLevel.AP:
                priority += 100
            # Specialized rooms are more constrained
            if course.room_type_required != RoomType.GENERAL:
                priority += 50
            return -priority  # Negative for descending sort

        sorted_courses = sorted(sections_needed.keys(), key=course_priority)

        for course_code in sorted_courses:
            course = COURSE_CATALOG.get(course_code)
            if not course:
                continue

            year_sections = sections_needed[course_code]
            total_sections = sum(year_sections.values())

            # Find compatible classrooms
            compatible_rooms = [
                c for c in classrooms
                if c.can_host(course)
            ]

            # Find compatible teachers
            compatible_teachers = [
                t for t in teachers
                if t.can_teach(course)
            ]

            # Determine which semesters this course runs
            if course.semesters == 2:
                semesters_to_schedule = [1, 2]  # Full year course
            else:
                semesters_to_schedule = [1]  # Single semester (adjust as needed)

            for section_num in range(total_sections):
                scheduled = False

                for semester in semesters_to_schedule:
                    for period in range(1, self.periods_per_day + 1):
                        if scheduled:
                            break

                        # Find available classroom
                        available_room = None
                        for room in compatible_rooms:
                            if classroom_available[semester][period][room.id]:
                                available_room = room
                                break

                        if not available_room:
                            continue

                        # Find available teacher with capacity
                        available_teacher = None
                        for teacher in compatible_teachers:
                            if (teacher_available[semester][period][teacher.id] and
                                teacher_sections[teacher.id] < teacher.max_periods_per_day * 2):
                                available_teacher = teacher
                                break

                        if not available_teacher:
                            continue

                        # Schedule this section
                        section_counter += 1
                        section = ScheduledSection(
                            course_code=course_code,
                            section_id=section_counter,
                            period=period,
                            semester=semester,
                            classroom_id=available_room.id,
                            teacher_id=available_teacher.id
                        )
                        scheduled_sections.append(section)

                        # Mark resources as used
                        classroom_available[semester][period][available_room.id] = False
                        teacher_available[semester][period][available_teacher.id] = False
                        teacher_sections[available_teacher.id] += 1

                        scheduled = True

                        # For year-long courses, schedule in both semesters
                        if course.semesters == 2 and semester == 1:
                            # Also schedule for semester 2
                            if (classroom_available[2][period][available_room.id] and
                                teacher_available[2][period][available_teacher.id]):
                                section2 = ScheduledSection(
                                    course_code=course_code,
                                    section_id=section_counter,
                                    period=period,
                                    semester=2,
                                    classroom_id=available_room.id,
                                    teacher_id=available_teacher.id
                                )
                                scheduled_sections.append(section2)
                                classroom_available[2][period][available_room.id] = False
                                teacher_available[2][period][available_teacher.id] = False

                if not scheduled:
                    print(f"WARNING: Could not schedule section of {course.name}")

        return MasterSchedule(
            sections=scheduled_sections,
            classrooms=classrooms,
            teachers=teachers
        )


def print_master_schedule(schedule: MasterSchedule, semester: int = 1):
    """Print the master schedule in a readable format."""
    print(f"\n{'='*80}")
    print(f"MASTER SCHEDULE - SEMESTER {semester}")
    print(f"{'='*80}")

    # Group sections by period
    for period in range(1, 7):
        sections = schedule.get_sections_by_period(period, semester)
        print(f"\nPeriod {period}")
        print("-" * 70)

        if not sections:
            print("  (No classes scheduled)")
            continue

        # Sort by classroom
        sections.sort(key=lambda s: s.classroom_id)

        for section in sections:
            course = section.course
            level_str = f" ({course.level.value})" if course.level != CourseLevel.REGULAR else ""
            teacher = next((t for t in schedule.teachers if t.id == section.teacher_id), None)
            teacher_name = teacher.name if teacher else section.teacher_id

            print(f"  {section.classroom_id:20} | {course.name}{level_str:30} | {teacher_name}")


def print_schedule_summary(schedule: MasterSchedule):
    """Print a summary of the schedule."""
    print(f"\n{'='*80}")
    print("SCHEDULE SUMMARY")
    print(f"{'='*80}")

    print(f"\nTotal Classrooms: {len(schedule.classrooms)}")
    for room in schedule.classrooms:
        print(f"  - {room.name} ({room.room_type.name})")

    print(f"\nTotal Teachers: {len(schedule.teachers)}")
    for teacher in schedule.teachers:
        ap_str = " [AP-qualified]" if teacher.can_teach_ap else ""
        sections = [s for s in schedule.sections if s.teacher_id == teacher.id and s.semester == 1]
        print(f"  - {teacher.name}{ap_str}: {len(sections)} sections/semester")

    # Validate
    errors = schedule.validate()
    if errors:
        print(f"\n⚠️  SCHEDULE VALIDATION ERRORS ({len(errors)}):")
        for error in errors[:10]:
            print(f"  - {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")
    else:
        print("\n✅ Schedule validation passed - no conflicts detected")


if __name__ == "__main__":
    students = {
        GraduationPath.MINIMUM: 20,
        GraduationPath.PRE_MED: 20,
        GraduationPath.ENGINEERING: 20,
    }

    scheduler = Scheduler(
        students_per_path=students,
        max_class_size=25,
        periods_per_day=6
    )

    schedule = scheduler.create_schedule()
    print_schedule_summary(schedule)
    print_master_schedule(schedule, semester=1)
