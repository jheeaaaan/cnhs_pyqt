# setup_db.py
from core.database import DatabaseConfigurationError

SQL = """


DROP TABLE IF EXISTS bmi_bmirecord CASCADE;
DROP TABLE IF EXISTS enrollment_shs_details CASCADE;
DROP TABLE IF EXISTS enrollment_certification CASCADE;
DROP TABLE IF EXISTS enrollment_previous_school CASCADE;
DROP TABLE IF EXISTS enrollment_guardian CASCADE;
DROP TABLE IF EXISTS enrollment_mother CASCADE;
DROP TABLE IF EXISTS enrollment_father CASCADE;
DROP TABLE IF EXISTS enrollment_house_address CASCADE;
DROP TABLE IF EXISTS enrollment_student CASCADE;
DROP TABLE IF EXISTS enrollment_learner CASCADE;
DROP TABLE IF EXISTS enrollment_section CASCADE;
DROP TABLE IF EXISTS auth_user CASCADE;


CREATE TABLE auth_user (
    id                  SERIAL PRIMARY KEY,
    username            VARCHAR(150) UNIQUE NOT NULL,
    password_hash       VARCHAR(256) NOT NULL,
    role                VARCHAR(30) NOT NULL,
    is_active           BOOLEAN DEFAULT TRUE,
    created_at          TIMESTAMP DEFAULT NOW()
);

-- =====================================================
-- SECTION MANAGEMENT
-- =====================================================

CREATE TABLE enrollment_section (
    id                  SERIAL PRIMARY KEY,

    name                VARCHAR(50) NOT NULL,

    grade               INTEGER NOT NULL
                        CHECK (grade BETWEEN 7 AND 12),

    level               VARCHAR(3) NOT NULL
                        CHECK (level IN ('JHS', 'SHS')),

    track               VARCHAR(30) DEFAULT '',

    school_year         VARCHAR(9) NOT NULL,

    adviser_name        VARCHAR(150) DEFAULT '',

    created_at          TIMESTAMP DEFAULT NOW(),

    UNIQUE(name, grade, school_year)
);


CREATE TABLE enrollment_learner (
    id                      SERIAL PRIMARY KEY,

    level                   VARCHAR(3) NOT NULL
                            CHECK (level IN ('JHS', 'SHS')),

    grade                   INTEGER NOT NULL
                            CHECK (grade BETWEEN 7 AND 12),

    section_id              INTEGER
                            REFERENCES enrollment_section(id)
                            ON DELETE SET NULL,

    track                   VARCHAR(50) DEFAULT '',

    semester                VARCHAR(10) DEFAULT '1st',

    status                  VARCHAR(20) DEFAULT 'Pending'
                            CHECK (status IN ('Pending', 'Enrolled', 'Dropped', 'Transferred')),

    electives               TEXT DEFAULT '',

    tve_major               VARCHAR(100) DEFAULT '',

    modalities              TEXT DEFAULT 'Face to Face',

    school_year             VARCHAR(9) NOT NULL DEFAULT '2026-2027',

    date_enrolled           TIMESTAMP DEFAULT NOW(),

    date_updated            TIMESTAMP DEFAULT NOW()
);


CREATE TABLE enrollment_student (
    id                          SERIAL PRIMARY KEY,

    learner_id                  INTEGER UNIQUE NOT NULL
                                REFERENCES enrollment_learner(id)
                                ON DELETE CASCADE,

    student_lrn                 VARCHAR(12) UNIQUE NOT NULL,

    student_has_lrn             BOOLEAN DEFAULT TRUE,

    student_psa_birth_cert      VARCHAR(50) DEFAULT '',

    student_is_balik_aral       BOOLEAN DEFAULT FALSE,

    student_last_name           VARCHAR(100) NOT NULL,

    student_first_name          VARCHAR(100) NOT NULL,

    student_middle_name         VARCHAR(100) DEFAULT '',

    student_extension_name      VARCHAR(20) DEFAULT '',

    student_birthdate           DATE NOT NULL,

    student_age                 INTEGER,

    student_sex                 VARCHAR(1) NOT NULL
                                CHECK (student_sex IN ('M', 'F')),

    student_place_of_birth      VARCHAR(150) DEFAULT '',

    student_mother_tongue       VARCHAR(50) DEFAULT '',

    student_is_ip               BOOLEAN DEFAULT FALSE,

    student_is_four_ps          BOOLEAN DEFAULT FALSE,

    student_four_ps_id          VARCHAR(30) DEFAULT ''
);


CREATE TABLE enrollment_house_address (
    id                              SERIAL PRIMARY KEY,

    learner_id                      INTEGER NOT NULL
                                    REFERENCES enrollment_learner(id)
                                    ON DELETE CASCADE,

    address_type                    VARCHAR(20) NOT NULL
                                    CHECK (address_type IN ('current', 'permanent')),

    address_house_no                VARCHAR(20) DEFAULT '',

    address_street                  VARCHAR(100) DEFAULT '',

    address_barangay                VARCHAR(100) DEFAULT '',

    address_municipality            VARCHAR(100) DEFAULT '',

    address_province                VARCHAR(100) DEFAULT '',

    address_country                 VARCHAR(50) DEFAULT 'Philippines',

    address_zip_code                VARCHAR(10) DEFAULT '',

    is_same_as_current              BOOLEAN DEFAULT TRUE,

    UNIQUE(learner_id, address_type)
);


CREATE TABLE enrollment_father (
    id                          SERIAL PRIMARY KEY,

    learner_id                  INTEGER UNIQUE NOT NULL
                                REFERENCES enrollment_learner(id)
                                ON DELETE CASCADE,

    father_last_name            VARCHAR(100) DEFAULT '',

    father_first_name           VARCHAR(100) DEFAULT '',

    father_middle_name          VARCHAR(100) DEFAULT '',

    father_contact              VARCHAR(20) DEFAULT '',

    father_occupation           VARCHAR(100) DEFAULT ''
);


CREATE TABLE enrollment_mother (
    id                          SERIAL PRIMARY KEY,

    learner_id                  INTEGER UNIQUE NOT NULL
                                REFERENCES enrollment_learner(id)
                                ON DELETE CASCADE,

    mother_last_name            VARCHAR(100) DEFAULT '',

    mother_first_name           VARCHAR(100) DEFAULT '',

    mother_middle_name          VARCHAR(100) DEFAULT '',

    mother_contact              VARCHAR(20) DEFAULT '',

    mother_occupation           VARCHAR(100) DEFAULT ''
);


CREATE TABLE enrollment_guardian (
    id                          SERIAL PRIMARY KEY,

    learner_id                  INTEGER UNIQUE NOT NULL
                                REFERENCES enrollment_learner(id)
                                ON DELETE CASCADE,

    guardian_last_name          VARCHAR(100) DEFAULT '',

    guardian_first_name         VARCHAR(100) DEFAULT '',

    guardian_middle_name        VARCHAR(100) DEFAULT '',

    guardian_relationship       VARCHAR(50) DEFAULT '',

    guardian_contact            VARCHAR(20) DEFAULT '',

    guardian_occupation         VARCHAR(100) DEFAULT ''
);


CREATE TABLE enrollment_previous_school (
    id                              SERIAL PRIMARY KEY,

    learner_id                      INTEGER UNIQUE NOT NULL
                                    REFERENCES enrollment_learner(id)
                                    ON DELETE CASCADE,

    previous_grade_completed        VARCHAR(20) DEFAULT '',

    previous_sy_completed           VARCHAR(9) DEFAULT '',

    previous_school_attended        VARCHAR(150) DEFAULT ''
);


CREATE TABLE enrollment_certification (
    id                          SERIAL PRIMARY KEY,

    learner_id                  INTEGER UNIQUE NOT NULL
                                REFERENCES enrollment_learner(id)
                                ON DELETE CASCADE,

    certifier_name              VARCHAR(200) DEFAULT '',

    date_signed                 DATE
);


CREATE TABLE enrollment_shs_details (
    id                          SERIAL PRIMARY KEY,

    learner_id                  INTEGER UNIQUE NOT NULL
                                REFERENCES enrollment_learner(id)
                                ON DELETE CASCADE,

    track                       VARCHAR(50) DEFAULT '',

    semester                    VARCHAR(10) DEFAULT '1st',

    electives                   TEXT DEFAULT '',

    tvl_major                   VARCHAR(100) DEFAULT '',

    learning_modality           VARCHAR(100) DEFAULT 'Face to Face'
);



CREATE TABLE bmi_bmirecord (
    id                          SERIAL PRIMARY KEY,

    learner_id                  INTEGER NOT NULL
                                REFERENCES enrollment_learner(id)
                                ON DELETE CASCADE,

    height                      FLOAT NOT NULL,

    weight                      FLOAT NOT NULL,

    bmi                         FLOAT NOT NULL,

    bmi_status                  VARCHAR(30) NOT NULL,

    school_year                 VARCHAR(9) NOT NULL,

    date_recorded               DATE DEFAULT NOW(),

    date_updated                TIMESTAMP DEFAULT NOW(),

    UNIQUE(learner_id, school_year)
);


CREATE INDEX idx_student_lrn
ON enrollment_student(student_lrn);

CREATE INDEX idx_learner_grade
ON enrollment_learner(grade);

CREATE INDEX idx_learner_status
ON enrollment_learner(status);

CREATE INDEX idx_section_grade
ON enrollment_section(grade);

CREATE INDEX idx_bmi_status
ON bmi_bmirecord(bmi_status);

CREATE INDEX idx_bmi_learner
ON bmi_bmirecord(learner_id);

-- =====================================================
-- SAMPLE ADMIN ACCOUNT
-- Password should still be hashed in application code
-- =====================================================

INSERT INTO auth_user (
    username,
    password_hash,
    role
)
VALUES (
    'admin',
    '$2b$12$Hz4xZJYAFTy5THcZk0FqQuMu5sSblWnhNpOg0k4Tng.YkaKNmH8nq',
    'Administrator'
);

"""

if __name__ == '__main__':
    from core.database import get_connection, release_connection
    try:
        conn = get_connection()
    except DatabaseConfigurationError as e:
        print(f"Database configuration error: {e}")
        raise SystemExit(1)

    try:
        with conn.cursor() as cur:
            cur.execute(SQL)
        conn.commit()
        print("All tables created successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        release_connection(conn)
