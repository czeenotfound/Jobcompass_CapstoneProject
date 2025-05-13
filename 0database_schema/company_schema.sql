BEGIN;
--
-- Create model Employer
--
CREATE TABLE "company_employer" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "first_name" varchar(100) NOT NULL, "middle_name" varchar(100) NOT NULL, "last_name" varchar(100) NOT NULL, "suffix" varchar(10) NOT NULL, "employer_status" varchar(50) NULL, "about_me" text NULL, "facebook" varchar(200) NULL, "twitter" varchar(200) NULL, "github" varchar(200) NULL);
--
-- Create model Company
--
CREATE TABLE "company_company" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "company_name" varchar(100) NULL, "avatar" varchar(255) NOT NULL, "email" varchar(254) NULL, "phone" varchar(15) NULL, "website_url" varchar(200) NULL, "about_us" text NULL, "dateFounded" date NULL, "employee_count" integer unsigned NULL CHECK ("employee_count" >= 0), "tin_number" varchar(15) NULL, "bir_file" varchar(255) NOT NULL, "dti_file" varchar(255) NOT NULL, "facebook" varchar(200) NULL, "twitter" varchar(200) NULL, "github" varchar(200) NULL, "verification_status" varchar(20) NOT NULL, "is_verified" bool NOT NULL, "is_active" bool NOT NULL, "address_id" bigint NULL UNIQUE REFERENCES "address_address" ("id") DEFERRABLE INITIALLY DEFERRED, "industry_id" bigint NULL REFERENCES "industry_industry" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "company_company_industry_id_8997df25" ON "company_company" ("industry_id");
COMMIT;
