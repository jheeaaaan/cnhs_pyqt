# Cansojong NHS Enrollment and BMI System Flow

## 1. System Overview

The system is a desktop application for managing student enrollment records and BMI monitoring for Junior High School and Senior High School learners. It helps school staff encode learner information, assign learners to sections, monitor pending and enrolled records, record height and weight, calculate BMI, and generate reports.

The program uses a PostgreSQL database, so all enrollment records, section records, user accounts, and BMI records are stored in one central database.

## 2. Main User Flow

```text
Start Program
    |
    v
Login Screen
    |
    v
Dashboard
    |
    +--> Enrollment Module
    |       |
    |       +--> Select Grade Level
    |       +--> Fill Out Enrollment Form
    |       +--> Assign Section or Save as Pending
    |       +--> Save Learner Record
    |       +--> View Enrollment Reports
    |
    +--> Section Management
    |       |
    |       +--> Create or View Sections
    |       +--> View Learners per Section
    |       +--> Transfer or Edit Learner Details
    |
    +--> BMI Module
    |       |
    |       +--> Select Grade and Section
    |       +--> Enter Height and Weight
    |       +--> System Computes BMI
    |       +--> Save BMI Record
    |       +--> View BMI Reports
    |
    +--> Account Settings
            |
            +--> Change Password
            +--> Logout
```

## 3. Login and Security Flow

```text
User enters username and password
    |
    v
System checks auth_user table
    |
    +--> Valid account and active user
    |       |
    |       v
    |   Open Main Dashboard
    |
    +--> Invalid account or password
            |
            v
        Show login error
```

Only registered users can access the system. Passwords are stored as hashed passwords in the database, not as plain text.

## 4. Dashboard Flow

After login, the user sees the dashboard. The dashboard gives a quick summary of:

- Total enrolled learners
- Pending learners
- BMI records for JHS
- BMI records for SHS
- Quick links to common enrollment and BMI tasks

This is the starting point for daily monitoring.

## 5. Enrollment Flow

```text
User opens Enrollment Form
    |
    v
Select grade level:
    - JHS: Grades 7 to 10
    - SHS: Grades 11 to 12
    |
    v
Encode learner information:
    - Student identity
    - Birth and demographic details
    - Address
    - Father, mother, and guardian details
    - Previous school details
    - Certification details
    |
    v
Select section
    |
    +--> Section selected
    |       |
    |       v
    |   Learner status becomes Enrolled
    |
    +--> No section selected
            |
            v
        Learner status becomes Pending
    |
    v
Save record to database
```

For Senior High School, the enrollment form also includes:

- Track
- Electives
- Semester
- TVL major, when applicable
- Learning modality

## 6. Section Management Flow

```text
User opens Sections page
    |
    v
System displays sections by grade level
    |
    +--> Create new section
    |
    +--> Open existing section
            |
            v
        View learners assigned to that section
            |
            +--> Search learner
            +--> Edit learner
            +--> Transfer learner to another section
            +--> Export section list, where available
```

Sections are shared by the Enrollment and BMI modules. Once learners are assigned to a section, they become available for BMI entry under that section.

## 7. Enrollment Report Flow

```text
User opens Enrollment Report
    |
    v
System loads learners for selected grade
    |
    v
Display totals and learner list
    |
    +--> Filter or search records
    +--> View enrolled learners
    +--> View pending learners
    +--> Edit learner details
```

Reports help staff monitor how many learners are already enrolled and how many are still pending.

## 8. BMI Flow

```text
User opens BMI Entry
    |
    v
Select grade level and section
    |
    v
System displays enrolled learners in that section
    |
    v
User enters height and weight
    |
    v
System calculates BMI:
    BMI = weight in kg / height in meters squared
    |
    v
System assigns BMI status
    |
    v
Save BMI record
```

The BMI module uses existing enrollment records. A learner must first exist in the enrollment database before BMI can be recorded.

## 9. BMI Report Flow

```text
User opens BMI Report
    |
    v
System loads BMI records by grade, level, section, or status
    |
    v
Display learner name, section, height, weight, BMI, and BMI status
    |
    v
User reviews nutritional status summary
```

The BMI report helps staff identify learners with normal BMI, thinness, overweight, or obesity classifications.

## 10. Database Flow

```text
Application Forms and Pages
    |
    v
Model Layer
    |
    v
PostgreSQL Database
```

The database is organized into connected tables:

- `auth_user` stores user accounts.
- `enrollment_section` stores sections.
- `enrollment_learner` stores the main enrollment record.
- `enrollment_student` stores student identity and personal details.
- `enrollment_house_address` stores current and permanent address details.
- `enrollment_father` stores father information.
- `enrollment_mother` stores mother information.
- `enrollment_guardian` stores guardian information.
- `enrollment_previous_school` stores previous school information.
- `enrollment_certification` stores certification details.
- `bmi_bmirecord` stores height, weight, BMI, and BMI status.

The separated tables are connected through `learner_id`, so all learner-related information still belongs to one learner record.

## 11. Simple Client Explanation

The system starts with a secured login. After logging in, the user is taken to the dashboard where they can monitor enrollment and BMI records. Staff can encode learners through the enrollment form, assign them to sections, and view reports. Once learners are enrolled in a section, they can be monitored in the BMI module. The system computes BMI automatically after height and weight are entered, then stores the result for reporting.

All data is saved in the database, and the learner information is organized into separate but connected tables. This makes the system easier to maintain, easier to monitor, and more organized for future reports.

## 12. User Roles in Practice

- Registrar or enrollment staff encode and update learner information.
- Adviser or section handler checks section lists and learner status.
- Health personnel or assigned staff enter height and weight for BMI monitoring.
- Administrators manage user access and monitor overall records.

## 13. End-to-End Example

```text
1. Staff logs in.
2. Staff opens Grade 11 Enrollment Form.
3. Staff encodes learner details.
4. Staff selects section STEM 11-A.
5. System saves learner as Enrolled.
6. Staff opens Grade 11 BMI Entry.
7. Staff selects STEM 11-A.
8. System shows the enrolled learner.
9. Staff enters height and weight.
10. System computes BMI and status.
11. Staff opens BMI Report to review results.
```
