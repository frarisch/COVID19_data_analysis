"""
Plot Corona data
... to enable data download uncomment the download at beginning

by frarisch, 30.10.2020
"""
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
from matplotlib.ticker import MultipleLocator

#import urllib.request
#url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
#urllib.request.urlretrieve(url,"owid-covid-data.csv")


plt.close('all')

file = r'owid-covid-data.csv'
df = pd.read_csv(file)
#print (df)
df.info()
header = df[1:1]
#print(header)

data = pd.read_csv(file, usecols = ['location','date','new_cases','new_deaths','population'])
#print (data)
data.info()
locations = data.loc[:, 'location']
new_cases = data.loc[:, 'new_cases']
new_deaths = data.loc[:, 'new_deaths']
date = data.loc[:, 'date']
population = data.loc[:, 'population']

# choose country
# EU + Switzerland
#countries_name = 'EU_Switzerland'
#countries = ['Austria','Belgium','Bulgaria','Croatia','Cyprus','Czech Republic','Denmark','Estonia','Finland','France','Germany','Greece','Hungary','Italy','Latvia','Lithuania','Luxembourg','Malta','Netherlands','Poland','Portugal','Ireland','Romania','Slovakia','Slovenia','Spain','Sweden','Switzerland']
#countries_name = 'central_europe' 
#countries = ['Austria','Czech Republic','Germany','Hungary','Poland','Slovakia','Slovenia','Switzerland']
countries_name = 'EU_parts' 
countries = ['Germany', 'Austria', 'Czech Republic', 'Italy', 'United Kingdom', 'France']

for n_days in [7,14]: # rolling sum of n days
    exp_days = n_days
    n_fit = 2; # n times n_days for fit
    dstart = dt.datetime(2020,3,1)
    dend = dt.datetime.now()+dt.timedelta(days=exp_days)
    
    leg1 = []
    leg2 = []
    fig, ax = plt.subplots(2,1)
    fig.set_size_inches(10,10)
    
    for i in countries:
        #print(i)
        idx = locations[locations.str.match(i)].index
        incidence = new_cases[idx].rolling(n_days).sum() / population[idx[1]] * 100000
        deaths = new_deaths[idx].rolling(n_days).sum() / population[idx[1]] * 100000
        dates = pd.to_datetime(date[idx])
        
        leg1.append(i + ' : ' + str((pd.eval(incidence.tail(1)).astype(int))[0]))
        leg2.append(i + ' : ' + str(round((pd.eval(deaths.tail(1)).astype(float))[0],1)))
        
        # extrapolate data
        p1, = ax[0].plot_date(dates[n_days:],incidence[n_days:],'-')
        p2, = ax[1].plot_date(dates[n_days:],deaths[n_days:],'-')
        
        x_data = pd.to_numeric(dates[n_days:]).tail(n_fit*n_days)
        
        y_incidence = incidence[n_days:].tail(n_fit*n_days)
        y_deaths = deaths[n_days:].tail(n_fit*n_days)
           
        startdate = pd.to_numeric(dates[n_days:]).tail(1)
        enddate = pd.to_datetime(x_data).tail(1)+np.timedelta64(exp_days,'D')
        new_dates = np.linspace(startdate,pd.to_numeric(enddate))
        
        fit1 = np.polyfit(x_data, np.log10(y_incidence), 1)
        fit2 = np.polyfit(x_data, np.log10(y_deaths), 1)
        y_incidence_exp = 10**np.polyval(fit1,new_dates)
        y_deaths_exp = 10**np.polyval(fit2,new_dates)
        
        ax[0].plot_date(pd.to_datetime(new_dates),y_incidence_exp,':',color = p1.get_color(),label='_nolegend_')
        ax[1].plot_date(pd.to_datetime(new_dates),y_deaths_exp,':',color = p2.get_color(),label='_nolegend_')
        
        
    ax[0].set_title(str(n_days)+' days incidence per 100.000')
    ax[0].xaxis.set_minor_locator(MultipleLocator())
    ax[0].grid(which='major', color='k', linestyle='-', linewidth=0.2)
    ax[0].grid(which='minor', color='k', linestyle='-', linewidth=0.05)
    ax[0].legend(leg1)  
    ax[0].set_xlim([dstart, dend])
        
    ax[1].set_title(str(n_days)+' days deaths per 100.000')
    ax[1].xaxis.set_minor_locator(MultipleLocator())
    ax[1].grid(which='major', color='k', linestyle='-', linewidth=0.2)
    ax[1].grid(which='minor', color='k', linestyle='-', linewidth=0.05)
    ax[1].legend(leg2) 
    ax[1].set_xlim([dstart, dend])
     
    plt.savefig(countries_name+'_'+str(n_days)+'days.png',bbox_inches='tight', dpi=150)
    plt.savefig(countries_name+'_'+str(n_days)+'days.eps',bbox_inches='tight')

    ax[0].set_yscale('log')
    ax[0].set_ylim([1, 1e4])
    ax[1].set_yscale('log')
    ax[1].set_ylim([0.01, 100])
    plt.savefig(countries_name+'_'+str(n_days)+'days_log.png',bbox_inches='tight', dpi=150)
    plt.savefig(countries_name+'_'+str(n_days)+'days_log.eps',bbox_inches='tight')


