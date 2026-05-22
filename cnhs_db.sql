

\restrict P9tS1pkhZs9Ox8PZO6UfCIZXYfON9uViJJ4SDc3KwEfgrGPRkVKipYDjXK5Pgq0


SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;



CREATE TABLE public.auth_user (
    id integer NOT NULL,
    username character varying(150) NOT NULL,
    password_hash character varying(256) NOT NULL,
    role character varying(30) NOT NULL,
    is_active boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.auth_user OWNER TO postgres;


CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.auth_user_id_seq OWNER TO postgres;


ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


CREATE TABLE public.bmi_bmirecord (
    id integer NOT NULL,
    learner_id integer NOT NULL,
    height double precision NOT NULL,
    weight double precision NOT NULL,
    bmi double precision NOT NULL,
    bmi_status character varying(30) NOT NULL,
    school_year character varying(9) NOT NULL,
    date_recorded date DEFAULT now(),
    date_updated timestamp without time zone DEFAULT now()
);


ALTER TABLE public.bmi_bmirecord OWNER TO postgres;


CREATE SEQUENCE public.bmi_bmirecord_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bmi_bmirecord_id_seq OWNER TO postgres;


ALTER SEQUENCE public.bmi_bmirecord_id_seq OWNED BY public.bmi_bmirecord.id;


CREATE TABLE public.enrollment_certification (
    id integer NOT NULL,
    learner_id integer NOT NULL,
    certifier_name character varying(200) DEFAULT ''::character varying,
    date_signed date
);


ALTER TABLE public.enrollment_certification OWNER TO postgres;


CREATE SEQUENCE public.enrollment_certification_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.enrollment_certification_id_seq OWNER TO postgres;

--
-- Name: enrollment_certification_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.enrollment_certification_id_seq OWNED BY public.enrollment_certification.id;


--
-- Name: enrollment_father; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.enrollment_father (
    id integer NOT NULL,
    learner_id integer NOT NULL,
    father_last_name character varying(100) DEFAULT ''::character varying,
    father_first_name character varying(100) DEFAULT ''::character varying,
    father_middle_name character varying(100) DEFAULT ''::character varying,
    father_contact character varying(20) DEFAULT ''::character varying,
    father_occupation character varying(100) DEFAULT ''::character varying
);


ALTER TABLE public.enrollment_father OWNER TO postgres;

--
-- Name: enrollment_father_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.enrollment_father_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.enrollment_father_id_seq OWNER TO postgres;

--
-- Name: enrollment_father_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.enrollment_father_id_seq OWNED BY public.enrollment_father.id;


--
-- Name: enrollment_guardian; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.enrollment_guardian (
    id integer NOT NULL,
    learner_id integer NOT NULL,
    guardian_last_name character varying(100) DEFAULT ''::character varying,
    guardian_first_name character varying(100) DEFAULT ''::character varying,
    guardian_middle_name character varying(100) DEFAULT ''::character varying,
    guardian_relationship character varying(50) DEFAULT ''::character varying,
    guardian_contact character varying(20) DEFAULT ''::character varying,
    guardian_occupation character varying(100) DEFAULT ''::character varying
);


ALTER TABLE public.enrollment_guardian OWNER TO postgres;

--
-- Name: enrollment_guardian_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.enrollment_guardian_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.enrollment_guardian_id_seq OWNER TO postgres;

--
-- Name: enrollment_guardian_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.enrollment_guardian_id_seq OWNED BY public.enrollment_guardian.id;


--
-- Name: enrollment_house_address; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.enrollment_house_address (
    id integer NOT NULL,
    learner_id integer NOT NULL,
    address_type character varying(20) NOT NULL,
    address_house_no character varying(20) DEFAULT ''::character varying,
    address_street character varying(100) DEFAULT ''::character varying,
    address_barangay character varying(100) DEFAULT ''::character varying,
    address_municipality character varying(100) DEFAULT ''::character varying,
    address_province character varying(100) DEFAULT ''::character varying,
    address_country character varying(50) DEFAULT 'Philippines'::character varying,
    address_zip_code character varying(10) DEFAULT ''::character varying,
    is_same_as_current boolean DEFAULT true,
    CONSTRAINT enrollment_house_address_address_type_check CHECK (((address_type)::text = ANY ((ARRAY['current'::character varying, 'permanent'::character varying])::text[])))
);


ALTER TABLE public.enrollment_house_address OWNER TO postgres;

--
-- Name: enrollment_house_address_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.enrollment_house_address_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.enrollment_house_address_id_seq OWNER TO postgres;

--
-- Name: enrollment_house_address_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.enrollment_house_address_id_seq OWNED BY public.enrollment_house_address.id;


--
-- Name: enrollment_learner; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.enrollment_learner (
    id integer NOT NULL,
    level character varying(3) NOT NULL,
    grade integer NOT NULL,
    section_id integer,
    track character varying(50) DEFAULT ''::character varying,
    semester character varying(10) DEFAULT '1st'::character varying,
    status character varying(20) DEFAULT 'Pending'::character varying,
    electives text DEFAULT ''::text,
    tve_major character varying(100) DEFAULT ''::character varying,
    modalities text DEFAULT 'Face to Face'::text,
    school_year character varying(9) DEFAULT '2026-2027'::character varying NOT NULL,
    date_enrolled timestamp without time zone DEFAULT now(),
    date_updated timestamp without time zone DEFAULT now(),
    manual_status_override boolean DEFAULT false,
    CONSTRAINT enrollment_learner_grade_check CHECK (((grade >= 7) AND (grade <= 12))),
    CONSTRAINT enrollment_learner_level_check CHECK (((level)::text = ANY ((ARRAY['JHS'::character varying, 'SHS'::character varying])::text[]))),
    CONSTRAINT enrollment_learner_status_check CHECK (((status)::text = ANY ((ARRAY['Pending'::character varying, 'Enrolled'::character varying, 'Dropped'::character varying, 'Transferred'::character varying])::text[])))
);


ALTER TABLE public.enrollment_learner OWNER TO postgres;

--
-- Name: enrollment_learner_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.enrollment_learner_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.enrollment_learner_id_seq OWNER TO postgres;

--
-- Name: enrollment_learner_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.enrollment_learner_id_seq OWNED BY public.enrollment_learner.id;


--
-- Name: enrollment_mother; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.enrollment_mother (
    id integer NOT NULL,
    learner_id integer NOT NULL,
    mother_last_name character varying(100) DEFAULT ''::character varying,
    mother_first_name character varying(100) DEFAULT ''::character varying,
    mother_middle_name character varying(100) DEFAULT ''::character varying,
    mother_contact character varying(20) DEFAULT ''::character varying,
    mother_occupation character varying(100) DEFAULT ''::character varying
);


ALTER TABLE public.enrollment_mother OWNER TO postgres;

--
-- Name: enrollment_mother_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.enrollment_mother_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.enrollment_mother_id_seq OWNER TO postgres;

--
-- Name: enrollment_mother_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.enrollment_mother_id_seq OWNED BY public.enrollment_mother.id;


--
-- Name: enrollment_previous_school; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.enrollment_previous_school (
    id integer NOT NULL,
    learner_id integer NOT NULL,
    previous_grade_completed character varying(20) DEFAULT ''::character varying,
    previous_sy_completed character varying(9) DEFAULT ''::character varying,
    previous_school_attended character varying(150) DEFAULT ''::character varying
);


ALTER TABLE public.enrollment_previous_school OWNER TO postgres;

--
-- Name: enrollment_previous_school_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.enrollment_previous_school_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.enrollment_previous_school_id_seq OWNER TO postgres;

--
-- Name: enrollment_previous_school_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.enrollment_previous_school_id_seq OWNED BY public.enrollment_previous_school.id;


--
-- Name: enrollment_section; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.enrollment_section (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    grade integer NOT NULL,
    level character varying(3) NOT NULL,
    track character varying(30) DEFAULT ''::character varying,
    school_year character varying(9) NOT NULL,
    adviser_name character varying(150) DEFAULT ''::character varying,
    created_at timestamp without time zone DEFAULT now(),
    CONSTRAINT enrollment_section_grade_check CHECK (((grade >= 7) AND (grade <= 12))),
    CONSTRAINT enrollment_section_level_check CHECK (((level)::text = ANY ((ARRAY['JHS'::character varying, 'SHS'::character varying])::text[])))
);


ALTER TABLE public.enrollment_section OWNER TO postgres;

--
-- Name: enrollment_section_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.enrollment_section_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.enrollment_section_id_seq OWNER TO postgres;

--
-- Name: enrollment_section_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.enrollment_section_id_seq OWNED BY public.enrollment_section.id;


--
-- Name: enrollment_shs_details; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.enrollment_shs_details (
    id integer NOT NULL,
    learner_id integer NOT NULL,
    track character varying(50) DEFAULT ''::character varying,
    semester character varying(10) DEFAULT '1st'::character varying,
    electives text DEFAULT ''::text,
    tvl_major character varying(100) DEFAULT ''::character varying,
    learning_modality character varying(100) DEFAULT 'Face to Face'::character varying
);


ALTER TABLE public.enrollment_shs_details OWNER TO postgres;

--
-- Name: enrollment_shs_details_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.enrollment_shs_details_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.enrollment_shs_details_id_seq OWNER TO postgres;

--
-- Name: enrollment_shs_details_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.enrollment_shs_details_id_seq OWNED BY public.enrollment_shs_details.id;


--
-- Name: enrollment_student; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.enrollment_student (
    id integer NOT NULL,
    learner_id integer NOT NULL,
    student_lrn character varying(12) NOT NULL,
    student_has_lrn boolean DEFAULT true,
    student_psa_birth_cert character varying(50) DEFAULT ''::character varying,
    student_is_balik_aral boolean DEFAULT false,
    student_last_name character varying(100) NOT NULL,
    student_first_name character varying(100) NOT NULL,
    student_middle_name character varying(100) DEFAULT ''::character varying,
    student_extension_name character varying(20) DEFAULT ''::character varying,
    student_birthdate date NOT NULL,
    student_age integer,
    student_sex character varying(1) NOT NULL,
    student_place_of_birth character varying(150) DEFAULT ''::character varying,
    student_mother_tongue character varying(50) DEFAULT ''::character varying,
    student_is_ip boolean DEFAULT false,
    student_is_four_ps boolean DEFAULT false,
    student_four_ps_id character varying(30) DEFAULT ''::character varying,
    CONSTRAINT enrollment_student_student_sex_check CHECK (((student_sex)::text = ANY ((ARRAY['M'::character varying, 'F'::character varying])::text[])))
);


ALTER TABLE public.enrollment_student OWNER TO postgres;

--
-- Name: enrollment_student_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.enrollment_student_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.enrollment_student_id_seq OWNER TO postgres;

--
-- Name: enrollment_student_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.enrollment_student_id_seq OWNED BY public.enrollment_student.id;


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: bmi_bmirecord id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bmi_bmirecord ALTER COLUMN id SET DEFAULT nextval('public.bmi_bmirecord_id_seq'::regclass);


--
-- Name: enrollment_certification id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_certification ALTER COLUMN id SET DEFAULT nextval('public.enrollment_certification_id_seq'::regclass);


--
-- Name: enrollment_father id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_father ALTER COLUMN id SET DEFAULT nextval('public.enrollment_father_id_seq'::regclass);


--
-- Name: enrollment_guardian id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_guardian ALTER COLUMN id SET DEFAULT nextval('public.enrollment_guardian_id_seq'::regclass);


--
-- Name: enrollment_house_address id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_house_address ALTER COLUMN id SET DEFAULT nextval('public.enrollment_house_address_id_seq'::regclass);


--
-- Name: enrollment_learner id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_learner ALTER COLUMN id SET DEFAULT nextval('public.enrollment_learner_id_seq'::regclass);


--
-- Name: enrollment_mother id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_mother ALTER COLUMN id SET DEFAULT nextval('public.enrollment_mother_id_seq'::regclass);


--
-- Name: enrollment_previous_school id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_previous_school ALTER COLUMN id SET DEFAULT nextval('public.enrollment_previous_school_id_seq'::regclass);


--
-- Name: enrollment_section id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_section ALTER COLUMN id SET DEFAULT nextval('public.enrollment_section_id_seq'::regclass);


--
-- Name: enrollment_shs_details id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_shs_details ALTER COLUMN id SET DEFAULT nextval('public.enrollment_shs_details_id_seq'::regclass);


--
-- Name: enrollment_student id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_student ALTER COLUMN id SET DEFAULT nextval('public.enrollment_student_id_seq'::regclass);


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user (id, username, password_hash, role, is_active, created_at) FROM stdin;
1	admin	$2b$12$Hz4xZJYAFTy5THcZk0FqQuMu5sSblWnhNpOg0k4Tng.YkaKNmH8nq	Administrator	t	2026-05-19 13:55:33.082354
\.


--
-- Data for Name: bmi_bmirecord; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bmi_bmirecord (id, learner_id, height, weight, bmi, bmi_status, school_year, date_recorded, date_updated) FROM stdin;
1	1	1.48	41.5	18.9	Normal	2026-2027	2026-05-19	2026-05-19 14:08:26.09439
2	2	1.45	33	15.7	Underweight	2026-2027	2026-05-19	2026-05-19 14:08:26.09439
3	3	1.5	44	19.6	Normal	2026-2027	2026-05-19	2026-05-19 14:08:26.09439
4	4	1.42	51	25.3	Overweight	2026-2027	2026-05-19	2026-05-19 14:08:26.09439
5	5	1.52	46.2	20	Normal	2026-2027	2026-05-19	2026-05-19 14:08:26.09439
6	6	1.53	43	18.4	Underweight	2026-2027	2026-05-19	2026-05-19 14:08:26.09439
7	7	1.56	49.5	20.3	Normal	2026-2027	2026-05-19	2026-05-19 14:08:26.09439
8	8	1.51	45	19.7	Normal	2026-2027	2026-05-19	2026-05-19 14:08:26.09439
9	9	1.58	65.2	26.1	Overweight	2026-2027	2026-05-19	2026-05-19 14:08:26.09439
10	10	1.52	48	20.8	Normal	2026-2027	2026-05-19	2026-05-19 14:08:26.09439
11	11	1.62	54	20.6	Normal	2026-2027	2026-05-19	2026-05-19 14:08:26.09439
12	12	1.55	47.5	19.8	Normal	2026-2027	2026-05-19	2026-05-19 14:08:26.09439
13	13	1.6	42	16.4	Underweight	2026-2027	2026-05-19	2026-05-19 14:08:26.09439
14	14	1.57	52.1	21.1	Normal	2026-2027	2026-05-19	2026-05-19 14:08:26.09439
15	15	1.64	82	30.5	Obese	2026-2027	2026-05-19	2026-05-19 14:08:26.09439
16	16	1.58	61.2	24.5	Normal	2026-2027	2026-05-19	2026-05-19 14:08:26.09439
17	17	1.67	56	20.1	Normal	2026-2027	2026-05-19	2026-05-19 14:08:26.09439
18	18	1.54	41	17.3	Underweight	2026-2027	2026-05-19	2026-05-19 14:08:26.09439
19	19	1.65	78.5	28.8	Overweight	2026-2027	2026-05-19	2026-05-19 14:08:26.09439
20	20	1.56	50	20.5	Normal	2026-2027	2026-05-19	2026-05-19 14:08:26.09439
21	21	1.7	62	21.5	Normal	2026-2027	2026-05-19	2026-05-19 14:08:26.09439
22	22	1.59	48	19	Normal	2026-2027	2026-05-19	2026-05-19 14:08:26.09439
23	23	1.73	53.4	17.8	Underweight	2026-2027	2026-05-19	2026-05-19 14:08:26.09439
24	24	1.57	54	21.9	Normal	2026-2027	2026-05-19	2026-05-19 14:08:26.09439
25	25	1.68	76	26.9	Overweight	2026-2027	2026-05-19	2026-05-19 14:08:26.09439
26	26	1.6	51.5	20.1	Normal	2026-2027	2026-05-19	2026-05-19 14:08:26.09439
27	27	1.71	65	22.2	Normal	2026-2027	2026-05-19	2026-05-19 14:08:26.09439
28	28	1.58	43.5	17.4	Underweight	2026-2027	2026-05-19	2026-05-19 14:08:26.09439
29	29	1.69	86	30.1	Obese	2026-2027	2026-05-19	2026-05-19 14:08:26.09439
30	30	1.62	59.8	22.8	Normal	2026-2027	2026-05-19	2026-05-19 14:08:26.09439
\.


--
-- Data for Name: enrollment_certification; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.enrollment_certification (id, learner_id, certifier_name, date_signed) FROM stdin;
2	22		\N
1	21		\N
6	31		2026-05-19
\.


--
-- Data for Name: enrollment_father; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.enrollment_father (id, learner_id, father_last_name, father_first_name, father_middle_name, father_contact, father_occupation) FROM stdin;
3	22					
5	2	jujucebu	cebu		0239781	
14	3					
2	21	cebu	cebu		134679952	
18	4	cebu	cebu		cebu	
24	5	cebu	cebu		123456789	
26	31	cebu	cebu		096236587979	
1	1	cebuuu	cebuuu		1326859879456	
\.


--
-- Data for Name: enrollment_guardian; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.enrollment_guardian (id, learner_id, guardian_last_name, guardian_first_name, guardian_middle_name, guardian_relationship, guardian_contact, guardian_occupation) FROM stdin;
3	22						
5	2	dsdsd	dsds			dsds	
14	3						
2	21						
18	4	cebu	cebu			cebu	
24	5						
26	31						
1	1						
\.


--
-- Data for Name: enrollment_house_address; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.enrollment_house_address (id, learner_id, address_type, address_house_no, address_street, address_barangay, address_municipality, address_province, address_country, address_zip_code, is_same_as_current) FROM stdin;
3	22	current						Philippines		t
5	2	current	12	cebu	cebu	cebu	cebu	Philippines	6045	t
14	3	current						Philippines		t
2	21	current	1234656	cebu	cebu	cebu	cebu	Philippines	6245	t
18	4	current	cebu	cebu	cebu	cebu	cebu	Philippines	14562	t
24	5	current	123	cebu	cebu	cebu	cebu	Philippines	6045	t
26	31	current	123	cebu	cebu	cebu	cebu	Philippines	6045	t
27	31	permanent						Philippines		t
1	1	current	123	123	cebuuu	cebuuu	cebuuu	Philippines	1233	t
\.


--
-- Data for Name: enrollment_learner; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.enrollment_learner (id, level, grade, section_id, track, semester, status, electives, tve_major, modalities, school_year, date_enrolled, date_updated, manual_status_override) FROM stdin;
6	JHS	8	2		1st	Enrolled			Face to Face	2026-2027	2026-05-19 14:08:26.09439	2026-05-19 14:08:26.09439	f
7	JHS	8	2		1st	Enrolled			Face to Face	2026-2027	2026-05-19 14:08:26.09439	2026-05-19 14:08:26.09439	f
8	JHS	8	2		1st	Enrolled			Face to Face	2026-2027	2026-05-19 14:08:26.09439	2026-05-19 14:08:26.09439	f
9	JHS	8	2		1st	Enrolled			Face to Face	2026-2027	2026-05-19 14:08:26.09439	2026-05-19 14:08:26.09439	f
10	JHS	8	2		1st	Enrolled			Face to Face	2026-2027	2026-05-19 14:08:26.09439	2026-05-19 14:08:26.09439	f
11	JHS	9	3		1st	Enrolled			Face to Face	2026-2027	2026-05-19 14:08:26.09439	2026-05-19 14:08:26.09439	f
12	JHS	9	3		1st	Enrolled			Face to Face	2026-2027	2026-05-19 14:08:26.09439	2026-05-19 14:08:26.09439	f
13	JHS	9	3		1st	Enrolled			Face to Face	2026-2027	2026-05-19 14:08:26.09439	2026-05-19 14:08:26.09439	f
14	JHS	9	3		1st	Enrolled			Face to Face	2026-2027	2026-05-19 14:08:26.09439	2026-05-19 14:08:26.09439	f
15	JHS	9	3		1st	Enrolled			Face to Face	2026-2027	2026-05-19 14:08:26.09439	2026-05-19 14:08:26.09439	f
16	JHS	10	4		1st	Enrolled			Face to Face	2026-2027	2026-05-19 14:08:26.09439	2026-05-19 14:08:26.09439	f
17	JHS	10	4		1st	Enrolled			Face to Face	2026-2027	2026-05-19 14:08:26.09439	2026-05-19 14:08:26.09439	f
18	JHS	10	4		1st	Enrolled			Face to Face	2026-2027	2026-05-19 14:08:26.09439	2026-05-19 14:08:26.09439	f
19	JHS	10	4		1st	Enrolled			Face to Face	2026-2027	2026-05-19 14:08:26.09439	2026-05-19 14:08:26.09439	f
20	JHS	10	4		1st	Enrolled			Face to Face	2026-2027	2026-05-19 14:08:26.09439	2026-05-19 14:08:26.09439	f
23	SHS	11	5	STEM	1st	Enrolled			Face to Face	2026-2027	2026-05-19 14:08:26.09439	2026-05-19 14:08:26.09439	f
24	SHS	11	5	STEM	1st	Enrolled			Face to Face	2026-2027	2026-05-19 14:08:26.09439	2026-05-19 14:08:26.09439	f
25	SHS	11	5	STEM	1st	Enrolled			Face to Face	2026-2027	2026-05-19 14:08:26.09439	2026-05-19 14:08:26.09439	f
26	SHS	12	6	TVL	1st	Enrolled		Home Economics	Face to Face	2026-2027	2026-05-19 14:08:26.09439	2026-05-19 14:08:26.09439	f
27	SHS	12	6	TVL	1st	Enrolled		Home Economics	Face to Face	2026-2027	2026-05-19 14:08:26.09439	2026-05-19 14:08:26.09439	f
28	SHS	12	6	TVL	1st	Enrolled		Home Economics	Face to Face	2026-2027	2026-05-19 14:08:26.09439	2026-05-19 14:08:26.09439	f
29	SHS	12	6	TVL	1st	Enrolled		Home Economics	Face to Face	2026-2027	2026-05-19 14:08:26.09439	2026-05-19 14:08:26.09439	f
30	SHS	12	6	TVL	1st	Enrolled		Home Economics	Face to Face	2026-2027	2026-05-19 14:08:26.09439	2026-05-19 14:08:26.09439	f
22	SHS	11	5	Academic	1st	Enrolled			Face to Face	2026-2027	2026-05-19 14:08:26.09439	2026-05-19 15:46:15.24379	f
2	JHS	7	\N		1st	Pending			Face to Face	2026-2027	2026-05-19 14:08:26.09439	2026-05-19 16:40:45.924481	f
3	JHS	7	1		1st	Enrolled			Face to Face	2026-2027	2026-05-19 14:08:26.09439	2026-05-19 16:44:05.584109	t
21	SHS	11	5	Academic	1st	Enrolled	Humanities and Social Sciences,Science,Technology,Engineering and Mathematics,General Academic Strand		Face to Face	2026-2027	2026-05-19 14:08:26.09439	2026-05-19 16:47:47.041277	t
4	JHS	7	1		1st	Enrolled			Face to Face	2026-2027	2026-05-19 14:08:26.09439	2026-05-19 16:58:14.774256	t
5	JHS	7	1		1st	Enrolled			Face to Face	2026-2027	2026-05-19 14:08:26.09439	2026-05-19 16:59:13.64817	t
31	JHS	7	\N		1st	Pending			Face to Face	2026-2027	2026-05-19 17:00:08.243805	2026-05-19 17:00:08.243805	f
1	JHS	7	1		1st	Enrolled			Face to Face	2026-2027	2026-05-19 14:08:26.09439	2026-05-19 17:01:32.948349	t
\.


--
-- Data for Name: enrollment_mother; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.enrollment_mother (id, learner_id, mother_last_name, mother_first_name, mother_middle_name, mother_contact, mother_occupation) FROM stdin;
3	22					
5	2	cebu	cebu		154654965	
14	3					
2	21	cebu	cebu		09235664	
18	4	cebu	cebu		12345679	
24	5	cebu	cebu		02364789	
26	31	cebu	cebu		096236587979	
1	1	cebuuu	cebuuu		12135645646	
\.


--
-- Data for Name: enrollment_previous_school; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.enrollment_previous_school (id, learner_id, previous_grade_completed, previous_sy_completed, previous_school_attended) FROM stdin;
3	22			
5	2	10	6	marionhon
14	3			
2	21	10	2023-2024	cebu
18	4	6	2023-2024	marigondon
24	5	6	2023	cebu
26	31			
1	1	6	2023-2025	cebuuu
\.


--
-- Data for Name: enrollment_section; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.enrollment_section (id, name, grade, level, track, school_year, adviser_name, created_at) FROM stdin;
1	Rizal	7	JHS		2026-2027	Maria Santos	2026-05-19 14:08:26.067134
2	Bonifacio	8	JHS		2026-2027	Juan Dela Cruz	2026-05-19 14:08:26.067134
3	Mabini	9	JHS		2026-2027	Elena Rocha	2026-05-19 14:08:26.067134
4	Luna	10	JHS		2026-2027	Ricardo Dalisay	2026-05-19 14:08:26.067134
5	STEM - A	11	SHS	STEM	2026-2027	Grace Poe	2026-05-19 14:08:26.067134
6	TVL - HE	12	SHS	TVL	2026-2027	Franklin Drilon	2026-05-19 14:08:26.067134
\.


--
-- Data for Name: enrollment_shs_details; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.enrollment_shs_details (id, learner_id, track, semester, electives, tvl_major, learning_modality) FROM stdin;
\.


--
-- Data for Name: enrollment_student; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.enrollment_student (id, learner_id, student_lrn, student_has_lrn, student_psa_birth_cert, student_is_balik_aral, student_last_name, student_first_name, student_middle_name, student_extension_name, student_birthdate, student_age, student_sex, student_place_of_birth, student_mother_tongue, student_is_ip, student_is_four_ps, student_four_ps_id) FROM stdin;
6	6	406123000801	t		f	Bautista	Anna	Gomez		2013-03-22	13	F		Bisaya	f	f	
7	7	406123000802	t		f	Bascon	Gabriel	Vargas		2013-07-14	12	M		Bisaya	f	f	
8	8	406123000803	t		f	Bersabal	Michelle	Torres		2013-01-30	13	F		Bisaya	f	f	
9	9	406123000804	t		f	Caballero	Christian	Mendoza		2013-08-19	12	M		Bisaya	f	f	
10	10	406123000805	t		f	Cabrera	Ella	Flores		2013-10-12	12	F		Tagalog	f	f	
11	11	406123000901	t		f	CaÃ±ete	John Lloyd	Alvarez		2012-09-05	14	M		Bisaya	f	f	
12	12	406123000902	t		f	Custodio	Grace	Mercado		2012-05-12	14	F		Bisaya	f	f	
13	13	406123000903	t		f	Daan	Kenneth	Santiago		2012-12-01	13	M		Bisaya	f	f	
14	14	406123000904	t		f	Davide	Mary	Ramos		2012-02-18	14	F		Bisaya	f	f	
15	15	406123000905	t		f	Deiparine	James	Villanueva		2012-07-22	13	M		Bisaya	f	f	
16	16	406123001001	t		f	Dela Torre	Princess	Mendoza		2011-11-30	15	F		Bisaya	f	f	
17	17	406123001002	t		f	Diaz	Joshua	Castillo		2011-04-14	15	M		Bisaya	f	f	
18	18	406123001003	t		f	Echavez	Kimberly	Sayson		2011-08-09	15	F		Bisaya	f	f	
19	19	406123001004	t		f	Enriquez	Ryan	Perez		2011-01-25	15	M		Tagalog	f	f	
20	20	406123001005	t		f	Escalante	Stephanie	Omana		2011-06-03	15	F		Bisaya	f	f	
23	23	406123001103	t		f	Franza	Matthew	Dizon		2010-05-28	16	M		Bisaya	f	f	
24	24	406123001104	t		f	Gabunada	Nicole	Suarez		2010-12-05	15	F		Bisaya	f	f	
25	25	406123001105	t		f	Generalao	Justin	Abella		2010-03-20	16	M		Bisaya	f	f	
26	26	406123001201	t		f	Fernandez	Chloe	Villanueva		2009-07-19	17	F		Bisaya	f	f	
27	27	406123001202	t		f	Garciano	Angelo	Rosales		2009-04-02	17	M		Bisaya	f	f	
28	28	406123001203	t		f	Hermosa	Janine	Gutierrez		2009-11-13	16	F		Bisaya	f	f	
29	29	406123001204	t		f	Inocando	Patrick	Salazar		2009-08-27	17	M		Bisaya	f	f	
30	30	406123001205	t		f	Labra	Erica	Padilla		2009-01-05	17	F		Bisaya	f	f	
22	22	406123001102	t		f	Espinosa	Rachel	Jimenez		2010-09-11	16	F		Bisaya	f	f	
2	2	406123000702	t		f	Alcantara	Judy	Cruz		2014-02-10	12	F		Bisaya	f	f	
3	3	406123000703	t		f	Aquino	Paolo	Santos		2014-09-24	11	M		Tagalog	f	f	
21	21	406123001101	t		f	Esperanza	David	Tan		2010-01-14	16	M		Kapampangan	f	f	
4	4	406123000704	t		f	Aranas	Sarah	Gomez		2014-11-05	11	F		Bisaya	f	f	
5	5	406123000705	t		f	Bacalso	John	Reyes		2014-04-18	12	M		Bisaya	f	f	
56	31	119978566412	t	2024	f	cebu	cebu	cebu	cebu	2026-05-19	12	M	cebu	Cebuano	f	f	
1	1	406123000701	t		f	Abad	Mark	Castro		2014-06-15	12	M		Bisaya	f	f	
\.


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 1, true);


