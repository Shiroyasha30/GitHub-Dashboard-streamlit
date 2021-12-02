from datetime import date, datetime
# from numpy.core.fromnumeric import size
# from pandas.core.algorithms import unique
# needs to be installed separately
import streamlit as st
import pandas as pd
import numpy as np
import requests
# import json
# needs to be installed separately
import matplotlib.pyplot as plt
st.set_page_config(page_title='GitHub Dashboard', layout='wide')


# Dataset - Extracted at runtime from GitHub api
# api links in comments

st.title('GitHub Dashboard')

user=st.text_input('Enter GitHub username: ', value='Shiroyasha30')

# st.warning('Few usernames or repositories can even lead to unforeseen errors!!')


def br():
    st.markdown('<br>', True)


# Size 22 as year limit is set from 2000 and above
def yearlyPlot(years):
    yearCounts=[0]*22
    for i in years:
        yearCounts[i-2000]+=1

    fig = plt.figure(figsize=(18, 6), facecolor='grey')
    ax= fig.add_subplot(1, 1, 1)
    ax.plot(range(0, 22), yearCounts, '-o', color='black')
    title='Yearly Commits'
    ax.set_title(title)
    ax.set_xlabel('years')
    ax.set_ylabel('No of commits')
    ax.xaxis.set_ticks(np.arange(0, 23, 2))
    start, end = ax.get_ylim()
    ax.yaxis.set_ticks(np.arange(0, end, 1))
    ax.grid()
    ax.set_facecolor('grey')
    st.pyplot(fig)

def monthlyPlot(commitMonths):
    monthCounts=[0]*12
    for i in commitMonths:
        monthCounts[i]+=1

    fig = plt.figure(figsize=(18, 6), facecolor='grey')
    ax= fig.add_subplot(1, 1, 1)
    ax.plot(range(1, 13), monthCounts, '-o', color='black')
    title='Monthly Commits'
    ax.set_title(title)
    ax.set_xlabel('months')
    ax.set_ylabel('No of commits')
    ax.xaxis.set_ticks(np.arange(0, 13, 2))
    start, end = ax.get_ylim()
    ax.yaxis.set_ticks(np.arange(0, end, 1))
    ax.grid()
    ax.set_facecolor('grey')
    st.pyplot(fig)

def dailyPlot(dates):
    dateCounts=[0]*31
    for i in dates:
        dateCounts[i]+=1

    fig4 = plt.figure(figsize=(18, 6), facecolor='grey')
    ax4= fig4.add_subplot(1, 1, 1)
    ax4.plot(range(1, 32), dateCounts, '-o', color='black')
    title4='Daily Commits'
    ax4.set_title(title4)
    ax4.set_xlabel('Dates')
    ax4.set_ylabel('No of commits')
    ax4.xaxis.set_ticks(np.arange(0, 31, 2))
    start, end = ax4.get_ylim()
    ax4.yaxis.set_ticks(np.arange(0, end, 1))
    ax4.grid()
    ax4.set_facecolor('grey')
    st.pyplot(fig4)

# using github api to get repo details of any user:
# https://api.github.com/users/<username>/repos


@st.cache
def repoListLoader():
    repoURL='https://api.github.com/users/'+user+'/repos'
    repoList=requests.get(repoURL)
    return repoList


@st.cache
def commitLoader(repo):
    commitURL='https://api.github.com/repos/'+user+'/'+repo+'/commits'
    commits=requests.get(commitURL)
    commits=commits.json()
    return commits


def repoListPage():
    
    repoList = repoListLoader()
    repoList=repoList.json()
    if(st.checkbox('Show Repo List', value=False)):
        st.write(repoList)

    length=len(repoList)
    year=st.text_input('Year (greater than 1999) : ', value='2021')
    months=[]
    validRepo=[]
    for i in range(length):
        if(repoList[i]['created_at'][0:4]==year):
            # d=datetime.strptime(repoList[i]['created_at'][0:10], '%Y-%m-%d')
            m=int(repoList[i]['created_at'][5:7])
            months.append(m)
            validRepo.append(i)

    monthCounts=[0]*13
    for m in months:
        monthCounts[m]+=1


    if(len(validRepo)):
        plots=st.multiselect('Choose Plots: ', ['Repo per month', 'Size comparison', 'Languages used'])

