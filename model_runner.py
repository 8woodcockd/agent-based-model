# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 14:04:48 2018

@author: Dean
"""
'''Run this file at the commad prompt once you have saved the correct list of 
variables you wish to use in the script and saved it. Enter 
"python model_runner.py" at the command line or run the model_runner.bat file 
by double clicking it.

Either suppress the plotting of the scatter charts inside model.py or close
the window when it pops up to continue the model_runner.py program or change
matplotlib.pyplot.show() to matplotlib.pyplot.show(block = False) in the 
model.py script. 

To view the model outputs view the text file "total_agent_store_out" generated 
and saved in the same diretory'''

import subprocess
import os

'''edit the input variables for the parameter sweep'''
num_of_agents = [10,20,30]
store_capacity = [100]
consumption_rate = [24]
move_cost = [2]
neighbourhood = [1]
env_growth_rate = [0.1]
num_of_iterations = [20,50]
# Should remain equal to num_of_iterations if not requiring animation effect.
# Otherwise, set to a number smaller than the smallest number of iterations
# listed.
animation_frame_interval = num_of_iterations

#save file is referred to as filename in the script
filename = "total_agent_store_out.txt"

'''if file exists, delete it'''
if os.path.isfile(filename):
    os.remove(filename)

'''iterate through the list of input parameters'''
for agent1 in num_of_agents:
    for agent2 in store_capacity:
        for agent3 in consumption_rate:
            for agent4 in move_cost:
                for agent5 in neighbourhood:
                    for agent6 in env_growth_rate:
                        for agent7 in num_of_iterations:
                            animation_frame_interval = agent7
                            subprocess.run('python model.py {0} {1} {2} {3} ' 
                                            '{4} {5} {6} {7}'.format(agent1,
                                             agent2,agent3,agent4,agent5,
                                             agent6,agent7,
                                             animation_frame_interval))
print('done')

