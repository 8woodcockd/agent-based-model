# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 10:46:55 2018

@author: Dean
"""
import random
import math


class Agent:

    
    def __init__(self, environment, agents, rows, cols):
        """Assign attributes to each agent.
        """ 
        self._x = random.randint(0,cols-1)
        self._y = random.randint(0,rows-1)
        self.environment = environment
        self.store = float(0)   # Ensures all store values of type: float.
        self.agents = agents
        self.cols = cols-1
        self.rows = rows-1
  
    def getx(self):
        # Specifiy conditions to get_x.
        return self._x
    
    def setx(self, value):
        # Specifiy conditions to set_x.
        if isinstance(value, int) == False: 
            print('x value must be integer')
            return
        if 0 <= value <= self.cols:
            self._x = value
        else:
            print('x value entered is outside of the acceptable range')

    def delx(self):
        # Specifiy conditions to del_x.
        del self._x
    
    def gety(self):
        # Specifiy conditions to get_y.
        return self._y
    
    def sety(self, value):
        # Specifiy conditions to set_y.
        if isinstance(value, int) == False: 
            print('y value must be integer')
            return
        if 0 <= value <= self.rows:
            self._y = value
        else:
            print('y value entered is outside of the acceptable range')
    
    def dely(self):
        # Specifiy conditions to del_y.
        del self._y
    
    # Re-direct from dummy variables to (x and y) to functions that control the
    # user interaction with the real variables _x and _y.
    x = property(getx, setx, delx, "I'm the 'x' property.")
    y = property(gety, sety, dely, "I'm the 'y' property.")
    
    def move(self, rows, cols, move_cost):
        """Change x and y coordinates (equal random chance of increasing by 1,
        decreasing by 1 or staying the same). Moving costs resources from the 
        agents store resources. The cost of movement can be set by the user
        (move_cost). Torus boundary implemented.
        """
        if random.random() < (1/3):
            self.y = (self.y + 1) % (rows) 
            self.store -= move_cost
        elif random.random() < 0.5:
            self.y = (self.y - 1) % (rows)
            self.store -= move_cost
        if random.random() < (1/3):
            self.x = (self.x + 1) % (cols)
            self.store -= move_cost
        elif random.random() < 0.5:
            self.x = (self.x - 1) % (cols)
            self.store -= move_cost
               
    def distance_between(self, agent):
        """calculate the distances between each pair of agents.
        """
        return (((self.x - agent.x)**2) + ((self.y - agent.y)**2))**0.5
        
    def extremes (self, num_of_agents):
        """Find and return the agent located furthest north, east, south and 
        west.
        """
        # Coordinates in the format [x, y].
        N_agent = [0, -math.inf]
        E_agent = [-math.inf, 0]
        S_agent = [0, math.inf]
        W_agent = [math.inf, 0]
        agents = self.agents  
        for i in range(num_of_agents):
             if agents[i].y > N_agent[1]:
                 N_agent = (agents[i].x, agents[i].y)
             if agents[i].x > E_agent[0]:
                 E_agent = (agents[i].x, agents[i].y)
             if agents[i].y < S_agent[1]:
                 S_agent = (agents[i].x, agents[i].y)
             if agents[i].x < W_agent[0]:
                 W_agent = (agents[i].x, agents[i].y)    
        return [N_agent, E_agent, S_agent, W_agent]
            
    def eat(self, store_capacity, consumption_rate):
        """Agent will eat a user specified amount of units from the environment 
        at its current position, or as much as is available in its position. 
        The agent will be sick if its store exceeds the store capacity 
        (specified by the user). If sick the agent will deposit a random 
        percentage (25-75%) of its store, in the environment at its current
        position.
        """
        
        if self.environment[self.y][self.x] > consumption_rate:
            self.environment[self.y][self.x] -= consumption_rate
            self.environment[self.y][self.x] = round(
                                            self.environment[self.y][self.x],1)
            self.store += consumption_rate
            self.store = round(self.store,1)
        else:
            self.store += self.environment[self.y][self.x]
            self.store = round(self.store,1)
            self.environment[self.y][self.x] = float(0)
            
        # 'int' used to ensure all store values are floats. Division in 'share  
        # with neighbours' could create floats from integers.
        if self.store > store_capacity:
            sicked_up = random.randint(int(0.25 * self.store),
                                       int(0.75 * self.store))
            self.environment[self.y][self.x] += sicked_up 
            self.store -= sicked_up   
        
    def share_with_neighbours(self, neighbourhood):
        """Calculate the distance between self and the current other 
        agent and if distance is less than or equal to the 
        neighbourhood (specified by the user) share the sum of the two agents' 
        stores equally between the two agents.
        """
        for agent in self.agents:
            if agent == self:
                continue
            else:
                distance = self.distance_between(agent) 
                if distance <= neighbourhood:
                    sum = self.store + agent.store
                    average = sum / 2
                    self.store = average
                    agent.store = average
    
    def agent_proximity_stats(self, num_of_agents):
        """Calculate the minimum and maximum distance between any of the
        agents. Also return information that on the list position and hence 
        which agents are closest together and which are furthest apart.
        """
        max = -math.inf
        min = math.inf
        min_i = 0
        min_j = 0
        max_i = 0
        max_j = 0
        agents = self.agents
        for i in range (num_of_agents):  
            for j in range (num_of_agents):
                if i < j:
                    distance = (((agents[i].x - agents[j].x)**2) + 
                                ((agents[i].y - agents[j].y)**2))**0.5                  
                    if distance > max:
                        max = round(distance, 2)
                        max_i = i
                        max_j = j
                    if distance < min: 
                        min = round(distance, 2)
                        min_i = i
                        min_j = j                          
        return [min_i, min_j, min, max_i, max_j, max]
    
    def agent_store_stats(self, num_of_agents):
        """Determine the maximum and minimum of all agent store values.
        """
        max_store = -math.inf
        min_store = math.inf
        agents = self.agents
        for i in range (num_of_agents):
            if agents[i].store > max_store:
                max_store = round(agents[i].store,1)
            if agents[i].store < min_store:
                min_store = round(agents[i].store,1)
        return [min_store, max_store]

    def __str__(self): 
        '''overide __str__(self) in agents to print the agent location and  
        current store.'''
        return 'The agents (x,y) coordinates are (' + str(self.x) + ',' + \
        str(self.y) + ') and the agent is storing ' + str(round(self.store,1))\
        + ' units'
      