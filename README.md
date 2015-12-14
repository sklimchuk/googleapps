# googleapps
Various scripts with Google Apps integration

gapps_scheduler.py - python app which interact with Google Form (based on Scheduler_xls document), 
reads entries from xls and notify user before 10 min of scheduled event via email and jabber.
<br />
How to use gapps_scheduler.py: <br />
1. Get your own OAuth Credentials: http://gspread.readthedocs.org/en/latest/oauth2.html <br />
You should have your docs-xxxx.json file used for OAuth with Google Docs in same directory where gapps_scheduler.py located. <br />
2. Prepare your Google Form (in script: Scheduler_xls) based on Excel file. <br />
Scheduler_xls columns legend: <br />
Column A (type = timestamp): When new entry created?  <br />
Column B (type = timestamp): When event should be done? <br />
Column C (type = text): What should be done? <br />
Column D (type = text): Comments, additional info. <br />
3. Update gapps_scheduler.py with your docs-xxxx.json and Google Form xls. <br />
4. Use :)
