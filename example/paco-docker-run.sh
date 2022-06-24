#!/bin/sh

#The XLS must be placed within the same folder as this script (from where the script runs).
XLS_FILE_NAME='UC.xlsx'

PACO_USERNAME="utilizador-universal@ua.pt"
#For a fully automated process you can fill your password below
#Watch out! It's an open text password!
#This is not mandatory - the password will be prompted as needed
#PACO_PASSWORD="" 


#Dry-run will run the script without actually changing anything
#You can force it here by setting the flag to True.
#You can also specify this inside the XLS planning sheet.
#Both need to be set False so the script finalizes the updates.
.
DRY_RUN="False"
#DRY_RUN="False"

BASE=$(pwd)

docker run --rm -i -t \
-p 4444:4444 -p 7900:7900 \
--mount type=bind,src=$BASE/.,dst=/data \
-e XLS_FULLPATH="/data/$XLS_FILE_NAME" \
-e PACO_USERNAME="$PACO_USERNAME" \
-e PACO_PASSWORD="$PACO_PASSWORD" \
-e DRY_RUN="$DRY_RUN" \
--shm-size="2g" rmarau/pacoautomationscript


