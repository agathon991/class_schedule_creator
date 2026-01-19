"""
Data models for the high school scheduling system.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional


class SubjectArea(Enum):
    """UC/CSU A-G subject areas plus additional categories."""
    HISTORY_SOCIAL_SCIENCE = "A"  # A requirement
    ENGLISH = "B"                  # B requirement
    MATHEMATICS = "C"              # C requirement
    LABORATORY_SCIENCE = "D"       # D requirement
    LANGUAGE_OTHER = "E"           # E requirement (Arabic counts)
    VISUAL_PERFORMING_ARTS = "F"   # F requirement
    COLLEGE_PREP_ELECTIVE = "G"    # G requirement
    PHYSICAL_EDUCATION = "PE"      # State requirement
    RELIGIOUS_STUDIES = "RS"       # School-specific (Islamic Studies, Quran)
    ELECTIVE = "ELEC"              # General electives


class RoomType(Enum):
    """Types of classrooms available."""
    GENERAL = auto()           # Standard classroom
    CHEMISTRY_LAB = auto()     # Chemistry laboratory
    BIOLOGY_LAB = auto()       # Biology/Science laboratory
    COMPUTER_LAB = auto()      # Computer lab
    ROBOTICS_LAB = auto()      # Robotics lab
    ART_ROOM = auto()          # Visual arts classroom
    GYM = auto()               # Physical education
    MUSIC_ROOM = auto()        # Music classroom


class GraduationPath(Enum):
    """Available graduation paths."""
    MINIMUM = "Minimum Requirements"
    PRE_MED = "Pre-Medical Track"
    ENGINEERING = "Engineering Track"


class CourseLevel(Enum):
    """Course difficulty levels."""
    REGULAR = "Regular"
    HONORS = "Honors"
    AP = "AP"


@dataclass
class Course:
    """Represents a course offering."""
    code: str
    name: str
    subject_area: SubjectArea
    level: CourseLevel = CourseLevel.REGULAR
    credits: int = 10  # 10 credits = 1 semester course (5 credits per semester)
    semesters: int = 2  # Duration in semesters (1 = half year, 2 = full year)
    room_type_required: RoomType = RoomType.GENERAL
    prerequisites: list[str] = field(default_factory=list)
    grade_levels: list[int] = field(default_factory=lambda: [9, 10, 11, 12])
    is_required_for_paths: list[GraduationPath] = field(default_factory=list)
    description: str = ""

    def __hash__(self):
        return hash(self.code)

    def __eq__(self, other):
        if isinstance(other, Course):
            return self.code == other.code
        return False


@dataclass
class Classroom:
    """Represents a physical classroom."""
    id: str
    name: str
    room_type: RoomType
    capacity: int = 25

    def can_host(self, course: Course) -> bool:
        """Check if this classroom can host a given course."""
        if course.room_type_required == RoomType.GENERAL:
            return True
        return self.room_type == course.room_type_required


@dataclass
class Teacher:
    """Represents a teacher."""
    id: str
    name: str
    subject_areas: list[SubjectArea]
    can_teach_ap: bool = False
    max_periods_per_day: int = 5  # Planning period needed

    def can_teach(self, course: Course) -> bool:
        """Check if this teacher can teach a given course."""
        if course.subject_area not in self.subject_areas:
            return False
        if course.level == CourseLevel.AP and not self.can_teach_ap:
            return False
        return True


@dataclass
class TimeSlot:
    """Represents a time slot in the schedule."""
    period: int  # 1-6 for a 6-period day
    day: int     # 1-5 for Monday-Friday (same schedule each day)

    def __hash__(self):
        return hash((self.period, self.day))


@dataclass
class Section:
    """A scheduled section of a course."""
    course: Course
    teacher: Optional['Teacher']
    classroom: Optional['Classroom']
    period: int
    semester: int  # 1 or 2
    year: int      # 1-4 (freshman-senior)
    students: list[str] = field(default_factory=list)

    @property
    def is_scheduled(self) -> bool:
        return self.teacher is not None and self.classroom is not None


@dataclass
class StudentSchedule:
    """A student's complete 4-year schedule."""
    student_id: str
    graduation_path: GraduationPath
    sections_by_year: dict[int, dict[int, list[Section]]] = field(default_factory=dict)
    # Structure: {year: {semester: [sections]}}

    def add_section(self, section: Section):
        if section.year not in self.sections_by_year:
            self.sections_by_year[section.year] = {1: [], 2: []}
        self.sections_by_year[section.year][section.semester].append(section)

    def get_total_credits(self) -> int:
        total = 0
        for year_sched in self.sections_by_year.values():
            for sem_sections in year_sched.values():
                for section in sem_sections:
                    total += section.course.credits // section.course.semesters
        return total
