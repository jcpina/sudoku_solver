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

# Each square index is formed by a duet (line_index, column_index) at the position 0
SQUARE_INDEXES = [(0,0), (0,3), (0,6), (3,0), (3,3), (3,6), (6,0), (6,3), (6,6)]
MAX_LOOPS = 2
END_GAME = -1

# A global variable
game_error = SudokuError()
    


def linepos2square_idx(line, line_pos):
    '''
    returns the square index (0..8) containing a given line and position
    '''
    line_idx = line.line_idx
    square_idx = int(line_idx/NUM_LINE_COL_PER_SQ)*NUM_LINE_COL_PER_SQ + int(line_pos/NUM_LINE_COL_PER_SQ)
    return square_idx

def linepos2square_pos(line, line_pos):
    '''
    returns the square position intersecting a given line and position
    '''
    line_idx = line.line_idx
    x = int(line_pos % NUM_LINE_COL_PER_SQ)
    y = int(line_idx % NUM_LINE_COL_PER_SQ)
    square_pos = (NUM_LINE_COL_PER_SQ*y + x)
    return(square_pos)

def colpos2square_idx(col, col_pos):
    '''
    returns the square index (0..8) containing a given column and position
    '''
    col_idx = col.column_idx
    square_idx = int(col_pos/NUM_LINE_COL_PER_SQ)*NUM_LINE_COL_PER_SQ + int(col_idx/NUM_LINE_COL_PER_SQ)
    return square_idx

def colpos2square_pos(col, col_pos):
    '''
    returns the square position intersecting a given column and position
    '''
    
    # Already have the math for lines ... hence convert position of interest
    # from column to line
    line_idx = col_pos
    line_pos = col.column_idx
    x = int(line_pos % NUM_LINE_COL_PER_SQ)
    y = int(line_idx % NUM_LINE_COL_PER_SQ)
    square_pos = (NUM_LINE_COL_PER_SQ*y + x)
    return(square_pos)


def line_column_update_pos(line, line_pos, cols, item):
    ''' . Updates the line position with the given item
        . Updates the column position at the intercept point
    '''
    line_idx = line.line_idx
    if(line.line[line_pos] == 0):
        line.line[line_pos] = item
        
        col_idx = line_pos
        col_pos = line_idx
        cols[col_idx].column[col_pos] = item
    else:
        print(">>> Error! >>>\n Trying to change value at line[",line_idx,"], pos[",line_pos,"]")
        game_error.inc()
    
def line_square_update_pos(line, line_pos, squares):
    '''
        . Updates the square position at the intercept point with the line at line_pos
    '''
    line_idx = line.line_idx
    value = line.line[line_pos]
    square_idx = linepos2square_idx(line, line_pos)
    square_pos = linepos2square_pos(line, line_pos)
    if(squares[square_idx].square[square_pos] == 0):
        squares[square_idx].square[square_pos] = value
    else:
        print(">>> Error! >>>\n Trying to change value at square[",square_idx,"], pos[",square_pos,"]")
        game_error.inc()

 
def column_line_update_pos(col, col_pos, lines, item):
    ''' . Updates the column position with the given item
        . Updates the line position at the intercept point
    '''
    col_idx = col.column_idx
    if col.column[col_pos] == 0:
        col.column[col_pos] = item
        
        line_idx = col_pos
        line_pos = col_idx
        lines[line_idx].line[line_pos] = item
    else:
        print(">>> Error! >>>\n Trying to change value at column[",col_idx,"], pos[",pos,"]")
        game_error.inc()

    
def column_square_update_pos(col, col_pos, lines, squares):
    '''
        . Updates the square position at the intercept point with the column at col_pos 
        Gets first the line and line position at the intercept point with the column
        and then updates the appropriate square position using the line to square 
        position update function 
    '''
    value = col.column[col_pos]
    col_idx = col.column_idx
    
    line_pos = col.column_idx
    line_idx = col_pos
    line_square_update_pos(lines[line_idx], line_pos, squares)
    