--
-- Name: bmi_bmirecord_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.bmi_bmirecord_id_seq', 30, true);


--
-- Name: enrollment_certification_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.enrollment_certification_id_seq', 6, true);


--
-- Name: enrollment_father_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.enrollment_father_id_seq', 29, true);


--
-- Name: enrollment_guardian_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.enrollment_guardian_id_seq', 29, true);


--
-- Name: enrollment_house_address_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.enrollment_house_address_id_seq', 30, true);


--
-- Name: enrollment_learner_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.enrollment_learner_id_seq', 31, true);


--
-- Name: enrollment_mother_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.enrollment_mother_id_seq', 29, true);


--
-- Name: enrollment_previous_school_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.enrollment_previous_school_id_seq', 29, true);


--
-- Name: enrollment_section_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.enrollment_section_id_seq', 6, true);


--
-- Name: enrollment_shs_details_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.enrollment_shs_details_id_seq', 1, false);


--
-- Name: enrollment_student_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.enrollment_student_id_seq', 59, true);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: bmi_bmirecord bmi_bmirecord_learner_id_school_year_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bmi_bmirecord
    ADD CONSTRAINT bmi_bmirecord_learner_id_school_year_key UNIQUE (learner_id, school_year);


--
-- Name: bmi_bmirecord bmi_bmirecord_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bmi_bmirecord
    ADD CONSTRAINT bmi_bmirecord_pkey PRIMARY KEY (id);


