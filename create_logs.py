import subprocess

### create_logs.py ###
### Purpose: create memex usage logs using sreport.
### jobs will run in sequence (not at all once)
### NOTE: need to run this in python3!

sedcmd = "| sed -e 's/[(]/\|/g' -e 's/[)]//g'"
startdate = "03/09/20"
#logfile = "030920.log"
logfile = "all.log"
header_opt = "-n"
groupings = "2,25,49"
str1 = "echo "+startdate+" >> "+logfile
str2 = "sudo sreport job SizesByAccount Grouping="+groupings+" -t HourPer --parsable "+header_opt+" start="+startdate+" "+sedcmd+" >> "+logfile
print('starting')
subprocess.run(str1,shell=True,check=True)
subprocess.run(str2,shell=True,check=True)
print('done')