def square_line_column_update_pos(square, lines, cols, square_pos, item):
    '''
        Updates the line and column position at the intercept point
    '''
    line_org = square.square_idx[0]
    col_org = square.square_idx[1]
    
    # Update line item
    line_idx = int(square_pos / NUM_LINE_COL_PER_SQ) + line_org
    line_pos = (square_pos % NUM_LINE_COL_PER_SQ) + col_org
    if(lines[line_idx].line[line_pos]) == 0:
        lines[line_idx].line[line_pos] = item
        
        # Update column item
        col_pos = line_idx
        col_idx = line_pos
        if(cols[col_idx].column[col_pos] == 0):
            cols[col_idx].column[col_pos] = item
        else:
            print(">>> Error! >>>\n Trying to change value at column[",col_idx,"], pos[",col_pos,"] old_val:", lines[line_idx].line[line_pos], "new val:", item)
            game_error.inc()
            

    else:
        print(">>> Error! >>>\n Trying to change value at line[",line_idx,"], pos[",line_pos,"]")
        game_error.inc()

    
def line_update_all(line, line_pos, cols, squares, item):
    ''' Update all the corresponding position for all data sets
    '''
    line_column_update_pos(line, line_pos, cols, item)
    line_square_update_pos(line, line_pos, squares)

def column_update_all(col, col_pos, lines, squares, item):
    ''' Update all the corresponding position for all data sets
    '''
    column_line_update_pos(col, col_pos, lines, item)
    column_square_update_pos(col, col_pos, lines, squares)
    
def square_update_all(square, sq_pos, lines, cols, item):
    ''' Update all the corresponding position for all data sets
    '''
    if square.square[sq_pos] == 0: 
        square.square[sq_pos] = item
        square_line_column_update_pos(square, lines, cols, sq_pos, item)
    else:
        print(">>> Error! >>>\n Trying to change value at square[",square.square_idx,"], pos[",sq_pos,"]")
        game_error.inc()
    
def print_results(lines, columns, squares):
    print("===== Game Lines =====")
    for i in lines:
        i.show_elements()
           
    # print("===== Game Rows =====")
    # for i in columns:
    #     i.show_elements()
    #
    # print("===== Game Squares =====")
    # for i in squares:
    #     i.show_elements()
        
    check_results(lines, columns)
    
    print("Game Algorithm Errors:", game_error.get())
        
def check_results(lines, columns):
    for i in lines:
        for num in range(1,10):
            if(i.is_duplicated(num)):
                print("*** Error *** - line[",i.line_idx,"], item: ", num)
                game_error.inc()
                
    for i in columns:
        for num in range(1,10):
            if(i.is_duplicated(num)):
                print("*** Error *** - column[",i.column_idx,"], item: ", num)
                game_error.inc()
                
def is_puzzle_solved(lines):
    solved = True
    for i in lines:
        if(i.has_item(0)):
            return(False)
                
    return(True)

                
def solve_square(lines, columns, squares):
    hit = False
    for num in range(1,10):
        for i in squares:
            if not (i.has_item(num)) :
                # item is missing, let's see if we can find it ..
                sq_scratch = i.item_possible_locations(lines, columns, num)
                pos = i.item_unique_possibility(sq_scratch)
                if pos >= 0:
                    print(">>>>>>> Hit for square:", i.square_idx, " at pos: ", pos, " for item: ", num)
                    square_update_all(i, pos, lines, columns, num)
                    hit = True
    return(hit)

def solve_line(lines, columns, squares):
    hit = False
    for num in range(1,10):
        for i in lines:
            if not (i.has_item(num)) :
                line_scratch = i.item_possible_locations(squares, columns, num)
                line_pos = i.item_unique_possibility(line_scratch)
                if line_pos >= 0:
                    print(">>>>>>> Hit line[", i.line_idx, "]:", i.line, " at pos: ", line_pos, " for item: ", num)
                    line_update_all(i, line_pos, columns, squares, num)
                    hit = True
    return(hit)

