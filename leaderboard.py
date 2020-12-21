import sys
import numpy as np
import pandas as pd

sys.path.append('..//scoreware-site//util//runner//')
import runnerutils

print('processing Stockade 15k and 5k results')

data=pd.read_csv('results/2020-12-20 2020 MVP Health Care Virtual Stockade-athon 15K and 5K Hudson Mohawk Road Runners Club.csv')

age_grader5=pd.read_csv('agegrade5.csv')
age_grader15=pd.read_csv('agegrade15.csv')

'''
male_best=age_grader['male'].max()*60
female_best=age_grader['female'].max()*60
'''

def timeToSeconds(time):
    temp=time.split('.') 
    temp=temp[0].split(':')
    print(len(temp))
    try:
        if (len(temp)==3):
            return 3600*int(temp[0])+60*int(temp[1])+int(temp[2])
        elif (len(temp)==2):
            return 60*int(temp[0])+int(temp[1])
        elif (len(temp)==1):
            return 60*int(temp[0])
    except:
        return 100000
    
def ageGrade(age, gender, timeSeconds, age_grader):
    if gender=='f':
        timeBest=age_grader['female'].iloc[age]*60
    else:
        timeBest=age_grader['male'].iloc[age]*60
    
    return timeBest/timeSeconds

data['seconds']=data['Time'].apply(lambda x: timeToSeconds(x))
#data=data.drop('Event registration date',axis=1)
data=data.drop('e-Mail', axis=1)

data5=data[data.Distance=='5k']
data15=data[data.Distance=='15k']

def wrangleData(data, age_grader):
    data=data.sort_values(by='seconds')
    data.Gender=data.Gender.apply(lambda x: x.lower())
    data.Gender=data.Gender.apply(lambda x: x[0])
    data['age_grade']=data.apply(lambda x:ageGrade(x.Age, x.Gender, x.seconds, age_grader),axis=1)
    data.age_grade=data.age_grade*100
    data.age_grade=data.age_grade.round(2)
    data=data.drop('seconds',axis=1)
    data=data.drop('Distance',axis=1)
    data=data.drop('State',axis=1)
    data=data.reset_index(drop=True)
    data.index+=1
    data=data.fillna("")

    return data

data5=wrangleData(data5,age_grader5);
print(data5)

data15=wrangleData(data15,age_grader15);
print(data15)

def createMarkdown(data, category):
    markdown="![image](hmrrc_65h.jpg) ![image](MVP-1.jpg)  ![image](FF_Logo_Stacked_7-150x118.jpg)  \n\n"
    #markdown='[Click here for age groups](https://bnorthan.github.io/Virtual15K_5K/'+category+'age)  \n\n'
    #markdown+='[Click here for age graded leaders](https://bnorthan.github.io/Virtual15K_5K/'+category+'age)  \n\n'
    markdown+=data.to_markdown()
    fname='leaderboard'+category+'.md'
    out_file=open(fname, "w")
    out_file.write(markdown)
    out_file.close()
    
def countTeams(data, columnName, title):
    teams=data[columnName].value_counts();
    teams=teams.drop('')
    teams=teams.rename('Number')
    markdown=title+'  \n'
    markdown+=teams.to_markdown()
    return markdown
    
createMarkdown(data5, '5k')
createMarkdown(data15, '15k')

home="![image](hmrrc_65h.jpg) ![image](MVP-1.jpg)  ![image](FF_Logo_Stacked_7-150x118.jpg)  \n\n"  
home+="## Virtual 15K and 5k Leaderboard  \n"
home+="[Click here for 5k results](https://bnorthan.github.io/Virtual15K_5K/leaderboard5k)  \n"  
home+="[Click here for 15k results](https://bnorthan.github.io/Virtual15K_5K/leaderboard15k)  \n"
home+="\n\n"

home+=countTeams(data15, 'Company', '## Number participants for each company in 15K  \n')
home+='  \n  \n'
home+=countTeams(data15, 'Team', '## Number participants for each team in 15K  \n')
home+='  \n  \n'
home+=countTeams(data5, 'Company', '## Number participants for each company in 5K  \n')
home+='  \n  \n'
home+=countTeams(data5, 'Team', '## Number participants for each team in 5K  \n')
home+='  \n  \n'

fname='leaderboard.md'
out_file=open(fname, "w")
out_file.write(home)
out_file.close()
    
'''

fname='leaderboard.md'
out_file=open(fname, "w")
out_file.write(markdown)
out_file.close()

csvname='leaderboard.csv'
data.to_csv(csvname)

sort_by_age_grade=data.sort_values(by='age_grade',ascending=False)
fname='agegrade.md'
out_file=open(fname, "w")

sort_by_age_grade=sort_by_age_grade.reset_index(drop=True)
sort_by_age_grade.index+=1

out_file.write(sort_by_age_grade.to_markdown())
out_file.close()

data["age_cat"]=data.Age.apply(lambda x:runnerutils.ageToCat_0_80_10(x))
age_cats=['0_9','10_19','20_29','30_39','40_49','50_59','60_69','70_79','80+']

females=data[data.Gender=='f']
males=data[data.Gender=='m']

age_markdown='';

for age in age_cats:
    age_markdown+='## Female '+age+'  \n\n'
    temp=females[females.age_cat==age]
    
    temp=temp.drop('age_cat',1)
    if (temp.shape[0]>0):
        age_markdown+=temp.to_markdown()+'  \n\n'
    else:
        age_markdown+='  \n\n'
        
    age_markdown+='## Male '+age+'  \n\n'
    temp=males[males.age_cat==age]
    
    temp=temp.drop('age_cat',1)
    if (temp.shape[0]>0):
        age_markdown+=temp.to_markdown()+'  \n\n'
    else:
        age_markdown+='  \n\n'
    
 
out_file=open('age.md', "w")
out_file.write(age_markdown)
out_file.close()
'''

    




