#!/bin/sh

PYTHON_SCRIPT_PATH="."

#Export to environment 
#Exports are now coming from docker run

#export XLS_FULLPATH="$(pwd)/POO2122.xlsx"
#export PACO_USERNAME="marau@ua.pt"
#export PACO_PASSWORD="pwd"
#export DRY_RUN="True"
#export DRY_RUN="True"

python3 ${PYTHON_SCRIPT_PATH}/main.py

