# setup_db.py
from core.database import execute

SQL = """
CREATE TABLE IF NOT EXISTS auth_user (
    id            SERIAL PRIMARY KEY,
    username      VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    is_active     BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS enrollment_section (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(50) NOT NULL,
    grade       INTEGER NOT NULL,
    level       VARCHAR(3) NOT NULL,
    track       VARCHAR(20) DEFAULT '',
    school_year VARCHAR(9) DEFAULT '2026-2027',
    UNIQUE (name, grade, school_year)
);

CREATE TABLE IF NOT EXISTS enrollment_learner (
    id                   SERIAL PRIMARY KEY,
    lrn                  VARCHAR(12) UNIQUE NOT NULL,
    has_lrn              BOOLEAN DEFAULT TRUE,
    psa_birth_cert       VARCHAR(30) DEFAULT '',
    is_balik_aral        BOOLEAN DEFAULT FALSE,
    last_name            VARCHAR(100) NOT NULL,
    first_name           VARCHAR(100) NOT NULL,
    middle_name          VARCHAR(100) DEFAULT '',
    extension_name       VARCHAR(10)  DEFAULT '',
    birthdate            DATE NOT NULL,
    age                  INTEGER,
    sex                  VARCHAR(1) NOT NULL,
    place_of_birth       VARCHAR(100) DEFAULT '',
    mother_tongue        VARCHAR(20)  DEFAULT '',
    is_ip                BOOLEAN DEFAULT FALSE,
    is_four_ps           BOOLEAN DEFAULT FALSE,
    four_ps_id           VARCHAR(30)  DEFAULT '',
    house_no             VARCHAR(20)  DEFAULT '',
    street               VARCHAR(100) DEFAULT '',
    barangay             VARCHAR(100) DEFAULT '',
    municipality         VARCHAR(100) DEFAULT '',
    province             VARCHAR(100) DEFAULT '',
    country              VARCHAR(50)  DEFAULT 'Philippines',
    zip_code             VARCHAR(4)   DEFAULT '',
    perm_house_no        VARCHAR(20)  DEFAULT '',
    perm_street          VARCHAR(100) DEFAULT '',
    perm_barangay        VARCHAR(100) DEFAULT '',
    perm_municipality    VARCHAR(100) DEFAULT '',
    perm_province        VARCHAR(100) DEFAULT '',
    perm_country         VARCHAR(50)  DEFAULT '',
    perm_zip_code        VARCHAR(4)   DEFAULT '',
    same_address         BOOLEAN DEFAULT TRUE,
    father_last_name     VARCHAR(100) DEFAULT '',
    father_first_name    VARCHAR(100) DEFAULT '',
    father_contact       VARCHAR(15)  DEFAULT '',
    mother_last_name     VARCHAR(100) DEFAULT '',
    mother_first_name    VARCHAR(100) DEFAULT '',
    mother_contact       VARCHAR(15)  DEFAULT '',
    guardian_last_name   VARCHAR(100) DEFAULT '',
    guardian_first_name  VARCHAR(100) DEFAULT '',
    guardian_contact     VARCHAR(15)  DEFAULT '',
    level                VARCHAR(3)  NOT NULL,
    grade                INTEGER NOT NULL,
    section_id           INTEGER REFERENCES enrollment_section(id) ON DELETE SET NULL,
    track                VARCHAR(20)  DEFAULT '',
    semester             VARCHAR(3)   DEFAULT '1st',
    status               VARCHAR(15)  DEFAULT 'Pending',
    school_year          VARCHAR(9)   DEFAULT '2026-2027',
    electives            TEXT DEFAULT '',
    tve_major            VARCHAR(100) DEFAULT '',
    last_grade_completed VARCHAR(20)  DEFAULT '',
    last_sy_completed    VARCHAR(9)   DEFAULT '',
    last_school_attended VARCHAR(100) DEFAULT '',
    modalities           TEXT DEFAULT 'Face to Face',
    certifier_name       VARCHAR(200) DEFAULT '',
    date_signed          DATE,
    date_enrolled        TIMESTAMP DEFAULT NOW(),
    date_updated         TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS bmi_bmirecord (
    id            SERIAL PRIMARY KEY,
    learner_id    INTEGER NOT NULL REFERENCES enrollment_learner(id) ON DELETE CASCADE,
    height        FLOAT NOT NULL,
    weight        FLOAT NOT NULL,
    bmi           FLOAT NOT NULL,
    bmi_status    VARCHAR(20) NOT NULL,
    school_year   VARCHAR(9) DEFAULT '2026-2027',
    date_recorded DATE DEFAULT NOW(),
    date_updated  TIMESTAMP DEFAULT NOW(),
    UNIQUE (learner_id, school_year)
);
"""

if __name__ == '__main__':
    try:
        conn = __import__('psycopg2').connect(
            dbname=__import__('os').environ.get('DB_NAME', 'cnhs_db'),
        )
    except:
        pass

    from core.database import get_connection, release_connection
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(SQL)
        conn.commit()
        print("✅ All tables created successfully.")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {e}")
    finally:
        release_connection(conn)