
# coding: utf-8

# In[106]:


import glob
import datetime
import email.policy, email.parser
import pandas as pd

# TASK 1
# Calculate how many emails were sent from each sender address to each recipient.

path=r'C:\maildir\*\sent\*'
files = glob.glob(path)
df=pd.DataFrame(columns=['sender','recipient'],index=range(len(files)*5))#initialize dataframe
xstr = lambda s: '' if s is None else s #useful function
i=0
for file in files:
    # parse file
    f = open(file,'rb')
    headers = email.parser.BytesParser(policy=email.policy.default).parse(f)
    # message from
    sender=headers.get('From')
    # message to
    lista=xstr(headers.get('To')) + ', ' + xstr(headers.get('Cc')) + ', ' + xstr(headers.get('Bcc'))
    lista = lista.split(', ')
    lista = list(set(filter(None,lista)))
    # update dataframe
    for name in lista:
        df.loc[i]=[sender,name]
        i+=1

df=df.dropna()
ans=df.groupby(['sender','recipient'])['recipient'].agg({'count':'count'}).reset_index()
ans
    
    
    


# In[119]:


ans.sort_values('count',ascending=False).reset_index().loc[:,['sender','recipient','count']].to_csv('sent_count.csv')


# In[156]:


# TASK 2
# Calculate the average number of emails received per day per employee per day of week

path=r'C:\maildir\*\inbox\[0-99999]_'
files = glob.glob(path)
df2=pd.DataFrame(columns=['employee','d'],index=range(len(files)*5))#initialize dataframe
i=0
for file in files:
    # parse file
    f = open(file,'rb')
    headers = email.parser.BytesParser(policy=email.policy.default).parse(f)
    # employee name
    emp=file.split('maildir')[-1].split('\\')[1]
    # date
    tt=datetime.datetime.strptime(headers.get('Date').split(', ')[1], '%d %b %Y %H:%M:%S %z').date()
    # update dataframe
    df2.loc[i]=[emp,tt]
    i+=1

df2=df2.dropna()
ans2=df2.groupby(['employee','d'])['d'].agg({'val':'count'}).reset_index()
ans2


# In[162]:


# add zeros for the days that an employee doesn't receive mail
for dd in ans2.d.unique():
    for emp in ans2.employee.unique():
        if emp not in ans2.employee[ans2.d==dd]:
            ans2=ans2.append({'employee':emp,'d':dd,'val':0},ignore_index=True)
ans2


# In[164]:


ans2['day_of_week']=ans2.d.apply(lambda c: c.weekday())
ans2.groupby(['employee','day_of_week'])['val'].agg({'avg_count':'mean'}).reset_index().to_csv('inbox_avg_count.csv')

