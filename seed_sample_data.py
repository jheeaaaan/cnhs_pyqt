# seed_sample_data.py
from datetime import date

from core.database import execute, get_connection, release_connection
from core.models import BMIRecord, Learner, Section
from setup_db import SQL


SCHOOL_YEAR = '2026-2027'


def ensure_schema():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(SQL)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        release_connection(conn)


def ensure_section(name, grade, level, track=''):
    row = execute(
        '''SELECT id FROM enrollment_section
           WHERE name=%s AND grade=%s AND school_year=%s''',
        (name, grade, SCHOOL_YEAR),
        fetch='one',
    )
    if row:
        return row[0]

    Section.create(name, grade, level, track, SCHOOL_YEAR)
    return execute(
        '''SELECT id FROM enrollment_section
           WHERE name=%s AND grade=%s AND school_year=%s''',
        (name, grade, SCHOOL_YEAR),
        fetch='one',
    )[0]


def learner_exists(lrn):
    row = execute(
        'SELECT learner_id FROM enrollment_student WHERE student_lrn=%s',
        (lrn,),
        fetch='one',
    )
    return row[0] if row else None


def seed_learners(section_ids):
    samples = [
        {
            'lrn': '100000000001',
            'has_lrn': True,
            'psa_birth_cert': 'PSA-0001',
            'is_balik_aral': False,
            'last_name': 'Santos',
            'first_name': 'Miguel',
            'middle_name': 'Reyes',
            'extension_name': '',
            'birthdate': date(2011, 4, 12),
            'age': 15,
            'sex': 'M',
            'place_of_birth': 'Daet, Camarines Norte',
            'mother_tongue': 'Tagalog',
            'is_ip': False,
            'is_four_ps': True,
            'four_ps_id': '4PS-2026-001',
            'house_no': '14',
            'street': 'Rizal Street',
            'barangay': 'Barangay 1',
            'municipality': 'Daet',
            'province': 'Camarines Norte',
            'zip_code': '4600',
            'father_last_name': 'Santos',
            'father_first_name': 'Ramon',
            'father_contact': '09170000001',
            'mother_last_name': 'Santos',
            'mother_first_name': 'Elena',
            'mother_contact': '09170000002',
            'guardian_last_name': 'Santos',
            'guardian_first_name': 'Elena',
            'guardian_contact': '09170000002',
            'level': 'JHS',
            'grade': 7,
            'section_id': section_ids['g7_mabini'],
            'status': 'Enrolled',
            'school_year': SCHOOL_YEAR,
            'last_grade_completed': 'Grade 6',
            'last_sy_completed': '2025-2026',
            'last_school_attended': 'Daet Elementary School',
            'certifier_name': 'Maria Dela Cruz',
            'date_signed': date(2026, 5, 18),
            'bmi': (152, 45),
        },
        {
            'lrn': '100000000002',
            'has_lrn': True,
            'psa_birth_cert': 'PSA-0002',
            'is_balik_aral': False,
            'last_name': 'Dela Cruz',
            'first_name': 'Andrea',
            'middle_name': 'Lopez',
            'extension_name': '',
            'birthdate': date(2010, 9, 7),
            'age': 15,
            'sex': 'F',
            'place_of_birth': 'Talisay, Camarines Norte',
            'mother_tongue': 'Bikol',
            'is_ip': False,
            'is_four_ps': False,
            'four_ps_id': '',
            'house_no': '27',
            'street': 'Maharlika Highway',
            'barangay': 'Barangay 2',
            'municipality': 'Talisay',
            'province': 'Camarines Norte',
            'zip_code': '4602',
            'father_last_name': 'Dela Cruz',
            'father_first_name': 'Jose',
            'father_contact': '09170000003',
            'mother_last_name': 'Dela Cruz',
            'mother_first_name': 'Ana',
            'mother_contact': '09170000004',
            'guardian_last_name': 'Dela Cruz',
            'guardian_first_name': 'Jose',
            'guardian_contact': '09170000003',
            'level': 'JHS',
            'grade': 8,
            'section_id': section_ids['g8_rizal'],
            'status': 'Enrolled',
            'school_year': SCHOOL_YEAR,
            'last_grade_completed': 'Grade 7',
            'last_sy_completed': '2025-2026',
            'last_school_attended': 'CNHS',
            'certifier_name': 'Maria Dela Cruz',
            'date_signed': date(2026, 5, 18),
            'bmi': (158, 49),
        },
        {
            'lrn': '100000000003',
            'has_lrn': True,
            'psa_birth_cert': 'PSA-0003',
            'is_balik_aral': True,
            'last_name': 'Villanueva',
            'first_name': 'Paolo',
            'middle_name': 'Garcia',
            'extension_name': '',
            'birthdate': date(2008, 1, 22),
            'age': 18,
            'sex': 'M',
            'place_of_birth': 'Daet, Camarines Norte',
            'mother_tongue': 'Tagalog',
            'is_ip': False,
            'is_four_ps': True,
            'four_ps_id': '4PS-2026-003',
            'house_no': '8',
            'street': 'Quezon Avenue',
            'barangay': 'Barangay 5',
            'municipality': 'Daet',
            'province': 'Camarines Norte',
            'zip_code': '4600',
            'father_last_name': 'Villanueva',
            'father_first_name': 'Oscar',
            'father_contact': '09170000005',
            'mother_last_name': 'Villanueva',
            'mother_first_name': 'Lorna',
            'mother_contact': '09170000006',
            'guardian_last_name': 'Villanueva',
            'guardian_first_name': 'Lorna',
            'guardian_contact': '09170000006',
            'level': 'SHS',
            'grade': 11,
            'section_id': section_ids['g11_stem'],
            'track': 'Academic',
            'electives': 'Pre-Calculus,Basic Calculus',
            'semester': '1st',
            'status': 'Enrolled',
            'school_year': SCHOOL_YEAR,
            'modalities': 'Face to Face',
            'last_grade_completed': 'Grade 10',
            'last_sy_completed': '2025-2026',
            'last_school_attended': 'CNHS',
            'certifier_name': 'Maria Dela Cruz',
            'date_signed': date(2026, 5, 18),
            'bmi': (169, 60),
        },
        {
            'lrn': '100000000004',
            'has_lrn': True,
            'psa_birth_cert': 'PSA-0004',
            'is_balik_aral': False,
            'last_name': 'Aquino',
            'first_name': 'Sofia',
            'middle_name': 'Mendoza',
            'extension_name': '',
            'birthdate': date(2007, 11, 30),
            'age': 18,
            'sex': 'F',
            'place_of_birth': 'Basud, Camarines Norte',
            'mother_tongue': 'Bikol',
            'is_ip': False,
            'is_four_ps': False,
            'four_ps_id': '',
            'house_no': '42',
            'street': 'Bonifacio Street',
            'barangay': 'Barangay 3',
            'municipality': 'Basud',
            'province': 'Camarines Norte',
            'zip_code': '4608',
            'father_last_name': 'Aquino',
            'father_first_name': 'Nestor',
            'father_contact': '09170000007',
            'mother_last_name': 'Aquino',
            'mother_first_name': 'Carla',
            'mother_contact': '09170000008',
            'guardian_last_name': 'Aquino',
            'guardian_first_name': 'Carla',
            'guardian_contact': '09170000008',
            'level': 'SHS',
            'grade': 12,
            'section_id': section_ids['g12_tvl'],
            'track': 'TVL',
            'electives': 'Cookery,Bread and Pastry',
            'tve_major': 'Cookery',
            'semester': '1st',
            'status': 'Pending',
            'school_year': SCHOOL_YEAR,
            'modalities': 'Face to Face',
            'last_grade_completed': 'Grade 11',
            'last_sy_completed': '2025-2026',
            'last_school_attended': 'CNHS',
            'certifier_name': 'Maria Dela Cruz',
            'date_signed': date(2026, 5, 18),
            'bmi': (161, 54),
        },
    ]

    inserted = 0
    skipped = 0
    bmi_rows = 0

    for sample in samples:
        height, weight = sample.pop('bmi')
        learner_id = learner_exists(sample['lrn'])
        if learner_id:
            skipped += 1
        else:
            Learner.create(**sample)
            learner_id = learner_exists(sample['lrn'])
            inserted += 1

        if learner_id:
            BMIRecord.save(learner_id, height, weight, SCHOOL_YEAR)
            bmi_rows += 1

    return inserted, skipped, bmi_rows


def main():
    ensure_schema()
    section_ids = {
        'g7_mabini': ensure_section('Mabini', 7, 'JHS'),
        'g8_rizal': ensure_section('Rizal', 8, 'JHS'),
        'g11_stem': ensure_section('STEM 11-A', 11, 'SHS', 'Academic'),
        'g12_tvl': ensure_section('TVL 12-A', 12, 'SHS', 'TVL'),
    }
    inserted, skipped, bmi_rows = seed_learners(section_ids)
    print(f'Seed complete: {inserted} learners inserted, {skipped} skipped, {bmi_rows} BMI rows saved.')


if __name__ == '__main__':
    main()
