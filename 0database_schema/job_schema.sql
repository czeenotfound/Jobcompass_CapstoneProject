BEGIN;
--
-- Create model Application
--
CREATE TABLE "job_application" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "submit_date" datetime NOT NULL);
--
-- Create model ApplicationStatus
--
CREATE TABLE "job_applicationstatus" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "status" varchar(20) NOT NULL, "status_date" datetime NOT NULL, "feedback" text NOT NULL);
--
-- Create model Conversation
--
CREATE TABLE "job_conversation" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL);
--
-- Create model Feedback
--
CREATE TABLE "job_feedback" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "feedback_type" varchar(20) NOT NULL, "content" text NOT NULL, "feedback_date" datetime NOT NULL);
--
-- Create model Interview
--
CREATE TABLE "job_interview" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "interview_date" datetime NULL, "interview_type" varchar(50) NULL, "interviewer" varchar(100) NULL, "notes" text NULL);
--
-- Create model Job
--
CREATE TABLE "job_job" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(100) NOT NULL, "salary_display_type" varchar(10) NULL, "currency" varchar(3) NOT NULL, "salary_fixed" integer unsigned NULL CHECK ("salary_fixed" >= 0), "salary_min" integer unsigned NULL CHECK ("salary_min" >= 0), "salary_max" integer unsigned NULL CHECK ("salary_max" >= 0), "salary_mode" varchar(10) NULL, "job_description" text NULL, "use_company_location" bool NOT NULL, "employment_job_type" varchar(20) NOT NULL, "location_job_type" varchar(20) NOT NULL, "posted_date_time" datetime NOT NULL, "is_available" bool NOT NULL);
--
-- Create model Job_Benefits
--
CREATE TABLE "job_job_benefits" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "bene_name" varchar(300) NOT NULL);
--
-- Create model Job_Education
--
CREATE TABLE "job_job_education" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "education_level" varchar(20) NULL, "degree" varchar(100) NOT NULL);
--
-- Create model Job_Experience
--
CREATE TABLE "job_job_experience" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "exp_type" varchar(10) NOT NULL, "exp_name" varchar(300) NOT NULL, "exp_years" integer NULL, "min_exp_years" integer NULL, "max_exp_years" integer NULL, "exp_description" text NOT NULL);
--
-- Create model Job_IdealCandidates
--
CREATE TABLE "job_job_idealcandidates" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "ideal_name" varchar(300) NOT NULL);
--
-- Create model Job_Responsibilities
--
CREATE TABLE "job_job_responsibilities" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "res_name" varchar(300) NOT NULL);
--
-- Create model JobFair
--
CREATE TABLE "job_jobfair" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(100) NOT NULL, "url_location" varchar(200) NULL, "description" text NOT NULL, "fair_event_held" varchar(20) NOT NULL, "start_date" date NULL, "end_date" date NULL, "start_time" time NULL, "end_time" time NULL, "contact_email" varchar(254) NULL, "contact_phone" varchar(15) NOT NULL, "max_attendees" integer NULL, "application_starts" date NULL, "application_deadline" date NULL, "image" varchar(255) NOT NULL, "is_featured" bool NOT NULL, "is_active" bool NOT NULL, "posted_date" datetime NOT NULL);
--
-- Create model JobFairRegistration
--
CREATE TABLE "job_jobfairregistration" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "submit_date" datetime NOT NULL);
--
-- Create model Message
--
CREATE TABLE "job_message" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "content" text NOT NULL, "timestamp" datetime NOT NULL, "is_read" bool NOT NULL);
--
-- Create model Notification
--
CREATE TABLE "job_notification" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "message" text NOT NULL, "sent_date" datetime NOT NULL, "is_read" bool NOT NULL);
--
-- Create model Offer
--
CREATE TABLE "job_offer" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "salary_display_type" varchar(10) NULL, "currency" varchar(3) NOT NULL, "salary_fixed" integer unsigned NULL CHECK ("salary_fixed" >= 0), "salary_min" integer unsigned NULL CHECK ("salary_min" >= 0), "salary_max" integer unsigned NULL CHECK ("salary_max" >= 0), "salary_mode" varchar(10) NULL, "notes" text NULL, "benefits" text NULL, "offer_date" date NULL, "expiration_date" date NULL);
--
-- Create model RequiredSkill
--
CREATE TABLE "job_requiredskill" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "skill_name" varchar(50) NOT NULL);
--
-- Create model SaveJob
--
CREATE TABLE "job_savejob" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "save_date" datetime NOT NULL);
COMMIT;
