#!/usr/bin/env python3
"""
High School Schedule Creator

A comprehensive scheduling system for an Islamic high school in California
that meets UC/CSU A-G requirements while offering specialized courses in
Arabic, Islamic Studies, and Quran.

Features:
- Three graduation paths: Minimum, Pre-Med, Engineering
- Constraint-based scheduling algorithm
- Resource optimization (minimum classrooms and teachers)
- 4-year course planning for each graduation path

Actual Physical Constraints:
- 10 general purpose classrooms
- 1 chemistry lab
- 1 biology/science lab
- 1 computer lab
- 1 robotics lab
- Total: 14 rooms
"""

from models import GraduationPath, RoomType, SubjectArea, CourseLevel
from course_catalog import COURSE_CATALOG
from graduation_paths import get_all_paths, print_path_summary
from resource_calculator import ResourceCalculator, print_resource_analysis
from scheduler import Scheduler, print_master_schedule, print_schedule_summary


def print_header():
    """Print the program header."""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     HIGH SCHOOL SCHEDULE CREATOR                             ║
║                                                                              ║
║  California A-G Compliant Islamic High School Scheduling System              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")


def print_graduation_requirements():
    """Print the graduation requirements summary."""
    print("""
┌──────────────────────────────────────────────────────────────────────────────┐
│                        GRADUATION REQUIREMENTS                               │
├──────────────────────────────────────────────────────────────────────────────┤
│  UC/CSU A-G Requirements (15 year-long courses):                             │
│                                                                              │
│  A) History/Social Science .......... 2 years                                │
│     • World History (Grade 10)                                               │
│     • US History (Grade 11)                                                  │
│     • Government + Economics (Grade 12)                                      │
│                                                                              │
│  B) English ......................... 4 years                                │
│     • English 9, 10, 11, 12                                                  │
│                                                                              │
│  C) Mathematics ..................... 3 years (4 recommended)                │
│     • Algebra 1, Geometry, Algebra 2, Pre-Calculus/Calculus                  │
│                                                                              │
│  D) Laboratory Science .............. 2 years (3 recommended)                │
│     • Biology, Chemistry, Physics                                            │
│                                                                              │
│  E) Language Other Than English ..... 2 years (3 recommended)                │
│     • Arabic 1, 2, 3, 4 (Arabic satisfies this requirement)                  │
│                                                                              │
│  F) Visual and Performing Arts ...... 1 year                                 │
│     • Art 1, Music                                                           │
│                                                                              │
│  G) College-Prep Elective ........... 1 year                                 │
│     • Additional academic courses (CS, Robotics, etc.)                       │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│  California State Requirements:                                              │
│  • Physical Education: 2 years (Grades 9-10)                                 │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│  School-Specific Requirements:                                               │
│  • Islamic Studies: 4 years (one per grade level)                            │
│  • Quran Studies: 4 years (one per grade level)                              │
└──────────────────────────────────────────────────────────────────────────────┘
""")


def print_four_year_plans():
    """Print the 4-year plans for all graduation paths."""
    print("\n" + "=" * 80)
    print(" " * 20 + "FOUR-YEAR COURSE PLANS BY GRADUATION PATH")
    print("=" * 80)

    paths = get_all_paths()

    for path_type, path_plan in paths.items():
        print(f"\n{'━' * 80}")
        print(f"  {path_plan.path.value.upper()}")
        print(f"{'━' * 80}")
        print(f"\n  {path_plan.description}\n")

        year_names = {1: "FRESHMAN (Grade 9)", 2: "SOPHOMORE (Grade 10)",
                     3: "JUNIOR (Grade 11)", 4: "SENIOR (Grade 12)"}

        for year_plan in path_plan.year_plans:
            print(f"\n  ┌{'─' * 76}┐")
            print(f"  │ {year_names[year_plan.year]:74} │")
            print(f"  ├{'─' * 76}┤")

            # Get year-long and semester-only courses
            year_long = set(year_plan.semester1_courses) & set(year_plan.semester2_courses)
            sem1_only = set(year_plan.semester1_courses) - year_long
            sem2_only = set(year_plan.semester2_courses) - year_long

            print(f"  │ {'YEAR-LONG COURSES:':<74} │")
            for code in sorted(year_long):
                course = COURSE_CATALOG.get(code)
                if course:
                    level = f" [{course.level.value}]" if course.level != CourseLevel.REGULAR else ""
                    line = f"   • {course.name}{level}"
                    print(f"  │ {line:<74} │")

            if sem1_only or sem2_only:
                print(f"  │ {'':<74} │")
                if sem1_only:
                    print(f"  │ {'SEMESTER 1 ONLY:':<74} │")
                    for code in sorted(sem1_only):
                        course = COURSE_CATALOG.get(code)
                        if course:
                            line = f"   • {course.name}"
                            print(f"  │ {line:<74} │")

                if sem2_only:
                    print(f"  │ {'SEMESTER 2 ONLY:':<74} │")
                    for code in sorted(sem2_only):
                        course = COURSE_CATALOG.get(code)
                        if course:
                            line = f"   • {course.name}"
                            print(f"  │ {line:<74} │")

            print(f"  └{'─' * 76}┘")

        # Print path statistics
        total_courses = len(set(
            code for yp in path_plan.year_plans
            for code in yp.get_all_courses()
        ))
        ap_courses = [
            COURSE_CATALOG[code] for yp in path_plan.year_plans
            for code in yp.get_all_courses()
            if code in COURSE_CATALOG and COURSE_CATALOG[code].level == CourseLevel.AP
        ]
        print(f"\n  Summary: {total_courses} unique courses, {len(set(c.code for c in ap_courses))} AP courses")


