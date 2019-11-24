#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 01:16:07 2019

@author: marco
"""
''' This algorithm is structured like a competitive game.
    We can imagine a string as a series of characters. There are two
    cursors, that at the beginning of the game are placed at both ends of the string under the characters. 

    The algorithm first tries to find an immediate match, which could be at the current position of the cursors.
    If no immediate match is found, the two cursors try to find a match in the opposite end while moving towards the opposite side.
    The one who has made the least number of moves wins and moves the actual cursor.
    
    At the end of each turn, it checks for a match and the position of the cursors are reset.
'''

''' Side note: in the case of a string like SAPIENZA the result is 3: 
    even though there's only one match (the two As), each character BETWEEN
    the As, if considered by itself, allows for a palindrome substring such
    as APA, AIA, AEA, ... etc.  '''


#instr = 'DATAMININGSAPIENZA'
instr = str(input('Inserire stringa: '))
if len(instr) < 2:
    
    ans = len(instr)
else:
    res = 0
    start_i = 0
    end_i = len(instr)-1
    
    
    while start_i < end_i:
        
        #print(instr[start_i], instr[end_i], ' at ', start_i, ' ', end_i)
        
        if (end_i - start_i) == 2: # In this case there is only one letter left which has to be considered
            res += 1 # Of course it will be equal to itself, but will only contribute as one letter
            
            
        if instr[start_i] == instr[end_i]: # Immediate match, NICE.
            #print('Match',instr[start_i], instr[end_i], ' at ', start_i, ' ', end_i)
            res += 2
            start_i += 1
            end_i -= 1
        else:
            tmp_start_i = start_i
            tmp_end_i = end_i
            
            right_moves = 0
            left_moves = 0
            
            # The cursor starts from the right towards left
            while start_i < tmp_end_i:
                if instr[start_i] == instr[tmp_end_i]: # Match is found, stop moving the cursor
                    break
                tmp_end_i -= 1
                left_moves += 1
            # The cursor starts from the left towards right
            while tmp_start_i < end_i:
                if instr[tmp_start_i] == instr[end_i]: # Match is found, stop moving the cursor
                    break
                tmp_start_i += 1
                right_moves += 1
                
            
            if left_moves == right_moves:
                if instr[tmp_start_i] == instr[tmp_end_i]: # Found a match!
                    if tmp_start_i != tmp_end_i: # If they are not in the same position then it's a 2 letters match
                        start_i = tmp_start_i
                        end_i = tmp_end_i
                    else: # It is in the same place, the game has ended and there are no other letters to consider.
                        res += 1
                        start_i = end_i
                else: # Same number of moves, could be a match. It will be checked at the beginning of the next turn.
                    start_i += 1
                    end_i -= 1                   
                    
                            
            if left_moves < right_moves: # Found a match! It is more convenient to move the right cursor towards the left.
                end_i -= 1
            if left_moves > right_moves: # Found a match! It is more convenient to move the left cursor towards the right.
                start_i += 1
            
        
            
    

print('Result: ', res)