def solve_column(lines, columns, squares):
    hit = False
    for num in range(1,10):
        for i in columns:
            if not (i.has_item(num)) :
                line_scratch = i.item_possible_locations(squares, lines, num)
                col_pos = i.item_unique_possibility(line_scratch)
                if col_pos >= 0:
                    print(">>>>>>> Hit column[", i.column_idx, "]:", i.column, " at pos: ", col_pos, " for item: ", num)
                    column_update_all(i, col_pos, lines, squares, num)
                    hit = True
    return(hit)

def solve_square_lev_2(lines, columns, squares):
    hit = False
    for sq_idx in range(0,9):
        hit_count_per_position = [0,0,0,0,0,0,0,0,0]
        '''
        If there is only 1 hit in the position counter, then this
        array will have the value that is correct at this position
        '''
        hit_last_per_position =  [0,0,0,0,0,0,0,0,0]

        for item in range(1,10):
            '''
            The scratch buffer is a list of (square_position, candidate_value)
            for all positions in a given given square
            '''
            scratch = squares[sq_idx].build_all_items(lines, columns, item, sq_idx)
            for l in scratch:
                hit_count_per_position[l[0]] +=1
                hit_last_per_position[l[0]] = l[1]

        for pos in range(0,9):
            if hit_count_per_position[pos] == 1:
                print(">>>>>>> Hit square[", sq_idx, "] at pos: ", pos, " for item: ", hit_last_per_position[pos])
                square_update_all(squares[sq_idx], pos, lines, columns, hit_last_per_position[pos])
                hit = True
    return(hit)

def solve_line_lev_2(lines, columns, squares):
    hit = False
    for line_idx in range(0,9):
        hit_count_per_position = [0,0,0,0,0,0,0,0,0]
        '''
        If there is only 1 hit in the position counter, then this
        array will have the value that is correct at this position
        '''
        hit_last_per_position =  [0,0,0,0,0,0,0,0,0]

        for item in range(1,10):
            '''
            The scratch buffer is a list of (line_position, candidate_value)
            for all positions in a given given line
            '''
            scratch = lines[line_idx].build_all_items(squares, columns, item)
            for l in scratch:
                hit_count_per_position[l[0]] +=1
                hit_last_per_position[l[0]] = l[1]

        for pos in range(0,9):
            if hit_count_per_position[pos] == 1:
                print(">>>>>>> Hit line[", line_idx, "] at pos: ", pos, " for item: ", hit_last_per_position[pos])
                line_update_all(lines[line_idx], pos, columns, squares, hit_last_per_position[pos])
                hit = True
    return(hit)

def solve_column_lev_2(lines, columns, squares):
    hit = False
    for col_idx in range(0,9):
        hit_count_per_position = [0,0,0,0,0,0,0,0,0]
        '''
        If there is only 1 hit in the position counter, then this
        array will have the value that is correct at this position
        '''
        hit_last_per_position =  [0,0,0,0,0,0,0,0,0]

        for item in range(1,10):
            '''
            The scratch buffer is a list of (line_position, candidate_value)
            for all positions in a given given line
            '''
            scratch = columns[col_idx].build_all_items(squares, lines, item)
            for l in scratch:
                hit_count_per_position[l[0]] +=1
                hit_last_per_position[l[0]] = l[1]

        for pos in range(0,9):
            if hit_count_per_position[pos] == 1:
                print(">>>>>>> Hit column[", col_idx, "] at pos: ", pos, " for item: ", hit_last_per_position[pos])
                column_update_all(columns[col_idx], pos, lines, squares, hit_last_per_position[pos])
                hit = True
    return(hit)

