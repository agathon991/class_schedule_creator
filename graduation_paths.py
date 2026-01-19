"""
Graduation paths for the high school.
Defines the course requirements for each graduation track.
"""

from dataclasses import dataclass, field
from models import GraduationPath
from course_catalog import COURSE_CATALOG


@dataclass
class YearPlan:
    """Courses planned for a specific year."""
    year: int  # 1=Freshman, 2=Sophomore, 3=Junior, 4=Senior
    semester1_courses: list[str]  # Course codes
    semester2_courses: list[str]  # Course codes (usually same for year-long courses)

    def get_all_courses(self) -> list[str]:
        """Get all unique courses for this year."""
        return list(set(self.semester1_courses + self.semester2_courses))


@dataclass
class GraduationPathPlan:
    """Complete 4-year plan for a graduation path."""
    path: GraduationPath
    description: str
    year_plans: list[YearPlan]
    total_credits: int = 0

    def __post_init__(self):
        self.total_credits = self._calculate_credits()

    def _calculate_credits(self) -> int:
        """Calculate total credits for this path."""
        total = 0
        for year_plan in self.year_plans:
            for code in year_plan.get_all_courses():
                if code in COURSE_CATALOG:
                    total += COURSE_CATALOG[code].credits
        return total


def create_minimum_path() -> GraduationPathPlan:
    """
    Minimum Requirements Path (No AP courses)
    Meets UC/CSU A-G requirements with no AP courses.

    Requirements satisfied:
    - A: History/Social Science - 2 years (World History + US History + Govt + Econ)
    - B: English - 4 years
    - C: Mathematics - 3 years (Algebra 1, Geometry, Algebra 2)
    - D: Lab Science - 2 years (Biology, Chemistry)
    - E: Language Other - 2 years (Arabic 1, Arabic 2)
    - F: Visual/Performing Arts - 1 year (Art 1)
    - G: College-Prep Elective - 1 year (covered by additional Arabic)
    - PE: 2 years (state requirement)
    - Religious Studies: 4 years (school requirement)
    """
    year_plans = [
        # Freshman Year (Grade 9) - 6 classes per semester
        YearPlan(
            year=1,
            semester1_courses=["ENG9", "ALG1", "BIO", "ARAB1", "PE9", "REL1"],
            semester2_courses=["ENG9", "ALG1", "BIO", "ARAB1", "PE9", "REL1"]
        ),
        # Sophomore Year (Grade 10) - 6 classes per semester
        YearPlan(
            year=2,
            semester1_courses=["ENG10", "GEOM", "CHEM", "ARAB2", "PE10", "REL2"],
            semester2_courses=["ENG10", "GEOM", "CHEM", "ARAB2", "PE10", "REL2"]
        ),
        # Junior Year (Grade 11) - 6 classes per semester
        YearPlan(
            year=3,
            semester1_courses=["ENG11", "ALG2", "WHIST", "ART1", "ARAB3", "REL3"],
            semester2_courses=["ENG11", "ALG2", "WHIST", "ART1", "ARAB3", "REL3"]
        ),
        # Senior Year (Grade 12) - 6 classes per semester
        # Govt and Econ are 1-semester courses
        YearPlan(
            year=4,
            semester1_courses=["ENG12", "PRECALC", "USHIST", "GOVT", "ARAB4", "REL4"],
            semester2_courses=["ENG12", "PRECALC", "USHIST", "ECON", "ARAB4", "REL4"]
        ),
    ]

    return GraduationPathPlan(
        path=GraduationPath.MINIMUM,
        description="Minimum graduation requirements meeting UC/CSU A-G eligibility. "
                    "No AP courses. Recommended for students seeking a balanced workload.",
        year_plans=year_plans
    )


def create_premed_path() -> GraduationPathPlan:
    """
    Pre-Medical Track
    Optimized for medical school admissions with strong science and math foundation.

    Key AP courses:
    - AP Biology (essential for pre-med)
    - AP Chemistry (essential for pre-med)
    - AP Calculus AB (required for medical schools)
    - AP Psychology (useful for MCAT)
    - AP English Language/Literature (strong communication skills)

    This path exceeds minimum requirements with:
    - 4 years of math (through AP Calculus)
    - 3+ years of lab science (Bio, Chem, AP Bio, AP Chem)
    - Strong GPA-focused AP selection
    """
    year_plans = [
        # Freshman Year (Grade 9) - Build strong foundation
        YearPlan(
            year=1,
            semester1_courses=["ENG9", "ALG1", "BIO", "ARAB1", "PE9", "REL1"],
            semester2_courses=["ENG9", "ALG1", "BIO", "ARAB1", "PE9", "REL1"]
        ),
        # Sophomore Year (Grade 10) - Continue foundation, start Chemistry
        YearPlan(
            year=2,
            semester1_courses=["ENG10", "GEOM", "CHEM", "WHIST", "ARAB2", "REL2"],
            semester2_courses=["ENG10", "GEOM", "CHEM", "WHIST", "PE10", "REL2"]
        ),
        # Junior Year (Grade 11) - AP Sciences begin
        YearPlan(
            year=3,
            semester1_courses=["ENG11-AP", "ALG2", "BIO-AP", "USHIST", "ART1", "REL3"],
            semester2_courses=["ENG11-AP", "ALG2", "BIO-AP", "USHIST", "ART1", "REL3"]
        ),
        # Senior Year (Grade 12) - Peak AP load
        YearPlan(
            year=4,
            semester1_courses=["ENG12-AP", "CALC-AP-AB", "CHEM-AP", "PSYCH-AP", "GOVT", "REL4"],
            semester2_courses=["ENG12-AP", "CALC-AP-AB", "CHEM-AP", "PSYCH-AP", "ECON", "REL4"]
        ),
    ]

    return GraduationPathPlan(
        path=GraduationPath.PRE_MED,
        description="Pre-Medical Track optimized for medical school preparation. "
                    "Includes AP Biology, AP Chemistry, AP Calculus, and AP Psychology. "
                    "Strong foundation for MCAT preparation.",
        year_plans=year_plans
    )


