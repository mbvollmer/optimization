
# coding: utf-8

# # Assignment using Greedy Algorithms

# #### Here I will implement various greedy approaches to task assignment based on a data frame of costs, for my purposes I assumed that rows will be assigned to columns, but the inverse can be accomplished by just transposing the data frame.

# In[2]:


import pandas as pd


# In[3]:


costmatrix=pd.read_excel('AssignmentProblem10by10.xlsx')


# In[4]:


costmatrix


# ### Simple greedy assignment, moving from left to right

# In[46]:


def greedy(df):
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


# ### Absolute Minimum Assignment

# In[47]:


def findMin(df):
    """
    Takes a cost matrix and scans through all possible assignments to find the absolute lowest cost match for one worker
    and one job.
    Returns the minimum cost and a single entry dictionary with the column:row assignment pair.
    """
    locs = {}
    current_min = 9999999
    for i in df.columns:
        if min(df[i])<current_min:
            current_min = min(df[i])
            locs = {}
            locs.update({i:df[i][df[i]==min(df[i])].index.tolist()[0]})
    return current_min, locs


# In[21]:


def trueMinsFirst(df):
    """
    Instead of working sequentially from left to right like the previous algorithms, this algorithm finds the absolute
    minimum cost assignment in the data frame, makes that assignment and then repeats with the tasks and remaining people
    until there are none remaining.
    """
    soln = {}
    cost = 0
    for i in df.columns:
        assignment = findMin(df.drop(soln.values()).drop(soln.keys(),axis=1))
        soln.update(assignment[1])
        cost+=assignment[0]
    return soln, cost


# ### Swap Assignment

# In[25]:


def swapAssignment(df):
    """
    Takes a cost matrix and greedily assigns the cheapest available row to each column from left to right.
    Assumes that each row can be assigned to one column and vice versa
    After each assignment after the first, it checks if swapping the last assignment with the previous one will
        improve the objective function value
    Returns a dictionary with each column and the row that was assigned to it, as well as the total assignment cost
    """
    soln={}
    objfun=0
    for i in df.columns:
        soln.update({i:df.drop(list(soln.values()))[i][df[i]==min(df.drop(list(soln.values()))[i])].index.tolist()[0]})
        if len(soln)>1 and (df.loc[soln[i],i]+df.loc[soln[previous],previous])>(df.loc[soln[previous],i]+df.loc[soln[i],previous]):
            objfun-=df.loc[soln[previous],previous]
            temp = soln[previous]
            soln.update({previous:soln[i],i:temp})
            objfun+=df.loc[soln[previous],previous]
        
        objfun+=df[i].loc[soln[i]]
        previous=i
    return soln,objfun
    


# ##### Now to test the algorithms on our 10x10 cost matrix:

# In[50]:


results = {}


# In[54]:


r1 = greedy(costmatrix)
results.update({'left to right':r1[1]})
print(r1)


# In[55]:


r2 = trueMinsFirst(costmatrix)
results.update({'true mins first':r2[1]})
print(r2)


# In[56]:


r3 = swapAssignment(costmatrix)
results.update({'swap':r3[1]})
print(r3)


# In[57]:


results


# ### Moving on to 100x100 cost matrix

# ##### Need to clean it first...

# In[30]:


bigcostmatrix = pd.read_csv('AssignmentProblemTestData100.txt',delim_whitespace=True,header=None)


# In[31]:


bigcostmatrix.head(16)


# In[32]:


bigcostmatrix.shape


# In[33]:


bigcostmatrix.loc[0:7]


# In[34]:


test = pd.concat([bigcostmatrix.loc[0],bigcostmatrix.loc[1]])
list(test)


# In[35]:


i = 0
fixed = []
while i < bigcostmatrix.shape[0]-1:
    fixed.append(list(pd.concat([bigcostmatrix.loc[i],bigcostmatrix.loc[i+1],bigcostmatrix.loc[i+2],bigcostmatrix.loc[i+3],
                            bigcostmatrix.loc[i+4],bigcostmatrix.loc[i+5],bigcostmatrix.loc[i+6],bigcostmatrix.loc[i+7]])))
    i+=8


# In[36]:


fixedbigcostmatrix = pd.DataFrame(fixed)
print(fixedbigcostmatrix.shape)
fixedbigcostmatrix.head()


# In[37]:


fixedbigcostmatrix.drop(100,axis=1,inplace=True)
fixedbigcostmatrix.drop(101,axis=1,inplace=True)
fixedbigcostmatrix.drop(102,axis=1,inplace=True)
fixedbigcostmatrix.drop(103,axis=1,inplace=True)


# In[38]:


fixedbigcostmatrix.head()


# ##### Now to actually test the algorithms:

# In[28]:


bigmatrixresults = {}


# In[49]:


result1 = greedy(fixedbigcostmatrix)
bigmatrixresults.update({'left to right':result1[1]})
print(result1)


# In[43]:


result2 = trueMinsFirst(fixedbigcostmatrix)
bigmatrixresults.update({'true mins first':result2[1]})
print(result2)


# In[44]:


result3 = swapAssignment(fixedbigcostmatrix)
bigmatrixresults.update({'swap':result3[1]})
print(result3)


# In[45]:


bigmatrixresults


# ##### It looks like for both cost matrices, pursuing the best possible assignment first yields the best results, followed by the swapping algorithm, and finally the basic left to right algorithm. This makes sense, as the "true mins first algorithm" has the highest complexity, and the basic left to right algorithm has the least.
