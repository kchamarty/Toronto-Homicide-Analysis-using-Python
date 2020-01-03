# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 11:06:52 2019

@author: KC
"""
# step1. Import all the required Libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
import re 
import matplotlib.patches as mpatches
  
# Function to remove ids from neighbour hoods 
def Clean(neighbourhood): 
    # Search for space followed byopening bracket in the name 
    # followed by any characters repeated any number of times until closed bracket 
    if re.search(' \(.*\)', neighbourhood): 
  
        # Extract the position of beginning of pattern 
        pos = re.search(' \(.*\)', neighbourhood).start() 
  
        # return the cleaned name 
        return neighbourhood[:pos] 
  
    else: 
        # if clean up needed return the same name 
        return neighbourhood 
    
    
plt.interactive(False)

# Step2. Read the required  data 
homicide_file=r'C:\Users\KC\Documents\Metro College\python\project\data\gtacrime\Homicide.csv'

df_homicide=pd.read_csv(homicide_file)
df_homicide.info() # get the summary of the data
df_homicide.columns
df_homicide.Occurrence_Date.describe()
df_homicide.Occurrence_year.describe()
df_homicide.Division.describe()
df_homicide.Neighbourhood.describe()
df_homicide.X.describe()
df_homicide.Y.describe()
df_homicide=df_homicide[['Occurrence_year', 'Division',
       'Homicide_Type', 'Occurrence_Date', 'Neighbourhood']] # getting only few columns for analysis

# Analysis Q1: Total number of Homicides by year  Viz: Bar Graph
dfa_homicide_yronly=df_homicide[['Occurrence_year']]
dfa_homicide_yronly['Homicide_count']=1
dfa_homi_yronly_cnt=dfa_homicide_yronly.groupby(['Occurrence_year']).count()
dfa_homi_yronly_cnt.plot.bar()


# Analysis Q2: Total number of Homicides by Divisions Viz: Pie Chart
dfa_homicide_divonly=df_homicide[['Division']]
dfa_homicide_divonly['Homicide_count']=1

dfa_homicide_divonly_cnt=dfa_homicide_divonly.groupby('Division',as_index=False).count()
explode=np.zeros(len(dfa_homicide_divonly_cnt.Division))
explode[6]=0.2
labels=dfa_homicide_divonly_cnt.Division
plt.pie(dfa_homicide_divonly_cnt.Homicide_count, labels= dfa_homicide_divonly_cnt.Division,              
        explode=explode, counterclock=False, shadow=True)
plt.title('Number of Homicides by Divisions',fontsize=30,fontstyle='oblique')
plt.legend(labels,loc=10)
plt.show()


# Analysis Q3: Total number of Homicides by  Neighbourhoods for top two divisions Viz: Bar
top2div=list(dfa_homicide_divonly_cnt[dfa_homicide_divonly_cnt['Homicide_count'].rank(ascending=0, method='min')<3].Division)
dfa_homicide_top2=df_homicide[(df_homicide.Division == top2div[0])|(df_homicide.Division == top2div[1])]
dfa_homicide_divnhonly=dfa_homicide_top2[['Division','Neighbourhood']]

for i in range(len(dfa_homicide_divnhonly.Neighbourhood)):
    dfa_homicide_divnhonly.iloc[i,1]=Clean(dfa_homicide_divnhonly.iloc[i,1])

dfa_homicide_divnhonly['Homicide_count']=1
dfa_homicide_divnhonly_cnt=dfa_homicide_divnhonly.groupby(['Division','Neighbourhood'],as_index=False).count()
color_array = ['r'] * len(dfa_homicide_divnhonly_cnt.Division[dfa_homicide_divnhonly_cnt.Division==top2div[0]]) + ['orange'] * len(dfa_homicide_divnhonly_cnt.Division[dfa_homicide_divnhonly_cnt.Division==top2div[1]])
plt.bar(dfa_homicide_divnhonly_cnt.Neighbourhood,dfa_homicide_divnhonly_cnt.Homicide_count, color=color_array)
plt.xticks(rotation=90) 
plt.xlabel('Neighbourhoods', fontsize=20)
plt.ylabel('Homicide_count', fontsize=20)
plt.title('Homicides per Neighbourhood in top two Districts',fontsize=30)
red_patch = mpatches.Patch(color='red', label=top2div[0])
orange_patch = mpatches.Patch(color='orange', label=top2div[1])
plt.legend(handles=[red_patch,orange_patch])
plt.show()

# Analysis Q4: Total number of Homicides by Homocide Type Viz: Bar Graph
dfa_homicide_tyonly=df_homicide[['Homicide_Type']]
dfa_homicide_tyonly['Homicide_count']=1
dfa_homi_tyonly_cnt=dfa_homicide_tyonly.groupby(['Homicide_Type']).count()
dfa_homi_tyonly_cnt.plot.bar()


# Analysis Q5 : count of homicides grouped by year and type 
dfa_homicide_yrnty=df_homicide[['Occurrence_year','Homicide_Type']]
dfa_homicide_yrnty['Homicide_count_yrandtp']=1
dfa_homicide_yrnty_cnt=dfa_homicide_yrnty.groupby(['Occurrence_year','Homicide_Type'],as_index=False).count()
dfa_homicide_yrnty_cnt_pvt=dfa_homicide_yrnty_cnt.pivot(index='Occurrence_year',columns='Homicide_Type',values='Homicide_count_yrandtp')
years=list(dfa_homicide_yrnty_cnt_pvt.index)
plt.figure(figsize=(10,8))
x=np.arange(len(years))
color=['r','b','g']
width=[0.0 ,0.25,0.50]
for i in range(3):
    plt.bar(x + width[i], dfa_homicide_yrnty_cnt_pvt.iloc[:,i] , color=color[i], label=dfa_homicide_yrnty_cnt_pvt.columns[i], width=0.25)
plt.xticks(x,years)
plt.legend(fontsize=10)
plt.title("Homicides by Year", fontsize =20)
plt.show()



# Analysis Q6 : Homicide counts in months and type

df_homicide['month'] = pd.DatetimeIndex(df_homicide['Occurrence_Date']).month
df_homicide_month=df_homicide[['month','Homicide_Type']]
df_homicide_month['hcount']=1
df_homicide_month_cnt=df_homicide_month.groupby(['month','Homicide_Type'],as_index=False).count()
df_homicide_month_cnt=df_homicide_month_cnt.pivot(index='month',columns='Homicide_Type',values='hcount')
import calendar
month_name=[]
month_abr=[]
for month_idx in range(1, 13):
    month_name.append(calendar.month_name[month_idx])
    month_abr.append(calendar.month_abbr[month_idx])
months=list(df_homicide_month_cnt.index)
plt.figure(figsize=(10,8))
x=np.arange(len(months))
color=['r','b','g']
width=[0.0,0.25,0.50]
for i in range(3):
    plt.bar(x + width[i], df_homicide_month_cnt.iloc[:,i] , color=color[i], label=df_homicide_month_cnt.columns[i], width=0.25)
plt.xticks(x,month_abr)
plt.legend(fontsize=10)
plt.title("Homicides by Months", fontsize =20)
plt.show()

# Analysis  : Time wise - But it is always between 4 and 5:00AM
df_homicide['time'] = pd.DatetimeIndex(df_homicide['Occurrence_Date']).time
df_homicide['time'].describe()

# Analysis Q7 : Has the Gun Violence increased or deceased in 2018 from 2004
df_homicide_gvrt=df_homicide[['Occurrence_year','Homicide_Type']]


#Separating 2004 and 2018 records
df_homicide_gvrt_2004=df_homicide_gvrt[df_homicide_gvrt.Occurrence_year==2004]
df_homicide_gvrt_2018=df_homicide_gvrt[df_homicide_gvrt.Occurrence_year==2018]
#Separating shooting records
df_homicide_gvrt_cnt_2004_sh=df_homicide_gvrt_2004[df_homicide_gvrt_2004.Homicide_Type=='Shooting'].drop('Homicide_Type',axis=1)
df_homicide_gvrt_cnt_2018_sh=df_homicide_gvrt_2018[df_homicide_gvrt_2018.Homicide_Type=='Shooting'].drop('Homicide_Type',axis=1)

#counting shootings for 2004 and 2018 separately
df_homicide_gvrt_cnt_2004_sh['shcount']=1
df_homicide_gvrt_cnt_2018_sh['shcount']=1
df_homicide_gvrt_cnt_2004_sh_cnt= df_homicide_gvrt_cnt_2004_sh.groupby('Occurrence_year',as_index=False).count()
df_homicide_gvrt_cnt_2018_sh_cnt= df_homicide_gvrt_cnt_2018_sh.groupby('Occurrence_year',as_index=False).count()

#counting all homicides for 2004 and 2018 separately
df_homicide_gvrt_2004['alcount']=1
df_homicide_gvrt_2018['alcount']=1
df_homicide_gvrt_2004_all_cnt =df_homicide_gvrt_2004.groupby('Occurrence_year',as_index=False).count().drop('Homicide_Type',axis=1)
df_homicide_gvrt_2018_all_cnt =df_homicide_gvrt_2018.groupby('Occurrence_year',as_index=False).count().drop('Homicide_Type',axis=1)

#calculating the ratio
gunviolence_ratio_2004=float(df_homicide_gvrt_cnt_2004_sh_cnt.shcount/df_homicide_gvrt_2004_all_cnt.alcount)
gunviolence_ratio_2018=float(df_homicide_gvrt_cnt_2018_sh_cnt.shcount/df_homicide_gvrt_2018_all_cnt.alcount)

print('Gun violence ratio in 2004 is {} and Gun violence ratio in 2018 is{}'.format(gunviolence_ratio_2004,gunviolence_ratio_2018))          

# Analysis Q8 : Top 5 safe neighbourhoods to live in

df_homicide_safenh=df_homicide[['Neighbourhood','Division']]
df_homicide_safenh['hcount']=1
df_homicide_safenh_cnt=df_homicide_safenh.groupby(['Division','Neighbourhood'],as_index=False)['hcount'].count()
top2div_safe=list(dfa_homicide_divonly_cnt[dfa_homicide_divonly_cnt['Homicide_count'].rank(ascending=1, method='min')<3].Division)
df_top2div_safenh=df_homicide_safenh_cnt[(df_homicide_safenh_cnt.Division==top2div_safe[0])|(df_homicide_safenh_cnt.Division==top2div_safe[1])]
top6div_safenh=df_top2div_safenh[df_top2div_safenh['hcount'].rank(ascending=1, method='first')<6].Neighbourhood

df_homicide_safenh_cnt[df_homicide_safenh_cnt['hcount'].rank(ascending=1, method='min')<6].Neighbourhood


# Read the Shape File 
gta_division_shape=r'C:\Users\KC\Documents\Metro College\python\project\data\gtacrime\Police_Divisions\Police_Divisions.shp'
map_gta_df = gpd.read_file(gta_division_shape)  # data type is a GEOdataframe

df_homicide_analysis=df_homicide[['Division','Occurrence_year']]
df_homicide_analysis['hcount']=1
df_homicide_analysis_yrdiv=df_homicide_analysis.groupby(['Occurrence_year','Division'],as_index=False).count()

# Analysis Q9 : Geo Plotting of Homicides in the year 2004 Per Division 
df_homicide_analysis_2004=df_homicide_analysis_yrdiv[df_homicide_analysis_yrdiv.Occurrence_year==2004]

merged_div = map_gta_df.set_index('DIV').join(df_homicide_analysis_2004.set_index('Division')) # join the geodataframe with the cleaned up csv dataframe
merged_div.hcount[merged_div['hcount'].isnull()]=0
variable = 'hcount' # set a variable that will call whatever column we want to visualise on the map
vmin, vmax = 120, 220  # set the range for the choropleth

fig, ax = plt.subplots(1, figsize=(15, 8)) # create figure and axes for Matplotlib
ax1=merged_div.plot(column=variable, cmap='OrRd', linewidth=1.2, ax=ax, edgecolor='0.8')
for i, geo in merged_div.centroid.iteritems():
    ax1.annotate(s=i, xy=[geo.x, geo.y], color="black")
    # show the subplot
    ax1.figure
ax.axis('off')
ax.set_title('Homicides in Toronto in 2004', fontdict={'fontsize': '25', 'fontweight' : '3'})
plt.show()


fig.savefig(r'C:\Users\KC\Documents\Metro College\python\project\data\gtacrime\CrimesInTororno_2004.png', dpi=300)

#Analysis Q10: Everything from here.
# Geo Plotting of Homicides in the year 2004 to 2005 Per Division 
df_homicide_analysis_2004_05=df_homicide_analysis_yrdiv[(df_homicide_analysis_yrdiv.Occurrence_year==2004)|(df_homicide_analysis_yrdiv.Occurrence_year==2005)]
df_homicide_analysis_2004_05=df_homicide_analysis_2004_05.iloc[0:,1:3]
df_homicide_analysis_2004_05_sum=df_homicide_analysis_2004_05.groupby('Division',as_index=False).sum()
merged_div = map_gta_df.set_index('DIV').join(df_homicide_analysis_2004.set_index('Division')) # join the geodataframe with the cleaned up csv dataframe
merged_div.hcount[merged_div['hcount'].isnull()]=0
variable = 'hcount' # set a variable that will call whatever column we want to visualise on the map
vmin, vmax = 120, 220  # set the range for the choropleth

fig, ax = plt.subplots(1, figsize=(15, 8)) # create figure and axes for Matplotlib
ax1=merged_div.plot(column=variable, cmap='OrRd', linewidth=1.2, ax=ax, edgecolor='0.8')
for i, geo in merged_div.centroid.iteritems():
    ax1.annotate(s=i, xy=[geo.x, geo.y], color="black")
    # show the subplot
    ax1.figure
ax.axis('off')
ax.set_title('Homicides in Toronto in 2004 and 2005', fontdict={'fontsize': '25', 'fontweight' : '3'})
plt.show()


fig.savefig(r'C:\Users\KC\Documents\Metro College\python\project\data\gtacrime\CrimesInTororno_2005.png', dpi=300)

# Geo Plotting of Homicides in the year 2004 to 2006 Per Division 
df_homicide_analysis_2004_06=df_homicide_analysis_yrdiv[(df_homicide_analysis_yrdiv.Occurrence_year==2004)|(df_homicide_analysis_yrdiv.Occurrence_year==2005)|(df_homicide_analysis_yrdiv.Occurrence_year==2006)]
df_homicide_analysis_2004_06=df_homicide_analysis_2004_06.iloc[0:,1:3]
df_homicide_analysis_2004_06_sum=df_homicide_analysis_2004_06.groupby('Division',as_index=False).sum()
merged_div = map_gta_df.set_index('DIV').join(df_homicide_analysis_2004.set_index('Division')) # join the geodataframe with the cleaned up csv dataframe
merged_div.hcount[merged_div['hcount'].isnull()]=0
variable = 'hcount' # set a variable that will call whatever column we want to visualise on the map
vmin, vmax = 120, 220  # set the range for the choropleth

fig, ax = plt.subplots(1, figsize=(15, 8)) # create figure and axes for Matplotlib
ax1=merged_div.plot(column=variable, cmap='OrRd', linewidth=1.2, ax=ax, edgecolor='0.8')
for i, geo in merged_div.centroid.iteritems():
    ax1.annotate(s=i, xy=[geo.x, geo.y], color="black")
    # show the subplot
    ax1.figure
ax.axis('off')
ax.set_title('Homicides in Toronto from 2004 to 2006', fontdict={'fontsize': '25', 'fontweight' : '3'})
plt.show()


fig.savefig(r'C:\Users\KC\Documents\Metro College\python\project\data\gtacrime\CrimesInTororno_2006.png', dpi=300)

# Geo Plotting of All Homicides Per Division 

df_analysis = df_homicide[['Division','Occurrence_year','Homicide_Type', 'Hood_ID', 'Neighbourhood']]
df_homi_analysis=df_homicide[['Division']]
df_homi_analysis['count']=1
df_homi_analysis_cnt=df_homi_analysis.groupby('Division',as_index=False).count()

merged_div = map_gta_df.set_index('DIV').join(df_homi_analysis_cnt.set_index('Division')) # join the geodataframe with the cleaned up csv dataframe
merged_div.head()
variable = 'count' # set a variable that will call whatever column we want to visualise on the map
vmin, vmax = 120, 220  # set the range for the choropleth

fig, ax = plt.subplots(1, figsize=(15, 8)) # create figure and axes for Matplotlib
ax1=merged_div.plot(column=variable, cmap='OrRd', linewidth=1.2, ax=ax, edgecolor='0.8')
for i, geo in merged_div.centroid.iteritems():
    ax1.annotate(s=i, xy=[geo.x, geo.y], color="black")
    # show the subplot
    ax1.figure
ax.axis('off')
ax.set_title('Homicides in Toronto From 2004 to 2018', fontdict={'fontsize': '25', 'fontweight' : '3'})
plt.show()
fig.savefig(r'C:\Users\KC\Documents\Metro College\python\project\data\gtacrime\CrimesInTororno_2004-2018.png', dpi=300)






