# core/errors.py
import psycopg2
from psycopg2 import errorcodes


def friendly_error_message(error):
    """Convert technical database exceptions into messages users can act on."""
    original = _root_error(error)
    text = str(original).lower()
    pgcode = getattr(original, 'pgcode', None)

    if pgcode == errorcodes.UNIQUE_VIOLATION:
        if 'student_lrn' in text or 'lrn' in text:
            return 'A learner with this LRN already exists. Please check the LRN and try again.'
        if _mentions(text, 'enrollment_section', 'name', 'grade', 'school_year'):
            return 'A section with this name already exists for the selected grade and school year.'
        return 'This record already exists. Please check the details and try again.'

    if pgcode == errorcodes.NOT_NULL_VIOLATION:
        field = _field_name(original) or _field_name_from_text(text)
        if field:
            return f'Please complete the required field: {field}.'
        return 'Please complete all required fields before saving.'

    if pgcode == errorcodes.FOREIGN_KEY_VIOLATION:
        if 'section_id' in text:
            return 'The selected section is no longer available. Please refresh the page and select a section again.'
        if 'learner_id' in text:
            return 'The selected learner record could not be found. Please refresh the page and try again.'
        return 'A related record is missing. Please refresh the page and try again.'

    if pgcode == errorcodes.STRING_DATA_RIGHT_TRUNCATION:
        return 'One of the entered values is too long. Please shorten the text and try again.'

    if pgcode == errorcodes.INVALID_TEXT_REPRESENTATION:
        return 'One of the entered values has an invalid format. Please check the form and try again.'

    if pgcode == errorcodes.UNDEFINED_TABLE:
        return 'A required database table is missing. Please run the database setup, then try again.'

    if pgcode == errorcodes.UNDEFINED_COLUMN:
        return 'The database structure is not up to date. Please run the database setup, then try again.'

    if isinstance(original, psycopg2.OperationalError):
        return 'The system could not connect to the database. Please check if PostgreSQL is running.'

    if 'duplicate' in text or 'unique' in text:
        return 'This record already exists. Please check the details and try again.'

    if 'not null' in text:
        return 'Please complete all required fields before saving.'

    if 'does not exist' in text and ('relation' in text or 'column' in text):
        return 'The database structure is not ready. Please run the database setup, then try again.'

    return 'Something went wrong while saving. Please check the form and try again.'


def show_error(parent, title, error):
    from PyQt5.QtWidgets import QMessageBox
    from core.message_boxes import critical

    critical(parent, title, friendly_error_message(error))


def _root_error(error):
    return getattr(error, '__cause__', None) or error


def _mentions(text, *parts):
    return all(part in text for part in parts)


def _field_name(error):
    diag = getattr(error, 'diag', None)
    field = getattr(diag, 'column_name', None) if diag else None
    return _pretty_field(field)


def _field_name_from_text(text):
    known_fields = {
        'student_lrn': 'LRN',
        'student_last_name': 'Last name',
        'student_first_name': 'First name',
        'student_birthdate': 'Birthdate',
        'student_sex': 'Sex',
        'level': 'School level',
        'grade': 'Grade',
        'name': 'Section name',
    }
    for key, label in known_fields.items():
        if key in text:
            return label
    return ''


def _pretty_field(field):
    if not field:
        return ''
    labels = {
        'student_lrn': 'LRN',
        'student_last_name': 'Last name',
        'student_first_name': 'First name',
        'student_birthdate': 'Birthdate',
        'student_sex': 'Sex',
        'level': 'School level',
        'grade': 'Grade',
        'name': 'Section name',
    }
    return labels.get(field, field.replace('_', ' ').title())
