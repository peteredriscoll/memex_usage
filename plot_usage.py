import json
import numpy as np
import matplotlib.pyplot as p
import matplotlib.dates as mdates
import datetime
p.ion()

with open('cpuhours.json') as json_file:
    cpuhours=json.load(json_file)
with open('numjobs.json') as json_file:
    numjobs=json.load(json_file)
with open('header.json') as json_file:
    header=json.load(json_file)

weeks=np.array(cpuhours['week'])[:,0]  #start of weeks
nweeks=len(weeks)
#hourspercpu = cpuhours/numjobs

nbins=5
bin_labels = header[2:2+nbins]
cpu_bins = [1,24,48,120,121]
cpu_mids = np.zeros(nbins)
for i in range(nbins-1): cpu_mids[i]=np.mean(cpu_bins[i:i+1])
cpu_mids[nbins-1]=np.mean([121,3e3])
bin_colors=['blue','green','orange','purple','pink']
dept_sym=['o','square']

### Loop through depts.
dept = 'dtm'
i_dept = 0
p.figure()
ax=p.gca()
formatter = mdates.DateFormatter("%m")#-%d")
ax.xaxis.set_major_formatter(formatter)
locator = mdates.DayLocator()
ax.xaxis.set_major_locator(locator)
for i_bin in range(nbins):
    xvalues = [datetime.datetime.strptime(d,"%m/%d/%y").date() for d in weeks]
    p.plot(xvalues,np.array(cpuhours[dept])[:,i_bin].astype(float),label=bin_labels[i_bin])
p.xlabel('week')
p.ylabel('cpu hours')
p.legend(loc='best')


### Plot cpu hours vs N cpu
p.figure()
for i_bin in range(nbins):
    p.plot(np.zeros(nweeks)+cpu_bins[i_bin],np.array(cpuhours[dept])[:,i_bin].astype(float),dept_sym[i_dept],label=bin_labels[i_bin],color=bin_colors[i_bin])
    ydata=np.array(cpuhours[dept])[:,i_bin].astype(float)
    #p.errorbar(cpu_mids[i_bin],np.mean(ydata),label=dept,yerr=np.std(ydata))
    #p.bar(cpu_mids[i_bin],np.mean(ydata),width=cpu_mids[i_bin]-cpu_bins[i_bin],align='center')
p.legend(loc='best')



### Compute ave length of a run in a week
i_bin=0
avenumjobs_bin = np.array(numjobs[dept])[:,i_bin].astype(float)*cpu_bins[i_bin]
jobhours = np.array(cpuhours[dept])[:,i_bin].astype(float)/avenumjobs_bin
p.figure()
p.plot(jobhours,avenumjobs_bin,'o')
p.xlabel('job hours')
p.ylabel('N jobs (ave)')
