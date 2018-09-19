# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 10:46:55 2018

@author: Dean
"""
import random
import math

class Agent:

    def __init__(self, environment, agents, rows, cols):
        self._x = random.randint(0,cols-1)
        self._y = random.randint(0,rows-1)
        self.environment = environment
        self.store = float(0)   # ensures all store values of type: float
        self.agents = agents
        self.cols = cols-1
        self.rows = rows-1
  
    def getx(self):
        return self._x
    
    def setx(self, value):
        if isinstance(value, int) == False: 
            print('x value must be integer')
            return
        if 0 <= value <= self.cols:
            self._x = value
        else:
            print('x value entered is outside of the acceptable range')

    def delx(self):
        del self._x
    
    def gety(self):
        return self._y
    
    def sety(self, value):
        if isinstance(value, int) == False: 
            print('y value must be integer')
            return
        if 0 <= value <= self.rows:
            self._y = value
        else:
            print('y value entered is outside of the acceptable range')
    
    def dely(self):
        del self._y
    
    x = property(getx, setx, delx, "I'm the 'x' property.")
    y = property(gety, sety, dely, "I'm the 'y' property.")
    
    def move(self, rows, cols, move_cost):
    # change coordinates of x and y (equal random chance of increasing by 1,
    # decreasing by 1 or staying the same). Moving costs store resources and 
    # is variable (move_cost).
    # use modulus to implement torus boundary
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
               
    
    
    '''calculate the distances between each pair of agents'''
    def distance_between(self, agent):
        return (((self.x - agent.x)**2) + 
        ((self.y - agent.y)**2))**0.5
        
    def extremes (self, num_of_agents):
        #coordinates format [x, y]
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
        '''agent will eat 10 units of the environment or as much as is  
        available in its position. The agent will be sick if its store exceeds  
        store_capacity it will deposit its whole store at its position in the 
        environment'''    
        
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
            
        
        # Sick up store at current location if eaten more than 100 units
        # ensures all store values are floats. Division in 'share with 
        # neighbours' could create floats from integers.
        if self.store > store_capacity:
            sicked_up = random.randint(int(0.25*self.store),
                                       int(0.75*self.store))
            self.environment[self.y][self.x] += sicked_up 
            self.store -= sicked_up   
        
    def share_with_neighbours(self, neighbourhood):
        # Loop through the agents in self.agents .
        for agent in self.agents:
            if agent == self:
                continue
            else:
                '''Calculate the distance between self and the current other 
                agent and if distance is less than or equal to the 
                neighbourhood share the sum of the two agents' stores equally 
                between the two agents'''
                distance = self.distance_between(agent) 
                if distance <= neighbourhood:
                    sum = self.store + agent.store
                    average = sum / 2
                    self.store = average
                    agent.store = average
                    #print('agent ' + str(distance) + ' units away. Average 
                    #store ' + str(average))
    
    def agent_proximity_stats(self, num_of_agents):
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
                        max = distance
                        max_i = i
                        max_j = j
                    if distance < min: 
                        min = distance
                        min_i = i
                        min_j = j                          
        return [min_i, min_j, min, max_i, max_j, max]
    
    def agent_store_stats(self, num_of_agents):
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
        current store'''
        return 'The agents (x,y) coordinates are (' + str(self.x) + ',' + \
        str(self.y) + ') and the agent is storing ' + str(round(self.store,1))\
        + ' units'
        #return str(self.x) + ', ' + str(self.y)

    
    
      


        