def original_sudoku_lines():
    # Expert - Unresolved Super complique
    lines.append(SudokuLine([0,5,3,0,0,0,4,0,0], 0))
    lines.append(SudokuLine([0,0,0,0,0,0,0,3,9], 1))
    lines.append(SudokuLine([0,0,6,0,0,2,0,1,0], 2))
    lines.append(SudokuLine([8,0,0,6,0,0,0,5,0], 3))
    lines.append(SudokuLine([0,0,0,0,0,0,0,0,0], 4))
    lines.append(SudokuLine([0,0,1,0,8,4,2,0,0], 5))
    lines.append(SudokuLine([0,0,0,4,2,0,0,0,6], 6))
    lines.append(SudokuLine([9,0,0,0,7,0,0,0,0], 7))
    lines.append(SudokuLine([3,7,0,0,0,0,0,9,0], 8))
    
        # Expert 
    # lines.append(SudokuLine([0,6,5,8,0,0,7,0,0], 0))
    # lines.append(SudokuLine([0,9,0,0,2,0,5,0,0], 1))
    # lines.append(SudokuLine([0,0,0,3,4,0,2,0,0], 2))
    # lines.append(SudokuLine([0,7,2,9,0,3,0,0,0], 3))
    # lines.append(SudokuLine([0,0,0,6,8,0,0,0,0], 4))
    # lines.append(SudokuLine([6,0,0,0,0,0,0,0,1], 5))
    # lines.append(SudokuLine([0,0,0,0,0,0,0,9,0], 6))
    # lines.append(SudokuLine([0,0,0,0,0,0,0,0,6], 7))
    # lines.append(SudokuLine([5,0,0,0,0,2,3,0,0], 8))
    


    return lines

