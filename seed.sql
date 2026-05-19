-- =====================================================
-- CANSOJONG NHS DATA SEED: SECTIONS, STUDENTS, AND BMI LOGS
-- (Fixed to match actual database schema)
-- =====================================================

-- 1. INSERT SECTIONS
INSERT INTO enrollment_section (name, grade, level, track, school_year, adviser_name) VALUES
('Rizal', 7, 'JHS', '', '2026-2027', 'Maria Santos'),
('Bonifacio', 8, 'JHS', '', '2026-2027', 'Juan Dela Cruz'),
('Mabini', 9, 'JHS', '', '2026-2027', 'Elena Rocha'),
('Luna', 10, 'JHS', '', '2026-2027', 'Ricardo Dalisay'),
('STEM - A', 11, 'SHS', 'STEM', '2026-2027', 'Grace Poe'),
('TVL - HE', 12, 'SHS', 'TVL', '2026-2027', 'Franklin Drilon');


-- 2. INSERT LEARNERS, STUDENTS, AND CORRESPONDING BMI RECORDS
DO $$
DECLARE
    sec_g7  INT := (SELECT id FROM enrollment_section WHERE grade = 7 LIMIT 1);
    sec_g8  INT := (SELECT id FROM enrollment_section WHERE grade = 8 LIMIT 1);
    sec_g9  INT := (SELECT id FROM enrollment_section WHERE grade = 9 LIMIT 1);
    sec_g10 INT := (SELECT id FROM enrollment_section WHERE grade = 10 LIMIT 1);
    sec_g11 INT := (SELECT id FROM enrollment_section WHERE grade = 11 LIMIT 1);
    sec_g12 INT := (SELECT id FROM enrollment_section WHERE grade = 12 LIMIT 1);

    g7_ids  INT[] := '{}'; g8_ids  INT[] := '{}'; g9_ids  INT[] := '{}';
    g10_ids INT[] := '{}'; g11_ids INT[] := '{}'; g12_ids INT[] := '{}';

    tmp_id INT;
