### create_logs.py ###
### Purpose: create memex usage logs using sreport.
### jobs will run in sequence (not at all once)
### NOTE: need to run this in python3!  in memex shel: "module load python/3.6.7"

import subprocess
from dateutil import rrule
import datetime
import json

weeks = []
for dt in rrule.rrule(rrule.WEEKLY, dtstart=datetime.datetime(2019,4,1),until=datetime.datetime.now()):
    deltat = datetime.timedelta(days=6)
    weeks.append([dt,dt+deltat])  #[start,end]

### parse sreport data.
sedcmd = "| sed -e 's/[(]/\|/g' -e 's/[)]//g'"
#startdate = "03/09/20"
logfile = "all.log"
groupings = "2,25,49,121"
cpuhours = {'week':[],'dge':[],'dpb':[],'dtm':[],'emb':[],'gl':[],'obs':[],'hq':[]}
numjobs = {'week':[],'dge':[],'dpb':[],'dtm':[],'emb':[],'gl':[],'obs':[],'hq':[]}

### Loop through weeks
for week in weeks:
    startdate = week[0].strftime("%m/%d/%y")
    enddate = week[1].strftime("%m/%d/%y")
    print(week,startdate,enddate)
    header_opt = " " #"-n"
    str1 = "sudo sreport job SizesByAccount Grouping="+groupings+" -t HourPer --parsable "+header_opt+" start="+startdate+" end="+enddate+" "+sedcmd
    result = subprocess.run(str1,shell=True,check=True,stdout=subprocess.PIPE)
    lines = result.stdout.decode().split('\n')
    header = lines[4].split('|')
    skiplines = 4  #skip if there's a header.
    cpuhours['week'].append([startdate,enddate])
    for line in lines[skiplines+1:-1]:
        dept=line.split('|')[1]
        group1=line.split('|')[2]
        group1p=line.split('|')[3]
        group2=line.split('|')[4]
        group2p=line.split('|')[5]
        group3=line.split('|')[6]
        group3p=line.split('|')[7]
        group4=line.split('|')[8]
        group4p=line.split('|')[9]
        group5=line.split('|')[10]
        group5p=line.split('|')[11]
        cpuhours[dept].append([group1,group2,group3,group4,group5])

    str2 = "sudo sreport job SizesByAccount PrintJobCount Grouping="+groupings+" -t HourPer --parsable "+header_opt+" start="+startdate+" end="+enddate+" "+sedcmd
    result = subprocess.run(str2,shell=True,check=True,stdout=subprocess.PIPE)
    lines = result.stdout.decode().split('\n')
    header = lines[4].split('|')
    skiplines = 4  #skip if there's a header.
    numjobs['week'].append([startdate,enddate])
    for line in lines[skiplines+1:-1]:
        dept=line.split('|')[1]
        group1=line.split('|')[2]
        group2=line.split('|')[3]
        group3=line.split('|')[4]
        group4=line.split('|')[5]
        group5=line.split('|')[6]
        numjobs[dept].append([group1,group2,group3,group4,group5])


### save to file
with open('cpuhours.json','w') as json_file:
    json.dump(cpuhours,json_file)
with open('numjobs.json','w') as json_file:
    json.dump(numjobs,json_file)
with open('header.json','w') as json_file:
    json.dump(header,json_file)
    
print('done')
