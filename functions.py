import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import pandas as pd
import math as m
import numpy as np

def percents(df,value,name):
    sums = df.groupby('survey')[value].sum()
    temp = df.copy()
    for index, row in df.iterrows():
        temp.loc[index,name] = row[value] / sums[row.survey] * 100

    return temp

def percents_disorders(df,num_respondents,value,name):
    temp = df.copy()
    for index, row in df.iterrows():
        temp.loc[index,name] = row[value] / num_respondents * 100

    return temp

def percents_2_levels(df,value,name,groupby1,groupby2):
    sums = df.groupby([groupby1,groupby2])[value].sum()
    temp = df.copy()
    for index, row in df.iterrows():
        temp.loc[index,name] = row[value] / sums[row[groupby1],row[groupby2]] * 100

    return temp

def percents_2_levels_disorders(df,num_respondents,value,name,groupby):
    sums = num_respondents.groupby(groupby)[value].sum()
    temp = df.copy()
    for index, row in df.iterrows():
        temp.loc[index,name] = row[value] / sums[row[groupby]] * 100

    return temp

def barplot_all_years(data,x,y,colour):
    fig, ax = plt.subplots(figsize=(8,8))
    sns.set_style("white")
    sns.despine(left=True, bottom=True)
    plt.tight_layout()
    ax = sns.barplot(data, x=x, y=y, color=colour)
    ax.set_title('Number of Respondents per Survey')
    ax.bar_label(ax.containers[0])
    ax.set(xlabel=None, ylabel=None, yticks=[])

def barplot_per_year_vals_pers(data,x,y,years,xlabel,title,topylabel,bottomylabel):
    fig, axes = plt.subplots(len(y),len(years), figsize=(18,10), sharey='row')

    fig.suptitle(title)
    sns.despine(left=True)  
    

    for i, row in enumerate(axes):
        for j, ax in enumerate(row):
            sns.barplot(ax=ax, x=data[data.survey == years[j]][x], y=data[data.survey == years[j]][y[i]], palette='deep')
            ax.set(xlabel=None,yticklabels=[])
            index = 0
            for _, row in data[data.survey == years[j]].iterrows():
                if row[y[i]] > 0:
                    if i == 0:
                        if row[y[i]] < 50:
                            ax.text(index, row[y[i]] + 10, f'{row[y[i]]:.0f}', ha='center', color='black')
                        else:
                            ax.text(index, row[y[i]] - 50, f'{row[y[i]]:.0f}', ha='center', color='white')
                    else:
                        if row[y[i]] < 5:
                            ax.text(index, row[y[i]] + 1, f'{row[y[i]]:.0f}', ha='center', color='black')
                        else:
                            ax.text(index, row[y[i]] - 4, f'{row[y[i]]:.0f}', ha='center', color='white')
                index += 1
            if i == 0:
                ax.set(title=years[j])

    
    axes[0][0].set(ylabel=topylabel)
    axes[1][0].set(ylabel=bottomylabel)
    axes[1][2].set(xlabel=xlabel)

def barplot_err(data,x,y,title,yerr,xlabel,ylabel):
    fig, ax = plt.subplots(1,1, figsize=(6,6), sharey=True)

    fig.suptitle(title)
    sns.despine(left=True)  
    plt.tight_layout()

    data.plot(ax=ax,x=x, y=y, yerr=yerr, kind='bar', legend=False, capsize=7, color=sns.color_palette('deep'),width=0.8)
    ax.set(xlabel=xlabel,ylabel=ylabel)
    ax.grid(axis='x')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    ax.set_yticklabels([])

    index = 0
    for _, row in data.iterrows():
        if row[y] > 0:
            ax.text(index, row[y] * 0.6, f'{row[y]:.0f}', ha='center', color='white')
                
                
        index += 1

def barplot_per_year_err(data,x,y,years,title,yerr,xlabel,ylabel):
    fig, axes = plt.subplots(1,len(years), figsize=(13,4), sharey=True)

    fig.suptitle(title)
    sns.despine(left=True)  

    for j, ax in enumerate(axes):
        data[data.survey == years[j]].plot(ax=ax,x=x, y=y, yerr=yerr, kind='bar', legend=False, capsize=3, color=sns.color_palette('deep'),width=0.8)
        ax.set(xlabel=None)
        ax.grid(axis='x')
        ax.set(title=years[j])
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        
    
    axes[len(years)-1].set(xlabel=xlabel)
    axes[0].set(ylabel=ylabel)
    sns.set_palette('deep')