def create_engineering_path() -> GraduationPathPlan:
    """
    Engineering Track (Computer Science, Computer Engineering, Chemical Engineering)
    Optimized for engineering and CS undergraduate programs.

    Key AP courses:
    - AP Computer Science Principles (intro to CS)
    - AP Computer Science A (programming in Java)
    - AP Calculus AB (essential for engineering)
    - AP Physics 1 (algebra-based physics)
    - AP Chemistry (for Chemical Engineering)

    This path includes:
    - 4 years of math (through AP Calculus)
    - Strong CS foundation
    - Robotics experience
    - Physics and Chemistry for engineering foundations
    """
    year_plans = [
        # Freshman Year (Grade 9) - Foundation + intro to CS
        YearPlan(
            year=1,
            semester1_courses=["ENG9", "ALG1", "BIO", "CSP-AP", "PE9", "REL1"],
            semester2_courses=["ENG9", "ALG1", "BIO", "CSP-AP", "PE9", "REL1"]
        ),
        # Sophomore Year (Grade 10) - Math + CS progression
        YearPlan(
            year=2,
            semester1_courses=["ENG10", "GEOM", "CHEM", "CSA-AP", "ARAB1", "REL2"],
            semester2_courses=["ENG10", "GEOM", "CHEM", "CSA-AP", "PE10", "REL2"]
        ),
        # Junior Year (Grade 11) - AP Sciences + Robotics
        YearPlan(
            year=3,
            semester1_courses=["ENG11", "ALG2", "PHYS-AP-1", "ROBOTICS", "ARAB2", "REL3"],
            semester2_courses=["ENG11", "ALG2", "PHYS-AP-1", "ROBOTICS", "WHIST", "REL3"]
        ),
        # Senior Year (Grade 12) - Calculus + Advanced work
        YearPlan(
            year=4,
            semester1_courses=["ENG12", "CALC-AP-AB", "CHEM-AP", "ROBOTICS-ADV", "GOVT", "REL4"],
            semester2_courses=["ENG12", "CALC-AP-AB", "CHEM-AP", "USHIST", "ECON", "REL4"]
        ),
    ]

    return GraduationPathPlan(
        path=GraduationPath.ENGINEERING,
        description="Engineering Track for Computer Science, Computer Engineering, "
                    "and Chemical Engineering pathways. Includes AP CS Principles, "
                    "AP CS A, AP Physics 1, AP Chemistry, AP Calculus, and Robotics.",
        year_plans=year_plans
    )


def get_all_paths() -> dict[GraduationPath, GraduationPathPlan]:
    """Get all graduation path plans."""
    return {
        GraduationPath.MINIMUM: create_minimum_path(),
        GraduationPath.PRE_MED: create_premed_path(),
        GraduationPath.ENGINEERING: create_engineering_path(),
    }


def get_all_required_courses() -> set[str]:
    """Get all unique courses required across all graduation paths."""
    all_courses = set()
    for path_plan in get_all_paths().values():
        for year_plan in path_plan.year_plans:
            all_courses.update(year_plan.get_all_courses())
    return all_courses


def print_path_summary(path_plan: GraduationPathPlan):
    """Print a summary of a graduation path."""
    print(f"\n{'='*70}")
    print(f"GRADUATION PATH: {path_plan.path.value}")
    print(f"{'='*70}")
    print(f"\n{path_plan.description}\n")

    for year_plan in path_plan.year_plans:
        grade = 8 + year_plan.year  # Convert year 1-4 to grade 9-12
        year_names = {1: "Freshman", 2: "Sophomore", 3: "Junior", 4: "Senior"}
        print(f"\n{year_names[year_plan.year]} Year (Grade {grade})")
        print("-" * 40)

        # Get year-long courses (in both semesters)
        year_long = set(year_plan.semester1_courses) & set(year_plan.semester2_courses)
        sem1_only = set(year_plan.semester1_courses) - year_long
        sem2_only = set(year_plan.semester2_courses) - year_long

        print("Year-long courses:")
        for code in sorted(year_long):
            course = COURSE_CATALOG.get(code)
            if course:
                level_str = f" ({course.level.value})" if course.level.value != "Regular" else ""
                print(f"  - {course.name}{level_str}")

        if sem1_only:
            print("Semester 1 only:")
            for code in sorted(sem1_only):
                course = COURSE_CATALOG.get(code)
                if course:
                    print(f"  - {course.name}")

        if sem2_only:
            print("Semester 2 only:")
            for code in sorted(sem2_only):
                course = COURSE_CATALOG.get(code)
                if course:
                    print(f"  - {course.name}")


if __name__ == "__main__":
    paths = get_all_paths()
    for path_plan in paths.values():
        print_path_summary(path_plan)

    print("\n" + "=" * 70)
    print("ALL REQUIRED COURSES ACROSS PATHS")
    print("=" * 70)
    all_courses = get_all_required_courses()
    print(f"Total unique courses needed: {len(all_courses)}")
    for code in sorted(all_courses):
        course = COURSE_CATALOG.get(code)
        if course:
            print(f"  {code}: {course.name}")
