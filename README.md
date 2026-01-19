# High School Schedule Creator

A Python-based scheduling system for an Islamic high school in California that meets UC/CSU A-G requirements while offering specialized courses in Arabic, Islamic Studies, and Quran.

## Features

- **Three Graduation Paths**: Minimum Requirements, Pre-Medical Track, Engineering Track
- **Constraint-Based Scheduling**: Automatic conflict detection and resolution
- **Resource Optimization**: Calculates minimum classrooms and teachers needed
- **4-Year Course Planning**: Complete course sequences for each graduation path
- **California A-G Compliant**: Meets UC/CSU admission requirements

## Requirements

- Python 3.10 or higher
- No external dependencies (uses standard library only)

## Usage

```bash
python main.py
```

## Project Structure

```
class_schedule_creator/
├── main.py                 # Main entry point - run this
├── models.py               # Data models (Course, Classroom, Teacher, etc.)
├── course_catalog.py       # Complete course catalog with all offerings
├── graduation_paths.py     # 4-year plans for each graduation path
├── resource_calculator.py  # Calculates minimum resources needed
├── scheduler.py            # Constraint-based scheduling algorithm
├── requirements.txt        # Python dependencies (none required)
└── README.md               # This file
```

## Graduation Paths

### 1. Minimum Requirements (No AP)
Meets UC/CSU A-G requirements with a balanced workload. Recommended for students who want to focus on extracurriculars or need more support.

### 2. Pre-Medical Track
Optimized for medical school preparation with:
- AP Biology
- AP Chemistry
- AP Calculus AB
- AP Psychology
- AP English Language/Literature

### 3. Engineering Track
Designed for Computer Science, Computer Engineering, and Chemical Engineering pathways with:
- AP Computer Science Principles
- AP Computer Science A
- AP Physics 1
- AP Chemistry
- AP Calculus AB
- Robotics (2 years)

## UC/CSU A-G Requirements Met

| Area | Requirement | Courses |
|------|-------------|---------|
| A | History/Social Science (2 years) | World History, US History, Government, Economics |
| B | English (4 years) | English 9, 10, 11, 12 (or AP versions) |
| C | Mathematics (3 years) | Algebra 1, Geometry, Algebra 2, Pre-Calc/Calculus |
| D | Laboratory Science (2 years) | Biology, Chemistry, Physics |
| E | Language Other Than English (2 years) | Arabic 1, 2, 3, 4 |
| F | Visual/Performing Arts (1 year) | Art 1, Music |
| G | College-Prep Elective (1 year) | CS, Robotics, Psychology, etc. |

## School-Specific Requirements

- **Physical Education**: 2 years (California state requirement)
- **Islamic Studies**: 4 years (one per grade level)
- **Quran Studies**: 4 years (one per grade level)

## Special Facilities

The school includes the following specialized classrooms:
- Chemistry Laboratory
- Biology/Science Laboratory
- Computer Laboratory
- Robotics Laboratory
- Art Room
- Gymnasium
- Music Room

## Resource Analysis (60 students, 20 per path)

With medium enrollment (20 students per graduation path):

### Minimum Classrooms: 18
- General Classrooms: 12
- Chemistry Laboratory: 1
- Biology/Science Laboratory: 1
- Computer Laboratory: 1
- Robotics Laboratory: 1
- Art Room: 1
- Gymnasium: 1

### Minimum Teachers: 22
- History/Social Science: 3
- English: 3 (1 AP-qualified)
- Mathematics: 3 (1 AP-qualified)
- Laboratory Science: 2 (1 AP-qualified)
- World Languages (Arabic): 2
- Visual/Performing Arts: 1
- Computer Science/Robotics: 1 (1 AP-qualified)
- Physical Education: 2
- Religious Studies: 5

## Constraints Enforced

1. **Classroom Conflicts**: One class per classroom per period
2. **Teacher Conflicts**: One teacher per classroom per period
3. **Room Type Requirements**: Chemistry in chem lab, Biology in bio lab, etc.
4. **Teacher Qualifications**: AP courses require AP-qualified teachers
5. **Prerequisites**: Courses scheduled in proper sequence
6. **Planning Periods**: Teachers have one planning period per day

## Customization

To adjust for different enrollment numbers, modify `main.py`:

```python
students_per_path = {
    GraduationPath.MINIMUM: 20,      # Adjust these numbers
    GraduationPath.PRE_MED: 20,
    GraduationPath.ENGINEERING: 20,
}
max_class_size = 25      # Maximum students per section
periods_per_day = 6      # Number of class periods
```

## Sources

- [California State Minimum High School Graduation Requirements](https://www.cde.ca.gov/ci/gs/hs/hsgrmin.asp)
- [UC/CSU A-G Subject Requirements](https://admission.universityofcalifornia.edu/admission-requirements/first-year-requirements/subject-requirement-a-g.html)
