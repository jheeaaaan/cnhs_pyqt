# core/models.py
from dataclasses import dataclass, field
from typing import ClassVar, Optional, List
from datetime import date, datetime
from core.database import execute, get_connection, release_connection


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
    modalities: str = ''
    last_grade_completed: str = ''
    last_sy_completed: str = ''
    last_school_attended: str = ''
    certifier_name: str = ''
    is_balik_aral: bool = False
    psa_birth_cert: str = ''
    manual_status_override: bool = False

    STUDENT_COLUMNS: ClassVar[dict] = {
        'lrn': 'student_lrn',
        'has_lrn': 'student_has_lrn',
        'psa_birth_cert': 'student_psa_birth_cert',
        'is_balik_aral': 'student_is_balik_aral',
        'last_name': 'student_last_name',
        'first_name': 'student_first_name',
        'middle_name': 'student_middle_name',
        'extension_name': 'student_extension_name',
        'birthdate': 'student_birthdate',
        'age': 'student_age',
        'sex': 'student_sex',
        'place_of_birth': 'student_place_of_birth',
        'mother_tongue': 'student_mother_tongue',
        'is_ip': 'student_is_ip',
        'is_four_ps': 'student_is_four_ps',
        'four_ps_id': 'student_four_ps_id',
    }
    ADDRESS_COLUMNS: ClassVar[dict] = {
        'house_no': 'address_house_no',
        'street': 'address_street',
        'barangay': 'address_barangay',
        'municipality': 'address_municipality',
        'province': 'address_province',
        'country': 'address_country',
        'zip_code': 'address_zip_code',
        'same_address': 'is_same_as_current',
    }
    PERMANENT_ADDRESS_COLUMNS: ClassVar[dict] = {
        'perm_house_no': 'address_house_no',
        'perm_street': 'address_street',
        'perm_barangay': 'address_barangay',
        'perm_municipality': 'address_municipality',
        'perm_province': 'address_province',
        'perm_country': 'address_country',
        'perm_zip_code': 'address_zip_code',
        'same_address': 'is_same_as_current',
    }
    FATHER_COLUMNS: ClassVar[dict] = {
        'father_last_name': 'father_last_name',
        'father_first_name': 'father_first_name',
        'father_contact': 'father_contact',
    }
    MOTHER_COLUMNS: ClassVar[dict] = {
        'mother_last_name': 'mother_last_name',
        'mother_first_name': 'mother_first_name',
        'mother_contact': 'mother_contact',
    }
    GUARDIAN_COLUMNS: ClassVar[dict] = {
        'guardian_last_name': 'guardian_last_name',
        'guardian_first_name': 'guardian_first_name',
        'guardian_contact': 'guardian_contact',
    }
    PREVIOUS_SCHOOL_COLUMNS: ClassVar[dict] = {
        'last_grade_completed': 'previous_grade_completed',
        'last_sy_completed': 'previous_sy_completed',
        'last_school_attended': 'previous_school_attended',
    }
    CERTIFICATION_COLUMNS: ClassVar[dict] = {
        'certifier_name': 'certifier_name',
        'date_signed': 'date_signed',
    }
    MAIN_COLUMNS: ClassVar[set] = {
        'level', 'grade', 'section_id', 'track', 'semester', 'status',
        'school_year', 'electives', 'tve_major', 'modalities',
        'manual_status_override',
    }

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
    def _present(value):
        return value is not None and str(value).strip() != ''

    @staticmethod
    def _is_tvl_track(track):
        return (track or '').strip() in ('TVL', 'TechPro/TVL')

    @staticmethod
    def enrollment_status_for(data):
        status = (data.get('status') or 'Pending').strip()
        if data.get('manual_status_override') and status:
            return status
        if status in ('Dropped', 'Transferred'):
            return status

        # Core required fields (guardian fields are EXCLUDED — they are optional)
        required_fields = [
            'lrn', 'last_name', 'first_name', 'middle_name', 'extension_name',
            'birthdate', 'age', 'sex', 'place_of_birth', 'mother_tongue',
            'house_no', 'street', 'barangay', 'municipality', 'province',
            'zip_code',
            'father_last_name', 'father_first_name', 'father_contact',
            'mother_last_name', 'mother_first_name', 'mother_contact',
            'level', 'grade', 'section_id', 'school_year',
            'last_grade_completed', 'last_sy_completed', 'last_school_attended',
            'certifier_name',
        ]

        complete = True
        for key in required_fields:
            value = data.get(key)
            if key in ('age', 'grade'):
                try:
                    if int(value) <= 0:
                        complete = False
                        break
                except (TypeError, ValueError):
                    complete = False
                    break
            elif not Learner._present(value):
                complete = False
                break

        if (data.get('level') or '').strip() == 'SHS':
            complete = complete and Learner._present(data.get('track'))
            complete = complete and Learner._present(data.get('semester'))
            complete = complete and bool([
                e for e in str(data.get('electives') or '').split(',')
                if e.strip()
            ])
            if Learner._is_tvl_track(data.get('track')):
                complete = complete and Learner._present(data.get('tve_major'))

        return 'Enrolled' if complete else 'Pending'

    def with_computed_status(self):
        self.status = Learner.enrollment_status_for(self.__dict__)
        return self

    @staticmethod
    def _ensure_status_override_column():
        execute(
            '''ALTER TABLE enrollment_learner
               ADD COLUMN IF NOT EXISTS manual_status_override BOOLEAN DEFAULT FALSE'''
        )

    @staticmethod
    def _cols():
        return '''l.id, st.student_lrn, st.student_has_lrn,
                  st.student_last_name, st.student_first_name,
                  st.student_middle_name, st.student_extension_name,
                  st.student_birthdate, st.student_age, st.student_sex,
                  st.student_place_of_birth, st.student_mother_tongue,
                  st.student_is_ip, st.student_is_four_ps, st.student_four_ps_id,
                  ca.address_house_no, ca.address_street, ca.address_barangay,
                  ca.address_municipality, ca.address_province, ca.address_zip_code,
                  f.father_last_name, f.father_first_name, f.father_contact,
                  m.mother_last_name, m.mother_first_name, m.mother_contact,
                  g.guardian_last_name, g.guardian_first_name, g.guardian_contact,
                  l.level, l.grade, l.section_id, COALESCE(s.name,'') as section_name,
                  l.track, l.semester, l.status, l.school_year, l.electives,
                  l.tve_major, l.modalities, ps.previous_grade_completed, ps.previous_sy_completed,
                  ps.previous_school_attended, c.certifier_name,
                  st.student_is_balik_aral, st.student_psa_birth_cert,
                  COALESCE(l.manual_status_override, FALSE)'''

    @staticmethod
    def _joins():
        return ''' FROM enrollment_learner l
                  JOIN enrollment_student st ON st.learner_id = l.id
                  LEFT JOIN enrollment_house_address ca
                         ON ca.learner_id = l.id AND ca.address_type = 'current'
                  LEFT JOIN enrollment_father f ON f.learner_id = l.id
                  LEFT JOIN enrollment_mother m ON m.learner_id = l.id
                  LEFT JOIN enrollment_guardian g ON g.learner_id = l.id
                  LEFT JOIN enrollment_previous_school ps ON ps.learner_id = l.id
                  LEFT JOIN enrollment_certification c ON c.learner_id = l.id
                  LEFT JOIN enrollment_section s ON l.section_id = s.id'''

    @staticmethod
    def get_all(grade=None, level=None, status=None, section_id=None, track=None):
        Learner._ensure_status_override_column()
        sql = f'SELECT {Learner._cols()} {Learner._joins()} WHERE 1=1'
        params = []
        if grade:      sql += ' AND l.grade=%s';      params.append(grade)
        if level:      sql += ' AND l.level=%s';      params.append(level)
        if section_id: sql += ' AND l.section_id=%s'; params.append(section_id)
        if track:      sql += ' AND l.track=%s';      params.append(track)
        sql += ' ORDER BY st.student_last_name, st.student_first_name'
        rows = execute(sql, params, fetch='all')
        learners = [Learner(*r).with_computed_status() for r in (rows or [])]
        if status:
            learners = [l for l in learners if l.status == status]
        return learners

    @staticmethod
    def get_by_id(learner_id):
        Learner._ensure_status_override_column()
        sql = f'SELECT {Learner._cols()} {Learner._joins()} WHERE l.id=%s'
        row = execute(sql, (learner_id,), fetch='one')
        return Learner(*row).with_computed_status() if row else None

    @staticmethod
    def create(**kwargs):
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                Learner._ensure_status_override_column()
                kwargs['manual_status_override'] = bool(kwargs.get('manual_status_override', False))
                kwargs['status'] = Learner.enrollment_status_for(kwargs)
                legacy_cols = Learner._table_columns(cur, 'enrollment_learner')
                main = {
                    k: v for k, v in kwargs.items()
                    if k in Learner.MAIN_COLUMNS or k in legacy_cols
                }
                learner_id = Learner._insert(cur, 'enrollment_learner', main)
                Learner._insert_detail(cur, 'enrollment_student', learner_id,
                                       kwargs, Learner.STUDENT_COLUMNS)
                Learner._insert_address(cur, learner_id, 'current',
                                        kwargs, Learner.ADDRESS_COLUMNS)
                Learner._insert_address(cur, learner_id, 'permanent',
                                        kwargs, Learner.PERMANENT_ADDRESS_COLUMNS)
                Learner._insert_detail(cur, 'enrollment_father', learner_id,
                                       kwargs, Learner.FATHER_COLUMNS)
                Learner._insert_detail(cur, 'enrollment_mother', learner_id,
                                       kwargs, Learner.MOTHER_COLUMNS)
                Learner._insert_detail(cur, 'enrollment_guardian', learner_id,
                                       kwargs, Learner.GUARDIAN_COLUMNS)
                Learner._insert_detail(cur, 'enrollment_previous_school', learner_id,
                                       kwargs, Learner.PREVIOUS_SCHOOL_COLUMNS)
                Learner._insert_detail(cur, 'enrollment_certification', learner_id,
                                       kwargs, Learner.CERTIFICATION_COLUMNS)
            conn.commit()
            return learner_id
        except Exception:
            conn.rollback()
            raise
        finally:
            release_connection(conn)

    @staticmethod
    def update(learner_id, **kwargs):
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                Learner._ensure_status_override_column()
                current = Learner.get_by_id(learner_id)
                merged = current.__dict__.copy() if current else {}
                merged.update(kwargs)
                kwargs['status'] = Learner.enrollment_status_for(merged)
                legacy_cols = Learner._table_columns(cur, 'enrollment_learner')
                main = {
                    k: v for k, v in kwargs.items()
                    if k in Learner.MAIN_COLUMNS or k in legacy_cols
                }
                main['date_updated'] = datetime.now()
                Learner._update_table(cur, 'enrollment_learner', learner_id, main)
                Learner._upsert_detail(cur, 'enrollment_student', learner_id,
                                       kwargs, Learner.STUDENT_COLUMNS)
                Learner._upsert_address(cur, learner_id, 'current',
                                        kwargs, Learner.ADDRESS_COLUMNS)
                Learner._upsert_address(cur, learner_id, 'permanent',
                                        kwargs, Learner.PERMANENT_ADDRESS_COLUMNS)
                Learner._upsert_detail(cur, 'enrollment_father', learner_id,
                                       kwargs, Learner.FATHER_COLUMNS)
                Learner._upsert_detail(cur, 'enrollment_mother', learner_id,
                                       kwargs, Learner.MOTHER_COLUMNS)
                Learner._upsert_detail(cur, 'enrollment_guardian', learner_id,
                                       kwargs, Learner.GUARDIAN_COLUMNS)
                Learner._upsert_detail(cur, 'enrollment_previous_school', learner_id,
                                       kwargs, Learner.PREVIOUS_SCHOOL_COLUMNS)
                Learner._upsert_detail(cur, 'enrollment_certification', learner_id,
                                       kwargs, Learner.CERTIFICATION_COLUMNS)
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            release_connection(conn)

    @staticmethod
    def delete(learner_id):
        execute('DELETE FROM enrollment_learner WHERE id=%s', (learner_id,))

    @staticmethod
    def _table_columns(cur, table_name):
        cur.execute(
            '''SELECT column_name FROM information_schema.columns
               WHERE table_name = %s''',
            (table_name,)
        )
        return {row[0] for row in cur.fetchall()}

    @staticmethod
    def _insert(cur, table, values):
        cols = list(values.keys())
        vals = ', '.join(['%s'] * len(cols))
        cur.execute(
            f'INSERT INTO {table} ({", ".join(cols)}) VALUES ({vals}) RETURNING id',
            [values[c] for c in cols]
        )
        return cur.fetchone()[0]

    @staticmethod
    def _insert_detail(cur, table, learner_id, source, mapping):
        values = {'learner_id': learner_id}
        values.update({db_col: source[k] for k, db_col in mapping.items() if k in source})
        Learner._insert(cur, table, values)

    @staticmethod
    def _insert_address(cur, learner_id, address_type, source, mapping):
        values = {'learner_id': learner_id, 'address_type': address_type}
        values.update({db_col: source[k] for k, db_col in mapping.items() if k in source})
        Learner._insert(cur, 'enrollment_house_address', values)

    @staticmethod
    def _update_table(cur, table, learner_id, values):
        if not values:
            return
        cols = list(values.keys())
        sets = ', '.join(f'{c}=%s' for c in cols)
        cur.execute(
            f'UPDATE {table} SET {sets} WHERE id=%s',
            [values[c] for c in cols] + [learner_id]
        )

    @staticmethod
    def _upsert_detail(cur, table, learner_id, source, mapping):
        values = {db_col: source[k] for k, db_col in mapping.items() if k in source}
        if not values:
            return
        cols = ['learner_id'] + list(values.keys())
        vals = [learner_id] + [values[c] for c in values]
        updates = ', '.join(f'{c}=EXCLUDED.{c}' for c in values)
        cur.execute(
            f'''INSERT INTO {table} ({", ".join(cols)})
                VALUES ({", ".join(["%s"] * len(cols))})
                ON CONFLICT (learner_id) DO UPDATE SET {updates}''',
            vals
        )

    @staticmethod
    def _upsert_address(cur, learner_id, address_type, source, mapping):
        values = {db_col: source[k] for k, db_col in mapping.items() if k in source}
        if not values:
            return
        cols = ['learner_id', 'address_type'] + list(values.keys())
        vals = [learner_id, address_type] + [values[c] for c in values]
        updates = ', '.join(f'{c}=EXCLUDED.{c}' for c in values)
        cur.execute(
            f'''INSERT INTO enrollment_house_address ({", ".join(cols)})
                VALUES ({", ".join(["%s"] * len(cols))})
                ON CONFLICT (learner_id, address_type) DO UPDATE SET {updates}''',
            vals
        )

    @staticmethod
    def count(grade=None, level=None, status=None):
        return len(Learner.get_all(grade=grade, level=level, status=status))


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
                        st.student_last_name||', '||st.student_first_name as learner_name,
                        COALESCE(s.name,'') as section_name,
                        b.height, b.weight, b.bmi, b.bmi_status, b.school_year
                 FROM bmi_bmirecord b
                 JOIN enrollment_learner l ON b.learner_id=l.id
                 JOIN enrollment_student st ON st.learner_id=l.id
                 LEFT JOIN enrollment_section s ON l.section_id=s.id
                 WHERE b.school_year='2026-2027' '''
        params = []
        if grade:
            sql += ' AND (l.grade=%s OR s.grade=%s)'
            params.extend([grade, grade])
        if level:
            sql += ' AND (l.level=%s OR s.level=%s)'
            params.extend([level, level])
        if track:
            sql += ' AND (l.track=%s OR s.track=%s)'
            params.extend([track, track])
        if section_id: sql += ' AND l.section_id=%s'; params.append(section_id)
        if bmi_status: sql += ' AND b.bmi_status=%s'; params.append(bmi_status)
        sql += ' ORDER BY st.student_last_name, st.student_first_name'
        rows = execute(sql, params, fetch='all')
        return [BMIRecord(*r) for r in (rows or [])]
