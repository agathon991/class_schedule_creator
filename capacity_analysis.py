#!/usr/bin/env python3
"""
Capacity analysis for the school based on actual available classrooms.

Available facilities:
- 10 general purpose classrooms
- 1 chemistry lab
- 1 biology/science lab
- 1 computer lab
- 1 robotics lab
- 1 gymnasium (with basketball court and weights room)
Total: 15 rooms

Note: No dedicated art room, music room, or theater.
Art and music classes use general classrooms.
"""

import math
from collections import defaultdict

from models import GraduationPath, RoomType, SubjectArea, CourseLevel
from course_catalog import COURSE_CATALOG
from graduation_paths import get_all_paths, get_all_required_courses
from resource_calculator import ResourceCalculator


# Actual classroom counts
ACTUAL_ROOMS = {
    RoomType.GENERAL: 10,
    RoomType.CHEMISTRY_LAB: 1,
    RoomType.BIOLOGY_LAB: 1,
    RoomType.COMPUTER_LAB: 1,
    RoomType.ROBOTICS_LAB: 1,
    RoomType.GYM: 1,
}

PERIODS_PER_DAY = 6
MAX_CLASS_SIZE = 25


def analyze_room_demand_per_student():
    """
    Analyze how many room-periods each graduation path requires per student.
    This helps understand the bottleneck resources.
    """
    paths = get_all_paths()

    print("\n" + "=" * 70)
    print("ROOM DEMAND ANALYSIS PER STUDENT (per semester)")
    print("=" * 70)

    for path_type, path_plan in paths.items():
        print(f"\n{path_plan.path.value}")
        print("-" * 50)

        # Count periods needed by room type across all 4 years
        room_periods = defaultdict(int)

        for year_plan in path_plan.year_plans:
            # Each course in semester 1 needs 1 period
            for code in year_plan.semester1_courses:
                course = COURSE_CATALOG.get(code)
                if course:
                    room_periods[course.room_type_required] += 1

        # Sum across years (4 years of high school)
        print("  Room periods needed per semester (across 4 years):")
        for room_type, periods in sorted(room_periods.items(), key=lambda x: x[0].name):
            room_name = room_type.name.replace("_", " ").title()
            print(f"    {room_name}: {periods}")


def calculate_max_enrollment():
    """
    Calculate maximum enrollment given actual classroom constraints.

    The bottleneck is the room type with the highest demand relative to supply.
    """
    paths = get_all_paths()

    print("\n" + "=" * 70)
    print("MAXIMUM ENROLLMENT ANALYSIS")
    print("=" * 70)

    print(f"\nAvailable Classrooms:")
    for room_type, count in ACTUAL_ROOMS.items():
        print(f"  {room_type.name.replace('_', ' ').title()}: {count}")

    print(f"\nPeriods per day: {PERIODS_PER_DAY}")
    print(f"Max class size: {MAX_CLASS_SIZE}")

    # Calculate total room-periods available per semester
    total_capacity = {}
    for room_type, count in ACTUAL_ROOMS.items():
        total_capacity[room_type] = count * PERIODS_PER_DAY
    print(f"\nTotal room-periods available per day:")
    for room_type, capacity in total_capacity.items():
        print(f"  {room_type.name.replace('_', ' ').title()}: {capacity}")

    # Count how many sections of each course type needed for N students per path
    # Assuming equal distribution across paths
    def sections_needed_for_enrollment(students_per_path: int) -> dict[RoomType, int]:
        """Calculate total sections by room type for given enrollment."""
        room_sections = defaultdict(int)

        for path_type, path_plan in paths.items():
            for year_plan in path_plan.year_plans:
                for code in year_plan.semester1_courses:
                    course = COURSE_CATALOG.get(code)
                    if course:
                        # Sections needed = ceil(students / max_class_size)
                        sections = math.ceil(students_per_path / MAX_CLASS_SIZE)
                        room_sections[course.room_type_required] += sections

        return dict(room_sections)

    # Find maximum enrollment by testing different values
    print("\n" + "-" * 50)
    print("Testing enrollment levels (students per graduation path):")
    print("-" * 50)

    for students_per_path in [10, 15, 20, 25, 30, 35, 40, 50]:
        sections_by_room = sections_needed_for_enrollment(students_per_path)
        total_students = students_per_path * 3

        feasible = True
        bottleneck = None
        bottleneck_ratio = 0

        for room_type, sections_needed in sections_by_room.items():
            capacity = total_capacity.get(room_type, 0)
            if sections_needed > capacity:
                feasible = False
                ratio = sections_needed / capacity if capacity > 0 else float('inf')
                if ratio > bottleneck_ratio:
                    bottleneck_ratio = ratio
                    bottleneck = room_type

        status = "✓ FEASIBLE" if feasible else f"✗ EXCEEDS {bottleneck.name if bottleneck else 'capacity'}"
        print(f"  {students_per_path} per path ({total_students} total): {status}")

        if feasible:
            max_feasible = students_per_path

    print(f"\n{'=' * 70}")
    print(f"MAXIMUM FEASIBLE ENROLLMENT: {max_feasible} students per path")
    print(f"                             ({max_feasible * 3} total students)")
    print(f"{'=' * 70}")

    return max_feasible