def barplot_per_diagnosis_err(data,x,y,diagnosis,title,yerr,xlabel,ylabel):
    fig, axes = plt.subplots(1,len(diagnosis), figsize=(13,4), sharey=True)

    fig.suptitle(title)
    sns.despine(left=True)  

    for j, ax in enumerate(axes):
        data[data.diagnosis == diagnosis[j]].plot(ax=ax,x=x, y=y, yerr=yerr, kind='bar', legend=False, capsize=3, color=sns.color_palette('deep'),width=0.8)
        ax.set(xlabel=None)
        ax.grid(axis='x')
        ax.set(title=diagnosis[j])
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        
    
    axes[len(diagnosis)-1].set(xlabel=xlabel)
    axes[0].set(ylabel=ylabel)
    sns.set_palette('deep')        
    

def stack_barplots(data_1,data_2,title):
    fig, (ax1, ax2) = plt.subplots(2,1, figsize=(8,8))

    sns.set_palette('deep')
    data_1.plot(stacked=True, kind='bar', ax=ax1)
    data_2.plot(stacked=True, kind='bar', ax=ax2, legend=False)

    ax1.set(ylabel='Number of Respondents')
    ax2.set(ylabel='Percentage of Respondents')
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=0)
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=0)
    sns.despine(left=True)
    ax1.legend_.set_title(None) 
    ax1.set_yticklabels([])
    ax2.set_yticklabels([])
    ax1.set_xlabel(None)
    ax2.set_xlabel(None)
    ax1.grid(axis='x')
    ax2.grid(axis='x')
    fig.suptitle(title);

    for ax, data in zip([ax1,ax2],[data_1,data_2]):
        index = 0
        for y, row in data.iterrows():
            cs = 0
            for item in row:
                cs += item
                if ax == ax2:
                    if item < 10:
                        ax.text(index, cs + 2, f'{item:.0f}', ha='center', color='black')
                    else:
                        ax.text(index, cs - (item * 0.6), f'{item:.0f}', ha='center', color='white')
                else:
                    if item < 70:
                        ax.text(index, cs + 20, f'{item:.0f}', ha='center', color='black')
                    elif item <= 125:
                        ax.text(index, cs - (item * 0.8), f'{item:.0f}', ha='center', color='white')
                    else:
                        ax.text(index, cs - (item * 0.6), f'{item:.0f}', ha='center', color='white')
            index += 1

def confidence_interval(data,proportion,civ=0.95):
    Z = stats.norm.ppf(1 - (1-civ)/2)
    for index, row in data.iterrows():
        prevalence = row[proportion] / 100
        ci = m.sqrt(prevalence*(1-prevalence)/data.loc[index,'number'].sum()) * Z
        data.loc[index,f'{proportion}_err'] = ci * 100
        
    return data

def confidence_interval_disorder(data,proportion,num_respondents,civ=0.95):
    Z = stats.norm.ppf(1 - (1-civ)/2)
    for index, row in data.iterrows():
        prevalence = row[proportion] / 100
        ci = m.sqrt(prevalence*(1-prevalence)/num_respondents) * Z
        data.loc[index,f'{proportion}_err'] = ci * 100
        
    return data

def confidence_interval_2_level(data,proportion,number,groupby1,groupby2,civ=0.95):
    sums = data.groupby([groupby1,groupby2])[number].sum()
    Z = stats.norm.ppf(1 - (1-civ)/2)
    for index, row in data.iterrows():
        prevalence = row[proportion] / 100
        ci = m.sqrt(prevalence*(1-prevalence)/sums[row[groupby1],row[groupby2]]) * Z
        data.loc[index,f'{proportion}_err'] = ci * 100
       
    return data

def confidence_interval_2_level_disorders(data,proportion,num_respondents,number,groupby,civ=0.95):
    sums = num_respondents.groupby(groupby)[number].sum()
    Z = stats.norm.ppf(1 - (1-civ)/2)
    for index, row in data.iterrows():
        prevalence = row[proportion] / 100
        ci = m.sqrt(prevalence*(1-prevalence)/sums[row[groupby]]) * Z
        data.loc[index,f'{proportion}_err'] = ci * 100
       
    return data

groups=['Under 25','26-35','36-45','46-55','Over 55']

