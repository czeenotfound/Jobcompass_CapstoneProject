BEGIN;
--
-- Create model Skill
--
CREATE TABLE "skill_skill" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(255) NOT NULL UNIQUE, "is_validated" bool NOT NULL, "created_at" datetime NOT NULL);
COMMIT;
