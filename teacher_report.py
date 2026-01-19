#!/usr/bin/env python3
"""
Teacher assignment report - shows all teachers and their course assignments.
"""

from collections import defaultdict
from models import GraduationPath, SubjectArea, CourseLevel
from course_catalog import COURSE_CATALOG
from graduation_paths import get_all_paths
from resource_calculator import ResourceCalculator


def generate_teacher_report(students_per_path: int = 25):
    """Generate a detailed teacher assignment report."""

    paths = get_all_paths()

    # Calculate sections needed for each course
    course_sections = defaultdict(int)
    course_years = defaultdict(set)  # Track which years each course is taught

    for path_type, path_plan in paths.items():
        for year_plan in path_plan.year_plans:
            for code in set(year_plan.semester1_courses):
                sections = 1  # At least 1 section per path
                course_sections[code] = max(course_sections[code], 3)  # 3 paths = up to 3 sections
                course_years[code].add(year_plan.year)

    # Group courses by subject area
    subject_courses = defaultdict(list)
    for code, sections in course_sections.items():
        course = COURSE_CATALOG.get(code)
        if course:
            subject_courses[course.subject_area].append({
                'code': code,
                'name': course.name,
                'level': course.level,
                'sections': sections,
                'years': sorted(course_years[code])
            })

    # Define teacher assignments
    print("=" * 80)
    print("TEACHER ASSIGNMENTS AND COURSE LOAD")
    print("=" * 80)
    print(f"\nBased on {students_per_path} students per graduation path ({students_per_path * 3} total)")
    print("Each teacher teaches up to 5 periods per day (1 planning period)\n")

    year_names = {1: "9th", 2: "10th", 3: "11th", 4: "12th"}

    # Process each subject area
    teacher_assignments = {}

    # =========================================================================
    # ENGLISH (3 teachers, 1 AP-qualified)
    # =========================================================================
    print("\n" + "─" * 80)
    print("ENGLISH DEPARTMENT (3 teachers)")
    print("─" * 80)

    print("\n📚 English Teacher 1 (AP-qualified)")
    print("   Courses:")
    print("   • AP English Language (11th grade) - 1 section")
    print("   • AP English Literature (12th grade) - 1 section")
    print("   • English 11 (11th grade) - 1 section")
    print("   • English 12 (12th grade) - 1 section")
    print("   Total: 4 sections/day")

    print("\n📚 English Teacher 2")
    print("   Courses:")
    print("   • English 9 (9th grade) - 3 sections")
    print("   • English 10 (10th grade) - 2 sections")
    print("   Total: 5 sections/day")

    print("\n📚 English Teacher 3")
    print("   Courses:")
    print("   • English 10 (10th grade) - 1 section")
    print("   • English 11 (11th grade) - 1 section")
    print("   • English 12 (12th grade) - 1 section")
    print("   Total: 3 sections/day")

    # =========================================================================
    # MATHEMATICS (3 teachers, 1 AP-qualified)
    # =========================================================================
    print("\n" + "─" * 80)
    print("MATHEMATICS DEPARTMENT (3 teachers)")
    print("─" * 80)

    print("\n📐 Math Teacher 1 (AP-qualified)")
    print("   Courses:")
    print("   • AP Calculus AB (11th-12th grade) - 2 sections")
    print("   • Pre-Calculus (12th grade) - 1 section")
    print("   • Algebra 2 (11th grade) - 2 sections")
    print("   Total: 5 sections/day")

    print("\n📐 Math Teacher 2")
    print("   Courses:")
    print("   • Algebra 1 (9th grade) - 3 sections")
    print("   • Geometry (10th grade) - 2 sections")
    print("   Total: 5 sections/day")

    print("\n📐 Math Teacher 3")
    print("   Courses:")
    print("   • Geometry (10th grade) - 1 section")
    print("   • Algebra 2 (11th grade) - 1 section")
    print("   Total: 2 sections/day")

    # =========================================================================
    # LABORATORY SCIENCE (2 teachers, 1 AP-qualified)
    # =========================================================================
    print("\n" + "─" * 80)
    print("SCIENCE DEPARTMENT (2 teachers)")
    print("─" * 80)

    print("\n🔬 Science Teacher 1 (AP-qualified)")
    print("   Courses:")
    print("   • AP Biology (11th-12th grade) - 1 section")
    print("   • AP Chemistry (12th grade) - 2 sections")
    print("   • AP Physics 1 (11th-12th grade) - 1 section")
    print("   Total: 4 sections/day")
    print("   Room: Chemistry Lab, Biology Lab")

    print("\n🔬 Science Teacher 2")
    print("   Courses:")
    print("   • Biology (9th grade) - 3 sections")
    print("   • Chemistry (10th grade) - 3 sections")
    print("   Total: 6 sections/day (may need adjustment)")
    print("   Room: Chemistry Lab, Biology Lab")

    # =========================================================================
    # HISTORY/SOCIAL SCIENCE (3 teachers)
    # =========================================================================
    print("\n" + "─" * 80)
    print("HISTORY/SOCIAL SCIENCE DEPARTMENT (3 teachers)")
    print("─" * 80)

    print("\n📜 History Teacher 1")
    print("   Courses:")
    print("   • World History (10th-11th grade) - 2 sections")
    print("   • US History (11th-12th grade) - 2 sections")
    print("   Total: 4 sections/day")

    print("\n📜 History Teacher 2")
    print("   Courses:")
    print("   • US Government (12th grade, Sem 1) - 3 sections")
    print("   • Economics (12th grade, Sem 2) - 3 sections")
    print("   Total: 3 sections/semester")

    print("\n📜 History Teacher 3")
    print("   Courses:")
    print("   • World History (10th grade) - 1 section")
    print("   • US History (11th grade) - 1 section")
    print("   Total: 2 sections/day")

    # =========================================================================
    # WORLD LANGUAGES - ARABIC (2 teachers)
    # =========================================================================
    print("\n" + "─" * 80)
    print("ARABIC DEPARTMENT (2 teachers)")
    print("─" * 80)

    print("\n🌍 Arabic Teacher 1")
    print("   Courses:")
    print("   • Arabic 1 (9th-10th grade) - 3 sections")
    print("   • Arabic 2 (10th-11th grade) - 2 sections")
    print("   Total: 5 sections/day")

    print("\n🌍 Arabic Teacher 2")
    print("   Courses:")
    print("   • Arabic 2 (10th-11th grade) - 1 section")
    print("   • Arabic 3 (11th grade) - 1 section")
    print("   • Arabic 4 (12th grade) - 1 section")
    print("   Total: 3 sections/day")

    # =========================================================================
    # RELIGIOUS STUDIES (3 teachers)
    # Islamic Studies & Quran is ONE year-long course per grade:
    #   Semester 1: Islamic Studies focus
    #   Semester 2: Quran focus
    # =========================================================================
    print("\n" + "─" * 80)
    print("RELIGIOUS STUDIES DEPARTMENT (3 teachers)")
    print("─" * 80)
    print("\n   Note: Each course is year-long with Islamic Studies (Sem 1) + Quran (Sem 2)")

    print("\n🕌 Religious Studies Teacher 1")
    print("   Courses:")
    print("   • Religious Studies 1 (9th grade) - 3 sections")
    print("   • Religious Studies 2 (10th grade) - 2 sections")
    print("   Total: 5 sections/day (full load)")

    print("\n🕌 Religious Studies Teacher 2")
    print("   Courses:")
    print("   • Religious Studies 2 (10th grade) - 1 section")
    print("   • Religious Studies 3 (11th grade) - 3 sections")
    print("   Total: 4 sections/day")

    print("\n🕌 Religious Studies Teacher 3")
    print("   Courses:")
    print("   • Religious Studies 4 (12th grade) - 3 sections")
    print("   Total: 3 sections/day")

    # =========================================================================
    # PHYSICAL EDUCATION (2 teachers)
    # =========================================================================
    print("\n" + "─" * 80)
    print("PHYSICAL EDUCATION DEPARTMENT (2 teachers)")
    print("─" * 80)

    print("\n🏃 PE Teacher 1")
    print("   Courses:")
    print("   • Physical Education 9 (9th grade) - 3 sections")
    print("   Total: 3 sections/day")
    print("   Room: Gymnasium")

    print("\n🏃 PE Teacher 2")
    print("   Courses:")
    print("   • Physical Education 10 (10th grade) - 1 section")
    print("   Total: 1 section/day (part-time or combined duties)")
    print("   Room: Gymnasium")

    # =========================================================================
    # VISUAL/PERFORMING ARTS (1 teacher)
    # =========================================================================
    print("\n" + "─" * 80)
    print("ARTS DEPARTMENT (1 teacher)")
    print("─" * 80)

    print("\n🎨 Art Teacher 1")
    print("   Courses:")
    print("   • Art 1 (11th grade) - 2 sections")
    print("   Total: 2 sections/day (part-time possible)")
    print("   Room: General classroom")

    # =========================================================================
    # COMPUTER SCIENCE / ROBOTICS (1 teacher, AP-qualified)
    # =========================================================================
    print("\n" + "─" * 80)
    print("TECHNOLOGY DEPARTMENT (1 teacher)")
    print("─" * 80)

    print("\n💻 CS/Robotics Teacher 1 (AP-qualified)")
    print("   Courses:")
    print("   • AP Computer Science Principles (9th grade) - 1 section")
    print("   • AP Computer Science A (10th grade) - 1 section")
    print("   • Robotics (11th grade) - 1 section")
    print("   • Advanced Robotics (12th grade) - 1 section")
    print("   • AP Psychology (12th grade) - 1 section")
    print("   Total: 5 sections/day")
    print("   Room: Computer Lab, Robotics Lab, General classroom")

    # =========================================================================
    # SUMMARY
    # =========================================================================
    print("\n" + "=" * 80)
    print("SUMMARY BY DEPARTMENT")
    print("=" * 80)

    summary = [
        ("English", 3, 1, "ENG9, ENG10, ENG11, ENG12, AP Eng Lang, AP Eng Lit"),
        ("Mathematics", 3, 1, "ALG1, GEOM, ALG2, PRECALC, AP Calc AB"),
        ("Science", 2, 1, "BIO, CHEM, AP Bio, AP Chem, AP Physics 1"),
        ("History/Social Science", 3, 0, "World Hist, US Hist, Govt, Econ"),
        ("Arabic", 2, 0, "Arabic 1, 2, 3, 4"),
        ("Religious Studies", 3, 0, "REL 1-4 (Islamic Studies + Quran)"),
        ("Physical Education", 2, 0, "PE 9, PE 10"),
        ("Arts", 1, 0, "Art 1"),
        ("Technology", 1, 1, "AP CSP, AP CSA, Robotics, Adv Robotics, AP Psych"),
    ]

    print(f"\n{'Department':<25} {'Teachers':<10} {'AP-Qual':<10} {'Courses'}")
    print("─" * 80)
    total_teachers = 0
    total_ap = 0
    for dept, teachers, ap, courses in summary:
        print(f"{dept:<25} {teachers:<10} {ap:<10} {courses}")
        total_teachers += teachers
        total_ap += ap
    print("─" * 80)
    print(f"{'TOTAL':<25} {total_teachers:<10} {total_ap:<10}")

    print("\n" + "=" * 80)
    print("COURSE OFFERINGS BY GRADE LEVEL")
    print("=" * 80)

    grade_courses = {
        9: ["English 9", "Algebra 1", "Biology", "Arabic 1", "PE 9",
            "Religious Studies 1 (Islamic Studies/Quran)", "AP CS Principles*"],
        10: ["English 10", "Geometry", "Chemistry", "World History",
             "Arabic 1/2", "PE 10", "Religious Studies 2 (Islamic Studies/Quran)",
             "AP CS A*"],
        11: ["English 11 / AP English Lang", "Algebra 2", "AP Biology*",
             "World History / US History", "Arabic 2/3", "Art 1",
             "Religious Studies 3 (Islamic Studies/Quran)", "AP Physics 1*", "Robotics*"],
        12: ["English 12 / AP English Lit", "Pre-Calc / AP Calculus AB",
             "AP Chemistry*", "US History", "Government", "Economics",
             "Arabic 3/4", "Religious Studies 4 (Islamic Studies/Quran)",
             "AP Psychology*", "Advanced Robotics*"]
    }

    for grade, courses in grade_courses.items():
        print(f"\n📖 Grade {grade}:")
        for course in courses:
            ap_marker = " [AP]" if course.endswith("*") else ""
            course_name = course.rstrip("*")
            print(f"   • {course_name}{ap_marker}")


if __name__ == "__main__":
    generate_teacher_report(students_per_path=25)
