
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


#This problem seeks to assign tasks(rows) to workers(columns) based on some cost represented in the data frame
#The problem assumes that each worker should be assigned one task, and each task should be assigned one worker


# In[3]:


costmatrix=pd.read_excel('AssignmentProblem10by10.xlsx')


# In[4]:


costmatrix


# In[5]:


def greedy(df):
    """
    Takes a cost matrix as a data frame
    Greedily assigns the cheapest available row to each column from left to right.
    Assumes that each row can be assigned to one column and vice versa
    Returns a list of the assignments in the same order as the columns of the data frame
    """
    soln=[]
    for i in df.columns:
        soln.append(df.drop(soln)[i][df[i]==min(df.drop(soln)[i])].index.tolist()[0])
    return soln


# In[6]:


#On second thought, maybe a dictionary is more appropriate
def greedyDict(df):
    """
    Takes a cost matrix and greedily assigns the cheapest available row to each column from left to right.
    Assumes that each row can be assigned to one column and vice versa
    Returns a dictionary with each column and the row that was assigned to it
    """
    soln={}
    for i in df.columns:
        soln.update({i:df.drop(list(soln.values()))[i][df[i]==min(df.drop(list(soln.values()))[i])].index.tolist()[0]})
    return soln


# In[7]:


#Now returning objective function value as well
def greedyDict2(df):
    """
    Takes a cost matrix and greedily assigns the cheapest available row to each column from left to right.
    Assumes that each row can be assigned to one column and vice versa
    Returns a dictionary with each column and the row that was assigned to it, as well as the total assignment cost
    """
    soln={}
    objfun=0
    for i in df.columns:
        soln.update({i:df.drop(list(soln.values()))[i][df[i]==min(df.drop(list(soln.values()))[i])].index.tolist()[0]})
        objfun+=df[i].loc[soln[i]]
    return soln,objfun


# In[8]:


greedyDict2(costmatrix)