--
-- Name: enrollment_certification enrollment_certification_learner_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_certification
    ADD CONSTRAINT enrollment_certification_learner_id_key UNIQUE (learner_id);


--
-- Name: enrollment_certification enrollment_certification_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_certification
    ADD CONSTRAINT enrollment_certification_pkey PRIMARY KEY (id);


--
-- Name: enrollment_father enrollment_father_learner_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_father
    ADD CONSTRAINT enrollment_father_learner_id_key UNIQUE (learner_id);


--
-- Name: enrollment_father enrollment_father_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_father
    ADD CONSTRAINT enrollment_father_pkey PRIMARY KEY (id);


--
-- Name: enrollment_guardian enrollment_guardian_learner_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_guardian
    ADD CONSTRAINT enrollment_guardian_learner_id_key UNIQUE (learner_id);


--
-- Name: enrollment_guardian enrollment_guardian_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_guardian
    ADD CONSTRAINT enrollment_guardian_pkey PRIMARY KEY (id);


--
-- Name: enrollment_house_address enrollment_house_address_learner_id_address_type_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_house_address
    ADD CONSTRAINT enrollment_house_address_learner_id_address_type_key UNIQUE (learner_id, address_type);


--
-- Name: enrollment_house_address enrollment_house_address_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_house_address
    ADD CONSTRAINT enrollment_house_address_pkey PRIMARY KEY (id);


