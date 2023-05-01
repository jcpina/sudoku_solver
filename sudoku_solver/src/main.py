'''
Sudoku Resolver

This program solves sudoku grills 3x3

Created on April 13, 2023
@author: Jean Charles Pina
'''

from classes import SudokuLine
from classes import SudokuColumn
from classes import SudokuSquare
from classes import SUDOKU_UNIT, NUM_LINE_COL_PER_SQ
from classes import SudokuError
from guess_state_machine import SudokuGuess
from guess_state_machine import GUESS_STATE_1, GUESS_STATE_2, GUESS_STATE_3, GUESS_STATE_4, GUESS_STATE_END
from update_and_conversions_utilities import *
from solvers import *

# Each square index is formed by a duet (line_index, column_index) at the position 0
SQUARE_INDEXES = [(0,0), (0,3), (0,6), (3,0), (3,3), (3,6), (6,0), (6,3), (6,6)]
MAX_LOOPS = 2
END_GAME = GUESS_STATE_END

# A global variable
game_error = SudokuError()
    
def print_results(lines, columns = 0, squares = 0):
    if lines:
        print("===== Game Lines =====")
        for i in lines:
            i.show_elements()
           
    if columns:
        print("===== Game Rows =====")
        for i in columns:
            i.show_elements()
    
    if squares:
        print("===== Game Squares =====")
        for i in squares:
            i.show_elements()
        
    check_results(lines, columns)
    
    print("Game Algorithm Errors:", game_error.get())
        
def check_results(lines, columns):
    """ Check for doubles (twice the same number) in the lines and columns """
    if lines:
        for i in lines:
            for num in range(1,10):
                if(i.is_duplicated(num)):
                    print("*** Error *** - line[",i.line_idx,"], item: ", num)
                    game_error.inc()
                
    if columns:
        for i in columns:
            for num in range(1,10):
                if(i.is_duplicated(num)):
                    print("*** Error *** - column[",i.column_idx,"], item: ", num)
                    game_error.inc()
                
def is_puzzle_solved(lines):
    """ Check if the puzzle is solved """
    solved = True
    for i in lines:
        if(i.has_item(0)):
            return(False)
                
    return(True)

def original_sudoku_lines(lines):
    lines.clear()
    # Expert - 2 guesses
    # lines.append(SudokuLine([0,6,5,8,0,0,7,0,0], 0))
    # lines.append(SudokuLine([0,9,0,0,2,0,5,0,0], 1))
    # lines.append(SudokuLine([0,0,0,3,4,0,2,0,0], 2))
    # lines.append(SudokuLine([0,7,2,9,0,3,0,0,0], 3))
    # lines.append(SudokuLine([0,0,0,6,8,0,0,0,0], 4))
    # lines.append(SudokuLine([6,0,0,0,0,0,0,0,1], 5))
    # lines.append(SudokuLine([0,0,0,0,0,0,0,9,0], 6))
    # lines.append(SudokuLine([0,0,0,0,0,0,0,0,6], 7))
    # lines.append(SudokuLine([5,0,0,0,0,2,3,0,0], 8))
    
    # Expert - 3 guesses
    # lines.append(SudokuLine([0,0,0,0,2,0,0,0,0], 0))
    # lines.append(SudokuLine([8,1,3,0,0,0,0,0,7], 1))
    # lines.append(SudokuLine([0,0,0,5,0,0,0,0,0], 2))
    # lines.append(SudokuLine([0,4,0,0,5,3,1,0,0], 3))
    # lines.append(SudokuLine([0,6,0,0,0,0,0,0,0], 4))
    # lines.append(SudokuLine([1,0,0,4,0,6,0,0,0], 5))
    # lines.append(SudokuLine([0,0,2,3,0,0,0,0,0], 6))
    # lines.append(SudokuLine([7,0,0,1,0,0,4,0,9], 7))
    # lines.append(SudokuLine([4,0,0,0,0,0,0,7,8], 8))
    
    # Hard
    lines.append(SudokuLine([0,0,0,7,2,0,9,0,3], 0))
    lines.append(SudokuLine([0,0,1,0,0,0,0,0,0], 1))
    lines.append(SudokuLine([0,4,0,0,0,0,0,0,0], 2))
    lines.append(SudokuLine([0,0,0,0,0,0,7,0,0], 3))
    lines.append(SudokuLine([0,0,0,0,0,8,3,0,5], 4))
    lines.append(SudokuLine([0,0,4,6,5,2,0,0,0], 5))
    lines.append(SudokuLine([9,1,0,4,0,7,0,0,0], 6))
    lines.append(SudokuLine([0,0,0,0,0,0,0,6,0], 7))
    lines.append(SudokuLine([0,8,6,0,0,1,0,0,9], 8))
    
        # Easy
    # lines.append(SudokuLine([0,9,0,0,0,6,2,0,4], 0))
    # lines.append(SudokuLine([5,6,8,7,0,4,0,0,3], 1))
    # lines.append(SudokuLine([0,0,2,0,0,0,0,8,7], 2))
    # lines.append(SudokuLine([7,0,0,8,9,5,1,0,0], 3))
    # lines.append(SudokuLine([0,1,9,0,6,0,0,3,0], 4))
    # lines.append(SudokuLine([0,0,0,0,0,1,4,0,0], 5))
    # lines.append(SudokuLine([4,7,0,6,5,0,8,0,0], 6))
    # lines.append(SudokuLine([0,5,1,9,4,3,0,0,6], 7))
    # lines.append(SudokuLine([9,0,0,0,0,0,3,4,0], 8))
    
        # Empty Grid
    # lines.append(SudokuLine([], 0))
    # lines.append(SudokuLine([], 1))
    # lines.append(SudokuLine([], 2))
    # lines.append(SudokuLine([], 3))
    # lines.append(SudokuLine([], 4))
    # lines.append(SudokuLine([], 5))
    # lines.append(SudokuLine([], 6))
    # lines.append(SudokuLine([], 7))
    # lines.append(SudokuLine([], 8))
    
    return lines

