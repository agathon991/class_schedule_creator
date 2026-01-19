"""
Course catalog for the high school.
Defines all available courses organized by subject area and level.
"""

from models import (
    Course, SubjectArea, RoomType, CourseLevel, GraduationPath
)


def create_course_catalog() -> dict[str, Course]:
    """Create and return the complete course catalog."""
    courses = {}

    # =========================================================================
    # A) HISTORY / SOCIAL SCIENCE (2 years required for A-G)
    # =========================================================================

    # World History (typically 10th grade)
    courses["WHIST"] = Course(
        code="WHIST",
        name="World History",
        subject_area=SubjectArea.HISTORY_SOCIAL_SCIENCE,
        credits=10,
        semesters=2,
        grade_levels=[10],
        description="World history, cultures, and geography"
    )

    courses["WHIST-AP"] = Course(
        code="WHIST-AP",
        name="AP World History",
        subject_area=SubjectArea.HISTORY_SOCIAL_SCIENCE,
        level=CourseLevel.AP,
        credits=10,
        semesters=2,
        grade_levels=[10],
        description="Advanced Placement World History"
    )

    # US History (typically 11th grade)
    courses["USHIST"] = Course(
        code="USHIST",
        name="US History",
        subject_area=SubjectArea.HISTORY_SOCIAL_SCIENCE,
        credits=10,
        semesters=2,
        grade_levels=[11],
        description="United States History"
    )

    courses["USHIST-AP"] = Course(
        code="USHIST-AP",
        name="AP US History",
        subject_area=SubjectArea.HISTORY_SOCIAL_SCIENCE,
        level=CourseLevel.AP,
        credits=10,
        semesters=2,
        grade_levels=[11],
        description="Advanced Placement US History"
    )

    # Government (typically 12th grade, 1 semester)
    courses["GOVT"] = Course(
        code="GOVT",
        name="US Government",
        subject_area=SubjectArea.HISTORY_SOCIAL_SCIENCE,
        credits=5,
        semesters=1,
        grade_levels=[12],
        description="American Government and Civics"
    )

    courses["GOVT-AP"] = Course(
        code="GOVT-AP",
        name="AP US Government",
        subject_area=SubjectArea.HISTORY_SOCIAL_SCIENCE,
        level=CourseLevel.AP,
        credits=5,
        semesters=1,
        grade_levels=[12],
        description="Advanced Placement US Government"
    )

    # Economics (typically 12th grade, 1 semester)
    courses["ECON"] = Course(
        code="ECON",
        name="Economics",
        subject_area=SubjectArea.HISTORY_SOCIAL_SCIENCE,
        credits=5,
        semesters=1,
        grade_levels=[12],
        description="Principles of Economics"
    )

    # =========================================================================
    # B) ENGLISH (4 years required for A-G)
    # =========================================================================

    courses["ENG9"] = Course(
        code="ENG9",
        name="English 9",
        subject_area=SubjectArea.ENGLISH,
        credits=10,
        semesters=2,
        grade_levels=[9],
        description="Freshman English"
    )

    courses["ENG10"] = Course(
        code="ENG10",
        name="English 10",
        subject_area=SubjectArea.ENGLISH,
        credits=10,
        semesters=2,
        grade_levels=[10],
        prerequisites=["ENG9"],
        description="Sophomore English"
    )

    courses["ENG11"] = Course(
        code="ENG11",
        name="English 11",
        subject_area=SubjectArea.ENGLISH,
        credits=10,
        semesters=2,
        grade_levels=[11],
        prerequisites=["ENG10"],
        description="Junior English"
    )

    courses["ENG11-AP"] = Course(
        code="ENG11-AP",
        name="AP English Language",
        subject_area=SubjectArea.ENGLISH,
        level=CourseLevel.AP,
        credits=10,
        semesters=2,
        grade_levels=[11],
        prerequisites=["ENG10"],
        description="AP English Language and Composition"
    )

    courses["ENG12"] = Course(
        code="ENG12",
        name="English 12",
        subject_area=SubjectArea.ENGLISH,
        credits=10,
        semesters=2,
        grade_levels=[12],
        prerequisites=["ENG11"],
        description="Senior English"
    )

    courses["ENG12-AP"] = Course(
        code="ENG12-AP",
        name="AP English Literature",
        subject_area=SubjectArea.ENGLISH,
        level=CourseLevel.AP,
        credits=10,
        semesters=2,
        grade_levels=[12],
        prerequisites=["ENG11"],
        description="AP English Literature and Composition"
    )

    # =========================================================================
    # C) MATHEMATICS (3 years required, 4 recommended for A-G)
    # =========================================================================

    courses["ALG1"] = Course(
        code="ALG1",
        name="Algebra 1",
        subject_area=SubjectArea.MATHEMATICS,
        credits=10,
        semesters=2,
        grade_levels=[9],
        description="Elementary Algebra"
    )

    courses["GEOM"] = Course(
        code="GEOM",
        name="Geometry",
        subject_area=SubjectArea.MATHEMATICS,
        credits=10,
        semesters=2,
        grade_levels=[9, 10],
        prerequisites=["ALG1"],
        description="Euclidean Geometry"
    )

    courses["ALG2"] = Course(
        code="ALG2",
        name="Algebra 2",
        subject_area=SubjectArea.MATHEMATICS,
        credits=10,
        semesters=2,
        grade_levels=[10, 11],
        prerequisites=["GEOM"],
        description="Advanced Algebra"
    )

    courses["PRECALC"] = Course(
        code="PRECALC",
        name="Pre-Calculus",
        subject_area=SubjectArea.MATHEMATICS,
        credits=10,
        semesters=2,
        grade_levels=[11, 12],
        prerequisites=["ALG2"],
        description="Pre-Calculus with Trigonometry"
    )

    courses["CALC-AP-AB"] = Course(
        code="CALC-AP-AB",
        name="AP Calculus AB",
        subject_area=SubjectArea.MATHEMATICS,
        level=CourseLevel.AP,
        credits=10,
        semesters=2,
        grade_levels=[11, 12],
        prerequisites=["PRECALC"],
        description="AP Calculus AB"
    )

    courses["CALC-AP-BC"] = Course(
        code="CALC-AP-BC",
        name="AP Calculus BC",
        subject_area=SubjectArea.MATHEMATICS,
        level=CourseLevel.AP,
        credits=10,
        semesters=2,
        grade_levels=[12],
        prerequisites=["CALC-AP-AB"],
        description="AP Calculus BC"
    )

    courses["STATS-AP"] = Course(
        code="STATS-AP",
        name="AP Statistics",
        subject_area=SubjectArea.MATHEMATICS,
        level=CourseLevel.AP,
        credits=10,
        semesters=2,
        grade_levels=[11, 12],
        prerequisites=["ALG2"],
        description="AP Statistics"
    )

    # =========================================================================
    # D) LABORATORY SCIENCE (2 years required, 3 recommended for A-G)
    # =========================================================================

    courses["BIO"] = Course(
        code="BIO",
        name="Biology",
        subject_area=SubjectArea.LABORATORY_SCIENCE,
        credits=10,
        semesters=2,
        room_type_required=RoomType.BIOLOGY_LAB,
        grade_levels=[9, 10],
        description="Introductory Biology with Lab"
    )

    courses["BIO-AP"] = Course(
        code="BIO-AP",
        name="AP Biology",
        subject_area=SubjectArea.LABORATORY_SCIENCE,
        level=CourseLevel.AP,
        credits=10,
        semesters=2,
        room_type_required=RoomType.BIOLOGY_LAB,
        grade_levels=[11, 12],
        prerequisites=["BIO", "CHEM"],
        description="AP Biology"
    )

    courses["CHEM"] = Course(
        code="CHEM",
        name="Chemistry",
        subject_area=SubjectArea.LABORATORY_SCIENCE,
        credits=10,
        semesters=2,
        room_type_required=RoomType.CHEMISTRY_LAB,
        grade_levels=[10, 11],
        prerequisites=["ALG1"],
        description="Introductory Chemistry with Lab"
    )

    courses["CHEM-AP"] = Course(
        code="CHEM-AP",
        name="AP Chemistry",
        subject_area=SubjectArea.LABORATORY_SCIENCE,
        level=CourseLevel.AP,
        credits=10,
        semesters=2,
        room_type_required=RoomType.CHEMISTRY_LAB,
        grade_levels=[11, 12],
        prerequisites=["CHEM", "ALG2"],
        description="AP Chemistry"
    )

    courses["PHYS"] = Course(
        code="PHYS",
        name="Physics",
        subject_area=SubjectArea.LABORATORY_SCIENCE,
        credits=10,
        semesters=2,
        room_type_required=RoomType.BIOLOGY_LAB,  # Can use science lab
        grade_levels=[11, 12],
        prerequisites=["ALG2"],
        description="Introductory Physics with Lab"
    )

    courses["PHYS-AP-1"] = Course(
        code="PHYS-AP-1",
        name="AP Physics 1",
        subject_area=SubjectArea.LABORATORY_SCIENCE,
        level=CourseLevel.AP,
        credits=10,
        semesters=2,
        room_type_required=RoomType.BIOLOGY_LAB,
        grade_levels=[11, 12],
        prerequisites=["GEOM"],
        description="AP Physics 1: Algebra-Based"
    )

    courses["PHYS-AP-C"] = Course(
        code="PHYS-AP-C",
        name="AP Physics C",
        subject_area=SubjectArea.LABORATORY_SCIENCE,
        level=CourseLevel.AP,
        credits=10,
        semesters=2,
        room_type_required=RoomType.BIOLOGY_LAB,
        grade_levels=[12],
        prerequisites=["PHYS", "CALC-AP-AB"],
        description="AP Physics C: Mechanics"
    )

    courses["ENVSCI-AP"] = Course(
        code="ENVSCI-AP",
        name="AP Environmental Science",
        subject_area=SubjectArea.LABORATORY_SCIENCE,
        level=CourseLevel.AP,
        credits=10,
        semesters=2,
        room_type_required=RoomType.BIOLOGY_LAB,
        grade_levels=[11, 12],
        prerequisites=["BIO"],
        description="AP Environmental Science"
    )

    # =========================================================================
    # E) LANGUAGE OTHER THAN ENGLISH (2 years required, 3 recommended)
    # Arabic counts for this requirement
    # =========================================================================

    courses["ARAB1"] = Course(
        code="ARAB1",
        name="Arabic 1",
        subject_area=SubjectArea.LANGUAGE_OTHER,
        credits=10,
        semesters=2,
        grade_levels=[9, 10, 11, 12],
        description="Beginning Arabic Language"
    )

    courses["ARAB2"] = Course(
        code="ARAB2",
        name="Arabic 2",
        subject_area=SubjectArea.LANGUAGE_OTHER,
        credits=10,
        semesters=2,
        grade_levels=[9, 10, 11, 12],
        prerequisites=["ARAB1"],
        description="Intermediate Arabic Language"
    )

    courses["ARAB3"] = Course(
        code="ARAB3",
        name="Arabic 3",
        subject_area=SubjectArea.LANGUAGE_OTHER,
        credits=10,
        semesters=2,
        grade_levels=[10, 11, 12],
        prerequisites=["ARAB2"],
        description="Advanced Arabic Language"
    )

    courses["ARAB4"] = Course(
        code="ARAB4",
        name="Arabic 4",
        subject_area=SubjectArea.LANGUAGE_OTHER,
        credits=10,
        semesters=2,
        grade_levels=[11, 12],
        prerequisites=["ARAB3"],
        description="Advanced Arabic Language and Literature"
    )

    # =========================================================================
    # F) VISUAL AND PERFORMING ARTS (1 year required for A-G)
    # =========================================================================

    courses["ART1"] = Course(
        code="ART1",
        name="Art 1",
        subject_area=SubjectArea.VISUAL_PERFORMING_ARTS,
        credits=10,
        semesters=2,
        room_type_required=RoomType.GENERAL,  # Uses general classroom
        grade_levels=[9, 10, 11, 12],
        description="Introduction to Visual Arts"
    )

    courses["ART2"] = Course(
        code="ART2",
        name="Art 2",
        subject_area=SubjectArea.VISUAL_PERFORMING_ARTS,
        credits=10,
        semesters=2,
        room_type_required=RoomType.GENERAL,  # Uses general classroom
        grade_levels=[10, 11, 12],
        prerequisites=["ART1"],
        description="Intermediate Visual Arts"
    )

    courses["MUSIC1"] = Course(
        code="MUSIC1",
        name="Music",
        subject_area=SubjectArea.VISUAL_PERFORMING_ARTS,
        credits=10,
        semesters=2,
        room_type_required=RoomType.GENERAL,  # Uses general classroom
        grade_levels=[9, 10, 11, 12],
        description="Introduction to Music"
    )

    # =========================================================================
    # G) COLLEGE-PREP ELECTIVES (1 year required for A-G)
    # =========================================================================

    courses["CSP-AP"] = Course(
        code="CSP-AP",
        name="AP Computer Science Principles",
        subject_area=SubjectArea.COLLEGE_PREP_ELECTIVE,
        level=CourseLevel.AP,
        credits=10,
        semesters=2,
        room_type_required=RoomType.COMPUTER_LAB,
        grade_levels=[9, 10, 11, 12],
        description="AP Computer Science Principles"
    )

    courses["CSA-AP"] = Course(
        code="CSA-AP",
        name="AP Computer Science A",
        subject_area=SubjectArea.COLLEGE_PREP_ELECTIVE,
        level=CourseLevel.AP,
        credits=10,
        semesters=2,
        room_type_required=RoomType.COMPUTER_LAB,
        grade_levels=[10, 11, 12],
        prerequisites=["CSP-AP"],
        description="AP Computer Science A (Java)"
    )

    courses["ROBOTICS"] = Course(
        code="ROBOTICS",
        name="Robotics",
        subject_area=SubjectArea.COLLEGE_PREP_ELECTIVE,
        credits=10,
        semesters=2,
        room_type_required=RoomType.ROBOTICS_LAB,
        grade_levels=[10, 11, 12],
        description="Introduction to Robotics"
    )

    courses["ROBOTICS-ADV"] = Course(
        code="ROBOTICS-ADV",
        name="Advanced Robotics",
        subject_area=SubjectArea.COLLEGE_PREP_ELECTIVE,
        credits=10,
        semesters=2,
        room_type_required=RoomType.ROBOTICS_LAB,
        grade_levels=[11, 12],
        prerequisites=["ROBOTICS"],
        description="Advanced Robotics and Engineering"
    )

    courses["PSYCH-AP"] = Course(
        code="PSYCH-AP",
        name="AP Psychology",
        subject_area=SubjectArea.COLLEGE_PREP_ELECTIVE,
        level=CourseLevel.AP,
        credits=10,
        semesters=2,
        grade_levels=[11, 12],
        description="AP Psychology"
    )

    # =========================================================================
    # PHYSICAL EDUCATION (State requirement - 2 years)
    # =========================================================================

    courses["PE9"] = Course(
        code="PE9",
        name="Physical Education 9",
        subject_area=SubjectArea.PHYSICAL_EDUCATION,
        credits=10,
        semesters=2,
        room_type_required=RoomType.GYM,  # Gymnasium with basketball court
        grade_levels=[9],
        description="Freshman Physical Education"
    )

    courses["PE10"] = Course(
        code="PE10",
        name="Physical Education 10",
        subject_area=SubjectArea.PHYSICAL_EDUCATION,
        credits=10,
        semesters=2,
        room_type_required=RoomType.GYM,  # Gymnasium with basketball court
        grade_levels=[10],
        prerequisites=["PE9"],
        description="Sophomore Physical Education"
    )

    # =========================================================================
    # RELIGIOUS STUDIES (School-specific requirements)
    # =========================================================================

    courses["ISLAM1"] = Course(
        code="ISLAM1",
        name="Islamic Studies 1",
        subject_area=SubjectArea.RELIGIOUS_STUDIES,
        credits=10,
        semesters=2,
        grade_levels=[9],
        description="Introduction to Islamic Studies"
    )

    courses["ISLAM2"] = Course(
        code="ISLAM2",
        name="Islamic Studies 2",
        subject_area=SubjectArea.RELIGIOUS_STUDIES,
        credits=10,
        semesters=2,
        grade_levels=[10],
        prerequisites=["ISLAM1"],
        description="Intermediate Islamic Studies"
    )

    courses["ISLAM3"] = Course(
        code="ISLAM3",
        name="Islamic Studies 3",
        subject_area=SubjectArea.RELIGIOUS_STUDIES,
        credits=10,
        semesters=2,
        grade_levels=[11],
        prerequisites=["ISLAM2"],
        description="Advanced Islamic Studies"
    )

    courses["ISLAM4"] = Course(
        code="ISLAM4",
        name="Islamic Studies 4",
        subject_area=SubjectArea.RELIGIOUS_STUDIES,
        credits=10,
        semesters=2,
        grade_levels=[12],
        prerequisites=["ISLAM3"],
        description="Senior Islamic Studies"
    )

    courses["QURAN1"] = Course(
        code="QURAN1",
        name="Quran Studies 1",
        subject_area=SubjectArea.RELIGIOUS_STUDIES,
        credits=10,
        semesters=2,
        grade_levels=[9],
        description="Introduction to Quran Studies"
    )

    courses["QURAN2"] = Course(
        code="QURAN2",
        name="Quran Studies 2",
        subject_area=SubjectArea.RELIGIOUS_STUDIES,
        credits=10,
        semesters=2,
        grade_levels=[10],
        prerequisites=["QURAN1"],
        description="Intermediate Quran Studies"
    )

    courses["QURAN3"] = Course(
        code="QURAN3",
        name="Quran Studies 3",
        subject_area=SubjectArea.RELIGIOUS_STUDIES,
        credits=10,
        semesters=2,
        grade_levels=[11],
        prerequisites=["QURAN2"],
        description="Advanced Quran Studies"
    )

    courses["QURAN4"] = Course(
        code="QURAN4",
        name="Quran Studies 4",
        subject_area=SubjectArea.RELIGIOUS_STUDIES,
        credits=10,
        semesters=2,
        grade_levels=[12],
        prerequisites=["QURAN3"],
        description="Senior Quran Studies"
    )

    return courses


# Pre-built catalog
COURSE_CATALOG = create_course_catalog()