# Bar graph for Repositories created per month that given year
        x, y, z=st.columns([5, 7, 5])

        fig=plt.figure(figsize=(8, 4), facecolor='grey')
        ax=fig.add_subplot(1, 1, 1)
        ax.bar(range(0, 13), monthCounts, color='green')
        ax.set_xlabel('Month')
        ax.set_ylabel('No of Repos')
        ax.set_title('Repositories created per month')
        ax.grid()
        ax.set_facecolor('grey')

        if('Repo per month' in plots):
            y.pyplot(fig)

        
        a, blank, b=st.columns([8, 1, 5])

    # Line Chart for size comparison of repositories

        fig1=plt.figure(figsize=(10, 5), facecolor='grey')
        ax1=fig1.add_subplot(1, 1, 1)
        sizes=[]
        for i in validRepo:
            sizes.append(repoList[i]['size'])
        ax1.plot(range(len(sizes)), sizes, '-o', color='darkorange')
        ax1.set_xlabel('Repository id')
        ax1.set_ylabel('Size of repository')
        ax1.set_title('Size of Repositories')
        ax1.grid()
        ax1.set_facecolor('grey')
        if('Size comparison' in plots):
            a.pyplot(fig1)

    # Pie chart for language comparison

        fig2=plt.figure(figsize=(10, 5), facecolor='grey')
        ax2=fig2.add_subplot(1, 1, 1)
        languages=[]
        for i in validRepo:
            if repoList[i]['language']:
                languages.append(repoList[i]['language'])
            else:
                languages.append('Unidentified')
        languages=np.array(languages)
        languageCounts=np.array(list(map(lambda x: languages.tolist().count(x), np.unique(languages))))
        ax2.pie(languageCounts, labels=np.unique(languages), autopct='%1.1f%%')
        ax2.set_title('Languages used in repositories')
        if('Languages used' in plots):
            b.pyplot(fig2)




# Commits


        br()
        st.sidebar.markdown(f'<br>{len(validRepo)} repositories available for {user}', True)
        br()

        names=[]
        for i in range(len(validRepo)):
            names.append(repoList[i]['name'])

        repo=st.sidebar.selectbox('Choose a repo', names)


# using github api to get commit details of a specific repository:
# https://api.github.com/repos/<username>/<reponame>/commits


        if(repo):
            commits=commitLoader(repo)

            dates=[]
            years=[]
            commitMonths=[]
            for i in range(len(commits)):
                dates.append(int(commits[i]['commit']['author']['date'][8:10]))
                commitMonths.append(int(commits[i]['commit']['author']['date'][5:7]))
                years.append(int(commits[i]['commit']['author']['date'][0:4]))

            yearsar=np.array(years)
            commitMonthsar=np.array(commitMonths)

            st.header(f'Commits in {repo}')
            st.subheader('Default commits view is chosen on the basis of commit frequency of each repository')

            c=0
            if(len(np.unique(yearsar))>1):
                # yearlyPlot(years)
                c=0
            elif(len(np.unique(commitMonthsar))>1):
                # monthlyPlot(commitMonths)
                c=1
            else:
                # dailyPlot(dates)
                c=2

            choice=st.radio('Choose commit view: ', ('Yearly', 'Monthly', 'Daily'), index=c)
            if(choice=='Yearly'):
                yearlyPlot(years)
            elif(choice=='Monthly'):
                monthlyPlot(commitMonths)
            else:
                dailyPlot(dates)

        if(st.checkbox('Show commit List', value=False)):
            st.write(commits)
    else:
        st.info('No Valid Repo available')





page=st.sidebar.selectbox('Page', ['Repo List'], index=0)
if(page=='Repo List'):
    repoListPage()