def build_cols_squares(lines, columns, squares):
    columns.clear()
    # Build the columns from the line's info 
    for i in range (0, SUDOKU_UNIT):
        columns.append(SudokuColumn(lines, i))
    
    # Build the squares from the line's info
    squares.clear()
    for i in SQUARE_INDEXES:
        squares.append(SudokuSquare(lines, i))  


if __name__ == '__main__':
    lines = []
    columns = []
    squares = []
    guess_state = GUESS_STATE_1
    guess_count = 0
    gsm = SudokuGuess() # Guess State Machine
    
    lines = original_sudoku_lines(lines)
    build_cols_squares(lines, columns, squares)
    print_results(lines)
    
    solved = False
    loop_times = 0
    
    while not solved:
        # Need to brake the loop if not solved the 2nd time ...
        if(guess_state == GUESS_STATE_END):
            break
        
        loop_times += 1
        
        ''' Solving at Square '''
        trial = 0
        while(solve_square(lines, columns, squares)):
            print("Looking at squares - Passes : ", trial)
            trial+=1
        
        if(is_puzzle_solved(lines)):
            break
            
        ''' Solving at line '''
        trial = 0
        while(solve_line(lines, columns, squares)):
            print("Looking at lines - Passes : ", trial)
            trial+=1

        if(is_puzzle_solved(lines)):
            break

        #print_results(lines, columns, squares)

        ''' Solving at Column '''
        trial = 0
        while(solve_column(lines, columns, squares)):
            print("Looking at columns - Passes : ", trial)
            trial+=1

        if(is_puzzle_solved(lines)):
            break
        
        ''' Solving at Square level 2 '''
        trial = 0
        while(solve_square_lev_2(lines, columns, squares)):
            print("Looking at Squares level 2 - Passes ", trial)
            trial += 1
            
        if(is_puzzle_solved(lines)):
            break
            
        ''' Solving at Line level 2 '''
        trial = 0
        while(solve_line_lev_2(lines, columns, squares)):
            print("Looking at Lines level 2 - Passes ", trial)
            trial += 1
            
        if(is_puzzle_solved(lines)):
            break
        
        ''' Solving at Column level 2 '''
        trial = 0
        while(solve_column_lev_2(lines, columns, squares)):
            print("Looking at Columns level 2 - Passes ", trial)
            trial += 1
            
        if(is_puzzle_solved(lines)):
            break
        
        # print_results(lines, columns, squares)
        
        guess_state = gsm.get_state()
        
        if(loop_times > MAX_LOOPS and guess_state == GUESS_STATE_1):
            print("Sorry!!! Need some help!!!")
            
            # print_results(lines, columns, squares)
            
            guess_state = gsm.state_1(lines, columns, squares)
        
        if(loop_times > 2 and guess_state > GUESS_STATE_1):
            loop_times = 1
            
            update_puzzle = gsm.state_2_3()
            
            if(update_puzzle):
                lines = original_sudoku_lines(lines)

                # Build the columns from the line's info
                build_cols_squares(lines,columns,squares)
                
                # Update the original Sudoku puzzle with the guess value
                line_update_all(lines[gsm.guessed_idx], 
                                gsm.guessed_position, columns, squares, 
                                gsm.guessed_value)
            
            guess_state = gsm.get_state()
            
            # print_results(lines, columns, squares)

        solved = True
        for i in lines:
            if(i.has_item(0)):
                solved = False
                
        if(solved):
            break
                    
    if is_puzzle_solved(lines):
        check_results(lines, columns)
        print("\n\t\tAwesome!!! Sudoku solved !!!!")
        if(gsm.guess_count != 0):
            print("\t\tTotal number of guesses:", (gsm.guess_count + 1))
            print("\t\tSuccessful Guess: line idx:", gsm.guessed_idx,
                  "line pos:", gsm.guessed_position,
                  "value:", gsm.guessed_value)

        
    else:
        print("\n\t\t****** Sorry!!! Need some help!!! *******")
        
    print_results(lines)
    print("\n\tGame Algorithm Errors:", game_error.inc())
           

                    