def print_detailed_resource_analysis(students_per_path, max_class_size, periods_per_day):
    """Print detailed resource analysis."""
    calculator = ResourceCalculator(
        students_per_path=students_per_path,
        max_class_size=max_class_size,
        periods_per_day=periods_per_day
    )
    requirements = calculator.calculate_requirements()

    print("\n" + "=" * 80)
    print(" " * 25 + "MINIMUM RESOURCE REQUIREMENTS")
    print("=" * 80)

    total_students = sum(students_per_path.values())

    print(f"""
┌──────────────────────────────────────────────────────────────────────────────┐
│  INPUT PARAMETERS                                                            │
├──────────────────────────────────────────────────────────────────────────────┤
│  Total Students: {total_students:<60} │
│    • Minimum Path: {students_per_path.get(GraduationPath.MINIMUM, 0):<57} │
│    • Pre-Med Path: {students_per_path.get(GraduationPath.PRE_MED, 0):<57} │
│    • Engineering Path: {students_per_path.get(GraduationPath.ENGINEERING, 0):<53} │
│  Maximum Class Size: {max_class_size:<55} │
│  Periods Per Day: {periods_per_day:<58} │
└──────────────────────────────────────────────────────────────────────────────┘
""")

    # Classrooms
    room_type_names = {
        RoomType.GENERAL: "General Classrooms",
        RoomType.CHEMISTRY_LAB: "Chemistry Laboratory",
        RoomType.BIOLOGY_LAB: "Biology/Science Laboratory",
        RoomType.COMPUTER_LAB: "Computer Laboratory",
        RoomType.ROBOTICS_LAB: "Robotics Laboratory",
        RoomType.ART_ROOM: "Art Room",
        RoomType.GYM: "Gymnasium",
        RoomType.MUSIC_ROOM: "Music Room",
    }

    print("┌──────────────────────────────────────────────────────────────────────────────┐")
    print("│  🏫 MINIMUM CLASSROOMS REQUIRED                                             │")
    print("├──────────────────────────────────────────────────────────────────────────────┤")

    total_rooms = 0
    for room_type in RoomType:
        count = requirements.min_classrooms.get(room_type, 0)
        if count > 0:
            name = room_type_names.get(room_type, room_type.name)
            line = f"  • {name}: {count}"
            print(f"│ {line:<76} │")
            total_rooms += count

    print("├──────────────────────────────────────────────────────────────────────────────┤")
    print(f"│  TOTAL CLASSROOMS NEEDED: {total_rooms:<50} │")
    print("└──────────────────────────────────────────────────────────────────────────────┘")

    # Teachers
    subject_names = {
        SubjectArea.HISTORY_SOCIAL_SCIENCE: "History/Social Science",
        SubjectArea.ENGLISH: "English",
        SubjectArea.MATHEMATICS: "Mathematics",
        SubjectArea.LABORATORY_SCIENCE: "Laboratory Science (Bio, Chem, Physics)",
        SubjectArea.LANGUAGE_OTHER: "World Languages (Arabic)",
        SubjectArea.VISUAL_PERFORMING_ARTS: "Visual/Performing Arts",
        SubjectArea.COLLEGE_PREP_ELECTIVE: "Computer Science / Robotics",
        SubjectArea.PHYSICAL_EDUCATION: "Physical Education",
        SubjectArea.RELIGIOUS_STUDIES: "Religious Studies (Islamic/Quran)",
    }

    print("\n┌──────────────────────────────────────────────────────────────────────────────┐")
    print("│  👨‍🏫 MINIMUM TEACHERS REQUIRED                                               │")
    print("├──────────────────────────────────────────────────────────────────────────────┤")

    total_teachers = 0
    for subject in SubjectArea:
        if subject in requirements.min_teachers:
            info = requirements.min_teachers[subject]
            if info["total"] > 0:
                name = subject_names.get(subject, subject.name)
                ap_note = f" ({info['ap_qualified']} AP-qualified)" if info["ap_qualified"] > 0 else ""
                line = f"  • {name}: {info['total']}{ap_note}"
                print(f"│ {line:<76} │")
                total_teachers += info["total"]

    print("├──────────────────────────────────────────────────────────────────────────────┤")
    print(f"│  TOTAL TEACHERS NEEDED: {total_teachers:<52} │")
    print("└──────────────────────────────────────────────────────────────────────────────┘")

    return requirements


