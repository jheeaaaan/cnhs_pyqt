# core/models.py
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import date, datetime
from core.database import execute


# ── SECTION ──────────────────────────────────────────────────────
@dataclass
class Section:
    id: Optional[int] = None
    name: str = ''
    grade: int = 0
    level: str = ''      # 'JHS' or 'SHS'
    track: str = ''      # 'Academic', 'TVL', or ''
    school_year: str = '2026-2027'

    @staticmethod
    def get_all(grade=None, level=None, track=None):
        sql = 'SELECT id,name,grade,level,track,school_year FROM enrollment_section WHERE 1=1'
        params = []
        if grade:  sql += ' AND grade=%s';  params.append(grade)
        if level:  sql += ' AND level=%s';  params.append(level)
        if track:  sql += ' AND track=%s';  params.append(track)
        sql += ' ORDER BY grade, name'
        rows = execute(sql, params, fetch='all')
        return [Section(*r) for r in (rows or [])]

    @staticmethod
    def create(name, grade, level, track='', school_year='2026-2027'):
        execute(
            'INSERT INTO enrollment_section (name,grade,level,track,school_year)'
            ' VALUES (%s,%s,%s,%s,%s)',
            (name, grade, level, track, school_year)
        )

    @staticmethod
    def delete(section_id):
        execute('DELETE FROM enrollment_section WHERE id=%s', (section_id,))
    
    @staticmethod
    def rename(section_id, new_name):
        from core.database import execute
        execute('UPDATE enrollment_section SET name = %s WHERE id = %s', (new_name, section_id))


# ── LEARNER ──────────────────────────────────────────────────────
@dataclass
class Learner:
    id: Optional[int] = None
    lrn: str = ''
    has_lrn: bool = True
    last_name: str = ''
    first_name: str = ''
    middle_name: str = ''
    extension_name: str = ''
    birthdate: Optional[date] = None
    age: int = 0
    sex: str = ''
    place_of_birth: str = ''
    mother_tongue: str = ''
    is_ip: bool = False
    is_four_ps: bool = False
    four_ps_id: str = ''
    house_no: str = ''
    street: str = ''
    barangay: str = ''
    municipality: str = ''
    province: str = ''
    zip_code: str = ''
    father_last_name: str = ''
    father_first_name: str = ''
    father_contact: str = ''
    mother_last_name: str = ''
    mother_first_name: str = ''
    mother_contact: str = ''
    guardian_last_name: str = ''
    guardian_first_name: str = ''
    guardian_contact: str = ''
    level: str = ''
    grade: int = 0
    section_id: Optional[int] = None
    section_name: str = ''
    track: str = ''
    semester: str = '1st'
    status: str = 'Pending'
    school_year: str = '2026-2027'
    electives: str = ''
    tve_major: str = ''
    last_grade_completed: str = ''
    last_sy_completed: str = ''
    last_school_attended: str = ''
    certifier_name: str = ''
    is_balik_aral: bool = False
    psa_birth_cert: str = ''

    @property
    def full_name(self):
        first_part = f'{self.first_name} {self.middle_name}'.strip()
        if self.last_name and first_part:
            return f'{self.last_name}, {first_part}'
        return (self.last_name or first_part or 'Unknown').strip()

    @property
    def electives_list(self):
        return [e.strip() for e in self.electives.split(',') if e.strip()]

    @staticmethod
    def _cols():
        return '''l.id, l.lrn, l.has_lrn, l.last_name, l.first_name,
                  l.middle_name, l.extension_name, l.birthdate, l.age, l.sex,
                  l.place_of_birth, l.mother_tongue, l.is_ip, l.is_four_ps, l.four_ps_id,
                  l.house_no, l.street, l.barangay, l.municipality, l.province, l.zip_code,
                  l.father_last_name, l.father_first_name, l.father_contact,
                  l.mother_last_name, l.mother_first_name, l.mother_contact,
                  l.guardian_last_name, l.guardian_first_name, l.guardian_contact,
                  l.level, l.grade, l.section_id, COALESCE(s.name,'') as section_name,
                  l.track, l.semester, l.status, l.school_year, l.electives,
                  l.tve_major, l.last_grade_completed, l.last_sy_completed,
                  l.last_school_attended, l.certifier_name, l.is_balik_aral, l.psa_birth_cert'''

    @staticmethod
    def get_all(grade=None, level=None, status=None, section_id=None, track=None):
        sql = f'SELECT {Learner._cols()} FROM enrollment_learner l'
        sql += ' LEFT JOIN enrollment_section s ON l.section_id = s.id WHERE 1=1'
        params = []
        if grade:      sql += ' AND l.grade=%s';      params.append(grade)
        if level:      sql += ' AND l.level=%s';      params.append(level)
        if status:     sql += ' AND l.status=%s';     params.append(status)
        if section_id: sql += ' AND l.section_id=%s'; params.append(section_id)
        if track:      sql += ' AND l.track=%s';      params.append(track)
        sql += ' ORDER BY l.last_name, l.first_name'
        rows = execute(sql, params, fetch='all')
        return [Learner(*r) for r in (rows or [])]

    @staticmethod
    def get_by_id(learner_id):
        sql = f'SELECT {Learner._cols()} FROM enrollment_learner l'
        sql += ' LEFT JOIN enrollment_section s ON l.section_id=s.id WHERE l.id=%s'
        row = execute(sql, (learner_id,), fetch='one')
        return Learner(*row) if row else None

    @staticmethod
    def create(**kwargs):
        cols = ', '.join(kwargs.keys())
        vals = ', '.join(['%s'] * len(kwargs))
        execute(f'INSERT INTO enrollment_learner ({cols}) VALUES ({vals})',
                list(kwargs.values()))

    @staticmethod
    def update(learner_id, **kwargs):
        sets = ', '.join(f'{k}=%s' for k in kwargs)
        execute(f'UPDATE enrollment_learner SET {sets} WHERE id=%s',
                list(kwargs.values()) + [learner_id])

    @staticmethod
    def count(grade=None, level=None, status=None):
        sql = 'SELECT COUNT(*) FROM enrollment_learner WHERE 1=1'
        params = []
        if grade:  sql += ' AND grade=%s';  params.append(grade)
        if level:  sql += ' AND level=%s';  params.append(level)
        if status: sql += ' AND status=%s'; params.append(status)
        row = execute(sql, params, fetch='one')
        return row[0] if row else 0


