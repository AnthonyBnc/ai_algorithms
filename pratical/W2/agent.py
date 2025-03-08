from utils import distance_squared, turn_heading
from ipythonblocks import BlockGrid
from statistics import mean
from IPython import HTML, display, clear_output
from time import sleep

import sys
import random 
import copy
import collections
import numbers

class Thing: 
    """This represents any physical object that can appear in an Environment.
    You subclass Thing to get the things you want. Each thing can have a
    .__name__  slot (used for output only)."""

    def __repr__(self):
        return '<{}>'.format(getattr(self, '__name__', self.__class__.__name__))
    
    def is_alive(self):
        """Things that are 'alive' should return true"""
        return hasattr(self, 'alive') and self.alive
    
    def show_state(self):
        """Display the agent's internal state. Subclasses should override."""
        print("I don't know how to show_state")

    def display(self, canvas, x, y, width, height):
        """Display an image of this Thing on the canvas"""
        pass

class Agent(Thing):
    """An Agent is a subclass of Thing with one required instance attribute 
    (aka slot), .program, which should hold a function that takes one argument,
    the percept, and returns an action. (What counts as a percept or action 
    will depend on the specific environment in which the agent exists.)
    Note that 'program' is a slot, not a method. If it were a method, then the
    program could 'cheat' and look at aspects of the agent. It's not supposed
    to do that: the program can only look at the percepts. An agent program
    that needs a model of the world (and of the agent itself) will have to
    build and maintain its own model. There is an optional slot, .performance,
    which is a number giving the performance measure of the agent in its
    environment."""

    def __init__(self, program=None, sensing_radius=1):
        self.alive = True
        self.bump = False
        self.holding = []
        self.performance = 0
        self.sensing_radius = sensing_radius
        if program is None or not isinstance(program, collections.abc.Callable):
            print("Can't find a valid program for {}, falling back to default".format(self.__class__.__name__))

            def program(percept):
                return eval(input('Percept={}; action? '.format(percept)))

        self.program = program
    
    def can_grab(self, thing):
        """Return True if this agent can grab this thing.
        Override for appropriate subclasses of Agent and Thing."""
        return False
    
    def TraceAgent(agent):
        """Wrap the agent's program to print its input and output. This will let
    you see what the agent is doing in the environment."""
        old_program = agent.program

        def new_program(percept):
            action = old_program(percept)
            print('{} perceives {} and does {}'.format(agent, percept, action))
            return action 
        
        agent.program = new_program
        return agent

class Environment: 
    """Abstract class representing an Environment. 'Real' Environment classes
    inherit from this. Your Environment will typically need to implement:
        percept:           Define the percept that an agent sees.
        execute_action:    Define the effects of executing an action.
                           Also update the agent.performance slot.
    The environment keeps a list of .things and .agents (which is a subset
    of .things). Each agent has a .performance slot, initialized to 0.
    Each thing has a .location slot, even though some environments may not
    need this."""

    def __init__(self):
        self.things = []
        self.agents = []

    def thing_classes(self):
        return []
    
    def percept(self, agent):
        """Return the percept that the agent sees at this point. (Implement this.)"""
        raise NotImplementedError
    
    def excute_action(self, agent, action):
        """Change the world to reflect this action. (Implement this.)"""
        raise NotImplementedError
    
    def default_location(self, thing):
        """Default location to place a new thing with unspecified location."""
        return None
    
    def exogenous_change(sef):
        """If there is spontaneous change in the world, override this."""
        pass

    def is_done(self):
        """By default, we're done when we can't find a live agent"""
        return not any(agent.is_alive() for agent in self.agents)
    
    def step(self):
        """Run the environment for one time step. If the
        actions and exogenous changes are independent, this method will
        do. If there are interactions between them, you'll need to
        override this method."""
        if not self.is_done():
            actions = []
            for agent in self.agents:
                if agent.alive:
                    actions.append(agent.program(self.percept(agent)))
                else:
                    actions.append("")
            for (agent, action) in zip(self.agents, actions):
                self.execute_action(agent, action)
            self.exogenous_change()

    def run(self, steps=1000):
        """Run the Environment for given number of the time steps."""
        for step in range(steps):
            if self.is_done():
                return
            self.step()
    
    def list_things_at(self, location, tclass=Thing):
        """Return all things exactly at a given location."""
        if isinstance(location, numbers.Number):
            return [thing for thing in self.things
                    if thing.location == location and isinstance(thing, tclass)]
        return [thing for thing in self.things
                if all(x == y for x, y in zip (thing.location, location)) and isinstance(thing, tclass)]
    
    def some_thing_at(self, location, tclass=Thing):
        """Return true if at least one of the things at location 
        is an instance of class tclass (or a subclass)"""

    def add_thing(self, thing, location=None):
        """Add a thing to the environment, setting its location. For
        concenience, if thing is an agent program we make a new agent
        for it. (Shoudn't need to override this.)"""
        if not isinstance(thing, Thing):
            thing = Agent(thing)
        if thing in self.things:
            print("Can't add the same thing twice")
        else:
            thing.location = location if location is not None else self.default_location(thing)
            self.things.append(thing)
            if isinstance(thing, Agent):
                thing.performance = 0
                self.agents.append(thing)
    
    def delete_thing(self, thing):
        """Remove a thing from the environments"""
        try:
            self.things.remove(thing)
        except ValueError as e:
            print(e)
            print(" in Environment delete_thing")
            print(" Thing to be removed: {} at {}".format(thing, thing.location))
            print(" from list: {}". format([(thing, thing.location) for thing in self.things]))
        if thing in self.agents:
            self.agents.remove(thing)
