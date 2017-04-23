from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, gui #import some libraries from PsychoPy
from psychopy import *
from psychopy.constants import *  # things like STARTED, FINISHED
import random #import some libraries from python
import array
import numpy
import os  # handy system and path functions
import pylab

files = gui.fileOpenDlg('.')
if not files:
    core.quit()

#get the data from all the files
allIntensities, allResponses = [],[]
combinedInten = [1,2,3,4,5,6,7]
combinedCorrResp = [0,0,0,0,0,0,0]
combinedIncorrResp = [0,0,0,0,0,0,0]
combinedResp = [0,0,0,0,0,0,0]
finalResp = []
finalInten = []
for thisFileName in files:
    thisDat = misc.fromFile(thisFileName)
    allIntensities.append(thisDat.intensities)
    allResponses.append(thisDat.data)
    print 'intensities: ',thisDat.intensities
    print len(thisDat.intensities)
    for i in range(0,len(thisDat.intensities)):
        if thisDat.intensities[i]> 7:
            thisDat.intensities[i] = 7
    for i in range(0,len(thisDat.intensities)):
        if thisDat.data[i] == 1:
            combinedCorrResp[thisDat.intensities[i]-1] += 1
        else:
            combinedIncorrResp[thisDat.intensities[i]-1] += 1
intsToBeDeleted = []
for i in range(1,8):
    tmp1 = combinedCorrResp[i-1]+combinedIncorrResp[i-1]
    print 'tmp1',tmp1
    if tmp1 != 0:
        combinedResp[i-1] = combinedCorrResp[i-1]/tmp1
    else:
        intsToBeDeleted.append(i)

for i in range(0,7):
    add = 1
    for j in range(0,len(intsToBeDeleted)):
        if combinedInten[i] == intsToBeDeleted[j]:
            add = 0
    if add == 1:
        finalInten.append(combinedInten[i])
        finalResp.append(combinedResp[i])
    
import locale
locale.setlocale(locale.LC_NUMERIC, 'C')
#plot each staircase
#pylab.subplot(121)
colors = 'brgkcmbrgkcm'
#lines, names = [],[]
#for fileN, thisStair in enumerate(allIntensities):
    #lines.extend(pylab.plot(thisStair))
    #names = files[fileN]
    #pylab.plot(thisStair, label=files[fileN])
#pylab.legend()

#get combined data
print 'allintentisites ', allIntensities, 'allResponses ',allResponses
#combinedInten, combinedResp, combinedN = \
#             data.functionFromStaircase(allIntensities, allResponses,6)

#fit curve - in this case using a Weibull function
guess= [7,2]
#fit curve - in this case using a Weibull function
#fit = data.FitFunction('weibullYN',combinedInten, combinedResp, \
#guess = guess)
print 'finalInten',finalInten, 'finalResp',finalResp#,'combinedN',combinedN
fit = data.FitFunction('weibullYN',finalInten, finalResp, \
guess = guess)
#fit = data.FitWeibull(finalInten,finalResp)#,guess=guess)
#guess = guess)
#guess=[0.2, 0.5])
smoothInt = pylab.arange(0,10,0.5)
smoothResp = fit.eval(smoothInt)
thresh = int(fit.inverse(0.8))
thresh99 = int(fit.inverse(0.99))
thresh80 = int(fit.inverse(0.80))


print 'thresholds: ',thresh99, thresh80

#plot curve
pylab.subplot(122)
pylab.plot(smoothInt, smoothResp, 'o')
#pylab.plot([thresh, thresh],[0,0.8],'--'); pylab.plot([0, thresh],\
#[0.8,0.8],'--')
pylab.title('threshold = %0.3f' %(thresh))
#plot points
#pylab.plot(combinedInten, combinedResp, 'o')
pylab.ylim([0,1.2])

pylab.show()