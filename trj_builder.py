# By Fereshteh ASGARI
import json
import datetime, time
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import scipy.stats as ss 
import scipy as sp
import numpy
import powerlaw
from scipy.stats.kde import gaussian_kde
from scipy.stats import norm
from numpy import linspace,hstack
from pylab import plot,show,hist
import scipy
fmt="%Y%m%dT%H%M%S"



#trajectory_builder merges activities of one day to extract real trajectories
#Input: Data of one day
#Output: list of trajectories of corresponding day and list of iter-activity time
def trajectory_builder(day):
    #First, remove the activities without tracking points
    cc=1
    n_day={}
    delta_t=15
    for activity in range(1,len(day)+1):
        if len(day[str(activity)]["trackPoints"]) > 0 :
            n_day[str(cc)]=day[str(activity)]
            cc+=1
    day=n_day
    #Now, building the tarjectories
    #print len(day)
    time_diff=[]
    total_traj=[]
    distance_list=[] # stores the distance of each extracted trajectories
    distnc=0
    if day!={}  :
        trj=day['1']["trackPoints"]
        distnc=day['1']["distance"]
    else:
       pass
    for r in range(2,len(day)+1):
        #print'r in itereation',r, len(day)
        #print day[str(r)]["s_time"]
        s_t=day[str(r)]["s_time"]
        e_t=day[str(r-1)]["e_time"]
        s_t= datetime.datetime.strptime(s_t.split('+')[0],fmt)
        e_t= datetime.datetime.strptime(e_t.split('+')[0],fmt)
        ##print s_t, r
        diff= s_t-e_t
        if (diff.days== -1) &(diff.seconds/60 == 1439):
            time_diff.append(0)
        else:
            time_diff.append(diff.seconds/60)
        if ((diff.days==0)&(diff.seconds/60 < delta_t)) or ((diff.days== -1) &(diff.seconds/60 == 1439)):
            #if len(day[str(r+1)]["trackPoints"]) > 0 :
                trj.extend(day[str(r)]["trackPoints"])
                distnc+=day[str(r)]["distance"]
                if (r==len(day)) :
                    total_traj.append(trj)
                    distance_list.append(distnc/1000)###the new added one :)))
                    #print 'case1, last one'
        elif (r==len(day)):  #means it's the end of trajectory and end of activities of the day
            distance_list.append(distnc/1000)
            total_traj.append(trj)
            total_traj.append(day[str(r)]["trackPoints"])
            distance_list.append(day[str(r)]["distance"]/1000)
            #print 'Special case'
        else: #means it's the end of trajectory bu there are still activities to be parserd
            distance_list.append(distnc/1000)
            total_traj.append(trj)
            trj=day[str(r)]["trackPoints"]
            distnc=day[str(r)]["distance"]
           
    t=len(total_traj)
    return distance_list,total_traj,time_diff


