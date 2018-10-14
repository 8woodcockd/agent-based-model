# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 21:06:47 2018

@author: Dean
"""
'''Ensure '%matplotlib qt' has been entered at the IPython console to ensure 
the animation pops open in a new window. It will not run otherwise. '''

# Import necessary modules to run the model
import matplotlib.pyplot
import matplotlib.animation
import matplotlib.cbook
import agentframework
import csv
import random
import sys
import math
import os

# Enter model variables to be used. These will be overidden by any variables 
# entered at the command prompt if available.
num_of_agents = 12
store_capacity = 100
consumption_rate = 24
move_cost = 12
neighbourhood = 10
env_growth_rate = 0.1
num_of_iterations = 200
animation_frame_interval = 5
completed_frames = 0        # Do not edit
completed_iterations = 0    # Do not edit
max_env = 0
min_env = 0
carry_on = True             # Do not edit
inputs_list = []

def evironment_stats():            
    """Determine the maximum and minimum values of the environment.
    """
    global max_env
    global min_env
    max_env = -math.inf
    min_env = math.inf
    max_env = -math.inf
    for i in range(rows):
        if max(environment[i]) > max_env:
            max_env = max(environment[i])
        if min(environment[i]) < min_env:
            min_env = min(environment[i])

def results():
    """Calculate, plot and save the final model outputs.
    """
    # Plot the final results if the last frame is not showing the result of 
    # the final iteration
    if carry_on is True:
        if num_of_iterations % animation_frame_interval != 0:
            #Move the agents and make them eat in a new randomised order for 
            #each iteration.
            for j in range(num_of_iterations % animation_frame_interval):
                rand_order = list(range(num_of_agents))
                random.shuffle(rand_order)
                for i in rand_order:
                    agents[i].move(rows, cols, move_cost)
                for i in rand_order:
                    agents[i].eat(store_capacity, consumption_rate)
                for i in rand_order:
                    agents[i].share_with_neighbours(neighbourhood)
    plot_scatter(max_env)       
    # Determine the min and max distance between agents, which agents they are, 
    # and their coordinates.
    # stats[min_i, min_j, min_distance, max_i, max_j, max_distance]      
    if num_of_agents > 1:
        stats = agents[1].agent_proximity_stats(num_of_agents)
        min_i = stats[0]
        min_j = stats[1]
        max_i = stats[3]
        max_j = stats[4]
        a = '\nAt the end of the model run, the agents closest together are '\
        'agent {0} (x:{1}, y:{2}) \nand agent {3} (x:{4}, y:{5}). \n'\
        'They are {6} units apart.\n'
        print(a.format(str(stats[0]), str(agents[min_i].x),
                       str(agents[min_i].y), str(stats[1]),
                       str(agents[min_j].x), str(agents[min_j].y), 
                       str(stats[2])))
        a = 'At the end of the model run, the agents furthest apart are ' \
        'agent {0} (x:{1}, y:{2}) \nand agent {3} (x:{4}, y:{5}). \n'\
        'They are {6} units apart.\n'
        print(a.format(str(stats[3]), str(agents[max_i].x),
                       str(agents[max_i].y), str(stats[4]),
                       str(agents[max_j].x), str(agents[max_j].y),
                       str(stats[5]))) 
    
    # Write the environment data to a file after agents have moved and eaten
    # it.
    with open ('Model_Outputs/environment_out.txt', 'w') as f:
        for line in environment:
            for value in line:
                f.write(str(value) + " ")
            f.write("\n")
    
    # Calculate total eaten by all agents.
    total_agent_store = 0
    for i in range (num_of_agents):
        total_agent_store = total_agent_store + agents[i].store
    
    # Create and/or append existing file containing total eaten by all agents.    
    with open ('Model_Outputs/total_agent_store_out.txt', 'a') as f:
        f.write('no. of agent(s)s: {0}, store capacity: {1}, '\
                'consumption_rate: {2}, move cost: {3}, environmental growth '\
                'rate: {4}, number of iterations: {5}, neighbourhood radius: '\
                 '{6}, total agent store: {7} \n\n'.format(
                    str(num_of_agents), str(store_capacity), 
                    str(consumption_rate), str(move_cost), 
                    str(env_growth_rate), str(num_of_iterations),
                    str(neighbourhood), str(round(total_agent_store,1))))
                         
    # Print the overidden agent string.
    for i in range (num_of_agents):
        print(agents[i])
    
    # Save figure as an image before quiting the program creating a name from 
    # the input variables used.
    fig.savefig('Model_Outputs/' + str(num_of_agents)+ '_' +
                str(store_capacity) + '_' + str(consumption_rate) + '_' +
                str(move_cost) + '_' + str(neighbourhood) + '_' +
                str(env_growth_rate) + '_' + str(num_of_iterations) + '_' +
                str(animation_frame_interval) + '.png')
    print('Model run complete.')
    sys.exit()

def gen_function():
    """Generate the next number in the sequence of iterations if the specified
    conditions are met.
    """
    global carry_on
    a = 0
    while (a < frame_num) & (carry_on):
        yield a			# Returns control and waits next call.
        a = a + 1

def update(frame):
    """Move the agents, then make them eat and then share with neighbours in a 
    new randomised order (rand_order) for each iteration.
    """
    global carry_on
    global completed_frames
    global completed_iterations
    
    for j in range(animation_frame_interval): 
        rand_order = list(range(num_of_agents))
        random.shuffle(rand_order)
        for i in rand_order:
            agents[i].eat(store_capacity, consumption_rate)
        for i in rand_order:
            agents[i].move(rows, cols, move_cost)
        # Calculate: store_stats = [min_store, max_store].
        store_stats = agents[0].agent_store_stats(num_of_agents)
        for i in rand_order:
            agents[i].share_with_neighbours(neighbourhood)
        # The environment grows.
        for i in range(rows):
            for j in range(cols):
                environment[i][j] += env_growth_rate
                environment[i][j] = round(environment[i][j],1)
        
        # Implmenting an alternative stopping condition.
        # Stop if agent store becomes < 0.
        # If any of the agents stores fell below 0, they are not sustained by
        # their resources and after moving the model will stop running.  
        # Records the completed iterations and, therefore, the iteration
        # in which the model stops due to the implemented stopping 
        # condition.
        # store_stats = [min_store, max_store]
        completed_iterations += 1
        if store_stats[0] < 0:
            carry_on = False
            print('Stopping condition implemented after', \
                  str(completed_iterations), 'iterations because at least ' \
                  'one agent store fell below zero.')
            results()
            return
    plot_scatter(max_env)
    completed_frames += 1
    print(completed_frames, ' frames complete')
    if completed_frames == frame_num:
        results()

def plot_scatter(max_env):
    """Create a scatter plot to show the agent position. Force the environment
    to be shown using the same colorbar throughout the animation.
    """
    fig.clear()
    fig.suptitle('Agent-based model')
    ax = fig.subplots()
    #set the limits of the plot axes
    matplotlib.pyplot.xlim(0, cols-1)
    matplotlib.pyplot.ylim(0, rows-1)
    ax.set_xlabel('distance (unspecified units)', fontsize=10)
    ax.set_ylabel('distance (unspecified units)', fontsize=10)
    # Show environment background data with colorbar.
    c = ax.imshow(environment, vmin = 0, vmax = int(max_env))
    ticks_interval = round((max_env / 10),0)
    ticks_list =[]
    ticks_gen = 0
    for i in range(10):
        ticks_list.append(int(ticks_gen))
        ticks_gen += ticks_interval
    ticks_list.append(int(max_env))
    cbar = fig.colorbar(c, ticks=ticks_list)
    cbar.ax.set_yticklabels(ticks_list)
    cbar.set_label('Environment resource level', rotation=90, labelpad=20)
    # Colour plotted points black.
    for i in range(num_of_agents):
        matplotlib.pyplot.scatter(agents[i].x, agents[i].y, color='black') 
    # Calculate extremeties (E, S, W, N). Function defined in agentframework.py
    # Color extremeties red.
    extremeties = agents[0].extremes(num_of_agents)
    for i in range(len(extremeties)):
        matplotlib.pyplot.scatter(extremeties[i][0],extremeties[i][1], 
                                  color='red') 
    params = 'Model Parameters:\nnum_of_agents: {0}, store_capacity: {1},\n'\
    'consumption_rate: {2}, move_cost: {3}, neighbourhood: {4},\n'\
    'env_growth_rate: {5}, num_of_iterations: {6},\n'\
    'animation_frame_interval: {7}'
    parameters = params.format(str(num_of_agents), str(store_capacity),
             str(consumption_rate), str(move_cost), str(neighbourhood),
             str(env_growth_rate), str(num_of_iterations),
             str(animation_frame_interval))
    props = dict(boxstyle='round', facecolor='ghostwhite', alpha=0.5)
    ax.text(
            0.1, 1.2, parameters, transform=ax.transAxes, fontsize=10,
            horizontalalignment='left', verticalalignment='top', bbox=props, 
            wrap = True)

def skip():
    """Do nothing"""
    # Used to 'skip' init_func in matplotlib.animation.FuncAnimation.
    return


# Get the current directory in order to place outputs in a folder in the 
# current working directory location.
current_directory = os.getcwd()
output_directory = os.path.join(current_directory, r'Model_Outputs')
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Interactive command line user interface allowing the user to decide if they 
# want to use the default variables or enter their own variables. If the user  
# is familiar with the program and has enter all the required system arguments
# the model will save time and just run.
print(len(sys.argv))
if len(sys.argv) != 9:
    print("Do you want to enter your own model variables (if you do not the " 
          "script defaults shall be used)?\n Please type 'y' or 'n' at the " 
          "command line and press enter:")
    ans = False
    while ans is False:
        answer = input()
        if answer == 'y':   
            ans = True
            print('Please enter the following parameters separated by one '+
              'space in the following format:\n'+
              '{1} {2} {3} {4} {5} {6} {7} {8}\nwhere:\n'+
              '{1} is the number of agents to be generated in the model.\n'+ 
              '{2} is the store capacity of each agent (the maximum units of '+
              'resource an agent can contain).\n'+
              '{3} is the consumption rate of each agent (the amount of '+
              'resources the agent will take from the environment, if  '+ 
              'available, in its current position, and add to its store per '+
              'iteration).\n'+
              '{4} is the resource unit cost to each agent of each movement '+  
              'in the x or y direction.\n'
              '{5} is the neighbourhood (the radial unit distance '+ 
              'surrounding each agent within which each agent will identify '+
              'and share, equally, resources with other agents.\n'+
              '{6} is the environmental growth rate (the value added to each '+ 
              'position (raster grid cell) in the environment per iteration).'+
              '\n'
              '{7} is the number of iterations the model will progress '+
              'through, providing an alternative stopping condition does '+ 
              'not terminate the model run beforehand.\n'
              '{8} is the animation frame interval. This allows a number of '+
              'iterations to be skipped before a frame is generated for '+ 
              'the animation.\n\n'
              'Note: all inputs should be integer except the environmental '+
              'growth rate which may be decimal (1 decimal place.).')
            ans2 = False
            while ans2 is False:
                inputs_list = []
                inputs = input()
                inputs = inputs.split(" ")
                for i in inputs:
                    inputs_list.append(float(i))
                # Set the custom input parameters after model has been run 
                # from the list generated by the command line input if 
                # condition has been met.
                if inputs_list[6] > inputs_list[7]:
                    ans2 = True
                    num_of_agents = int(inputs_list[0])
                    store_capacity = int(inputs_list[1])
                    consumption_rate = int(inputs_list[2])
                    move_cost = int(inputs_list[3])
                    neighbourhood = int(inputs_list[4])
                    env_growth_rate = inputs_list[5]
                    num_of_iterations = int(inputs_list[6])
                    animation_frame_interval = int(inputs_list[7])   
                else:
                    print(
                      'ERROR: animation_frame_interval (', +
                      animation_frame_interval, ' entered) '
                      'must be greater than num_of_iterations (', +
                      num_of_iterations, 'entered).\nPlease revise and ' 
                      're-enter the model parameters.'
                      )                          
        elif answer == 'n':
            ans = True
        else:
            print("Try again. Type 'y' or 'n' and press enter")
# Arguments entered via the command line will overide the script defaults 
# and be used if available.
if len(sys.argv) == 9:    
    num_of_agents = int(sys.argv[1])
    store_capacity = int(sys.argv[2])
    consumption_rate = int(sys.argv[3])
    move_cost = int(sys.argv[4])
    neighbourhood = int(sys.argv[5])
    env_growth_rate = float(sys.argv[6])
    num_of_iterations = int(sys.argv[7])
    animation_frame_interval = int(sys.argv[8])    
    print(
        'Model parameters entered:\n'\
        'num_of_agents:', num_of_agents, ', store_capacity: ', store_capacity,\
        ', consumption_rate: ', consumption_rate, ', move_cost: ', move_cost,\
        ', neighbourhood: ', neighbourhood, ', env_growth_rate: ', \
        env_growth_rate, ', num_of_iterations: ',num_of_iterations, \
        ', animation_frame_interval: ', animation_frame_interval)
    if num_of_iterations < animation_frame_interval:
        print('ERROR: animation_frame_interval (',animation_frame_interval, +
              ' entered) must be greater than num_of_iterations (',+
              num_of_iterations, 'entered).\nPlease restart model with ' + 
              'revised parameters.')
        sys.exit()
# If no arguments are entered via the command line the script defaults are 
# used.
elif len(sys.argv) == 1:
    if(len(inputs_list) == 0):
        print('default variables values obtained from spyder script')
# If some, but not all, arguments are entered via the command line.
elif 1 < len(sys.argv) < 9:
    print('ERROR: not enough arguments entered. \n' +
          'len sys.argv is', len(sys.argv), 'but should be 9 \n' +
          'Please enter: python model.py {num_of_agents} ' + 
          '{store_capacity} {consumption_rate} {move_cost} {neighbourhood} ' + 
          '{env_growth_rate} {num_of_iterations} {animation_frame_interval}')
    sys.exit()

# Load the environment.
environment = []
with open('Model_Inputs/env_in.txt', newline ='') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader: 
        rowlist = []
        for value in row:
            rowlist.append(value)
        environment.append(rowlist)
# Calculate the number of x and y values and hence the grid area.
rows = len(environment)
cols = len(environment[0])
# Calculate min and max environment values to use when creating the colorbar.
evironment_stats()
# Create the agents.
agents = []        
for i in range(num_of_agents):
    agents.append(agentframework.Agent(environment, agents, rows, cols))

# Create the figure and plot initial environment and agent positions. 
fig = matplotlib.pyplot.figure(figsize=(9, 9))
plot_scatter(max_env)
# Create the animation using the update function which will call the results 
# function when complete.
frame_num = int(num_of_iterations / animation_frame_interval)
animation = matplotlib.animation.FuncAnimation(fig, update, 
                                               frames = gen_function, 
                                               init_func = skip, interval=250, 
                                               repeat = False)
matplotlib.pyplot.show()

