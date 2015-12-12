# googleapps
Various scripts with Google Apps integration

gapps_scheduler.py - python app which interact with Google Form (based on Scheduler_xls document), 
reads entries from xls and notify user before 10 min of scheduled event via email and jabber.

Scheduler_xls columns legend:
Column A (type = timestamp): When new entry created? 
Column B (type = timestamp): When event should be done?
Column C (type = text): What should be done?
Column D (type = text): Comments, additional info.
