import os
from parse_paco import PACO_UC
from parse_xls import Excel
import getpass

#Scan environment vars
DRY_RUN = os.getenv('DRY_RUN').lower()=="true" if os.getenv('DRY_RUN') is not None else True
EXCEL_PATH = os.getenv('XLS_FULLPATH')
PACO_USERNAME = os.getenv('PACO_USERNAME')
PACO_PASSWORD = os.getenv('PACO_PASSWORD')

if not PACO_USERNAME or not PACO_PASSWORD:
    print ("""\nThe script is running without a proper username/password input.
    You may type it in now, or ignore (Press <Enter>) - you'll be asked at the authentication portal)""")
    if not PACO_USERNAME:
        PACO_USERNAME = getpass.getuser("Username: ").rstrip()
    else:
        print(PACO_USERNAME)
    if not PACO_PASSWORD:
       PACO_PASSWORD = getpass.getpass("Password: ")

if not PACO_USERNAME or not PACO_PASSWORD:
    print("You will have to fill your credentials. Follow the URL above to open the Firefox instance!!!")


excel = Excel( nome = EXCEL_PATH )

#parse sumarios already marked as published - used for a consistency check in PACO
sumarios_published = list(excel.get_sumarios_marked_published())

#parse sumarios ready for publishing
sumarios_to_publish = list(excel.get_sumarios_to_publish_with_attendance_filled())

if not sumarios_to_publish:
    print("Well... there's nothing to update!")
    quit(0)
else:
    print("Will proceed for a total of {} sumário(s)".format(len(sumarios_to_publish)))

#for s in sumarios_to_publish: print(s.presencas_mec)
#for s in sumarios_to_publish: print(s.aula)
#print(sumarios_to_publish)
#print(sumarios_to_publish_aulas)
#quit()



PACO_UC_CODE = excel.get_uc_code()
PACO_TP_CODE = excel.get_tp_code()
DRY_RUN = DRY_RUN or excel.get_dry_run_bool() # Gets the dry_run flag embedded in the xls

if DRY_RUN: print("Dry run: The script runs without updating data.")

print ("Opening Firefox...")
with PACO_UC( uc_code=PACO_UC_CODE,
              tp_code=PACO_TP_CODE,
              username=PACO_USERNAME,
              password=PACO_PASSWORD,
              dry_run=DRY_RUN ) as paco:

    if paco.contar_sumarios() != len(sumarios_published):
        print("####### ERROR #######")
        print("The number of Sumários in XLS and PACO is inconsistent.")
        print("Perform a manual check...")
        print("It may be that multiple users are posting Sumários - This check may need to be reviewed.")
        quit()

    for sum in sumarios_to_publish:
        print ("Updating Aula {}...",format(sum.aula))
        paco.adicionar_sumario(sum)

    if not DRY_RUN:
        excel.update_status_published([s.aula for s in sumarios_to_publish])
    else:
        print("Dry Run: Not updating excel")
        