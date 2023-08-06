# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 19:45:07 2021

@author: ricon
"""
from .player import Player
from .computer import Computer

class Game:
    #How difficult should it be?
    print('To which number do you want to guess? (integer: for example 100)')
    difficulty = int(input())
    
    #initialize random computer number
    x = Computer()
    x.difficulty = difficulty
    x.rand_generator()
    
    #initialize the player
    y = Player()
    count = 0
    while x.get() != y.get():
        y.new_guess()
        if x.get() < y.get():   
            print('The number is lower, try it again.')
        elif x.get() > y.get():
            print('The number is higher, try it again')
        else:
            pass
        count += 1
        
    print('You got it, you did it in {} rounds. Concratulations!!!'.\
          format(count))