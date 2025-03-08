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

class XYEnvironment(Environment):
    """This class is for environments on a 2D plane, with locations
    labelled by (x, y) points, either discrete or continuous.
    
    Agents perceive things within a radius. Each agent in the 
    encironment has a .loaction slot which should be alocation such
    as (0, 1), and a. holding slot, which should be a list of things
    that are held."""

    def __init__(self, width=10, height=10):
        super().__init__()

        self.width = width 
        self.height = height
        self.observers = []

        self.x_start, self.y_start = (0, 0)
        self.x_end, self.y_end = (self.width, self.height)

    perceptible_distance = 1

    def things_near(self, location, radius=None):
        """Return all things within radius of location."""
        if radius is None:
            radius = self.perceptible_distance
        radius2 = radius * radius
        return [(thing, thing.location)
            for thing in self.things if distance_squared(
                location, thing.location) <= radius2]
    
    def percept(self, agent):
        """By default, agent perceives things within a default radius."""
        return (agent.location, self.things_near(location=agent.location, radius=agent.sensing_radius))

    def execute_action(self, agent, action):
        agent.bump = False
        if action == "TurnRight":
            agent.direction += Direction.R
        elif action == "TurnLeft":
            agent.direction += Direction.L
        elif action == 'Suck' and 'Dirt' in [thing.__class__.__name__ for thing in self.list_things_at(agent.location)]:
            things = [thing for thing in self.list_things_at(agent.location) if thing.__class__.__name__ == 'Dirt']
            for thing in things:
                self.delete_thing(thing)
        elif action == 'up':
            if agent.location[1] > 0:
                new_location = (agent.location[0], agent.location[1] - 1)
                self.move_to(agent, new_location)
        elif action == 'down':
            if agent.location[1] < self.height - 1:
                new_location = (agent.location[0], agent.location[1] + 1)
                self.move_to(agent, new_location)
        elif action == 'left':
            if agent.location[1] > 0:
                new_location = (agent.location[0] - 1, agent.location[1])
                self.move_to(agent, new_location)

        elif action == 'right':
            if agent.location[1] < self.width - 1:
                new_location = (agent.location[0] + 1, agent.location[1])
                self.move_to(agent, new_location)
        elif action == 'Forward':
            agent.bump = self.move_to(agent, agent.direction.move_forward(agent.locattion))
        elif action == 'Grab':
            things = [thing for thing in self.list_things_at(agent.location) if agent.can_grab(thing)]
            if things:
                agent.holding.append(thing[0])
                print("Grabbing ", things[0].__class__.__name__ )
                self.delete_thing(things[0])
        elif action == 'Release':
            if agent.holding:
                dropped = agent.holding.pop()
                print("Dropping ", dropped.__class__.__name__)
                self.add_thing(dropped, location = agent.loaction)

    def default_location(self, thing):
        location = self.random_location_inbounds()
        while self.some_things_at(location, Obstacle):
            location = self.random_location_inbounds()
        return location 
    
    def move_to(self, thing, destination):
        """Move a thing to a new location. Returns True on success or False if there is an Obstacle.
        If thing is holding anything, they move with him."""
        thing.bump = self.some_thing_at(destination, Obstacle)
        if not thing.bump:
            thing.location = destination
            for o in self.observers:
                o.thing_moved(thing)
            for t in thing.holding:
                self.delete_thing(t)
                self.add_thing(t, destination)
                t.location = destination 
            return thing.bump
        
    def add_thing(self, thing, location=None, exclude_duplicate_class_item=False):
        """Add things to the world. If (exclude_duplicate_class_item) then the item won't be
        added if the location has at least one item of the same class."""
        if location is None:
            super().add_thing(thing)
        elif self.is_inbounds(location):
            if(exclude_duplicate_class_item and
               any(isinstance(t, thing.__class__) for t in self.list_things_at(location))):
                return
            super().add_thing(thing, location)
    
    def is_inbounds(self, location):
        """Checks to make sure that the location is inbounds (within walls if we have walls)"""
        x, y = location 
        return not (x < self.x_start or x > self.x_end or y < self.y_start or y > self.y_end)

    def random_location_inbound(self, exclude = None):
        """Returns a random location that is inbounds (within walls if we have walls)"""
        location = (random.randint(self.x_start, self.x_end), 
                    random.randint(self.y_start, self.y_end))
        return location 
    
    def delete_thing(self, thing):
        """Deletes thing, and everything it is holding (if thing is an agent)"""
        if isinstance(thing, Agent):
            del thing.holding
        
        super().delete_thing(thing)
        for obs in self.observers:
            obs.thing_deleted(thing)
        
    def add_walls(self):
        """Put walls around the entire perimeter of the grid."""
        for x in range(self.width):
            self.add_thing(Wall(), (x, 0))
            self.add_thing(Wall(), (x, self.height - 1))
        for y in range(1, self.height - 1):
            self.add_thing(Wall(), (0, y))
            self.add_thing(Wall(), (self.width - 1, y))

        self.x_start, self.y_start = (1,1)
        self.x_end, self.y_end = (self.width - 1, self.height - 1)
    
    def add_observer(self, observer):
        """Adds an observer to the list of observers.
        An observer is typically an EnvGUI.

        Each observer is notified of changes in move_to and add_thing,
        by calling the observer's methods thing_moved(thing)
        and thing_added(thing, loc)."""
        self.observers.append(observer)

    def turn_heading(self, heading, inc):
        """Return the heading to the left (inc=+1) or right (inc=-1) of heading."""
        return turn_heading(heading, inc)