def print_actual_facilities():
    """Print the actual facilities available at the school."""
    print("""
┌──────────────────────────────────────────────────────────────────────────────┐
│                        ACTUAL SCHOOL FACILITIES                              │
├──────────────────────────────────────────────────────────────────────────────┤
│  The school has the following classrooms available:                          │
│                                                                              │
│  General Purpose Classrooms ............... 10                               │
│  Chemistry Laboratory ..................... 1                                │
│  Biology/Science Laboratory ............... 1                                │
│  Computer Laboratory ...................... 1                                │
│  Robotics Laboratory ...................... 1                                │
│  Gymnasium (basketball court + weights) ... 1                                │
│  ─────────────────────────────────────────────                               │
│  TOTAL ROOMS .............................. 15                               │
│                                                                              │
│  Note: Art and music classes will use general classrooms.                    │
│        No dedicated theater/performing arts space.                           │
└──────────────────────────────────────────────────────────────────────────────┘
""")


def main():
    """Main entry point."""
    print_header()
    print_actual_facilities()
    print_graduation_requirements()

    # Configuration based on actual classroom constraints
    # Maximum feasible: 25 students per path (75 total)
    students_per_path = {
        GraduationPath.MINIMUM: 25,
        GraduationPath.PRE_MED: 25,
        GraduationPath.ENGINEERING: 25,
    }
    max_class_size = 25
    periods_per_day = 6

    # Print 4-year plans
    print_four_year_plans()

    # Print resource analysis
    requirements = print_detailed_resource_analysis(
        students_per_path, max_class_size, periods_per_day
    )

    # Create and print schedule
    print("\n" + "=" * 80)
    print(" " * 30 + "MASTER SCHEDULE")
    print("=" * 80)

    scheduler = Scheduler(
        students_per_path=students_per_path,
        max_class_size=max_class_size,
        periods_per_day=periods_per_day
    )

    schedule = scheduler.create_schedule()
    print_schedule_summary(schedule)

    print("\n" + "=" * 80)
    print(" " * 25 + "SEMESTER 1 CLASS SCHEDULE")
    print("=" * 80)
    print_master_schedule(schedule, semester=1)

    # Summary
    print("\n" + "=" * 80)
    print(" " * 30 + "FINAL SUMMARY")
    print("=" * 80)

    total_students = sum(students_per_path.values())
    total_rooms = sum(requirements.min_classrooms.values())
    total_teachers = sum(info["total"] for info in requirements.min_teachers.values())

    print(f"""
┌──────────────────────────────────────────────────────────────────────────────┐
│                           SCHOOL RESOURCE SUMMARY                            │
├──────────────────────────────────────────────────────────────────────────────┤
│  Total Students: {total_students:<59} │
│  Graduation Paths Offered: 3                                                 │
│    1. Minimum Requirements (No AP)                                           │
│    2. Pre-Medical Track (AP Bio, Chem, Calc, Psych)                          │
│    3. Engineering Track (AP CS, Physics, Calc, Chem)                         │
│                                                                              │
│  MINIMUM CLASSROOMS NEEDED: {total_rooms:<48} │
│  MINIMUM TEACHERS NEEDED: {total_teachers:<50} │
│                                                                              │
│  Schedule Structure:                                                         │
│    • {periods_per_day} periods per day                                                        │
│    • 2 semesters per year                                                    │
│    • Same schedule Monday-Friday                                             │
│    • 6-7 classes per student per semester                                    │
└──────────────────────────────────────────────────────────────────────────────┘
""")


if __name__ == "__main__":
    main()