BEGIN

    -- -----------------------------------------------------
    -- GRADE 7
    -- -----------------------------------------------------
    FOR i IN 1..5 LOOP
        INSERT INTO enrollment_learner (level, grade, section_id, status, school_year)
        VALUES ('JHS', 7, sec_g7, 'Enrolled', '2026-2027') RETURNING id INTO tmp_id;
        g7_ids := array_append(g7_ids, tmp_id);
    END LOOP;

    INSERT INTO enrollment_student (learner_id, student_lrn, student_last_name, student_first_name, student_middle_name, student_birthdate, student_age, student_sex, student_mother_tongue) VALUES
    (g7_ids[1], '406123000701', 'Abad',      'Mark',  'Castro', '2014-06-15', 12, 'M', 'Bisaya'),
    (g7_ids[2], '406123000702', 'Alcantara', 'Judy',  'Cruz',   '2014-02-10', 12, 'F', 'Bisaya'),
    (g7_ids[3], '406123000703', 'Aquino',    'Paolo', 'Santos', '2014-09-24', 11, 'M', 'Tagalog'),
    (g7_ids[4], '406123000704', 'Aranas',    'Sarah', 'Gomez',  '2014-11-05', 11, 'F', 'Bisaya'),
    (g7_ids[5], '406123000705', 'Bacalso',   'John',  'Reyes',  '2014-04-18', 12, 'M', 'Bisaya');

    INSERT INTO bmi_bmirecord (learner_id, height, weight, bmi, bmi_status, school_year) VALUES
    (g7_ids[1], 1.48, 41.5, 18.9, 'Normal',      '2026-2027'),
    (g7_ids[2], 1.45, 33.0, 15.7, 'Underweight', '2026-2027'),
    (g7_ids[3], 1.50, 44.0, 19.6, 'Normal',      '2026-2027'),
    (g7_ids[4], 1.42, 51.0, 25.3, 'Overweight',  '2026-2027'),
    (g7_ids[5], 1.52, 46.2, 20.0, 'Normal',      '2026-2027');


    -- -----------------------------------------------------
    -- GRADE 8
    -- -----------------------------------------------------
    FOR i IN 1..5 LOOP
        INSERT INTO enrollment_learner (level, grade, section_id, status, school_year)
        VALUES ('JHS', 8, sec_g8, 'Enrolled', '2026-2027') RETURNING id INTO tmp_id;
        g8_ids := array_append(g8_ids, tmp_id);
    END LOOP;

    INSERT INTO enrollment_student (learner_id, student_lrn, student_last_name, student_first_name, student_middle_name, student_birthdate, student_age, student_sex, student_mother_tongue) VALUES
    (g8_ids[1], '406123000801', 'Bautista',  'Anna',      'Gomez',   '2013-03-22', 13, 'F', 'Bisaya'),
    (g8_ids[2], '406123000802', 'Bascon',    'Gabriel',   'Vargas',  '2013-07-14', 12, 'M', 'Bisaya'),
    (g8_ids[3], '406123000803', 'Bersabal',  'Michelle',  'Torres',  '2013-01-30', 13, 'F', 'Bisaya'),
    (g8_ids[4], '406123000804', 'Caballero', 'Christian', 'Mendoza', '2013-08-19', 12, 'M', 'Bisaya'),
    (g8_ids[5], '406123000805', 'Cabrera',   'Ella',      'Flores',  '2013-10-12', 12, 'F', 'Tagalog');

    INSERT INTO bmi_bmirecord (learner_id, height, weight, bmi, bmi_status, school_year) VALUES
    (g8_ids[1], 1.53, 43.0, 18.4, 'Underweight', '2026-2027'),
    (g8_ids[2], 1.56, 49.5, 20.3, 'Normal',      '2026-2027'),
    (g8_ids[3], 1.51, 45.0, 19.7, 'Normal',      '2026-2027'),
    (g8_ids[4], 1.58, 65.2, 26.1, 'Overweight',  '2026-2027'),
    (g8_ids[5], 1.52, 48.0, 20.8, 'Normal',      '2026-2027');


    -- -----------------------------------------------------
    -- GRADE 9
    -- -----------------------------------------------------
    FOR i IN 1..5 LOOP
        INSERT INTO enrollment_learner (level, grade, section_id, status, school_year)
        VALUES ('JHS', 9, sec_g9, 'Enrolled', '2026-2027') RETURNING id INTO tmp_id;
        g9_ids := array_append(g9_ids, tmp_id);
    END LOOP;

    INSERT INTO enrollment_student (learner_id, student_lrn, student_last_name, student_first_name, student_middle_name, student_birthdate, student_age, student_sex, student_mother_tongue) VALUES
    (g9_ids[1], '406123000901', 'Cañete',    'John Lloyd', 'Alvarez',    '2012-09-05', 14, 'M', 'Bisaya'),
    (g9_ids[2], '406123000902', 'Custodio',  'Grace',      'Mercado',    '2012-05-12', 14, 'F', 'Bisaya'),
    (g9_ids[3], '406123000903', 'Daan',      'Kenneth',    'Santiago',   '2012-12-01', 13, 'M', 'Bisaya'),
    (g9_ids[4], '406123000904', 'Davide',    'Mary',       'Ramos',      '2012-02-18', 14, 'F', 'Bisaya'),
    (g9_ids[5], '406123000905', 'Deiparine', 'James',      'Villanueva', '2012-07-22', 13, 'M', 'Bisaya');

    INSERT INTO bmi_bmirecord (learner_id, height, weight, bmi, bmi_status, school_year) VALUES
    (g9_ids[1], 1.62, 54.0, 20.6, 'Normal',      '2026-2027'),
    (g9_ids[2], 1.55, 47.5, 19.8, 'Normal',      '2026-2027'),
    (g9_ids[3], 1.60, 42.0, 16.4, 'Underweight', '2026-2027'),
    (g9_ids[4], 1.57, 52.1, 21.1, 'Normal',      '2026-2027'),
    (g9_ids[5], 1.64, 82.0, 30.5, 'Obese',       '2026-2027');


    -- -----------------------------------------------------
    -- GRADE 10
    -- -----------------------------------------------------
    FOR i IN 1..5 LOOP
        INSERT INTO enrollment_learner (level, grade, section_id, status, school_year)
        VALUES ('JHS', 10, sec_g10, 'Enrolled', '2026-2027') RETURNING id INTO tmp_id;
        g10_ids := array_append(g10_ids, tmp_id);
    END LOOP;

    INSERT INTO enrollment_student (learner_id, student_lrn, student_last_name, student_first_name, student_middle_name, student_birthdate, student_age, student_sex, student_mother_tongue) VALUES
    (g10_ids[1], '406123001001', 'Dela Torre', 'Princess',  'Mendoza',  '2011-11-30', 15, 'F', 'Bisaya'),
    (g10_ids[2], '406123001002', 'Diaz',       'Joshua',    'Castillo', '2011-04-14', 15, 'M', 'Bisaya'),
    (g10_ids[3], '406123001003', 'Echavez',    'Kimberly',  'Sayson',   '2011-08-09', 15, 'F', 'Bisaya'),
    (g10_ids[4], '406123001004', 'Enriquez',   'Ryan',      'Perez',    '2011-01-25', 15, 'M', 'Tagalog'),
    (g10_ids[5], '406123001005', 'Escalante',  'Stephanie', 'Omana',    '2011-06-03', 15, 'F', 'Bisaya');

    INSERT INTO bmi_bmirecord (learner_id, height, weight, bmi, bmi_status, school_year) VALUES
    (g10_ids[1], 1.58, 61.2, 24.5, 'Normal',      '2026-2027'),
    (g10_ids[2], 1.67, 56.0, 20.1, 'Normal',      '2026-2027'),
    (g10_ids[3], 1.54, 41.0, 17.3, 'Underweight', '2026-2027'),
    (g10_ids[4], 1.65, 78.5, 28.8, 'Overweight',  '2026-2027'),
    (g10_ids[5], 1.56, 50.0, 20.5, 'Normal',      '2026-2027');


    -- -----------------------------------------------------
    -- GRADE 11 (STEM)
    -- -----------------------------------------------------
    FOR i IN 1..5 LOOP
        INSERT INTO enrollment_learner (level, grade, section_id, status, track, school_year)
        VALUES ('SHS', 11, sec_g11, 'Enrolled', 'STEM', '2026-2027') RETURNING id INTO tmp_id;
        g11_ids := array_append(g11_ids, tmp_id);
    END LOOP;

    INSERT INTO enrollment_student (learner_id, student_lrn, student_last_name, student_first_name, student_middle_name, student_birthdate, student_age, student_sex, student_mother_tongue) VALUES
    (g11_ids[1], '406123001101', 'Esperanza',  'David',   'Tan',     '2010-01-14', 16, 'M', 'Tagalog'),
    (g11_ids[2], '406123001102', 'Espinosa',   'Rachel',  'Jimenez', '2010-09-11', 16, 'F', 'Bisaya'),
    (g11_ids[3], '406123001103', 'Franza',     'Matthew', 'Dizon',   '2010-05-28', 16, 'M', 'Bisaya'),
    (g11_ids[4], '406123001104', 'Gabunada',   'Nicole',  'Suarez',  '2010-12-05', 15, 'F', 'Bisaya'),
    (g11_ids[5], '406123001105', 'Generalao',  'Justin',  'Abella',  '2010-03-20', 16, 'M', 'Bisaya');

    INSERT INTO bmi_bmirecord (learner_id, height, weight, bmi, bmi_status, school_year) VALUES
    (g11_ids[1], 1.70, 62.0, 21.5, 'Normal',      '2026-2027'),
    (g11_ids[2], 1.59, 48.0, 19.0, 'Normal',      '2026-2027'),
    (g11_ids[3], 1.73, 53.4, 17.8, 'Underweight', '2026-2027'),
    (g11_ids[4], 1.57, 54.0, 21.9, 'Normal',      '2026-2027'),
    (g11_ids[5], 1.68, 76.0, 26.9, 'Overweight',  '2026-2027');


    -- -----------------------------------------------------
    -- GRADE 12 (TVL)
    -- -----------------------------------------------------
    FOR i IN 1..5 LOOP
        INSERT INTO enrollment_learner (level, grade, section_id, status, track, tve_major, school_year)
        VALUES ('SHS', 12, sec_g12, 'Enrolled', 'TVL', 'Home Economics', '2026-2027') RETURNING id INTO tmp_id;
        g12_ids := array_append(g12_ids, tmp_id);
    END LOOP;

    INSERT INTO enrollment_student (learner_id, student_lrn, student_last_name, student_first_name, student_middle_name, student_birthdate, student_age, student_sex, student_mother_tongue) VALUES
    (g12_ids[1], '406123001201', 'Fernandez', 'Chloe',   'Villanueva', '2009-07-19', 17, 'F', 'Bisaya'),
    (g12_ids[2], '406123001202', 'Garciano',  'Angelo',  'Rosales',    '2009-04-02', 17, 'M', 'Bisaya'),
    (g12_ids[3], '406123001203', 'Hermosa',   'Janine',  'Gutierrez',  '2009-11-13', 16, 'F', 'Bisaya'),
    (g12_ids[4], '406123001204', 'Inocando',  'Patrick', 'Salazar',    '2009-08-27', 17, 'M', 'Bisaya'),
    (g12_ids[5], '406123001205', 'Labra',     'Erica',   'Padilla',    '2009-01-05', 17, 'F', 'Bisaya');

    INSERT INTO bmi_bmirecord (learner_id, height, weight, bmi, bmi_status, school_year) VALUES
    (g12_ids[1], 1.60, 51.5, 20.1, 'Normal',      '2026-2027'),
    (g12_ids[2], 1.71, 65.0, 22.2, 'Normal',      '2026-2027'),
    (g12_ids[3], 1.58, 43.5, 17.4, 'Underweight', '2026-2027'),
    (g12_ids[4], 1.69, 86.0, 30.1, 'Obese',       '2026-2027'),
    (g12_ids[5], 1.62, 59.8, 22.8, 'Normal',      '2026-2027');

END $$;