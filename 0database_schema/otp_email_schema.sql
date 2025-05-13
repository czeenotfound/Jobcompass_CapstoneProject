BEGIN;
--
-- Create model EmailDevice
--
CREATE TABLE "otp_email_emaildevice" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(64) NOT NULL, "confirmed" bool NOT NULL, "key" varchar(80) NOT NULL, "user_id" bigint NOT NULL REFERENCES "users_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "otp_email_emaildevice_user_id_0215c274" ON "otp_email_emaildevice" ("user_id");
COMMIT;
