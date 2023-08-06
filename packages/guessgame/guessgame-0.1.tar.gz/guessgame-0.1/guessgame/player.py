# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 19:46:21 2021

@author: ricon
"""

class Player:
    def __init__(self, guess_num=0):
        self.guess_num = guess_num
        print('Make a first guess.')
        
    def new_guess(self):
        self.guess_num = int(input())
        
    def get(self):
        return self.guess_num