--
-- Name: enrollment_learner enrollment_learner_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_learner
    ADD CONSTRAINT enrollment_learner_pkey PRIMARY KEY (id);


--
-- Name: enrollment_mother enrollment_mother_learner_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_mother
    ADD CONSTRAINT enrollment_mother_learner_id_key UNIQUE (learner_id);


--
-- Name: enrollment_mother enrollment_mother_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_mother
    ADD CONSTRAINT enrollment_mother_pkey PRIMARY KEY (id);


--
-- Name: enrollment_previous_school enrollment_previous_school_learner_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_previous_school
    ADD CONSTRAINT enrollment_previous_school_learner_id_key UNIQUE (learner_id);


--
-- Name: enrollment_previous_school enrollment_previous_school_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_previous_school
    ADD CONSTRAINT enrollment_previous_school_pkey PRIMARY KEY (id);


--
-- Name: enrollment_section enrollment_section_name_grade_school_year_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_section
    ADD CONSTRAINT enrollment_section_name_grade_school_year_key UNIQUE (name, grade, school_year);


--
-- Name: enrollment_section enrollment_section_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_section
    ADD CONSTRAINT enrollment_section_pkey PRIMARY KEY (id);


--
-- Name: enrollment_shs_details enrollment_shs_details_learner_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_shs_details
    ADD CONSTRAINT enrollment_shs_details_learner_id_key UNIQUE (learner_id);


