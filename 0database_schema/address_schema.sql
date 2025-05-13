BEGIN;
--
-- Create model Address
--
CREATE TABLE "address_address" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "country" varchar(100) NOT NULL, "countrypostal" varchar(100) NOT NULL, "region" varchar(100) NOT NULL, "city" varchar(100) NOT NULL, "street" varchar(255) NOT NULL);
COMMIT;
