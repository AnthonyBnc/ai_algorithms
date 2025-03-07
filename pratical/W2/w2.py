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