--
-- Name: enrollment_shs_details enrollment_shs_details_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_shs_details
    ADD CONSTRAINT enrollment_shs_details_pkey PRIMARY KEY (id);


--
-- Name: enrollment_student enrollment_student_learner_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_student
    ADD CONSTRAINT enrollment_student_learner_id_key UNIQUE (learner_id);


--
-- Name: enrollment_student enrollment_student_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_student
    ADD CONSTRAINT enrollment_student_pkey PRIMARY KEY (id);


--
-- Name: enrollment_student enrollment_student_student_lrn_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_student
    ADD CONSTRAINT enrollment_student_student_lrn_key UNIQUE (student_lrn);


--
-- Name: idx_bmi_learner; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_bmi_learner ON public.bmi_bmirecord USING btree (learner_id);


--
-- Name: idx_bmi_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_bmi_status ON public.bmi_bmirecord USING btree (bmi_status);


--
-- Name: idx_learner_grade; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_learner_grade ON public.enrollment_learner USING btree (grade);


--
-- Name: idx_learner_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_learner_status ON public.enrollment_learner USING btree (status);


--
-- Name: idx_section_grade; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_section_grade ON public.enrollment_section USING btree (grade);


--
-- Name: idx_student_lrn; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_student_lrn ON public.enrollment_student USING btree (student_lrn);


