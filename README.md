# Paco Automation Script

Set of helper scripts to automate the export of Sumários and Presenças from your favorite Excel to PACO.
If you don't understand this, then this project may not be of interest for you.

## Disclaimer

* This project is for personal use only.
* It has been tested on a limited number of scenarios. It may certainly not cover all edge cases of the platform.
* It's highly dependant on the DOM provided by the platform.
* The DOM or the internal navigation flow may change and break the script.
* You are free to download, change or run it as you please, but take it *at your own risk!*

## Getting Started

1. Download the example folder
2. Populate the xlsx file accordingly
    * Do not change the sheet's name or the structure of the file (columns and heading lines)
    * It's important that you fill the UC_code and TP_code correctly.
    * If you don't know the codes, run the script with emty cells and check the error to find the codes.
3. Update *paco-docker-run.sh* with your personal data
4. It's highly recommended a dry-run test beforehand
5. Run the script from a terminal: ```sh paco-docker-run.sh```
    * The first time you run the script takes some additional time to download the image and setup the docker container
6. At any time during execution you may see the automated process:
    * Open your favorite browser and follow: http://localhost:7900
        * password: secret

### Good to Know

The Excel file holds two tables (Planeamento and PresençaAulas). They are relationally dependent on the *Aula* number. It's your responsability to maintain consistency.
Each time you run the script:
 * It scans the Excel file to find *Sumários* not yet published.
 * Of those, it checks whether the session ocuured or not (if at least one student attends that *Aula*).
 * Updates PACO and stamps the Excel file with "PUBLISHED" status for that class session.
    * Don't manually edit the Status column yourself
    
## Platforms:
- Macos
- Linux
- Windows (should work running the script from powershell)

## Installation

* You'll need Docker installed.
* Terminal and Browser.
