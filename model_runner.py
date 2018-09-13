# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 14:04:48 2018

@author: Dean
"""
import subprocess
import os

'''edit the input variables for the parameter sweep'''
num_of_agents = [100]
num_of_iterations = list(range(1,50,1))
neighbourhood = [1]

'''save file as filename'''
filename = "total_agent_store_out.txt"

'''if file exists, delete it'''
if os.path.isfile(filename):
    os.remove(filename)

'''iterate through the list of input parameters'''
for agent1 in num_of_agents:
    print(agent1)
    for agent2 in num_of_iterations:
        for agent3 in neighbourhood:
            subprocess.call('python model.py {0} {1} {2}'.format(agent1,agent2,agent3))
    
print('done')