def detailed_feasibility_check(students_per_path: int):
    """
    Perform detailed feasibility check for a specific enrollment level.
    """
    paths = get_all_paths()

    print(f"\n{'=' * 70}")
    print(f"DETAILED FEASIBILITY CHECK: {students_per_path} students per path")
    print(f"{'=' * 70}")

    # Calculate sections needed by course
    course_sections = defaultdict(int)
    for path_type, path_plan in paths.items():
        for year_plan in path_plan.year_plans:
            for code in set(year_plan.semester1_courses):
                sections = math.ceil(students_per_path / MAX_CLASS_SIZE)
                course_sections[code] += sections

    # Aggregate by room type
    room_sections = defaultdict(int)
    room_courses = defaultdict(list)

    for code, sections in course_sections.items():
        course = COURSE_CATALOG.get(code)
        if course:
            room_sections[course.room_type_required] += sections
            room_courses[course.room_type_required].append((code, course.name, sections))

    print("\nSections needed by room type:")
    print("-" * 60)

    all_feasible = True
    for room_type in RoomType:
        if room_type in room_sections:
            needed = room_sections[room_type]
            available = ACTUAL_ROOMS.get(room_type, 0) * PERIODS_PER_DAY
            status = "✓" if needed <= available else "✗ OVERFLOW"
            if needed > available:
                all_feasible = False

            print(f"\n{room_type.name.replace('_', ' ').title()}:")
            print(f"  Sections needed: {needed}, Available periods: {available} {status}")
            print(f"  Courses:")
            for code, name, sects in room_courses[room_type]:
                print(f"    - {name}: {sects} section(s)")

    # Calculate teachers needed
    print("\n" + "-" * 60)
    print("Teachers needed:")

    calculator = ResourceCalculator(
        students_per_path={p: students_per_path for p in GraduationPath},
        max_class_size=MAX_CLASS_SIZE,
        periods_per_day=PERIODS_PER_DAY
    )
    min_teachers = calculator.calculate_min_teachers()

    total_teachers = 0
    for subject, info in min_teachers.items():
        if info["total"] > 0:
            ap_note = f" ({info['ap_qualified']} AP-qualified)" if info["ap_qualified"] > 0 else ""
            print(f"  {subject.name.replace('_', ' ').title()}: {info['total']}{ap_note}")
            total_teachers += info["total"]

    print(f"\n  TOTAL TEACHERS: {total_teachers}")

    return all_feasible


def main():
    """Run capacity analysis."""
    analyze_room_demand_per_student()
    max_enrollment = calculate_max_enrollment()
    detailed_feasibility_check(max_enrollment)

    # Also check if 15 per path is feasible
    print("\n")
    detailed_feasibility_check(15)


if __name__ == "__main__":
    main()