--
-- Name: bmi_bmirecord bmi_bmirecord_learner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bmi_bmirecord
    ADD CONSTRAINT bmi_bmirecord_learner_id_fkey FOREIGN KEY (learner_id) REFERENCES public.enrollment_learner(id) ON DELETE CASCADE;


--
-- Name: enrollment_certification enrollment_certification_learner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_certification
    ADD CONSTRAINT enrollment_certification_learner_id_fkey FOREIGN KEY (learner_id) REFERENCES public.enrollment_learner(id) ON DELETE CASCADE;


--
-- Name: enrollment_father enrollment_father_learner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_father
    ADD CONSTRAINT enrollment_father_learner_id_fkey FOREIGN KEY (learner_id) REFERENCES public.enrollment_learner(id) ON DELETE CASCADE;


--
-- Name: enrollment_guardian enrollment_guardian_learner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_guardian
    ADD CONSTRAINT enrollment_guardian_learner_id_fkey FOREIGN KEY (learner_id) REFERENCES public.enrollment_learner(id) ON DELETE CASCADE;


--
-- Name: enrollment_house_address enrollment_house_address_learner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_house_address
    ADD CONSTRAINT enrollment_house_address_learner_id_fkey FOREIGN KEY (learner_id) REFERENCES public.enrollment_learner(id) ON DELETE CASCADE;


