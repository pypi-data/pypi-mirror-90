# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 19:45:43 2021

@author: ricon
"""
from random import random

class Computer():
    def __init__(self, rand_num=0, difficulty=0):
        self.rand_num = rand_num
        self.difficulty = difficulty
    
    def rand_generator(self):
        #initialize a random number
        self.rand_num = int(random()*self.difficulty)
        
    def get(self):
        return self.rand_num