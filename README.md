# googleapps
Various scripts with Google Apps integration

gapps_scheduler.py - python app which interact with Google Form (based on Scheduler_xls document), 
reads entries from xls and notify user before 10 min of scheduled event via email and jabber.

You should have docs-8cb74cbd9fgs.json file used for OAuth with Google Docs in same directory where gapps_scheduler.py located.

Scheduler_xls columns legend: <br />
Column A (type = timestamp): When new entry created?  <br />
Column B (type = timestamp): When event should be done? <br />
Column C (type = text): What should be done? <br />
Column D (type = text): Comments, additional info. <br />
