#!/bin/bash

apps=("users" "admin" "resume" "company" "job" "industry" "skill" "address" "otp_email" "sessions" "auth")

for app in "${apps[@]}"
do
  echo "Generating SQL for $app..."
  python manage.py sqlmigrate "$app" 0001_initial > "${app}_schema.sql"
done