# ── BMI RECORD ───────────────────────────────────────────────────
@dataclass
class BMIRecord:
    id: Optional[int] = None
    learner_id: int = 0
    learner_name: str = ''
    section_name: str = ''
    height: float = 0.0
    weight: float = 0.0
    bmi: float = 0.0
    bmi_status: str = ''
    school_year: str = '2026-2027'

    @staticmethod
    def calc_bmi(height_cm, weight_kg):
        h = height_cm / 100
        bmi = round(weight_kg / (h ** 2), 1)
        if bmi < 16.0:   status = 'Severely Thin'
        elif bmi < 18.5: status = 'Thin'
        elif bmi < 25.0: status = 'Normal'
        elif bmi < 30.0: status = 'Overweight'
        elif bmi < 35.0: status = 'Obese I'
        else:            status = 'Obese II'
        return bmi, status

    @staticmethod
    def save(learner_id, height, weight, school_year='2026-2027'):
        bmi, status = BMIRecord.calc_bmi(height, weight)
        existing = execute(
            'SELECT id FROM bmi_bmirecord WHERE learner_id=%s AND school_year=%s',
            (learner_id, school_year), fetch='one'
        )
        if existing:
            execute('UPDATE bmi_bmirecord SET height=%s,weight=%s,bmi=%s,bmi_status=%s WHERE id=%s',
                    (height, weight, bmi, status, existing[0]))
        else:
            execute('INSERT INTO bmi_bmirecord (learner_id,height,weight,bmi,bmi_status,school_year)'
                    ' VALUES (%s,%s,%s,%s,%s,%s)',
                    (learner_id, height, weight, bmi, status, school_year))

    @staticmethod
    def get_all(grade=None, level=None, track=None, section_id=None, bmi_status=None):
        sql = '''SELECT b.id, b.learner_id,
                        l.last_name||', '||l.first_name as learner_name,
                        COALESCE(s.name,'') as section_name,
                        b.height, b.weight, b.bmi, b.bmi_status, b.school_year
                 FROM bmi_bmirecord b
                 JOIN enrollment_learner l ON b.learner_id=l.id
                 LEFT JOIN enrollment_section s ON l.section_id=s.id
                 WHERE b.school_year='2026-2027' '''
        params = []
        if grade:      sql += ' AND l.grade=%s';      params.append(grade)
        if level:      sql += ' AND l.level=%s';      params.append(level)
        if track:      sql += ' AND l.track=%s';      params.append(track)
        if section_id: sql += ' AND l.section_id=%s'; params.append(section_id)
        if bmi_status: sql += ' AND b.bmi_status=%s'; params.append(bmi_status)
        sql += ' ORDER BY l.last_name, l.first_name'
        rows = execute(sql, params, fetch='all')
        return [BMIRecord(*r) for r in (rows or [])]