from pandas import *
from numpy import *
from pulp import *
from openpyxl import *
import pandas as pd 

data = read_excel('Production_assignment_python.xlsx')
data['t'] = range(1,13)

data = data.set_index('t')
#print(data)

model = LpProblem('Produc', LpMinimize)

inv = LpVariable.dicts('inv',[1,2,3,4,5,6,7,8,9,10,11,12],0,None,'Integer')
prod = LpVariable.dicts('prod',[1,2,3,4,5,6,7,8,9,10,11,12],0,None,'Integer')
bin = LpVariable.dicts('bin',[1,2,3,4,5,6,7,8,9,10,11,12],0,None,'Binary')

time = [1,2,3,4,5,6,7,8,9,10,11,12]
inv[0] = 0
model += lpSum([inv[t]*data.loc[t,'storage cost']+ prod[t]*data.loc[t,'produuction Cost']+bin[t]*data.loc[t,'fixed cost'] for t in time])
for t in time:
    model += prod[t] - inv[t] + inv[t-1] >= data.loc[t,'demand']
    model += prod[t] <= bin[t]*data.loc[t,'Capacity']

model.solve()

opt_data = pd.DataFrame({'demand' : data['demand'], 
                         'production' : [prod[i].varValue for i in prod],
                         'inventory' : [inv[i].varValue for i in range(1,13)],
                          'Opoening' : [bin[i].varValue for i in bin]})


print(opt_data)
