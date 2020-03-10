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
dept = 'dtm'
p.figure()
for i_bin in range(nbins):
    xvalues = [datetime.datetime.strptime(d,"%m/%d/%y").date() for d in weeks]
    p.plot(weeks,np.array(cpuhours[dept])[:,i_bin],label=bin_labels[i_bin])
p.xlabel('week')
p.ylabel('cpu hours')
p.legend(loc='best')


### Plot cpu hours vs N cpu
p.figure()
for i_bin in range(nbins):
    #p.plot(np.zeros(nweeks)+cpu_bins[i_bin],np.array(cpuhours[dept])[:,i_bin].astype(float),'o',label=dept)
    ydata=np.array(cpuhours[dept])[:,i_bin].astype(float)
    #p.errorbar(cpu_mids[i_bin],np.mean(ydata),label=dept,yerr=np.std(ydata))
    p.bar(cpu_mids[i_bin],np.mean(ydata),width=cpu_mids[i_bin]-cpu_bins[i_bin],align='center')
p.legend(loc='best')