if __name__ == '__main__':
    lines = []
    columns = []
    squares = []
    guess_loop = 0
    
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
    
        # Medium
    # lines.append(SudokuLine([1,5,0,4,9,0,8,2,0], 0))
    # lines.append(SudokuLine([0,9,6,0,0,0,7,0,0], 1))
    # lines.append(SudokuLine([0,8,4,0,0,0,0,0,0], 2))
    # lines.append(SudokuLine([0,0,8,0,0,0,0,1,6], 3))
    # lines.append(SudokuLine([0,0,3,0,0,5,0,0,2], 4))
    # lines.append(SudokuLine([4,1,0,9,0,0,0,0,0], 5))
    # lines.append(SudokuLine([0,7,0,0,3,0,9,0,8], 6))
    # lines.append(SudokuLine([8,0,0,6,4,0,0,0,0], 7))
    # lines.append(SudokuLine([0,4,0,0,2,7,0,0,0], 8))

    # # Hard 
    # lines.append(SudokuLine([8,5,0,0,0,4,0,0,2], 0))
    # lines.append(SudokuLine([2,0,0,0,6,0,4,0,0], 1))
    # lines.append(SudokuLine([0,7,0,0,0,0,5,0,0], 2))
    # lines.append(SudokuLine([0,6,0,9,1,0,2,5,0], 3))
    # lines.append(SudokuLine([5,0,0,4,0,0,0,0,7], 4))
    # lines.append(SudokuLine([0,0,0,0,0,0,0,1,0], 5))
    # lines.append(SudokuLine([0,0,0,0,0,0,8,9,1], 6))
    # lines.append(SudokuLine([9,3,0,5,0,0,0,0,0], 7))
    # lines.append(SudokuLine([0,0,0,0,0,6,0,0,0], 8))
    
    # Expert
    # lines.append(SudokuLine([0,0,0,0,2,0,0,0,0], 0))
    # lines.append(SudokuLine([8,1,3,6,4,0,0,0,7], 1))
    # lines.append(SudokuLine([0,0,0,5,0,0,0,0,0], 2))
    # lines.append(SudokuLine([0,4,0,0,5,3,1,0,0], 3))
    # lines.append(SudokuLine([0,6,0,0,0,0,0,0,0], 4))
    # lines.append(SudokuLine([1,0,0,4,0,6,0,0,0], 5))
    # lines.append(SudokuLine([0,0,2,3,0,0,0,0,0], 6))
    # lines.append(SudokuLine([7,0,0,1,0,0,4,0,9], 7))
    # lines.append(SudokuLine([4,0,0,0,0,0,0,7,8], 8))

    # Expert 
    # lines.append(SudokuLine([0,6,5,8,0,0,7,0,0], 0))
    # lines.append(SudokuLine([0,9,0,0,2,0,5,0,0], 1))
    # lines.append(SudokuLine([0,0,0,3,4,0,2,0,0], 2))
    # lines.append(SudokuLine([0,7,2,9,0,3,0,0,0], 3))
    # lines.append(SudokuLine([0,0,0,6,8,0,0,0,0], 4))
    # lines.append(SudokuLine([6,0,0,0,0,0,0,0,1], 5))
    # lines.append(SudokuLine([0,0,0,0,0,0,0,9,0], 6))
    # lines.append(SudokuLine([0,0,0,0,0,0,0,0,6], 7))
    # lines.append(SudokuLine([5,0,0,0,0,2,3,0,0], 8))
    
    lines = original_sudoku_lines()

    # Build the columns from the line's info 
    for i in range (0, SUDOKU_UNIT):
        columns.append(SudokuColumn(lines, i))
        
    # Build the squares from the line's info
    for i in SQUARE_INDEXES:
        squares.append(SudokuSquare(lines, i))  
        
    print_results(lines, columns, squares)
    
    # original_lines = list(lines)  # Backup in case we need to guess


    solved = False
    loop_times = 0
    
    while not solved:
        # Need to brake the loop if not solved the 2nd time ...
        if(guess_loop == END_GAME):
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
        
        "=================== Guess Game ============================================================"
        
        if(loop_times > MAX_LOOPS and guess_loop == 0):
            print("Sorry!!! Need some help!!!")
            # print_results(lines, columns, squares)
            
            update = True
            test = 0
            while update:
                update = False
                test += 1
                print("Looking at Lines for duets - Passes ", test)
                hit_counter = 0
                for line_idx in range(0,9):
                    hit_count_per_position = [0,0,0,0,0,0,0,0,0]
                    '''
                    If there is only 2 hits in the position counter, then this
                    the line is a candidate for the guess game
                    '''
                    hit_1st_per_position = [0,0,0,0,0,0,0,0,0]
                    hit_last_per_position =  [0,0,0,0,0,0,0,0,0]
            
                    for item in range(1,10):
                        '''
                        The scratch buffer is a list of (line_position, candidate_value)
                        for all positions in a given given line
                        '''
                        scratch = lines[line_idx].build_all_items(squares, columns, item)
                        for l in scratch:
                            hit_count_per_position[l[0]] +=1
                            hit_last_per_position[l[0]] = l[1]
                            if(hit_count_per_position[l[0]] == 1): # and l[1] != 0:
                                hit_1st_per_position[l[0]] = l[1] 
            
                    for pos in range(0,9):
                        if hit_count_per_position[pos] == 2 and guess_loop == 0:
                            print("line Candidate [", line_idx, "] at pos: ", pos, " for item(s): ", hit_1st_per_position[pos], hit_last_per_position[pos])
                            hit_counter += 1
                            
                            ''' By default we take the first hit '''
                            ''' 
                                What to do ...
                                1. We need a flag that says we are in the guess game. So when we can back in this
                                part of the algorithm we know what to do ...
                                2. We need to create a FIFO because we might guess multiple times 
                                and along the way make a bad guess and have to come back if we get
                                stocked.
                                3. We need to backup the initial puzzle
                                4. make the guess to the initial grill
                                5. update the FIFO
                                6. restart the game
                                7. we know we made a bad guess when we can not find anymore couplets
                            '''
                            # Preparing for guessing
                            if(hit_counter == 1):
                                guess_info = [line_idx, pos, hit_1st_per_position[pos], hit_last_per_position[pos]]
                                # guess_loop = 1
                            else:
                                guess_info_2 = [line_idx, pos, hit_1st_per_position[pos], hit_last_per_position[pos]]
                                hit_counter = 0
                                guess_loop = 1
                            
        ''' We found our 2 guesses '''
        
        if(loop_times > 2 and guess_loop > 0):
            loop_times = 0
            hit_counter += 1
            
            lines.clear()
            lines = original_sudoku_lines()

            if(hit_counter < 3):
                line_idx = guess_info[0]
                line_pos = guess_info[1]
            else:
                line_idx = guess_info_2[0]
                line_pos = guess_info_2[1]

            
            print("New Guess .. Below results from old guess")
            print_results(lines, columns, squares)
            if (guess_loop == 1):
                
                # print_results(lines, columns, squares)
                
                guess_loop = 2
                line_value = guess_info[2]
                
                # print_results(lines, columns, squares)
                
                # Build the columns from the line's info 
                
                columns.clear()
                for i in range (0, SUDOKU_UNIT):
                    columns.append(SudokuColumn(lines, i))
                    
                # Build the squares from the line's info
                squares.clear()
                for i in SQUARE_INDEXES:
                    squares.append(SudokuSquare(lines, i))
                
                line_update_all(lines[line_idx], line_pos, columns, squares, line_value)
                
                print("=== Guessing 1st attempt line idx:", line_idx, "line pos:", line_pos, "value:", line_value)
                
                print_results(lines, columns, squares)

            elif (guess_loop == 2):
                
                guess_loop = 3
                # print_results(lines, columns, squares)

                loop_times = 0
                line_value = guess_info[3]
                
                # Build the columns from the line's info 
                columns.clear()
                for i in range (0, SUDOKU_UNIT):
                    columns.append(SudokuColumn(lines, i))
                    
                # Build the squares from the line's info
                squares.clear()
                for i in SQUARE_INDEXES:
                    squares.append(SudokuSquare(lines, i))
                    
                line_update_all(lines[line_idx], line_pos, columns, squares, line_value)
                
                print("=== Guessing 2nd attempt line idx:", line_idx, "line pos:", line_pos, "value:", line_value)

                print_results(lines, columns, squares)
                
            elif (guess_loop == 3):
                guess_loop = 4
                # print_results(lines, columns, squares)

                loop_times = 0
                line_value = guess_info_2[2]
                
                # Build the columns from the line's info 
                columns.clear()
                for i in range (0, SUDOKU_UNIT):
                    columns.append(SudokuColumn(lines, i))
                    
                # Build the squares from the line's info
                squares.clear()
                for i in SQUARE_INDEXES:
                    squares.append(SudokuSquare(lines, i))
                    
                line_update_all(lines[line_idx], line_pos, columns, squares, line_value)
                
                print("=== Guessing 3rd attempt line idx:", line_idx, "line pos:", line_pos, "value:", line_value)

                print_results(lines, columns, squares)
                
            elif (guess_loop == 4):
                guess_loop = 5
                # print_results(lines, columns, squares)

                loop_times = 0
                line_value = guess_info_2[3]
                
                # Build the columns from the line's info 
                columns.clear()
                for i in range (0, SUDOKU_UNIT):
                    columns.append(SudokuColumn(lines, i))
                    
                # Build the squares from the line's info
                squares.clear()
                for i in SQUARE_INDEXES:
                    squares.append(SudokuSquare(lines, i))
                    
                line_update_all(lines[line_idx], line_pos, columns, squares, line_value)
                
                print("=== Guessing 4th attempt line idx:", line_idx, "line pos:", line_pos, "value:", line_value)

                print_results(lines, columns, squares)
                
            else:
                guess_loop = END_GAME
                

                        
        solved = True
        for i in lines:
            if(i.has_item(0)):
                solved = False
                
        if(solved):
            break
                    
    if is_puzzle_solved(lines):
        check_results(lines, columns)
        print("Awesome!!! Sudoku solved !!!!")
    else:
        print("Sorry!!! Need some help!!!")
            
    print("===== Game Lines =====")
    for i in lines:
        i.show_elements()
        
    print("Game Algorithm Errors:", game_error.inc())
           

                    
