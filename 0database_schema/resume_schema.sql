BEGIN;
--
-- Create model Certification
--
CREATE TABLE "resume_certification" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL);
--
-- Create model Education
--
CREATE TABLE "resume_education" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "education_level" varchar(20) NULL, "degree" varchar(100) NOT NULL, "institution" varchar(100) NOT NULL, "graduation_date" date NULL);
--
-- Create model Experience
--
CREATE TABLE "resume_experience" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(100) NOT NULL, "company" varchar(100) NOT NULL, "start_date" date NULL, "end_date" date NULL, "description" text NOT NULL);
--
-- Create model Project
--
CREATE TABLE "resume_project" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(100) NOT NULL, "description" text NOT NULL, "url" varchar(200) NULL);
--
-- Create model Skill
--
CREATE TABLE "resume_skill" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(50) NOT NULL);
--
-- Create model SocialLink
--
CREATE TABLE "resume_sociallink" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "platform" varchar(50) NOT NULL, "url" varchar(200) NULL);
--
-- Create model Resume
--
CREATE TABLE "resume_resume" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "avatar" varchar(255) NOT NULL, "first_name" varchar(100) NOT NULL, "middle_name" varchar(100) NOT NULL, "last_name" varchar(100) NOT NULL, "suffix" varchar(10) NOT NULL, "about_me" text NOT NULL, "salary_display_type" varchar(10) NULL, "currency" varchar(3) NULL, "expt_salary_fixed" integer unsigned NULL CHECK ("expt_salary_fixed" >= 0), "expt_salary_min" integer unsigned NULL CHECK ("expt_salary_min" >= 0), "expt_salary_max" integer unsigned NULL CHECK ("expt_salary_max" >= 0), "expt_salary_mode" varchar(20) NULL, "job_position" varchar(150) NOT NULL, "location_job_type" varchar(20) NOT NULL, "employment_job_type" varchar(20) NOT NULL, "upload_resume" varchar(255) NOT NULL, "address_id" bigint NULL UNIQUE REFERENCES "address_address" ("id") DEFERRABLE INITIALLY DEFERRED, "industry_id" bigint NULL REFERENCES "industry_industry" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "resume_resume_industry_id_24ab6ee4" ON "resume_resume" ("industry_id");
COMMIT;