--
-- Name: enrollment_learner enrollment_learner_section_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_learner
    ADD CONSTRAINT enrollment_learner_section_id_fkey FOREIGN KEY (section_id) REFERENCES public.enrollment_section(id) ON DELETE SET NULL;


--
-- Name: enrollment_mother enrollment_mother_learner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_mother
    ADD CONSTRAINT enrollment_mother_learner_id_fkey FOREIGN KEY (learner_id) REFERENCES public.enrollment_learner(id) ON DELETE CASCADE;


--
-- Name: enrollment_previous_school enrollment_previous_school_learner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_previous_school
    ADD CONSTRAINT enrollment_previous_school_learner_id_fkey FOREIGN KEY (learner_id) REFERENCES public.enrollment_learner(id) ON DELETE CASCADE;


--
-- Name: enrollment_shs_details enrollment_shs_details_learner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_shs_details
    ADD CONSTRAINT enrollment_shs_details_learner_id_fkey FOREIGN KEY (learner_id) REFERENCES public.enrollment_learner(id) ON DELETE CASCADE;


--
-- Name: enrollment_student enrollment_student_learner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollment_student
    ADD CONSTRAINT enrollment_student_learner_id_fkey FOREIGN KEY (learner_id) REFERENCES public.enrollment_learner(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict P9tS1pkhZs9Ox8PZO6UfCIZXYfON9uViJJ4SDc3KwEfgrGPRkVKipYDjXK5Pgq0

